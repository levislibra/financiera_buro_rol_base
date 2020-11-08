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
	saldo_informes = fields.Integer('Saldo Informes')
	
	solicitar_informe_enviar_a_revision = fields.Boolean('Solicitar informe al enviar a revision')
	solicitar_informe_dias = fields.Integer('Dias para forzar solicitud de nuevo informe')
	asignar_identidad_rol = fields.Boolean('Asignar identidad ROL al solicitar informe')
	asignar_domicilio_rol = fields.Boolean('Asignar domicilio ROL al solicitar informe')
	evaluar_cda_solicitar_informe = fields.Boolean('Evaluar CDAs al solicitar informe')
	evaluar_cda_enviar_a_revision = fields.Boolean('Evaluar CDAs al enviar a revision')
	asignar_cda_otorgamiento = fields.Boolean('Asignar otorgamientos de CDAs')
	modelo_experto = fields.Char('Modelo experto a evaluar')
	cda_ids = fields.One2many('financiera.buro.rol.cda', 'config_id', 'Modelos CDA')
	company_id = fields.Many2one('res.company', 'Empresa', required=False, default=lambda self: self.env['res.company']._company_default_get('financiera.buro.rol.configuracion'))
	
	@api.one
	def actualizar_saldo_informes(self):
		s = requests.Session()
		params = {
			'action': 'login',
			'username': self.usuario,
			'password': self.password,
		}
		r = s.post('https://informe.riesgoonline.com/api/usuarios/sesion', params=params)
		data = r.json()
		self.saldo_informes = int(data['cliente_informes'])

class ExtendsResCompany(models.Model):
	_name = 'res.company'
	_inherit = 'res.company'

	rol_configuracion_id = fields.Many2one('financiera.buro.rol.configuracion', 'Configuracion Riesgo Online')

