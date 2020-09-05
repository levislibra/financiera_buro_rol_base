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
	rol_id = fields.Many2one('rol', "ROL - Consulta actual", compute='_compute_rol_consulta_actual')
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

	def consultar_informe(self):
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
					self.rol_ids = [self.env['rol'].from_dict(data)]
				else:
					ValidationError("Falta DNI, CUIT o CUIL.")
		else:
			ValidationError("Falta configuracion Riesgo Online.")

	@api.one
	def button_consultar_informe(self):
		self.consultar_informe()
		return {'type': 'ir.actions.do_nothing'}

	def consultar_resultado_informe_rol(self):
		return self.rol_experto_resultado

	def solicitar_informe(self):
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
					'procesar_forzado': 1,
				}
				if rol_configuracion_id.modelo_experto:
					params['procesar_experto'] = rol_configuracion_id.modelo_experto
				cuit = self.buscar_persona()
				if cuit:
					url = 'https://informe.riesgoonline.com/api/informes/solicitar/'
					url = url + cuit
					r = requests.get(url, params=params)
					data = r.json()
					self.rol_ids = [self.env['rol'].from_dict(data)]
				else:
					ValidationError("Falta DNI, CUIT o CUIL.")
		else:
			ValidationError("Falta configuracion Riesgo Online.")

	@api.one
	def button_solicitar_informe(self):
		self.solicitar_informe()
		return {'type': 'ir.actions.do_nothing'}

	@api.one
	def _compute_rol_consulta_actual(self):
		if len(self.rol_ids) > 0:
			self.rol_id = self.rol_ids[0]


	@api.one
	def _compute_rol_domicilio(self):
		if len(self.rol_id.persona_id.domicilio_ids) > 0:
			self.rol_domicilio = self.rol_id.persona_id.domicilio_ids[0].domicilio

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
		if len(self.rol_domicilio_ids) > 0:
			domicilio = self.rol_domicilio_ids[0].domicilio.split(', ')
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

class ExtendsFinancieraPrestamo(models.Model):
	_name = 'financiera.prestamo'
	_inherit = 'financiera.prestamo'

	@api.one
	def enviar_a_revision(self):
		if len(self.company_id.rol_configuracion_id) > 0:
			rol_configuracion_id = self.company_id.rol_configuracion_id
			if rol_configuracion_id.solicitar_informe_enviar_a_revision:
				self.partner_id.solicitar_informe()
		super(ExtendsFinancieraPrestamo, self).enviar_a_revision()
