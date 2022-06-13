# -*- coding: utf-8 -*-
from openerp import models, fields, api
from datetime import datetime
from openerp.exceptions import UserError, ValidationError
import requests
from dateutil.parser import parse

class ExtendsResPartnerRol(models.Model):
	_name = 'res.partner'
	_inherit = 'res.partner'

	# rol_ids = fields.One2many('rol', 'partner_id', "ROL - Informes")
	# rol_id = fields.Many2one('rol', "ROL - Consulta actual")
	# domicilio_ids = fields.One2many(related='rol_id.persona_id.domicilio_ids')
	# telefono_ids = fields.Char('telefono_ids')
	# personas_igual_domicilio_ids = fields.One2many(related='rol_id.persona_id.personas_igual_domicilio_ids')
	# personas_relacionada_ids = fields.One2many(related='rol_id.persona_id.personas_relacionada_ids')
	# vecino_ids = fields.One2many(related='rol_id.persona_id.vecino_ids')
	# rol_modelo = fields.Char('Rol modelo')
	# rol_name = fields.Char('Nombre', related='rol_id.persona_id.nombre')
	# rol_cuit = fields.Char('Identificacion', related='rol_id.persona_id.rol_id')
	# rol_perfil_letra = fields.Char('Perfil', related='rol_id.persona_id.perfil_id.letra')
	# rol_perfil_texto = fields.Char('Detalle', related='rol_id.persona_id.perfil_id.texto')
	# rol_experto_nombre = fields.Char('Modelo evaluado', related='rol_id.persona_id.experto_id.nombre')
	# rol_experto_codigo = fields.Char('Codigo', related='rol_id.persona_id.experto_id.codigo')
	# rol_experto_ingreso = fields.Char('Ingresos', related='rol_id.persona_id.experto_id.ingreso')
	# rol_experto_resultado = fields.Char('Resultado', related='rol_id.persona_id.experto_id.resultado',
	# 	help='S: Superado\nN: Rechazado\nI: Incompleto\nV: Verificar.')
	# rol_experto_compromiso_mensual = fields.Char('Compromiso mensual', related='rol_id.persona_id.experto_id.compromiso_mensual')
	# rol_cda_aprobado_id = fields.Many2one('financiera.buro.rol.cda', 'CDA aprobado')
	# rol_cda_reporte_ids = fields.One2many('financiera.buro.rol.cda.reporte', 'partner_id', 'CDA reporte')
	# Nueva integracion
	rol_fecha_ultimo_informe = fields.Datetime('Fecha ultimo informe')
	rol_domicilio = fields.Char('Domicilio', compute='_compute_rol_domicilio')
	rol_capacidad_pago_mensual = fields.Float('ROL - CPM', digits=(16,2))
	rol_partner_tipo_id = fields.Many2one('financiera.partner.tipo', 'ROL - Tipo de cliente')
	rol_informe_ids = fields.One2many('financiera.rol.informe', 'partner_id', 'ROL - Informes')
	rol_variable_ids = fields.One2many('financiera.rol.informe.variable', 'partner_id', 'Variables')
	# Validador de identidad segun preguntas
	rol_validador_identidad_id = fields.Many2one('rol.validador.identidad', 'Preguntas')

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

	def is_int(self, value):
		try:
			int(value)
			return True
		except ValueError:
			return False

	def is_float(self, value):
		try:
			float(value)
			return True
		except ValueError:
			return False

	def is_date(self, value, fuzzy=False):
		try: 
			parse(value, fuzzy=fuzzy)
			return True
		except ValueError:
			return False

	def rol_process_dict(self, parent_key, key, value, list_values, profundidad):
		type = None
		if isinstance(value, dict):
			for sub_key, sub_value in value.iteritems():
				if key:
					self.rol_process_dict(key, sub_key, sub_value, list_values, profundidad+1)
				else:
					self.rol_process_dict("", sub_key, sub_value, list_values, profundidad+1)
		elif isinstance(value, list):
			i = 1
			for sub_value in value:
				self.rol_process_dict(key, key+'_'+str(i), sub_value, list_values, profundidad+1)
				i += 1
		elif self.is_int(value):
			type = 'Numero'
			value = str(value)
		elif self.is_float(value):
			type = 'Decimal'
			value = str(value)
		elif self.is_date(value):
			type = 'Fecha'
			value = str(value)
		else:
			type = 'Texto'
		if type:
			variable_nombre = ''
			if parent_key:
				variable_nombre = parent_key+'_'+key
			else:
				variable_nombre = key
			variable_valor = value
			variable_descripcion = key
			variable_tipo = type
			flag_pass = True
			if parent_key and (('telefonos_' in parent_key and len(parent_key) > 11) or ('informe' == parent_key)):
				flag_pass = False
			if flag_pass:
				variable_values = {
					'partner_id': self.id,
					'name': variable_nombre,
					'valor': variable_valor,
					'descripcion': variable_descripcion,
					'tipo': variable_tipo,
					'profundidad': profundidad,
					'sub_name': parent_key,
				}
				list_values.append((0,0, variable_values))

	# # Funcion documentada en la API!
	# def consultar_informe_rol(self, forzar=False):
	# 	rol_configuracion_id = self.company_id.rol_configuracion_id
	# 	if rol_configuracion_id:
	# 		dias_ultimo_informe = 0
	# 		if len(self.rol_id) > 0 and self.rol_id.fecha:
	# 			fecha_ultimo_informe = datetime.strptime(self.rol_id.fecha, "%Y-%m-%d %H:%M:%S")
	# 			fecha_actual = datetime.now()
	# 			diferencia = fecha_actual - fecha_ultimo_informe
	# 			dias_ultimo_informe = diferencia.days
	# 		if forzar or len(self.rol_id) == 0 or self.rol_id.fecha == False or dias_ultimo_informe >= rol_configuracion_id.solicitar_informe_dias:
	# 			params = {
	# 				'username': rol_configuracion_id.usuario,
	# 				'password': rol_configuracion_id.password,
	# 				'formato': 'json',
	# 				'version': 2,
	# 			}
	# 			cuit = self.buscar_persona()
	# 			if cuit:
	# 				url = 'https://informe.riesgoonline.com/api/informes/consultar/'
	# 				url = url + cuit
	# 				r = requests.get(url, params=params)
	# 				if r.status_code == 200:
	# 					data = r.json()
	# 					nuevo_informe_id = self.env['financiera.rol.informe'].create({})
	# 					self.rol_informe_ids = [nuevo_informe_id.id]
	# 					self.rol_variable_ids = [(6, 0, [])]
	# 					list_values = []
	# 					self.rol_process_dict("", "", data, list_values, 0)
	# 					nuevo_informe_id.write({'variable_ids': list_values})
	# 					self.button_asignar_identidad_rol()
	# 					self.button_asignar_domicilio_rol()
	# 					if rol_configuracion_id.ejecutar_cda:
	# 						self.check_cdas_rol()
	# 					if rol_configuracion_id.asignar_cda_otorgamiento:
	# 						self.button_asignar_cpm_y_tipo_rol()
	# 					rol_configuracion_id.id_informe += 1
	# 			else:
	# 				ValidationError("Falta DNI, CUIT o CUIL.")
	# 	else:
	# 		ValidationError("Falta configuracion Riesgo Online.")
	# 	return True


	# @api.one
	# def button_consultar_informe_rol(self):
	# 	forzar = self.company_id.rol_configuracion_id.forzar_solicitud
	# 	self.consultar_informe_rol(forzar)
	# 	return {'type': 'ir.actions.do_nothing'}

	def consultar_resultado_informe_rol(self):
		return self.rol_experto_resultado

	# Funcion documentada en la API!
	def solicitar_informe_rol(self, forzar=False):
		rol_configuracion_id = self.company_id.rol_configuracion_id
		if rol_configuracion_id:
			dias_para_consultar_nuevo_informe = rol_configuracion_id.dias_para_consultar_nuevo_informe
			dias_ultimo_informe = 0
			if self.rol_fecha_ultimo_informe:
				fecha_ultimo_informe = datetime.strptime(self.rol_fecha_ultimo_informe, "%Y-%m-%d %H:%M:%S")
				fecha_actual = datetime.now()
				diferencia = fecha_actual - fecha_ultimo_informe
				dias_ultimo_informe = diferencia.days
			if not self.rol_fecha_ultimo_informe or dias_ultimo_informe >= dias_para_consultar_nuevo_informe:
				params = {
					'username': rol_configuracion_id.usuario,
					'password': rol_configuracion_id.password,
					'formato': 'json',
					'version': 2,
				}
				if forzar:
					params['procesar_forzado'] = 1
				if rol_configuracion_id.modelo_experto:
					params['procesar_experto'] = rol_configuracion_id.modelo_experto
				cuit = self.buscar_persona()
				if cuit:
					url = 'https://informe.riesgoonline.com/api/informes/solicitar/'
					url = url + cuit
					r = requests.get(url, params=params)
					if r.status_code == 200:
						data = r.json()
					if not 'error' in data:
							nuevo_informe_id = self.env['financiera.rol.informe'].create({})
							self.rol_fecha_ultimo_informe = datetime.now()
							self.rol_informe_ids = [nuevo_informe_id.id]
							self.rol_variable_ids = [(6, 0, [])]
							list_values = []
							self.rol_process_dict("", "", data, list_values, 0)
							nuevo_informe_id.write({'variable_ids': list_values})
							self.button_asignar_identidad_rol()
							self.button_asignar_domicilio_rol()
							if rol_configuracion_id.ejecutar_cda:
									self.check_cdas_rol()
							if rol_configuracion_id.asignar_cda_otorgamiento:
								self.button_asignar_cpm_y_tipo_rol()
							rol_configuracion_id.id_informe += 1
				else:
					ValidationError("Falta DNI, CUIT o CUIL.")
			else:
				# El ultimo informe es valido
				return True
		else:
			ValidationError("Falta configuracion Riesgo Online.")
		return True
	
	@api.one
	def button_solicitar_informe_rol(self):
		forzar = self.company_id.rol_configuracion_id.forzar_solicitud
		self.solicitar_informe_rol(forzar)
		return {'type': 'ir.actions.do_nothing'}

	@api.multi
	def button_descargar_informe_rol(self):
		rol_configuracion_id = self.company_id.rol_configuracion_id
		if rol_configuracion_id:
			cuit = self.get_variable_name('persona_id')
			informe = self.get_variable_name('informe_id')
			if cuit and informe:
				cuit = cuit.valor
				informe = informe.valor
				url = 'https://informe.riesgoonline.com/api/informes/descargar/%s/%s'%(str(cuit),str(informe))
				url = url + '?username=%s&password=%s'%(rol_configuracion_id.usuario, rol_configuracion_id.password)
				opciones = '&opciones[]=contenidos&opciones[]=modulos&opciones[]=adjuntos&opciones[]=graficos&opciones[]=consultas'
				url = url + opciones
			else:
				raise UserError("CUIT o Nro de informe no encontrado.")
			return {
				'name'     : 'ROL informe',
				'res_model': 'ir.actions.act_url',
				'type'     : 'ir.actions.act_url',
				'target'   : 'new',
				'url'      : url
			}
		else:
			raise UserError("ROL no esta configurado.")

	def get_variable_name(self, name):
		ret = False
		for variable_id in self.rol_variable_ids:
			if variable_id.name == name:
				ret = variable_id
		return ret

	def get_variable_value(self, value):
		ret = False
		for variable_id in self.rol_variable_ids:
			if variable_id.valor == value:
				ret = variable_id
		return ret

	@api.one
	def _compute_rol_domicilio(self):
		variable_id = self.get_variable_value('legal_real_ws')
		if variable_id:
			variable_domicilio_id = self.get_variable_name(variable_id.sub_name+'_domicilio')
			if variable_domicilio_id:
				self.rol_domicilio = variable_domicilio_id.valor

	@api.multi
	def button_asignar_identidad_rol(self):
		# Solo se asignaran datos inalterables como nombre y cuit
		rol_configuracion_id = self.company_id.rol_configuracion_id
		if rol_configuracion_id:
			if rol_configuracion_id.asignar_nombre_cliente and rol_configuracion_id.asignar_nombre_cliente_variable:
				variable_id = self.get_variable_name(rol_configuracion_id.asignar_nombre_cliente_variable)
				if variable_id:
					self.name = variable_id.valor
			if rol_configuracion_id.asignar_identificacion_cliente and rol_configuracion_id.asignar_identificacion_cliente_variable:
				variable_id = self.get_variable_name(rol_configuracion_id.asignar_identificacion_cliente_variable)
				if variable_id:
					self.main_id_number = variable_id.valor
			if rol_configuracion_id.asignar_genero_cliente and rol_configuracion_id.asignar_genero_cliente_variable:
				variable_id = self.get_variable_name(rol_configuracion_id.asignar_genero_cliente_variable)
				if variable_id:
					if variable_id.valor == 'M':
						self.sexo = 'masculino'
					else:
						self.sexo = 'femenino'
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
	def check_cdas_rol(self):
		if self.rol_informe_ids and len(self.rol_informe_ids) > 0:
			self.rol_informe_ids[0].ejecutar_cdas()
	
	# Funcion documentada en la API!
	@api.one
	def obtener_preguntas_rol(self):
		ret = False
		if len(self.rol_validador_identidad_id) > 0:
			self.rol_validador_identidad_id.unlink()
		rol_configuracion_id = self.company_id.rol_configuracion_id
		if rol_configuracion_id:
			params = {
				'username': rol_configuracion_id.usuario,
				'password': rol_configuracion_id.password,
				'version': 2,
			}
			if len(self.rol_id) > 0:
				cuit = self.rol_cuit
				informe = self.rol_id.informe_id.rol_id
				url = 'https://informe.riesgoonline.com/api/validador/%s/%s'%(str(cuit),str(informe))
				r = requests.get(url, params=params)
				data = r.json()
				if 'error' in data.keys():
					ret = {
						'error': data['error']
					}
					raise ValidationError(ret['error'])
				else:
					new_rol_validacion_identidad_id = self.env['rol.validador.identidad'].from_dict(data, self.id)
					self.rol_validador_identidad_id = new_rol_validacion_identidad_id.id
					ret = data['resultado']
			else:
				ret = {
					'error': "Informe no encontrado."
				}
				raise ValidationError(ret['error'])
			return ret

	# Funcion documentada en la API!
	# porcentaje_correctas es un valor de 0 a 100.
	@api.one
	def set_respuestas_correctas(self, porcentaje_correctas):
		ret = False
		rol_configuracion_id = self.company_id.rol_configuracion_id
		self.confirm()
		if porcentaje_correctas >= rol_configuracion_id.porcentaje_respuestas_correctas:
			self.state = 'validated'
			ret = True
		else:
			raise ValidationError("No supero el minimo requerido de respuestas correctas.")
		return ret
