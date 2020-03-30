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
	
	asignar_capacidad_pago_mensual = fields.Boolean('Asignar capacidad de pago mensual automaticamente')
	asignar_partner_tipo_segun_perfil = fields.Boolean('Asignar tipo de cliente segun perfil automaticamente')
	dias_vovler_a_consultar = fields.Integer('Dias para volver a solicitar informe')
	consultar_distinto_modelo = fields.Boolean('Solicitar informe con distinto modelo')
	modelo_ids = fields.One2many('financiera.buro.rol.configuracion.modelo', 'configuracion_id', 'Modelos Experto segun Entidad', domain=['|', ('active', '=', False), ('active', '=', True)])
	perfil_to_cpm_ids = fields.One2many('financiera.buro.rol.perfil.cpm', 'configuracion_id', 'Asignacion de CPM segun Perfil')
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

	def get_rol_modelo_segun_entidad(self, entidad_id):
		result = None
		for modelo_id in self.modelo_ids:
			if modelo_id.entidad_id.id == entidad_id.id and modelo_id.active == True:
				if result == None:
					result = modelo_id.name
				else:
					raise ValidationError("Riego Online: Tiene dos o mas modelos para la misma entidad.")
		return result

	def get_rol_active_segun_entidad(self, entidad_id):
		result = None
		for modelo_id in self.modelo_ids:
			if modelo_id.entidad_id.id == entidad_id.id:
				if result == None:
					result = modelo_id.active
				else:
					raise ValidationError("Riego Online: Tiene dos o mas modelos para la misma entidad.")
		return result

	def get_capacidad_pago_mensual_segun_perfil(self, perfil):
		result = 0
		for line in self.perfil_to_cpm_ids:
			if perfil == line.perfil:
				result = line.capacidad_pago_mensual
				break
		return result

	def get_cliente_tipo_segun_perfil(self, perfil):
		result = None
		for line in self.perfil_to_cpm_ids:
			if perfil == line.perfil:
				result = line.partner_tipo_id
				break
		return result

class FinancieraBuroRolConfiguracionModelo(models.Model):
	_name = 'financiera.buro.rol.configuracion.modelo'

	configuracion_id = fields.Many2one('financiera.buro.rol.configuracion', "Configuracion ROL")
	entidad_id = fields.Many2one('financiera.entidad', 'Entidad')
	name = fields.Char('Modelo')
	active = fields.Boolean('Activo')
	company_id = fields.Many2one('res.company', 'Empresa', required=False, default=lambda self: self.env['res.company']._company_default_get('financiera.buro.rol.configuracion.modelo'))

class FinancieraBuroRolPerfilToCPM(models.Model):
	_name = 'financiera.buro.rol.perfil.cpm'

	configuracion_id = fields.Many2one('financiera.buro.rol.configuracion', "Configuracion Nosis")
	perfil = fields.Char('Perfil')
	capacidad_pago_mensual = fields.Float('Capcidad de pago mensual asignada', digits=(16,2))
	partner_tipo_id = fields.Many2one('financiera.partner.tipo', 'Tipo de cliente')
	company_id = fields.Many2one('res.company', 'Empresa', required=False, default=lambda self: self.env['res.company']._company_default_get('financiera.buro.rol.perfil'))

class ExtendsResCompany(models.Model):
	_name = 'res.company'
	_inherit = 'res.company'

	rol_configuracion_id = fields.Many2one('financiera.buro.rol.configuracion', 'Configuracion Riesgo Online')

