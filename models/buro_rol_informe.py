# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime, timedelta
from dateutil import relativedelta
from datetime import date
from openerp.exceptions import UserError, ValidationError
import time
import requests

class ExtendsResPartnerRol(models.Model):
	_name = 'res.partner'
	_inherit = 'res.partner'

	buro_rol_informe_ids = fields.One2many('financiera.buro.rol.informe', 'partner_id', 'Informes')
	rol_modelo = fields.Char('Rol modelo')
	rol_name = fields.Char('Nombre')
	rol_cuit = fields.Char('Identificacion')
	rol_perfil_letra = fields.Selection([
		('A', 'A. Perfil Excelente'),
		('B', 'B. Perfil Superior'),
		('C', 'C. Perfil Muy Bueno'),
		('D', 'D. Perfil Bueno'),
		('E', 'E. Perfil Adecuado'),
		('F', 'F. Perfil Con Limites'),
		('G', 'G. Perfil Insuficiente'),
		('H', 'H. Perfil Nulo'),
		('I', 'I. Perfil Incompleto')],
		'Perfil')
	rol_perfil_texto = fields.Char('Detalle')

	rol_experto_nombre = fields.Char('Modelo evaluado')
	rol_experto_codigo = fields.Char('Codigo')
	rol_experto_tarjeta = fields.Char('Tarjeta de Credito')
	rol_experto_puntos = fields.Integer('Puntos')
	rol_experto_detalles_estado = fields.Char('Estado')
	rol_experto_detalles_texto = fields.Text('Detalle')
	rol_experto_ingreso = fields.Char('Ingresos')
	rol_experto_resultado = fields.Selection([('S', 'Superado'), ('N', 'Rechazado'), ('I', 'Incompleto'), ('V', 'Verificar')], 'Resultado')
	rol_experto_compromiso_mensual = fields.Char('Compromiso mensual')
	rol_experto_monto_mensual_evaluado = fields.Char('CP evaluada (obsoleto)')
	rol_capacidad_pago_mensual = fields.Float('ROL - CPM', digits=(16,2))
	rol_partner_tipo_id = fields.Many2one('financiera.partner.tipo', 'ROL - Tipo de cliente')
	
	rol_domicilio_ids = fields.One2many('financiera.buro.rol.informe.domicilio', 'partner_id', 'Domicilios')
	rol_telefono_ids = fields.One2many('financiera.buro.rol.informe.telefono', 'partner_id', 'Telefonos')
	rol_actividad_ids = fields.One2many('financiera.buro.rol.informe.actividad', 'partner_id', 'Actividad comercial')
	rol_fecha_informe = fields.Datetime('Fecha del informe')

	def buscar_persona(self):
		ret = None
		rol_configuracion_id = self.company_id.rol_configuracion_id
		params = {
			'username': rol_configuracion_id.usuario,
			'password': rol_configuracion_id.password,
			'version': 2,
		}

		url = 'https://informe.riesgoonline.com/api/informes?buscar='
		url = url + self.main_id_number
		r = requests.get(url, params=params)
		data = r.json()
		if 'error' in data.keys():
			raise ValidationError(data['mensaje'])
		else:
			resultado = data['resultado']
			len_resultado = len(data['resultado'])
			mejor_nombre_correcto = 0
			for persona in resultado:
				actual_nombre_correcto = 0
				for nombre in self.name.upper().split():
					if nombre in persona['nombre'].upper():
						actual_nombre_correcto += 1
				if actual_nombre_correcto >= mejor_nombre_correcto:
					mejor_nombre_correcto = actual_nombre_correcto
					ret = persona['cuit']
		return ret

	@api.one
	def button_consultar_informe(self):
		self.consultar_informe()

	def consultar_informe(self):
		rol_configuracion_id = self.company_id.rol_configuracion_id
		params = {
			'username': rol_configuracion_id.usuario,
			'password': rol_configuracion_id.password,
			'formato': 'json',
			'version': 2,
		}
		cuit = self.buscar_persona()
		url = 'https://informe.riesgoonline.com/api/informes/consultar/'
		url = url + cuit
		r = requests.get(url, params=params)
		data = r.json()
		ret = self.procesar_respuesta_informe_rol(data, cuit, 'consulta')
		return ret

	def solicitar_informe(self):
		ret = False
		rol_configuracion_id = self.company_id.rol_configuracion_id
		entidad_id = self.env.user.entidad_login_id
		rol_modelo = rol_configuracion_id.get_rol_modelo_segun_entidad(entidad_id)
		if rol_modelo != None:
			params = {
				'username': rol_configuracion_id.usuario,
				'password': rol_configuracion_id.password,
				'formato': 'json',
				'version': 2,
				'procesar_forzado': 1,
			}
			params['procesar_experto'] = rol_modelo
			cuit = self.buscar_persona()
			url = 'https://informe.riesgoonline.com/api/informes/solicitar/'
			url = url + cuit
			r = requests.get(url, params=params)
			data = r.json()
			ret = self.procesar_respuesta_informe_rol(data, cuit, 'solicitud')
		return ret

	def procesar_respuesta_informe_rol(self, data, cuit, tipo):
		if 'error' in data.keys():
			raise ValidationError(data['mensaje'])
		else:
			codigo = data['informe']['id']
			fecha = date.fromtimestamp(data['informe']['fecha_hora'])
			sexo = None
			self.rol_name = data['persona']['nombre']
			self.rol_cuit = cuit
			informe_values = {
				'partner_id': self.id,
				'name': data['persona']['nombre'],
				'rol_id': codigo,
				'cuit': cuit,
				'sexo': data['persona']['sexo'],
				'clase': data['persona']['clase'],
				'fecha_nacimiento': data['persona']['fecha_nacimiento'],
				'perfil_letra': data['persona']['perfil']['letra'],
				'perfil_texto': data['persona']['perfil']['texto'],
				'fecha_informe': fecha,
			}
			nuevo_informe_id = self.env['financiera.buro.rol.informe'].create(informe_values)
			self.buro_rol_informe_ids = [nuevo_informe_id.id]
			nuevo_informe_id.tipo = tipo
			for data_domicilio in data['persona']['domicilios']:
				for domicilio_id in self.rol_domicilio_ids:
					domicilio_id.unlink()
				domicilio_values = {
					'buro_rol_informe_id': nuevo_informe_id.id,
					'domicilio': data_domicilio['domicilio'],
					'tipo': data_domicilio['tipo'],
				}
				nuevo_domicilio_id = self.env['financiera.buro.rol.informe.domicilio'].create(domicilio_values)
				nuevo_informe_id.domicilio_ids = [nuevo_domicilio_id.id]
				self.rol_domicilio_ids = [nuevo_domicilio_id.id]
			for data_telefono in data['persona']['telefonos']:
				for telefono_id in self.rol_telefono_ids:
					telefono_id.unlink()
				telefono_values = {
					'buro_rol_informe_id': nuevo_informe_id.id,
					'telefono': data_telefono['numero'],
					'anio_guia': data_telefono['anio_guia'],
					'titular': data_telefono['titular'],
				}
				nuevo_telefono_id = self.env['financiera.buro.rol.informe.telefono'].create(telefono_values)
				nuevo_informe_id.telefono_ids = [nuevo_telefono_id.id]
				self.rol_telefono_ids = [nuevo_telefono_id.id]
			for data_actividad in data['persona']['actividad']['actividades_afip']:
				for actividad_id in self.rol_actividad_ids:
					actividad_id.unlink()
				actividad_values = {
					'buro_rol_informe_id': nuevo_informe_id.id,
					'codigo': data_actividad['codigo'],
					'actividad_comercial': data_actividad['descripcion'],
					'formulario': data_actividad['formulario'],
				}
				nuevo_actividad_id = self.env['financiera.buro.rol.informe.actividad'].create(actividad_values)
				nuevo_informe_id.actividad_ids = [nuevo_actividad_id.id]
				self.rol_actividad_ids = [nuevo_actividad_id.id]
			# Perfil principal y Experto ROL
			self.rol_fecha_informe = fecha
			self.rol_perfil_letra = data['persona']['perfil']['letra']
			self.rol_perfil_texto = data['persona']['perfil']['texto']
			
			if 'experto' in data['persona'].keys():
				rol_experto = data['persona']['experto']
				self.rol_experto_nombre = rol_experto['nombre']
				nuevo_informe_id.rol_experto_nombre = rol_experto['nombre']
				self.rol_experto_codigo = rol_experto['codigo']
				self.rol_experto_tarjeta = rol_experto['tarjeta']
				self.rol_experto_puntos = rol_experto['puntos']
				rol_experto_detalles_texto = "<ul>"
				for detalles in rol_experto['detalles']:
					estado = detalles['estado']
					texto = detalles['texto']
					if estado == 'V':
						rol_experto_detalles_texto += '<li style="background-color: #E0E5E1">'
					if estado == 'A' or estado == 'S':
						rol_experto_detalles_texto += '<li style="background-color: #33A8FF">'
					if estado == 'R':
						rol_experto_detalles_texto += '<li style="background-color: #DC3B3E">'
					rol_experto_detalles_texto += str(estado)+" - "+texto+"</li>"
				rol_experto_detalles_texto += "</ul>"
				self.rol_experto_detalles_texto = rol_experto_detalles_texto
				self.rol_experto_ingreso = rol_experto['ingreso']
				self.rol_experto_compromiso_mensual = rol_experto['compromiso_mensual']
				self.rol_experto_resultado = rol_experto['resultado']
				nuevo_informe_id.rol_experto_resultado = rol_experto['resultado']
				self.rol_experto_monto_mensual_evaluado = rol_experto['otorgar_prestamo_max']
				# cpm = str(rol_experto['prestamo']).replace('.', '').replace(',00', '')
				rol_configuracion_id = self.company_id.rol_configuracion_id
				if self.rol_experto_resultado == 'S':
					rol_partner_tipo_id = rol_configuracion_id.get_cliente_tipo_segun_perfil(self.rol_perfil_letra)
					self.rol_partner_tipo_id = rol_partner_tipo_id.id
					if rol_configuracion_id.asignar_partner_tipo_segun_perfil:
						self.partner_tipo_id = rol_partner_tipo_id.id
					rol_cpm = rol_configuracion_id.get_capacidad_pago_mensual_segun_perfil(self.rol_perfil_letra)
					self.rol_capacidad_pago_mensual = rol_cpm
					nuevo_informe_id.rol_capacidad_pago_mensual = rol_cpm
					if rol_configuracion_id.asignar_capacidad_pago_mensual:
						self.capacidad_pago_mensual = rol_cpm
						nuevo_informe_id.capacidad_pago_mensual = rol_cpm
				elif self.rol_experto_resultado in ('I', 'N', 'V'):
					self.rol_partner_tipo_id = None
					self.rol_capacidad_pago_mensual = 0
					if rol_configuracion_id.asignar_partner_tipo_segun_perfil:
						self.partner_tipo_id = None
					if rol_configuracion_id.asignar_capacidad_pago_mensual:
						self.capacidad_pago_mensual = 0
						nuevo_informe_id.capacidad_pago_mensual = 0
			else:
				self.rol_experto_nombre = False
				self.rol_experto_ingreso = False
				self.rol_experto_compromiso_mensual = False
				self.rol_experto_resultado = False
				self.rol_capacidad_pago_mensual = 0
				self.rol_partner_tipo_id = False
		return self.rol_experto_resultado

	@api.one
	def button_solicitar_informe(self):
		ret = self.solicitar_informe()
		if ret == False:
			raise ValidationError("Falta configurar un modelo a evaluar para la entidad "+entidad_id.name+".")

	@api.one
	def asignar_identidad_rol(self):
		if self.rol_cuit != False:
			self.main_id_number = self.rol_cuit
		if self.rol_name != False:
			self.name = self.rol_name
		self.confirm()

	def consultar_resultado_informe_rol(self):
		return self.rol_experto_resultado

class FinancieraBuroRolInforme(models.Model):
	_name = 'financiera.buro.rol.informe'

	_order = "id desc"
	partner_id = fields.Many2one('res.partner', 'Cliente')
	name = fields.Char('Nombre')
	rol_id = fields.Char('Rol id')
	cuit = fields.Char('CUIT')
	documento = fields.Char('Documento')
	sexo = fields.Char('Sexo')
	clase = fields.Char('Clase')
	fecha_nacimiento = fields.Date('Fecha de nacimiento')
	perfil_letra = fields.Selection([
		('A', 'A. Perfil Excelente'),
		('B', 'B. Perfil Superior'),
		('C', 'C. Perfil Muy Bueno'),
		('D', 'D. Perfil Bueno'),
		('E', 'E. Perfil Adecuado'),
		('F', 'F. Perfil Con Limites'),
		('G', 'G. Perfil Insuficiente'),
		('H', 'H. Perfil Nulo'),
		('I', 'I. Perfil Incompleto')],
		'Perfil')
	tipo = fields.Selection([
		('consulta', 'Consulta'),
		('solicitud', 'Solicitud')],
		'Tipo')
	perfil_texto = fields.Char('Detalle')
	rol_experto_resultado = fields.Selection([('S', 'Superado'), ('N', 'Rechazado'), ('I', 'Incompleto'), ('V', 'Verificar')], 'Resultado')
	rol_experto_nombre = fields.Char('Modelo evaluado')
	domicilio_ids = fields.One2many('financiera.buro.rol.informe.domicilio', 'buro_rol_informe_id', 'Domicilios')
	telefono_ids = fields.One2many('financiera.buro.rol.informe.telefono', 'buro_rol_informe_id', 'Telefonos')
	actividad_ids = fields.One2many('financiera.buro.rol.informe.actividad', 'buro_rol_informe_id', 'Actividad comercial')
	fecha_informe = fields.Datetime('Fecha del informe')
	capacidad_pago_mensual = fields.Float('CPM', digits=(16,2))
	company_id = fields.Many2one('res.company', 'Empresa', required=False, default=lambda self: self.env['res.company']._company_default_get('financiera.buro.rol.informe'))


class FinancieraBuroRolInformeDomicilio(models.Model):
	_name = 'financiera.buro.rol.informe.domicilio'

	buro_rol_informe_id = fields.Many2one('financiera.buro.rol.informe', 'Informe', ondelete='cascade')
	partner_id = fields.Many2one('res.partner', 'Cliente')
	domicilio = fields.Char('Domicilio')
	tipo = fields.Char('Tipo')
	company_id = fields.Many2one('res.company', 'Empresa', required=False, default=lambda self: self.env['res.company']._company_default_get('financiera.buro.rol.informe.domicilio'))

class FinancieraBuroRolInformeTelefono(models.Model):
	_name = 'financiera.buro.rol.informe.telefono'

	buro_rol_informe_id = fields.Many2one('financiera.buro.rol.informe', 'Informe', ondelete='cascade')
	partner_id = fields.Many2one('res.partner', 'Cliente')
	telefono = fields.Char('Telefono')
	anio_guia = fields.Char('Año')
	titular = fields.Char('Titular')
	company_id = fields.Many2one('res.company', 'Empresa', required=False, default=lambda self: self.env['res.company']._company_default_get('financiera.buro.rol.informe.telefono'))

class FinancieraBuroRolInformeActividad(models.Model):
	_name = 'financiera.buro.rol.informe.actividad'

	buro_rol_informe_id = fields.Many2one('financiera.buro.rol.informe', 'Informe', ondelete='cascade')
	partner_id = fields.Many2one('res.partner', 'Cliente')
	actividad_comercial = fields.Char('Actividad comercial')
	codigo = fields.Integer('Codigo')
	formulario = fields.Integer('Formulario')
	company_id = fields.Many2one('res.company', 'Empresa', required=False, default=lambda self: self.env['res.company']._company_default_get('financiera.buro.rol.informe.actividad'))

class ExtendsFinancieraPrestamo(models.Model):
	_name = 'financiera.prestamo'
	_inherit = 'financiera.prestamo'

	@api.one
	def enviar_a_revision(self):
		if len(self.company_id.rol_configuracion_id) > 0:
			rol_configuracion_id = self.company_id.rol_configuracion_id
			if rol_configuracion_id.solicitar_informe_enviar_a_revision:
				rol_active = rol_configuracion_id.get_rol_active_segun_entidad(self.sucursal_id)
				rol_modelo = rol_configuracion_id.get_rol_modelo_segun_entidad(self.sucursal_id)
				if len(self.comercio_id) > 0:
					rol_active = rol_configuracion_id.get_rol_active_segun_entidad(self.comercio_id)
					rol_modelo = rol_configuracion_id.get_rol_modelo_segun_entidad(self.comercio_id)
				if rol_active:
					self.partner_id.solicitar_informe(rol_modelo)
					# para hacer test!
					# self.partner_id.consultar_informe()
		super(ExtendsFinancieraPrestamo, self).enviar_a_revision()
