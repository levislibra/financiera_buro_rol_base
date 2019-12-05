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
	resultado_saldo_informes = fields.Text("Resultado saldo informe")
	resultado_consulta_sesion = fields.Text("Resultado consulta sesion")
	
	asignar_capacidad_pago_mensual = fields.Boolean('Asignar capacidad de pago mensual automaticamente')
	dias_vovler_a_consultar = fields.Integer('Dias para volver a solicitar informe')
	consultar_distinto_modelo = fields.Boolean('Solicitar informe con distinto modelo')
	autorizar_automaticamente = fields.Boolean('Autorizar si hay planes aprobados')
	modelo_ids = fields.One2many('financiera.buro.rol.configuracion.modelo', 'configuracion_id', 'Modelos Experto segun Entidad')
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
		print r.text
		data = r.json()
		self.saldo_informes = int(data['cliente_informes'])
		# self.resultado_saldo_informes = data['cliente_informes']
		#r = s.get('https://informe.riesgoonline.com/api/informes?', params={'buscar': '32292307'})
		#self.resultado_consulta_sesion = r.text

	@api.one
	def consulta_sesion(self):
		params = {
			'action': 'logout',
		}
		r = requests.get('https://informe.riesgoonline.com/api/usuarios/sesion?', params=params)
		self.resultado_consulta_sesion = r
		print r

	@api.one
	def get_rol_modelo_segun_entidad(self, entidad_id):
		result = None
		for modelo_id in self.modelo_ids:
			if modelo_id.entidad_id.id == entidad_id.id:
				if result == None:
					result = modelo_id.name
				else:
					raise ValidationError("Riego Online: Tiene dos o mas modelos para la misma entidad.")
		return result

	@api.one
	def get_rol_active_segun_entidad(self, entidad_id):
		result = None
		for modelo_id in self.modelo_ids:
			if modelo_id.entidad_id.id == entidad_id.id:
				if result == None:
					result = modelo_id.active
				else:
					raise ValidationError("Riego Online: Tiene dos o mas modelos para la misma entidad.")
		return result


class FinancieraBuroRolConfiguracionModelo(models.Model):
	_name = 'financiera.buro.rol.configuracion.modelo'

	configuracion_id = fields.Many2one('financiera.buro.rol.configuracion', "Configuracion ROL")
	entidad_id = fields.Many2one('financiera.entidad', 'Entidad')
	name = fields.Char('Modelo')
	active = fields.Boolean('Activo')
	company_id = fields.Many2one('res.company', 'Empresa', required=False, default=lambda self: self.env['res.company']._company_default_get('financiera.buro.rol.configuracion.modelo'))

class ExtendsResCompany(models.Model):
	_name = 'res.company'
	_inherit = 'res.company'

	rol_configuracion_id = fields.Many2one('financiera.buro.rol.configuracion', 'Configuracion Riesgo Online')
