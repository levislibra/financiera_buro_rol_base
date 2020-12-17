# coding: utf-8

#
# To use this code in Python 2.7 you'll have to
#
#     pip install enum34

# This code parses date/times, so please
#
#     pip install python-dateutil
#
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


def from_int(x):
	ret = 0
	if isinstance(x, int):
		ret = x
	return ret


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


def from_datetime(x):
	if not x or x == "":
		ret = False
	else:
		ret = dateutil.parser.parse(x)
	return ret

def from_list(f, x):
	assert isinstance(x, list) or isinstance(x, bool)
	return [f(y) for y in x]


def to_class(c, x):
	assert isinstance(x, c)
	return x.to_dict()


def to_enum(c, x):
	assert isinstance(x, c)
	return x.value


def from_union(fs, x):
	for f in fs:
			try:
					return f(x)
			except:
					pass
	assert False


def from_none(x):
	assert x is None
	return x


class ActividadesAfip(models.Model):
	_name = 'rol.persona.actividad.actividadesafip'

	rol_persona_actividad_id = fields.Many2one('rol.persona.actividad', 'Actividad')
	codigo = fields.Integer('Codigo')
	descripcion = fields.Char('Descripcion')
	formulario = fields.Integer('Formulario')

	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			values = {
				'codigo': from_int(obj.get(u"codigo")),
				'descripcion': from_str(obj.get(u"descripcion")),
				'formulario': from_int(obj.get(u"formulario")),
			}
			rec = self.env['rol.persona.actividad.actividadesafip'].create(values).id
		return rec

class RolPersonaActividadAnses(models.Model):
	_name = 'rol.persona.actividad.anses'

	name = fields.Char('Nombre', default='ANSES')
	trabajador_casa_particular = fields.Boolean('Trabajador casa particular')
	prestacion_desempleo = fields.Boolean('Prestacion desempleo')
	plan_social = fields.Boolean('Plan social')
	prestacion_provincial = fields.Boolean('Prestacion provincial')
	prestacion_nacional = fields.Boolean('Prestacion nacional')
	asignacion_universal = fields.Boolean('Asignacion universal')
	progresar = fields.Boolean('Progresar')

	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			values = {
				'trabajador_casa_particular': from_bool(obj.get(u"trabajador_casa_particular")),
				'prestacion_desempleo': from_bool(obj.get(u"prestacion_desempleo")),
				'plan_social': from_bool(obj.get(u"plan_social")),
				'prestacion_provincial': from_bool(obj.get(u"prestacion_provincial")),
				'prestacion_nacional': from_bool(obj.get(u"prestacion_nacional")),
				'asignacion_universal': from_bool(obj.get(u"asignacion_universal")),
				'progresar': from_bool(obj.get(u"progresar")),
			}
			rec = self.env['rol.persona.actividad.anses'].create(values).id
		return rec

class Autonomo(models.Model):
	_name = 'rol.persona.actividad.autonomo'

	name = fields.Char('Nombre', default='AUTONOMO')
	categoria = fields.Char('Categoria')
	desde = fields.Datetime('Desde')
	hasta = fields.Datetime('Hasta')

	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			values = {
				'categoria': from_str(obj.get(u"categoria")),
				'desde': from_datetime(obj.get(u"desde")),
				'hasta': from_datetime(obj.get(u"hasta")),
			}
			rec = self.env['rol.persona.actividad.autonomo'].create(values).id
		return rec

class RolPersonaActividadCondicionTributaria(models.Model):
	_name = 'rol.persona.actividad.condiciontributaria'

	# _order = 'hasta desc'
	rol_persona_actividad_id = fields.Many2one('rol.persona.actividad', 'Actividad')
	monotributo = fields.Char('Monotributo')
	actividad = fields.Char('Actividad')
	ganancias = fields.Char('Ganancias')
	iva = fields.Char('IVA')
	empleador = fields.Char('Empleador')
	desde = fields.Datetime('Desde')
	hasta = fields.Datetime('Hasta')

	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			values = {
				'monotributo': from_str(obj.get(u"monotributo")),
				'actividad': from_str(obj.get(u"actividad")),
				'ganancias': from_str(obj.get(u"ganancias")),
				'iva': from_str(obj.get(u"iva")),
				'empleador': from_str(obj.get(u"empleador")),
				'desde': from_datetime(obj.get(u"desde")),
				'hasta': from_datetime(obj.get(u"hasta")),
			}
			rec = self.env['rol.persona.actividad.condiciontributaria'].create(values).id
		return rec

class RolPersonaActividadEmpleador(models.Model):
	_name = 'rol.persona.actividad.empleador'

	name = fields.Char('Nombre', default='EMPLEADOR')
	empleados = fields.Integer('Empleados')
	periodo = fields.Char('Periodo')

	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			values = {
				'empleados': from_int(obj.get(u"empleados")),
				'periodo': from_str(obj.get(u"periodo")),
			}
			rec = self.env['rol.persona.actividad.empleador'].create(values)
		return rec

# class RolPersonaActividadImpuestosAfip(models.Model):
# 	_name = 'rol.persona.actividad.impuestosafip'

# 	activos_ids = fields.One2many('rol.persona.actividad.impuesto')
# 	inactivos_ids = fields.One2many('rol.persona.actividad.impuesto')

# 	@api.model
# 	def from_dict(self, obj):
# 		rec = False
# 		if isinstance(obj, dict):
# 			rec = self.env['rol.persona.actividad.impuestosafip'].create({})
# 			rec.activos_ids = from_list(lambda x: x, obj.get(u"activos"))
# 			rec.inactivos_ids = from_list(lambda x: x, obj.get(u"inactivos"))
# 			rec = rec.id
# 		return rec

# Falta
class Ingresos:
	def __init__(self, ingresos, ingresos_rol, ingresos_bruto, ingresos_nse):
		self.ingresos = ingresos
		self.ingresos_rol = ingresos_rol
		self.ingresos_bruto = ingresos_bruto
		self.ingresos_nse = ingresos_nse

	@staticmethod
	def from_dict(obj):
		if isinstance(obj, dict):
			ingresos = from_int(obj.get(u"ingresos"))
			ingresos_rol = from_int(obj.get(u"ingresos_rol"))
			ingresos_bruto = from_int(obj.get(u"ingresos_bruto"))
			ingresos_nse = from_str(obj.get(u"ingresos_nse"))
			return Ingresos(ingresos, ingresos_rol, ingresos_bruto, ingresos_nse)

class RelacionDependencia(models.Model):
	_name = 'rol.persona.actividad.relaciondependencia'

	# _order = 'hasta desc'
	rol_persona_actividad_id = fields.Many2one('rol.persona.actividad')
	rol_id = fields.Char('Rol Id')
	desde = fields.Datetime('Desde')
	hasta = fields.Datetime('Hasta')

	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			values = {
				'rol_id': str(from_int(obj.get(u"id"))),
				'desde': from_datetime(obj.get(u"desde")),
				'hasta': from_datetime(obj.get(u"hasta")),
			}
			rec = self.env['rol.persona.actividad.relaciondependencia'].create(values).id
		return rec


class RolPersonaActividad(models.Model):
	_name = 'rol.persona.actividad'

	name = fields.Char('Nombre', default='ACTIVIDAD')
	empleado_publico = fields.Boolean('Empleado publico')
	empleador_id = fields.Many2one('rol.persona.actividad.empleador', 'Empleador')
	autonomo_id = fields.Many2one('rol.persona.actividad.autonomo', 'Autonomo')
	anses_id = fields.Many2one('rol.persona.actividad.anses', 'Anses')
	relacion_dependencia_ids = fields.One2many('rol.persona.actividad.relaciondependencia', 'rol_persona_actividad_id', 'Relacion dependencia')
	actividades_afip_ids = fields.One2many('rol.persona.actividad.actividadesafip', 'rol_persona_actividad_id', 'Actividades afip')
	condicion_tributaria_ids = fields.One2many('rol.persona.actividad.condiciontributaria', 'rol_persona_actividad_id', 'Condicion tributaria')
	# impuestos_afip_id = fields.Many2one('rol.persona.actividad.impuestosafip', 'Impuestos afip')
	fecha_informe = fields.Datetime('Fecha informe', compute='_compute_fecha_informe')
	# Como empleado
	actividad_empleado_vigencia = fields.Boolean('Empleado vigente', compute='_compute_actividad_empleado')
	actividad_empleado_antiguedad = fields.Integer('Empleado antiguedad', compute='_compute_actividad_empleado')
	actividad_empleado_continuidad = fields.Integer('Empleado continuidad', compute='_compute_actividad_empleado')
	# Como monotributista
	actividad_monotributista_vigencia = fields.Boolean('Monotributista vigente', compute='_compute_actividad_monotributista')
	actividad_monotributista_antiguedad = fields.Integer('Monotributista antiguedad', compute='_compute_actividad_monotributista')
	actividad_monotributista_continuidad = fields.Integer('Monotributista continuidad', compute='_compute_actividad_monotributista')
		# Como autonomo
	actividad_autonomo_vigencia = fields.Boolean('Autonomo vigente', compute='_compute_actividad_autonomo')
	actividad_autonomo_antiguedad = fields.Integer('Autonomo antiguedad', compute='_compute_actividad_autonomo')
	actividad_autonomo_continuidad = fields.Integer('Autonomo continuidad', compute='_compute_actividad_autonomo')
	actividad = fields.Selection([
		('empleado', 'Empleado'),
		('monotributista', 'Monotributista'),
		('autonomo', 'Autonomo')], 'Actividad', compute='_compute_actividad')
	actividad_vigencia = fields.Boolean('Vigencia de la actividad', compute='_compute_actividad')

	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			rec = self.env['rol.persona.actividad'].create({})
			rec.empleado_publico = from_bool(obj.get(u"empleado_publico"))
			rec.empleador_id = self.env['rol.persona.actividad.empleador'].from_dict(obj.get(u"empleador"))
			rec.autonomo_id = self.env['rol.persona.actividad.autonomo'].from_dict(obj.get(u"autonomo"))
			rec.anses_id = self.env['rol.persona.actividad.anses'].from_dict(obj.get(u"anses"))
			rec.relacion_dependencia_ids = from_list(self.env['rol.persona.actividad.relaciondependencia'].from_dict, obj.get(u"relacion_dependencia").get(u"empleadores"))
			rec.actividades_afip_ids = from_list(self.env['rol.persona.actividad.actividadesafip'].from_dict, obj.get(u"actividades_afip"))
			rec.condicion_tributaria_ids = from_list(self.env['rol.persona.actividad.condiciontributaria'].from_dict, obj.get(u"condicion_tributaria"))
			# rec.impuestos_afip_id = self.env['rol.persona.actividad.impuestosafip'].from_dict(obj.get(u"impuestos_afip"))
			rec = rec.id
		return rec

	@api.one
	def _compute_fecha_informe(self):
		informe_obj = self.pool.get('rol')
		informe_ids = informe_obj.search(self.env.cr, self.env.uid, [
			('persona_id.actividad_id', '=', self.id)
		])
		self.fecha_informe = informe_obj.browse(self.env.cr, self.env.uid, informe_ids[0]).fecha

	@api.one
	def _compute_actividad_empleado(self):
		fecha_informe = datetime.strptime(self.fecha_informe, "%Y-%m-%d %H:%M:%S")
		if len(self.relacion_dependencia_ids) > 0:
			relacion_dependencia_desde = datetime.strptime(self.relacion_dependencia_ids[len(self.relacion_dependencia_ids)-1].desde, "%Y-%m-%d %H:%M:%S")
			relacion_dependencia_hasta = datetime.strptime(self.relacion_dependencia_ids[0].hasta, "%Y-%m-%d %H:%M:%S")
			diferencia = fecha_informe - relacion_dependencia_hasta
			if diferencia.days < 120:
				self.actividad_empleado_vigencia = True
			diferencia = relacion_dependencia_hasta - relacion_dependencia_desde
			self.actividad_empleado_antiguedad = diferencia.days/30
			relacion_dependencia_ultimo_periodo_desde = datetime.strptime(self.relacion_dependencia_ids[0].desde, "%Y-%m-%d %H:%M:%S")
			diferencia = relacion_dependencia_hasta - relacion_dependencia_ultimo_periodo_desde
			self.actividad_empleado_continuidad = diferencia.days/30

	@api.one
	def _compute_actividad_monotributista(self):
		fecha_informe = datetime.strptime(self.fecha_informe, "%Y-%m-%d %H:%M:%S")
		len_condicion_tributaria = len(self.condicion_tributaria_ids)
		if len_condicion_tributaria > 0:
			monotributista_desde = datetime.strptime(self.condicion_tributaria_ids[0].desde, "%Y-%m-%d %H:%M:%S")
			monotributista_hasta = datetime.strptime(self.condicion_tributaria_ids[len_condicion_tributaria-1].hasta, "%Y-%m-%d %H:%M:%S")
			if self.condicion_tributaria_ids[len_condicion_tributaria-1].monotributo != "NO INSCRIPTO":
				diferencia = fecha_informe - monotributista_hasta
				if diferencia.days < 15:
					self.actividad_monotributista_vigencia = True
			diferencia = monotributista_hasta - monotributista_desde
			self.actividad_monotributista_antiguedad = diferencia.days/30
			# continuidad en monotributo
			continuidad = 0
			i = len_condicion_tributaria-1
			while i >= 0:
				desde = datetime.strptime(self.condicion_tributaria_ids[i].desde, "%Y-%m-%d %H:%M:%S")
				hasta = datetime.strptime(self.condicion_tributaria_ids[i].hasta, "%Y-%m-%d %H:%M:%S")
				diferencia = hasta - desde
				continuidad += diferencia.days
				if (i-1) >= 0:
					hasta_anterior = datetime.strptime(self.condicion_tributaria_ids[i-1].hasta, "%Y-%m-%d %H:%M:%S")
					diferencia = desde - hasta_anterior
					if diferencia.days > 30:
						# Lo concideramos NO continuidad
						break
				i -= 1
			self.actividad_monotributista_continuidad = continuidad/30

	@api.one
	def _compute_actividad_autonomo(self):
		fecha_informe = datetime.strptime(self.fecha_informe, "%Y-%m-%d %H:%M:%S")
		if len(self.autonomo_id) > 0 and self.autonomo_id.desde and self.autonomo_id.hasta:
			autonomo_desde = datetime.strptime(self.autonomo_id.desde, "%Y-%m-%d %H:%M:%S")
			autonomo_hasta = datetime.strptime(self.autonomo_id.hasta, "%Y-%m-%d %H:%M:%S")
			diferencia = fecha_informe - autonomo_hasta
			if diferencia.days < 15:
				self.actividad_autonomo_vigencia = True
			diferencia = autonomo_hasta - autonomo_desde
			self.actividad_autonomo_antiguedad = diferencia.days/30
			self.actividad_autonomo_continuidad = diferencia.days/30

	@api.one
	def _compute_actividad(self):
		relacion_dependencia_hasta = False
		monotributo_hasta = False
		autonomo_hasta = False
		fecha_mas_reciente = False
		diferencia = False
		fecha_actual = datetime.strptime(self.fecha_informe, "%Y-%m-%d %H:%M:%S")
		if len(self.relacion_dependencia_ids) > 0:
			relacion_dependencia_hasta = datetime.strptime(self.relacion_dependencia_ids[0].hasta, "%Y-%m-%d %H:%M:%S")
			fecha_mas_reciente = relacion_dependencia_hasta
			self.actividad = 'empleado'
			diferencia = fecha_actual - relacion_dependencia_hasta
			if diferencia.days < 120:
				self.actividad_vigencia = True
		if len(self.condicion_tributaria_ids) > 0:
			if self.condicion_tributaria_ids[0].monotributo != "NO INSCRIPTO":
				monotributo_hasta = datetime.strptime(self.condicion_tributaria_ids[0].hasta, "%Y-%m-%d %H:%M:%S")
				if fecha_mas_reciente == False or fecha_mas_reciente < monotributo_hasta:
					self.actividad = 'monotributista'
					fecha_mas_reciente = monotributo_hasta
					diferencia = fecha_actual - fecha_mas_reciente
					if diferencia.days < 15:
						self.actividad_vigencia = True
		if len(self.autonomo_id) > 0 and self.autonomo_id.hasta != False:
			autonomo_hasta = datetime.strptime(self.autonomo_id.hasta, "%Y-%m-%d %H:%M:%S")
			if fecha_mas_reciente == False or fecha_mas_reciente < autonomo_hasta:
				self.actividad = 'autonomo'
				fecha_mas_reciente = autonomo_hasta
				diferencia = fecha_actual - fecha_mas_reciente
				if diferencia.days < 15:
					self.actividad_vigencia = True

class RolPersonaBancarizacionEntidadesHistorico(models.Model):
	_name = 'rol.persona.bancarizacion.entidadeshistorico'

	rol_persona_bancarizacion_id = fields.Many2one('rol.persona.bancarizacion', 'Bancarizacion')
	entidad = fields.Char('Entidad')
	periodo = fields.Char('Periodo')
	periodo_fecha = fields.Datetime('Fecha periodo', compute='_compute_periodo_fecha')
	periodo_meses = fields.Integer('Meses hasta fecha informe', compute='_compute_periodo_meses')
	situacion = fields.Integer('Situacion')
	monto = fields.Integer('Monto')

	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			values = {
				'entidad': from_str(obj.get(u"entidad")),
				'periodo': from_str(obj.get(u"periodo")),
				'situacion': from_int(obj.get(u"situacion")),
				'monto': from_int(obj.get(u"monto")),
			}
			rec = self.env['rol.persona.bancarizacion.entidadeshistorico'].create(values).id
		return rec

	@api.one
	def _compute_periodo_fecha(self):
		self.periodo_fecha = datetime.strptime('02/'+str(self.periodo), "%d/%m/%Y")

	@api.one
	def _compute_periodo_meses(self):
		desde = datetime.strptime(self.periodo_fecha, "%Y-%m-%d 00:00:00")
		hasta = datetime.strptime(self.rol_persona_bancarizacion_id.fecha_informe, "%Y-%m-%d 00:00:00")
		diferencia = hasta - desde
		self.periodo_meses = diferencia.days/30

class RolPersonaBancarizacionChequesHistorico(models.Model):
	_name = 'rol.persona.bancarizacion.chequeshistorico'

	rol_persona_bancarizacion_id = fields.Many2one('rol.persona.bancarizacion', 'Bancarizacion')
	fecha_rechazo = fields.Date('Fecha rechazo')
	fecha_pago = fields.Date('Fecha pago')
	causal = fields.Char('Causal')
	monto = fields.Integer('Monto')
	multa = fields.Char('Multa')
	persona = fields.Char('Persona')

	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			values = {
				'fecha_rechazo': from_datetime(obj.get(u"fecha_rechazo")),
				'fecha_pago': from_datetime(obj.get(u"fecha_pago")),
				'causal': from_str(obj.get(u"causal")),
				'monto': from_int(obj.get(u"monto")),
				'multa': from_str(obj.get(u"multa")),
				'persona': from_str(obj.get(u"persona")),
			}
			rec = self.env['rol.persona.bancarizacion.chequeshistorico'].create(values).id
		return rec

class RolPersonaBancarizacion(models.Model):
	_name = 'rol.persona.bancarizacion'

	name = fields.Char('Nombre', default='BANCARIZACION')
	fecha_informe = fields.Datetime('Fecha informe', compute='_compute_fecha_informe')
	entidades_historico_ids = fields.One2many('rol.persona.bancarizacion.entidadeshistorico', 'rol_persona_bancarizacion_id', 'Entidades historico')
	cheques_historico_ids = fields.One2many('rol.persona.bancarizacion.chequeshistorico', 'rol_persona_bancarizacion_id', 'Cheques historico')
	sin_mora_desde = fields.Char('Sin mora desde')
	sin_mora_meses = fields.Integer('Meses sin mora')

	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			values = {
				'sin_mora_desde': from_str(obj.get(u"sin_mora_desde")),
				'sin_mora_meses': from_int(obj.get(u"sin_mora_meses")),
			}
			rec = self.env['rol.persona.bancarizacion'].create(values)
			rec['entidades_historico_ids'] = from_list(self.env['rol.persona.bancarizacion.entidadeshistorico'].from_dict, obj.get(u"entidades_historico"))
			rec['cheques_historico_ids'] = from_list(self.env['rol.persona.bancarizacion.chequeshistorico'].from_dict, obj.get(u"cheques_historico"))
			rec = rec.id
		return rec

	@api.one
	def _compute_fecha_informe(self):
		informe_obj = self.pool.get('rol')
		informe_ids = informe_obj.search(self.env.cr, self.env.uid, [
			('persona_id.bancarizacion_id', '=', self.id)
		])
		self.fecha_informe = informe_obj.browse(self.env.cr, self.env.uid, informe_ids[0]).fecha

	def resumen_situaciones_bancarias(self):
		ret = {
			'ultimo_mes': [0,0,0,0,0,0],
			'tres_meses': [0,0,0,0,0,0],
			'seis_meses': [0,0,0,0,0,0],
			'doce_meses': [0,0,0,0,0,0],
		}
		i = 0
		periodo = 1
		len_entidades_historico = len(self.entidades_historico_ids)
		while periodo <= 12 and i < len_entidades_historico:
			entidad_id = self.entidades_historico_ids[i]
			if periodo == 1:
				ret['ultimo_mes'][entidad_id.situacion-1] += 1
				ret['tres_meses'][entidad_id.situacion-1] += 1
				ret['seis_meses'][entidad_id.situacion-1] += 1
				ret['doce_meses'][entidad_id.situacion-1] += 1
			if periodo == 2 or periodo == 3:
				ret['tres_meses'][entidad_id.situacion-1] += 1
				ret['seis_meses'][entidad_id.situacion-1] += 1
				ret['doce_meses'][entidad_id.situacion-1] += 1
			if periodo == 4 or periodo == 5 or periodo == 6:
				ret['seis_meses'][entidad_id.situacion-1] += 1
				ret['doce_meses'][entidad_id.situacion-1] += 1
			if periodo > 6 and periodo <= 12:
				ret['doce_meses'][entidad_id.situacion-1] += 1
			if (i+1) < len_entidades_historico:
				if entidad_id.periodo != self.entidades_historico_ids[i+1].periodo:
					periodo += 1
			i += 1
		return ret

			

class RolInforme(models.Model):
	_name = 'rol.informe'

	name = fields.Char('Nombre', default='INFORME')
	rol_id = fields.Integer('ROL id')
	cliente = fields.Integer('Cliente')
	fecha_hora = fields.Datetime('Fecha y hora')

	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			values = {
				'rol_id': from_int(obj.get(u"id")),
				'cliente': from_int(obj.get(u"cliente")),
				'fecha_hora': date.fromtimestamp(from_int(obj.get(u"fecha_hora"))),
			}
			rec = self.env['rol.informe'].create(values).id
		return rec

class Juicio(models.Model):
	_name = 'rol.juicio'

	judicial_id = fields.Many2one('rol.judicial', 'Judicial')
	fecha = fields.Datetime('Fecha')
	provincia = fields.Char("Provincia")
	rol = fields.Char("Rol")
	texto = fields.Char('Texto')

	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			values = {
				'fecha': from_str(obj.get(u"fecha")),
				'provincia': from_str(obj.get(u"provincia")),
				'rol': from_str(obj.get(u"rol")),
				'texto': from_str(obj.get(u"texto")),
			}
			rec = self.env['rol.juicio'].create(values).id
		return rec

class Judicial(models.Model):
	_name = 'rol.judicial'

	juicio_ids = fields.One2many('rol.juicio', 'judicial_id', 'Juicios')
	# concursos_y_quiebras = concursos_y_quiebras

	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			values = {
				'juicio_ids': from_list(self.env['rol.juicio'].from_dict, obj.get(u"juicios")),
				# concursos_y_quiebras = from_list(lambda x: x, obj.get(u"concursos_y_quiebras"))
			}
			rec = self.env['rol.judicial'].create(values).id
			return rec

class RolPersonaDomicilio(models.Model):
	_name = 'rol.persona.domicilio'
	
	_rec_name = 'domicilio'
	rol_persona_id = fields.Many2one('rol.persona', 'Persona')
	domicilio = fields.Char('Domicilio')
	tipo = fields.Char('Tipo')

	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			values = {
				'domicilio': from_str(obj.get(u"domicilio")),
				'tipo': from_str(obj.get(u"tipo")),
			}
			rec = self.env['rol.persona.domicilio'].create(values).id
		return rec

class RolPersonaDominiosNIC(models.Model):
	_name = 'rol.persona.dominiosnic'

	dominio = fields.Char('Dominio')
	entidad = fields.Char('Entidad')
	tipo = fields.Char('Tipo')
	fecha = fields.Datetime('Fecha')

	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			values = {
				'dominio': from_str(obj.get(u"dominio")),
				'entidad': from_str(obj.get(u"entidad")),
				'tipo': from_str(obj.get(u"tipo")),
				'fecha': from_datetime(obj.get(u"fecha")),
			}
			rec = self.env['rol.persona.dominiosnic'].create(values).id
		return rec

class RolPersonaMarcaActa(models.Model):
	_name = 'rol.persona.marca.acta'

	rol_persona_marca_id = fields.Many2one('rol.persona.marca', 'Marca')
	numero = fields.Integer('Numero')
	fecha_presentacion = fields.Char('Fecha presentacion')
	tipo = fields.Char('Tipo')
	clase = fields.Integer('Clase')

	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			values = {
				'numero': from_int(obj.get(u"numero")),
				'fecha_presentacion': from_str(obj.get(u"fecha_presentacion")),
				'tipo': from_str(obj.get(u"tipo")),
				'clase': from_int(obj.get(u"clase")),
			}
			rec = self.env['rol.persona.marca.acta'].create(values).id
		return rec


class RolPersonaMarca(models.Model):
	_name = 'rol.persona.marca'
	
	_rec_name = 'nombre'
	rol_persona_id = fields.Many2one('rol.persona', 'Persona')
	nombre = fields.Char('Nombre')
	actas = fields.One2many('rol.persona.marca.acta', 'rol_persona_marca_id', 'Actas')

	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			values = {
				'nombre': from_str(obj.get(u"nombre")),
			}
			rec = self.env['rol.persona.marca'].create(values)
			rec['actas'] = from_list(self.env['rol.persona.marca.acta'].from_dict, obj.get(u"actas"))
			rec = rec.id
		return rec


class RolPersonaPerfil(models.Model):
	_name = 'rol.persona.perfil'
	
	name = fields.Char('Nombre')
	letra = fields.Char('Letra')
	texto = fields.Char('Texto')

	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			frase = ""
			if len(from_str(obj.get(u"texto")).split('.')) > 0:
				frase = from_str(obj.get(u"texto")).split('.')[0]
			values = {
				'name': from_str(obj.get(u"letra")) + ' - ' + frase,
				'letra': from_str(obj.get(u"letra")),
				'texto': from_str(obj.get(u"texto")),
			}
			rec = self.env['rol.persona.perfil'].create(values).id
		return rec

class RolExpertoDetalle(models.Model):
	_name = 'rol.experto.detalle'

	rol_experto_id = fields.Many2one('rol.experto', 'Experto')
	estado = fields.Char('estado')
	texto = fields.Char('texto')
	tipo = fields.Char('tipo')

	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			values = {
				'estado': from_str(obj.get(u"estado")),
				'texto': from_str(obj.get(u"texto")),
				'tipo': from_str(obj.get(u"tipo")),
			}
			rec = self.env['rol.experto.detalle'].create(values).id
		return rec

class RolExperto(models.Model):
	_name = 'rol.experto'
	
	name = fields.Char("Nombre")
	codigo = fields.Char("Codigo")
	nombre = fields.Char("Nombre")
	resultado = fields.Char("Resultado")
	detalles_ids = fields.One2many('rol.experto.detalle', 'rol_experto_id', 'Detalles')
	grupo  = fields.Char("Grupo")
	puntos  = fields.Char("Puntos")
	ingreso  = fields.Char("Ingreso")
	ingreso_declarado  = fields.Char("Ingreso declarado")
	compromiso_mensual  = fields.Char("Compromiso mensual")
	compromiso_mensual_rol  = fields.Char("Compromiso mensual rol")
	compromiso_adicional  = fields.Char("Compromiso adicional")
	compromiso_tc  = fields.Char("Compromiso tc")
	compromiso_pp  = fields.Char("Compromiso pp")
  
	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			values = {
				"name": "MODELO/"+from_str(obj.get(u"codigo")),
				"codigo": from_str(obj.get(u"codigo")),
				"nombre": from_str(obj.get(u"nombre")),
				"resultado": from_str(obj.get(u"resultado")),
				"grupo": from_str(obj.get(u"grupo")),
				"puntos": from_str(obj.get(u"puntos")),
				"ingreso": from_str(obj.get(u"ingreso")),
				"ingreso_declarado": from_str(obj.get(u"ingreso_declarado")),
				"compromiso_mensual": from_str(obj.get(u"compromiso_mensual")),
				"compromiso_mensual_rol": from_str(obj.get(u"compromiso_mensual_rol")),
				"compromiso_adicional": from_str(obj.get(u"compromiso_adicional")),
				"compromiso_tc": from_str(obj.get(u"compromiso_tc")),
				"compromiso_pp": from_str(obj.get(u"compromiso_pp")),
			}
			rec = self.env['rol.experto'].create(values)
			rec.detalles_ids = from_list(self.env['rol.experto.detalle'].from_dict, obj.get(u"detalles"))
			rec = rec.id
		return rec


class RolPersonaPersonas(models.Model):
	_name = 'rol.persona.personas'

	_rec_name = 'nombre'
	rol_persona_id = fields.Many2one('rol.persona', 'Persona')
	rol_persona_relacionada_id = fields.Many2one('rol.persona', 'Persona')
	nombre = fields.Char('Nombre')
	sexo = fields.Char('Sexo')
	domicilio = fields.Char('Domicilio')
	rol_id = fields.Char('Rol Id')
	relacion = fields.Char('Relacion')

	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			values = {
				'nombre': from_str(obj.get(u"nombre")),
				'sexo': from_str(obj.get(u"sexo")),
				'domicilio': from_str(obj.get(u"domicilio")),
				'rol_id': str(from_int(obj.get(u"id"))),
				'relacion': from_str(obj.get(u"relacion")),
			}
			rec = self.env['rol.persona.personas'].create(values).id
		return rec


class Telefono(models.Model):
	_name = 'rol.persona.telefono'

	_rec_name = 'numero'
	rol_persona_id = fields.Many2one('rol.persona', 'Persona')
	rol_persona_vecino_id = fields.Many2one('rol.persona', 'Persona')
	numero = fields.Char('Numero')
	titular = fields.Char('Titular')
	domicilio = fields.Char('Domicilio')

	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			values = {
				'numero': from_str(obj.get(u"numero")),
				'titular': from_str(obj.get(u"titular")),
				'domicilio': from_str(obj.get(u"domicilio")),
			}
			rec = self.env['rol.persona.telefono'].create(values).id
			return rec


class RolPersona(models.Model):
	_name = 'rol.persona'
	
	_rec_name = 'nombre'
	rol_id = fields.Char("Rol Id")
	nombre = fields.Char('Nombre')
	sexo = fields.Char('Sexo')
	edad = fields.Integer('Edad')
	tipo = fields.Char('Tipo')
	fallecido = fields.Boolean('Fallecido')
	jubilado = fields.Boolean('Jubilado')
	jubilado_beneficio = fields.Char('Jubilado beneficio')
	domicilio_ids = fields.One2many('rol.persona.domicilio', 'rol_persona_id', 'Domicilios')
	bancarizacion_id = fields.Many2one('rol.persona.bancarizacion', 'Bancarizacion')
	# emails = emails
	telefono_ids = fields.One2many('rol.persona.telefono', 'rol_persona_id', 'Telefonos')
	vecino_ids = fields.One2many('rol.persona.telefono', 'rol_persona_vecino_id', 'Vecinos')
	personas_igual_domicilio_ids = fields.One2many('rol.persona.personas', 'rol_persona_id', 'Personas igual domicilo')
	personas_relacionada_ids = fields.One2many('rol.persona.personas', 'rol_persona_relacionada_id', 'Personas relacionadas')
	marca_ids = fields.One2many('rol.persona.marca', 'rol_persona_id', 'Marcas')
	perfil_id = fields.Many2one('rol.persona.perfil', 'Perfil')
	actividad_id = fields.Many2one('rol.persona.actividad', 'Actividad')
	judicial_id = fields.Many2one('rol.judicial', 'Judicial')
	experto_id = fields.Many2one('rol.experto', "Experto")

	@api.model
	def from_dict(self, obj):
		rec = False
		if isinstance(obj, dict):
			values = {
				'rol_id': str(from_int(obj.get(u"id"))),
				'nombre': from_str(obj.get(u"nombre")),
				'sexo': from_str(obj.get(u"sexo")),
				'edad': from_int(obj.get(u"edad")),
				'tipo': from_str(obj.get(u"tipo")),
				'fallecido': from_bool(obj.get(u"fallecido")),
				'jubilado': from_bool(obj.get(u"jubilado")),
				'jubilado_beneficio': from_str(obj.get(u"jubilado_beneficio")),
			}
			rec = self.env['rol.persona'].create(values)
			rec.domicilio_ids = from_list(self.env['rol.persona.domicilio'].from_dict, obj.get(u"domicilios"))
			# 'emails' = from_list(lambda x: x, obj.get(u"emails"))
			rec.telefono_ids = from_list(self.env['rol.persona.telefono'].from_dict, obj.get(u"telefonos"))
			rec.vecino_ids = from_list(self.env['rol.persona.telefono'].from_dict, obj.get(u"vecinos"))
			rec.personas_igual_domicilio_ids = from_list(self.env['rol.persona.personas'].from_dict, obj.get(u"personas_igual_domicilio"))
			rec.personas_relacionada_ids = from_list(self.env['rol.persona.personas'].from_dict, obj.get(u"personas_relacionadas"))
			rec.marca_ids = from_list(self.env['rol.persona.marca'].from_dict, obj.get(u"marcas"))
			rec.dominios_nic_ids = from_list(self.env['rol.persona.dominiosnic'].from_dict, obj.get(u"dominios_nic"))
			rec.bancarizacion_id = self.env['rol.persona.bancarizacion'].from_dict(obj.get(u"bancarizacion"))
			rec.perfil_id = self.env['rol.persona.perfil'].from_dict(obj.get(u"perfil"))
			rec.actividad_id = self.env['rol.persona.actividad'].from_dict(obj.get(u"actividad"))
			rec.experto_id = self.env['rol.experto'].from_dict(obj.get(u"experto"))
			rec.judicial_id = self.env['rol.judicial'].from_dict(obj.get(u"judicial"))
			rec = rec.id
		return rec

class Rol(models.Model):
	_name = 'rol'

	_order = "id desc"
	partner_id = fields.Many2one('res.partner', 'Cliente')
	informe_id = fields.Many2one('rol.informe', 'Informe')
	persona_id = fields.Many2one('rol.persona', 'Persona')
	fecha = fields.Datetime('Fecha', related='informe_id.fecha_hora')
	state = fields.Char('Estado')
	company_id = fields.Many2one('res.company', 'Empresa', related='partner_id.company_id', readonly=True)
	
			
	@api.model
	def from_dict(self, obj, partner_id):
		rec = False
		if isinstance(obj, dict):
			rec = self.env['rol'].create({'partner_id': partner_id})
			rec.informe_id = self.env['rol.informe'].from_dict(obj.get(u"informe"))
			rec.persona_id = self.env['rol.persona'].from_dict(obj.get(u"persona"))
		return rec
