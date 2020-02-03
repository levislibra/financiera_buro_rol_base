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
	rol_experto_monto_mensual_evaluado = fields.Char('Capacidad de pago evaluada')
	rol_capacidad_pago_mensual = fields.Float('ROL -Capacidad de pago mensual', digits=(16,2))
	
	rol_domicilio_ids = fields.One2many('financiera.buro.rol.informe.domicilio', 'partner_id', 'Domicilios')
	rol_telefono_ids = fields.One2many('financiera.buro.rol.informe.telefono', 'partner_id', 'Telefonos')
	rol_actividad_ids = fields.One2many('financiera.buro.rol.informe.actividad', 'partner_id', 'Actividad comercial')
	rol_fecha_informe = fields.Datetime('Fecha del informe')

	@api.one
	def consultar_informe(self):
		rol_configuracion_id = self.company_id.rol_configuracion_id
		params = {
			'username': rol_configuracion_id.usuario,
			'password': rol_configuracion_id.password,
			'formato': 'json',
			'version': 2,
		}
		url = 'https://informe.riesgoonline.com/api/informes/consultar/'
		url = url + self.main_id_number
		r = requests.get(url, params=params)
		data = r.json()
		self.procesar_respuesta_informe_rol(data)

	@api.one
	def solicitar_informe(self, modelo=None):
		rol_configuracion_id = self.company_id.rol_configuracion_id
		params = {
			'username': rol_configuracion_id.usuario,
			'password': rol_configuracion_id.password,
			'formato': 'json',
			'version': 2,
			'procesar_forzado': 1,
		}
		if modelo != None:
			params['procesar_experto'] = modelo
		url = 'https://informe.riesgoonline.com/api/informes/solicitar/'
		url = url + self.main_id_number
		r = requests.get(url, params=params)
		data = r.json()
		self.procesar_respuesta_informe_rol(data)

	@api.one
	def procesar_respuesta_informe_rol(self, data):
		if 'error' in data.keys():
			raise ValidationError(data['mensaje'])
		else:
			codigo = data['informe']['id']
			fecha = date.fromtimestamp(data['informe']['fecha_hora'])
			sexo = None
			self.rol_name = data['persona']['nombre']
			# self.rol_cuit = data['persona']['cuit']
			informe_values = {
				'partner_id': self.id,
				'name': data['persona']['nombre'],
				'rol_id': codigo,
				# 'cuit': data['persona']['cuit'],
				'sexo': data['persona']['sexo'],
				'clase': data['persona']['clase'],
				'fecha_nacimiento': data['persona']['fecha_nacimiento'],
				'perfil_letra': data['persona']['perfil']['letra'],
				'perfil_texto': data['persona']['perfil']['texto'],
				'fecha_informe': fecha,
			}
			nuevo_informe_id = self.env['financiera.buro.rol.informe'].create(informe_values)
			self.buro_rol_informe_ids = [nuevo_informe_id.id]
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
				cpm = str(rol_experto['prestamo']).replace('.', '').replace(',00', '')
				self.rol_capacidad_pago_mensual = float(cpm)
				nuevo_informe_id.rol_capacidad_pago_mensual = float(cpm)
				rol_configuracion_id = self.company_id.rol_configuracion_id
				if rol_configuracion_id.asignar_capacidad_pago_mensual:
					self.capacidad_pago_mensual = self.rol_capacidad_pago_mensual
				if self.rol_experto_resultado == 'S':
					pass
				elif self.rol_experto_resultado == 'I':
					pass
				elif self.rol_experto_resultado == 'N':
					pass
				elif self.rol_experto_resultado == 'V':
					pass

	@api.one
	def button_solicitar_informe(self):
		self.solicitar_informe(self.rol_modelo)

	@api.one
	def asignar_identidad_rol(self):
		if self.rol_cuit != False:
			self.main_id_number = self.rol_cuit
		if self.rol_name != False:
			self.name = self.rol_name
		self.confirm()


class FinancieraBuroRolInforme(models.Model):
	_name = 'financiera.buro.rol.informe'

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
			rol_active = rol_configuracion_id.get_rol_active_segun_entidad(self.sucursal_id)
			rol_modelo = rol_configuracion_id.get_rol_modelo_segun_entidad(self.sucursal_id)
			if len(self.comercio_id) > 0:
				rol_active = rol_configuracion_id.get_rol_active_segun_entidad(self.comercio_id)
				rol_modelo = rol_configuracion_id.get_rol_modelo_segun_entidad(self.comercio_id)
			if rol_active:
				self.partner_id.solicitar_informe(rol_modelo)
				# dias_vovler_a_consultar = rol_configuracion_id.dias_vovler_a_consultar
				# consultar_distinto_modelo = rol_configuracion_id.consultar_distinto_modelo
				# rol_dias = False
				# if self.partner_id.rol_fecha_informe != False and dias_vovler_a_consultar > 0:
				# 	fecha_inicial = datetime.strptime(str(self.partner_id.rol_fecha_informe), '%Y-%m-%d %H:%M:%S')
				# 	fecha_final = datetime.now()
				# 	diferencia = fecha_final - fecha_inicial
				# 	if diferencia.days >= dias_vovler_a_consultar:
				# 		rol_dias = True
				# else:
				# 	rol_dias = True
				
				# rol_distinto_modelo = consultar_distinto_modelo and (rol_modelo != self.partner_id.rol_experto_codigo)
				# if rol_dias or rol_distinto_modelo:
				# 	self.partner_id.solicitar_informe(rol_modelo)
				# else:
				# 	self.partner_id.consultar_informe()
		super(ExtendsFinancieraPrestamo, self).enviar_a_revision()
