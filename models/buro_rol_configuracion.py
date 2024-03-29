# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime, timedelta
from dateutil import relativedelta
from openerp.exceptions import UserError, ValidationError
import time
import requests

class FinancieraBuroRolConfiguracion(models.Model):
	_name = 'financiera.buro.rol.configuracion'

	name = fields.Char('Nombre')
	usuario = fields.Char('Usuario')
	password = fields.Char('Password')
	api_key = fields.Char('API Key')
	saldo_informes = fields.Integer('Saldo Informes')
	
	id_informe = fields.Integer('Id proximo informe', default=1)
	id_cuestionario = fields.Integer('Id proximo cuestionario', default=1)
	forzar_solicitud = fields.Boolean('Forzar solicitud/consulta manual')
	ejecutar_cda = fields.Boolean('Ejecutar CDA')
	asignar_cda_otorgamiento = fields.Boolean('Asignar otorgamientos de CDAs')
	modelo_experto = fields.Char('Modelo experto a evaluar')
	porcentaje_respuestas_correctas = fields.Integer('Porcentaje respuestas correctas para validar',
		help="Valor de 0 a 100. Por lo general son 5 preguntas. Por ejemplo: 80 es para 4 respuestas correctas de 5.")
	dias_para_consultar_nuevo_informe = fields.Integer('Dias para consultar nuevo informe')
	# Nueva integracion
	asignar_nombre_cliente = fields.Boolean('Asignar Nombre al cliente')
	asignar_nombre_cliente_variable = fields.Char('Variable para el Nombre', default='persona_nombre')
	
	asignar_direccion_cliente = fields.Boolean('Asignar Direccion al cliente')
	asignar_direccion_cliente_variable = fields.Char('Variable para la direccion', default='persona_domicilios_1_domicilio')

	asignar_identificacion_cliente = fields.Boolean('Asignar identificacion al cliente')
	asignar_identificacion_cliente_variable = fields.Char('Variable para la identificacion', default='persona_id')

	asignar_genero_cliente = fields.Boolean('Asignar genero al cliente')
	asignar_genero_cliente_variable = fields.Char('Variable para genero', default='persona_sexo')
	company_id = fields.Many2one('res.company', 'Empresa', required=False, default=lambda self: self.env['res.company']._company_default_get('financiera.buro.rol.configuracion'))
	
	@api.one
	def actualizar_saldo_informes(self):
		s = requests.Session()
		params = {
			'action': 'login',
			# 'username': self.usuario,
			# 'password': self.password,
			'key': self.api_key,
		}
		r = s.post('https://informe.riesgoonline.com/api/usuarios/sesion', params=params)
		data = r.json()
		print("data: ", data)
		if r.status_code == 200:
			self.saldo_informes = int(data['cliente_informes'])
		elif 'error' in data:
			raise UserError("Error: " + data['error'])
		else:
			raise UserError("Error desconocido en configuracion ROL.")

class ExtendsResCompany(models.Model):
	_name = 'res.company'
	_inherit = 'res.company'

	rol_configuracion_id = fields.Many2one('financiera.buro.rol.configuracion', 'Configuracion Riesgo Online')

