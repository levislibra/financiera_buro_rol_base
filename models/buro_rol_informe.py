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
			'version': 2,
		}
		url = 'https://informe.riesgoonline.com/api/informes/consultar/'
		url = url + self.main_id_number
		print url
		r = requests.get(url, params=params)
		data = r.json()
		print data.keys()
		if 'error' in data.keys():
			print "ERROR"
			raise ValidationError("Para el CUIT " + self.main_id_number + " no existen informes consultados. Pruebe solicitar informe.")
		else:
			print "EXISTE EL RESULTADO"
			print data['persona'].keys()
			codigo = data['informe']['id']
			informe_existe = False
			for informe_id in self.buro_rol_informe_ids:
				print(str(codigo) == informe_id.rol_id)
				if str(codigo) == informe_id.rol_id:
					informe_existe = True
					break
			if informe_existe:
				raise ValidationError("El informe ya existe con ROL id " + str(codigo) + ".")
			else:
				sexo = None
				if data['persona']['sexo'] == 'M':
					sexo = 'masculino'
				elif data['persona']['sexo'] == 'F':
					sexo = 'femenino'
				informe_values = {
					'partner_id': self.id,
					'name': data['persona']['nombre'],
					'rol_id': codigo,
					'cuit': self.main_id_number,
					'sexo': sexo,
					# 'clase': data['persona']['clase'],
					# 'fecha_nacimiento': data['persona']['fecha_nacimiento'],
					'perfil_letra': data['persona']['perfil']['letra'],
					'perfil_texto': data['persona']['perfil']['texto'],
					# 'fecha_informe': datetime.fromtimestamp(data['informe']['fecha_hora'] / 1e3),
				}
				nuevo_informe_id = self.env['financiera.buro.rol.informe'].create(informe_values)
				self.buro_rol_informe_ids = [nuevo_informe_id.id]
				for data_domicilio in data['persona']['domicilios']:
					domicilio_values = {
						'buro_rol_informe_id': nuevo_informe_id.id,
						'domicilio': data_domicilio['domicilio'],
						'tipo': data_domicilio['tipo'],
					}
					nuevo_domicilio_id = self.env['financiera.buro.rol.informe.domicilio'].create(domicilio_values)
					nuevo_informe_id.domicilio_ids = [nuevo_domicilio_id.id]
				for data_telefono in data['persona']['telefonos']:
					telefono_values = {
						'buro_rol_informe_id': nuevo_informe_id.id,
						'telefono': data_telefono['numero'],
						'anio_guia': data_telefono['anio_guia'],
						'titular': data_telefono['titular'],
					}
					nuevo_telefono_id = self.env['financiera.buro.rol.informe.telefono'].create(telefono_values)
					nuevo_informe_id.telefono_ids = [nuevo_telefono_id.id]
				for data_actividad in data['persona']['actividad']['actividades_afip']:
					actividad_values = {
						'buro_rol_informe_id': nuevo_informe_id.id,
						'codigo': data_actividad['codigo'],
						'actividad_comercial': data_actividad['descripcion'],
						'formulario': data_actividad['formulario'],
					}
					nuevo_actividad_id = self.env['financiera.buro.rol.informe.actividad'].create(actividad_values)
					nuevo_informe_id.actividad_ids = [nuevo_actividad_id.id]


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
	domicilio_ids = fields.One2many('financiera.buro.rol.informe.domicilio', 'buro_rol_informe_id', 'Domicilios')
	telefono_ids = fields.One2many('financiera.buro.rol.informe.telefono', 'buro_rol_informe_id', 'Telefonos')
	actividad_ids = fields.One2many('financiera.buro.rol.informe.actividad', 'buro_rol_informe_id', 'Actividad comercial')
	fecha_informe = fields.Datetime('Fecha del informe')


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