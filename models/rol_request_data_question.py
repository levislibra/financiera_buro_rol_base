# coding: utf-8

# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = welcome_from_dict(json.loads(json_string))
from openerp import models, fields, api
from datetime import datetime, timedelta, date
from dateutil import relativedelta
from openerp.exceptions import UserError, ValidationError
from enum import Enum
import dateutil.parser

def from_str(x):
	ret = ""
	if isinstance(x, (str, unicode)):
		ret = x
	return ret

def from_bool(x):
	ret = None
	if isinstance(x, bool):
		ret = x
	return ret

def from_list(f, x):
	assert isinstance(x, list) or isinstance(x, bool)
	return [f(y) for y in x]

def to_class(c, x):
    assert isinstance(x, c)
    return x.to_dict()


class RolRespuesta(models.Model):
	_name = 'rol.respuesta'

	pregunta_id = fields.Many2one('rol.pregunta', 'Pregunta', ondelete="cascade")
	respuesta = fields.Char('Respuesta')
	verdadera = fields.Boolean('Verdadera')

	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			values = {
				'respuesta': from_str(obj.get(u"respuesta")),
				'verdadera': from_bool(obj.get(u"verdadera"))
			}
			rec = self.env['rol.respuesta'].create(values).id
		return rec

class RolPregunta(models.Model):
	_name = 'rol.pregunta'

	validador_identidad_id = fields.Many2one('rol.validador.identidad', 'Validador de identidad', ondelete="cascade")
	pregunta = fields.Char('Pregunta')
	respuesta_ids = fields.One2many('rol.respuesta', 'pregunta_id', 'Respuestas')

	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			rec = self.env['rol.pregunta'].create({})
			rec.pregunta = from_str(obj.get(u"pregunta"))
			rec.respuesta_ids = from_list(self.env['rol.respuesta'].from_dict, obj.get(u"respuestas"))
			rec = rec.id
		return rec

class RolValidadorIdentidad(models.Model):
	_name = 'rol.validador.identidad'

	name = fields.Char('Nombre para mostrar')
	partner_id = fields.Many2one('res.partner', 'Cliente')
	pregunta_ids = fields.One2many('rol.pregunta', 'validador_identidad_id', 'Preguntas')
	cuit = fields.Char('Cuit')
	nombre = fields.Char('Nombre')
	company_id = fields.Many2one('res.company', 'Empresa', related='partner_id.company_id', readonly=True)

	@api.model
	def create(self, values):
		rec = super(RolValidadorIdentidad, self).create(values)
		rec.update({
			'name': 'PVI/' + str(rec.id).zfill(8),
		})
		return rec


	@api.model
	def from_dict(self, obj, partner_id):
		rec = False
		if isinstance(obj, dict):
			rec = self.env['rol.validador.identidad'].create({'partner_id':partner_id})
			rec.pregunta_ids = from_list(self.env['rol.pregunta'].from_dict, obj.get(u"resultado").get(u"preguntas"))
			rec.cuit = from_str(obj.get(u"cuit"))
			rec.nombre = from_str(obj.get(u"nombre"))
		return rec

