# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime, timedelta
from dateutil import relativedelta
from openerp.exceptions import UserError, ValidationError
import time
import requests

class ExtendsResPartnerRol(models.Model):
	_name = 'res.partner'
	_inherit = 'res.partner'

	buro_rol_informe_ids = fields.One2many('financiera.buro.rol.informe', 'partner_id', 'Informes')

	@api.one
	def consultar_informe(self):
		buro_configuracion_id = self.env['financiera.buro.rol.configuracion'].browse(1)
		params = {
			'username': buro_configuracion_id.usuario,
			'password': buro_configuracion_id.password,
			'formato': 'json',
		}
		url = 'https://informe.riesgoonline.com/api/informes/consultar/'
		url = url + self.main_id_number
		print url
		r = requests.get(url, params=params)
		data = r.json()
		print data.keys()
		if 'error' in data.keys():
			print "ERROR"
		else:
			print "EXISTE LA CUNSULTA"
			# print data['resultado'].keys()
			# print data['resultado_informe'].keys()
			print data['resultado_modulos'].keys()
			# print data['resultado_modulos']['experto'].keys()
			print data['resultado_modulos']['estudio'].keys()
			print data['resultado_modulos']['resumen'].keys()
			codigo = data['resultado_informe']['codigo']
			informe_existe = False
			for informe_id in self.buro_rol_informe_ids:
				if codigo == informe_id.rol_id:
					informe_existe = True
					break
			if informe_existe:
				raise ValidationError("El informe ya existe con ROL id " + str(codigo) + ".")
			else:
				sexo = None
				if data['resultado_informe']['sexo'] == 'M':
					sexo = 'masculino'
				elif data['resultado_informe']['sexo'] == 'F':
					sexo = 'femenino'
				fbri_values = {
					'partner_id': self.id,
					'name': data['resultado_informe']['nombre'],
					'rol_id': data['resultado_informe']['codigo'],
					'cuit': data['resultado_informe']['cuit'],
					'sexo': sexo,
					'perfil': data['resultado_informe']['tipo'],
					# 'fecha_informe': data['resultado_informe']['']
				}
				nuevo_informe_id = self.env['financiera.buro.rol.informe'].create(fbri_values)
				self.buro_rol_informe_ids = [nuevo_informe_id.id]
				# if 'resultado_informe' in data.keys():
				# 	if 


class FinancieraBuroRolInforme(models.Model):
	_name = 'financiera.buro.rol.informe'

	partner_id = fields.Many2one('res.partner', 'Cliente')
	name = fields.Char('Nombre')
	rol_id = fields.Char('Rol id')
	cuit = fields.Char('CUIT')
	documento = fields.Char('Documento')
	sexo = fields.Selection([('masculino', 'Masculino'), ('femenino', 'Femenino')], 'Sexo')
	clase = fields.Char('Clase')
	fecha_de_nacimiento = fields.Date('Fecha de nacimiento')
	perfil = fields.Selection([
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
	domicilio_ids = fields.One2many('financiera.buro.rol.informe.domicilio', 'buro_rol_informe_id', 'Domicilios')
	telefono_ids = fields.One2many('financiera.buro.rol.informe.telefono', 'buro_rol_informe_id', 'Telefonos')
	actividad_ids = fields.One2many('financiera.buro.rol.informe.actividad', 'buro_rol_informe_id', 'Actividad comercial')
	fecha_informe = fields.Date('Fecha del informe')


class FinancieraBuroRolInformeDomicilio(models.Model):
	_name = 'financiera.buro.rol.informe.domicilio'

	buro_rol_informe_id = fields.Many2one('financiera.buro.rol.informe', 'Informe')
	domicilio = fields.Char('Domicilio')
	tipo = fields.Char('Tipo')

class FinancieraBuroRolInformeTelefono(models.Model):
	_name = 'financiera.buro.rol.informe.telefono'

	buro_rol_informe_id = fields.Many2one('financiera.buro.rol.informe', 'Informe')
	telefono = fields.Char('Telefono')
	anio_guia = fields.Char('Año')
	titular = fields.Char('Titular')

class FinancieraBuroRolInformeActividad(models.Model):
	_name = 'financiera.buro.rol.informe.actividad'

	buro_rol_informe_id = fields.Many2one('financiera.buro.rol.informe', 'Informe')
	actividad_comercial = fields.Char('Actividad comercial')
	codigo = fields.Integer('Codigo')
	formulario = fields.Integer('Formulario')