# -*- coding: utf-8 -*-
from openerp import models, fields, api
from datetime import datetime, timedelta
from dateutil import relativedelta
from datetime import date
from openerp.exceptions import UserError, ValidationError
import time
import requests
import json
import rol_request_data

class ExtendsResPartnerRol(models.Model):
	_name = 'res.partner'
	_inherit = 'res.partner'

	rol_ids = fields.One2many('rol', 'partner_id', "ROL")
	rol_id = fields.Many2one('rol', "ROL - Consulta actual")
	# buro_rol_informe_ids = fields.One2many('financiera.buro.rol.informe', 'partner_id', 'Informes')
	rol_modelo = fields.Char('Rol modelo')
	rol_name = fields.Char('Nombre', related='rol_id.persona_id.nombre')
	rol_cuit = fields.Char('Identificacion', related='rol_id.persona_id.rol_id')
	rol_perfil_letra = fields.Char('Perfil', related='rol_id.persona_id.perfil_id.letra')
	rol_perfil_texto = fields.Char('Detalle', related='rol_id.persona_id.perfil_id.texto')

	rol_experto_nombre = fields.Char('Modelo evaluado', related='rol_id.persona_id.experto_id.nombre')
	rol_experto_codigo = fields.Char('Codigo', related='rol_id.persona_id.experto_id.codigo')
	# rol_experto_detalles_estado = fields.Char('Estado')
	# rol_experto_detalles_texto = fields.Text('Detalle')
	rol_experto_ingreso = fields.Char('Ingresos', related='rol_id.persona_id.experto_id.ingreso')
	rol_experto_resultado = fields.Char('Resultado', related='rol_id.persona_id.experto_id.resultado',
		help='S: Superado\nN: Rechazado\nI: Incompleto\nV: Verificar.')
	rol_experto_compromiso_mensual = fields.Char('Compromiso mensual', related='rol_id.persona_id.experto_id.compromiso_mensual')
	# rol_experto_monto_mensual_evaluado = fields.Char('CP evaluada (obsoleto)')
	rol_capacidad_pago_mensual = fields.Float('ROL - CPM', digits=(16,2))
	rol_partner_tipo_id = fields.Many2one('financiera.partner.tipo', 'ROL - Tipo de cliente')
	# Info perfil
	rol_domicilio = fields.Char('Domicilio', compute='_compute_rol_domicilio')
	# rol_domicilio_ids = fields.One2many('financiera.buro.rol.informe.domicilio', 'partner_id', 'Domicilios')
	# rol_telefono_ids = fields.One2many('financiera.buro.rol.informe.telefono', 'partner_id', 'Telefonos')
	# rol_actividad_ids = fields.One2many('financiera.buro.rol.informe.actividad', 'partner_id', 'Actividad comercial')
	rol_fecha_informe = fields.Datetime('Fecha del informe', related='rol_id.fecha')
	rol_cda_aprobado_id = fields.Many2one('financiera.buro.rol.cda', 'CDA aprobado')
	rol_cda_reporte_ids = fields.One2many('financiera.buro.rol.cda.reporte', 'partner_id', 'CDA reporte')

	def buscar_persona(self):
		ret = None
		rol_configuracion_id = self.company_id.rol_configuracion_id
		if rol_configuracion_id:
			params = {
				'username': rol_configuracion_id.usuario,
				'password': rol_configuracion_id.password,
				'version': 2,
			}
			url = 'https://informe.riesgoonline.com/api/informes?buscar='
			if self.main_id_number and len(self.main_id_number) > 2:
				url = url + self.main_id_number
				r = requests.get(url, params=params)
				data = r.json()
				if 'error' in data.keys():
					raise ValidationError(data['error'])
				else:
					resultado = data['resultado']
					mejor_nombre_correcto = 0
					for persona in resultado:
						actual_nombre_correcto = 0
						for nombre in self.name.upper().split():
							if nombre in persona['nombre'].upper():
								actual_nombre_correcto += 1
						if actual_nombre_correcto >= mejor_nombre_correcto:
							mejor_nombre_correcto = actual_nombre_correcto
							ret = persona['cuit']
			else:
				ValidationError("Falta DNI, CUIT o CUIL.")
		else:
			ValidationError("Falta configuracion Riesgo Online.")
		return ret

	# Funcion documentada en la API!
	def consultar_informe_rol(self):
		rol_configuracion_id = self.company_id.rol_configuracion_id
		if rol_configuracion_id:
			dias_ultimo_informe = 0
			if len(self.rol_id) > 0 and self.rol_id.fecha:
				fecha_ultimo_informe = datetime.strptime(self.rol_id.fecha, "%Y-%m-%d %H:%M:%S")
				fecha_actual = datetime.now()
				diferencia = fecha_actual - fecha_ultimo_informe
				dias_ultimo_informe = diferencia.days
			if len(self.rol_id) == 0 or self.rol_id.fecha == False or dias_ultimo_informe >= rol_configuracion_id.solicitar_informe_dias:
				params = {
					'username': rol_configuracion_id.usuario,
					'password': rol_configuracion_id.password,
					'formato': 'json',
					'version': 2,
				}
				cuit = self.buscar_persona()
				if cuit:
					url = 'https://informe.riesgoonline.com/api/informes/consultar/'
					url = url + cuit
					r = requests.get(url, params=params)
					data = r.json()
					new_rol_id = self.env['rol'].from_dict(data)
					if len(new_rol_id.persona_id) > 0:
						new_rol_id.state = 'OK'
						self.rol_ids = [new_rol_id.id]
						self.rol_id = new_rol_id
					elif 'error' in data:
						new_rol_id.state = "Error: " + data['error']
						self.rol_id = None
					else:
						new_rol_id.state = 'Error desconocido al solicitar informe'
						self.rol_id = None
				else:
					ValidationError("Falta DNI, CUIT o CUIL.")
		else:
			ValidationError("Falta configuracion Riesgo Online.")
		if rol_configuracion_id.asignar_identidad_rol:
			self.button_asignar_identidad_rol()
		if rol_configuracion_id.asignar_domicilio_rol:
			self.button_asignar_domicilio_rol()
		return True

	@api.one
	def button_consultar_informe_rol(self):
		self.consultar_informe_rol()
		return {'type': 'ir.actions.do_nothing'}

	def consultar_resultado_informe_rol(self):
		return self.rol_experto_resultado

	# Funcion documentada en la API!
	def solicitar_informe_rol(self, forzar=False):
		rol_configuracion_id = self.company_id.rol_configuracion_id
		if rol_configuracion_id:
			dias_ultimo_informe = 0
			if len(self.rol_id) > 0 and self.rol_id.fecha:
				fecha_ultimo_informe = datetime.strptime(self.rol_id.fecha, "%Y-%m-%d %H:%M:%S")
				fecha_actual = datetime.now()
				diferencia = fecha_actual - fecha_ultimo_informe
				dias_ultimo_informe = diferencia.days
			if forzar or len(self.rol_id) == 0 or self.rol_id.fecha == False or dias_ultimo_informe >= rol_configuracion_id.solicitar_informe_dias:
				params = {
					'username': rol_configuracion_id.usuario,
					'password': rol_configuracion_id.password,
					'formato': 'json',
					'version': 2,
					'procesar_forzado': 1,
				}
				if rol_configuracion_id.modelo_experto:
					params['procesar_experto'] = rol_configuracion_id.modelo_experto
				cuit = self.buscar_persona()
				if cuit:
					url = 'https://informe.riesgoonline.com/api/informes/solicitar/'
					url = url + cuit
					r = requests.get(url, params=params)
					if r.status_code == 200:
						data = r.json()
						new_rol_id = self.env['rol'].from_dict(data)
						if len(new_rol_id.persona_id) > 0:
							new_rol_id.state = 'OK'
							self.rol_ids = [new_rol_id.id]
							self.rol_id = new_rol_id
						elif 'error' in data:
							new_rol_id.state = "Error: " + data['error']
							self.rol_id = None
						else:
							new_rol_id.state = 'Error al solicitar informe'
							self.rol_id = None
				else:
					ValidationError("Falta DNI, CUIT o CUIL.")
		else:
			ValidationError("Falta configuracion Riesgo Online.")
		if rol_configuracion_id.asignar_identidad_rol:
			self.button_asignar_identidad_rol()
		if rol_configuracion_id.asignar_domicilio_rol:
			self.button_asignar_domicilio_rol()
		return True
	
	@api.one
	def button_solicitar_informe_rol(self):
		forzar = self.company_id.rol_configuracion_id.forzar_solicitud
		self.solicitar_informe_rol(forzar)
		return {'type': 'ir.actions.do_nothing'}

	@api.one
	def _compute_rol_domicilio(self):
		for domicilio_id in self.rol_id.persona_id.domicilio_ids:
			if domicilio_id.tipo == 'legal_real_ws':
				self.rol_domicilio = domicilio_id.domicilio

	@api.multi
	def button_asignar_identidad_rol(self):
		# Solo se asignaran datos inalterables como nombre y cuit
		if self.rol_cuit != False:
			self.main_id_number = self.rol_cuit
		if self.rol_name != False:
			self.name = self.rol_name
		return {'type': 'ir.actions.do_nothing'}
	
	@api.multi
	def button_asignar_domicilio_rol(self):
		if self.rol_domicilio:
			domicilio = self.rol_domicilio.split(', ')
			if len(domicilio) > 0:
				self.street = domicilio[0]
			if len(domicilio) > 1:
				self.city = domicilio[1]
			if len(domicilio) > 2:
				state_obj = self.pool.get('res.country.state')
				state_ids = state_obj.search(self.env.cr, self.env.uid, [
					('name', '=ilike', domicilio[2])
				])
				if len(state_ids) > 0:
					self.state_id = state_ids[0]
					country_id = state_obj.browse(self.env.cr, self.env.uid, state_ids[0]).country_id
					self.country_id = country_id.id
			if len(domicilio) > 3:
				self.zip = domicilio[3]
		return {'type': 'ir.actions.do_nothing'}

	@api.multi
	def button_asignar_cpm_y_tipo_rol(self):
		self.partner_tipo_id = self.rol_partner_tipo_id.id
		self.capacidad_pago_mensual = self.rol_capacidad_pago_mensual
		return {'type': 'ir.actions.do_nothing'}

	@api.one
	def check_cdas(self):
		rol_configuracion_id = self.company_id.rol_configuracion_id
		if len(self.rol_id) > 0:
			persona_id = self.rol_id.persona_id
			sexo = persona_id.sexo
			edad = persona_id.edad
			# Generales
			fallecido = persona_id.fallecido
			perfil_letra = persona_id.perfil_id.letra
			# Actividad
			empleado_vigencia = persona_id.actividad_id.actividad_empleado_vigencia
			monotributista_vigencia = persona_id.actividad_id.actividad_monotributista_vigencia
			autonomo_vigencia = persona_id.actividad_id.actividad_autonomo_vigencia
			empleado_antiguedad = persona_id.actividad_id.actividad_empleado_antiguedad
			monotributista_antiguedad = persona_id.actividad_id.actividad_monotributista_antiguedad
			autonomo_antiguedad = persona_id.actividad_id.actividad_autonomo_antiguedad
			empleado_continuidad = persona_id.actividad_id.actividad_empleado_continuidad
			monotributista_continuidad = persona_id.actividad_id.actividad_monotributista_continuidad
			autonomo_continuidad = persona_id.actividad_id.actividad_autonomo_continuidad
			jubilado_pensionado = persona_id.jubilado
			# Bancarizacion
			resumen_situaciones_bancarias = persona_id.bancarizacion_id.resumen_situaciones_bancarias()
			cda_ids = self.company_id.rol_configuracion_id.cda_ids
			for cda_id in cda_ids:
				if cda_id.activo:
					cda_evaluacion = cda_id.evaluar_cda(self.id, fallecido, perfil_letra, sexo, edad, empleado_vigencia, monotributista_vigencia, autonomo_vigencia,
						empleado_antiguedad, monotributista_antiguedad, autonomo_antiguedad, 
						empleado_continuidad, monotributista_continuidad, autonomo_continuidad, jubilado_pensionado,
						resumen_situaciones_bancarias)
					if rol_configuracion_id.asignar_cda_otorgamiento:
						if cda_evaluacion == 'aprobado':
							self.rol_partner_tipo_id = cda_id.partner_tipo_id.id
							self.rol_capacidad_pago_mensual = cda_id.capacidad_pago_mensual
							self.partner_tipo_id = cda_id.partner_tipo_id.id
							self.capacidad_pago_mensual = cda_id.capacidad_pago_mensual
							self.rol_cda_aprobado_id = cda_id.id
							break
						else:
							self.rol_partner_tipo_id = False
							self.rol_capacidad_pago_mensual = 0
							self.partner_tipo_id = False
							self.capacidad_pago_mensual = 0
							self.rol_cda_aprobado_id = None

class ExtendsFinancieraPrestamo(models.Model):
	_name = 'financiera.prestamo'
	_inherit = 'financiera.prestamo'

	@api.one
	def enviar_a_revision(self):
		if len(self.company_id.rol_configuracion_id) > 0:
			rol_configuracion_id = self.company_id.rol_configuracion_id
			if rol_configuracion_id.solicitar_informe_enviar_a_revision:
				origen_ids = [g.id for g in rol_configuracion_id.origen_ids]
				if self.origen_id.id in origen_ids:
					self.partner_id.solicitar_informe_rol()
			if rol_configuracion_id.evaluar_cda_enviar_a_revision:
				self.partner_id.check_cdas()
		super(ExtendsFinancieraPrestamo, self).enviar_a_revision()
