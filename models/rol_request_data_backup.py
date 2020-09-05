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

from datetime import datetime
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
	if not x:
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


class ActividadesAfip:
	def __init__(self, codigo, descripcion, formulario):
			self.codigo = codigo
			self.descripcion = descripcion
			self.formulario = formulario

	@staticmethod
	def from_dict(obj):
			if isinstance(obj, dict):
				codigo = from_int(obj.get(u"codigo"))
				descripcion = from_str(obj.get(u"descripcion"))
				formulario = from_int(obj.get(u"formulario"))
				return ActividadesAfip(codigo, descripcion, formulario)

	def to_dict(self):
			result = {}
			result[u"codigo"] = from_int(self.codigo)
			result[u"descripcion"] = from_str(self.descripcion)
			result[u"formulario"] = from_int(self.formulario)
			return result


class Anses:
	def __init__(self, trabajador_casa_particular, prestacion_desempleo, plan_social, prestacion_provincial, prestacion_nacional, asignacion_universal, progresar):
			self.trabajador_casa_particular = trabajador_casa_particular
			self.prestacion_desempleo = prestacion_desempleo
			self.plan_social = plan_social
			self.prestacion_provincial = prestacion_provincial
			self.prestacion_nacional = prestacion_nacional
			self.asignacion_universal = asignacion_universal
			self.progresar = progresar

	@staticmethod
	def from_dict(obj):
			if isinstance(obj, dict):
				trabajador_casa_particular = from_bool(obj.get(u"trabajador_casa_particular"))
				prestacion_desempleo = from_bool(obj.get(u"prestacion_desempleo"))
				plan_social = from_bool(obj.get(u"plan_social"))
				prestacion_provincial = from_bool(obj.get(u"prestacion_provincial"))
				prestacion_nacional = from_bool(obj.get(u"prestacion_nacional"))
				asignacion_universal = from_bool(obj.get(u"asignacion_universal"))
				progresar = from_bool(obj.get(u"progresar"))
				return Anses(trabajador_casa_particular, prestacion_desempleo, plan_social, prestacion_provincial, prestacion_nacional, asignacion_universal, progresar)

	def to_dict(self):
			result = {}
			result[u"trabajador_casa_particular"] = from_bool(self.trabajador_casa_particular)
			result[u"prestacion_desempleo"] = from_bool(self.prestacion_desempleo)
			result[u"plan_social"] = from_bool(self.plan_social)
			result[u"prestacion_provincial"] = from_bool(self.prestacion_provincial)
			result[u"prestacion_nacional"] = from_bool(self.prestacion_nacional)
			result[u"asignacion_universal"] = from_bool(self.asignacion_universal)
			result[u"progresar"] = from_bool(self.progresar)
			return result


class Autonomo:
	def __init__(self, categoria, desde, hasta):
			self.categoria = categoria
			self.desde = desde
			self.hasta = hasta

	@staticmethod
	def from_dict(obj):
			if isinstance(obj, dict):
				categoria = from_str(obj.get(u"categoria"))
				desde = from_datetime(obj.get(u"desde"))
				hasta = from_datetime(obj.get(u"hasta"))
				return Autonomo(categoria, desde, hasta)

	def to_dict(self):
			result = {}
			result[u"categoria"] = from_str(self.categoria)
			result[u"desde"] = self.desde.isoformat()
			result[u"hasta"] = self.hasta.isoformat()
			return result


class CondicionTributaria:
	def __init__(self, monotributo, actividad, ganancias, iva, empleador, desde, hasta):
		self.monotributo = monotributo
		self.actividad = actividad
		self.ganancias = ganancias
		self.iva = iva
		self.empleador = empleador
		self.desde = desde
		self.hasta = hasta

	@staticmethod
	def from_dict(obj):
		if isinstance(obj, dict):
			monotributo = from_str(obj.get(u"monotributo"))
			actividad = from_str(obj.get(u"actividad"))
			ganancias = from_str(obj.get(u"ganancias"))
			iva = from_str(obj.get(u"iva"))
			empleador = from_str(obj.get(u"empleador"))
			desde = from_datetime(obj.get(u"desde"))
			hasta = from_datetime(obj.get(u"hasta"))
			return CondicionTributaria(monotributo, actividad, ganancias, iva, empleador, desde, hasta)

	def to_dict(self):
		result = {}
		result[u"monotributo"] = from_str(self.monotributo)
		result[u"actividad"] = from_str(self.actividad)
		result[u"ganancias"] = from_str(self.ganancias)
		result[u"iva"] = from_str(self.iva)
		result[u"empleador"] = from_str(self.empleador)
		result[u"desde"] = self.desde.isoformat()
		result[u"hasta"] = self.hasta.isoformat()
		return result


class Empleador:
	def __init__(self, empleados, periodo):
		self.empleados = empleados
		self.periodo = periodo

	@staticmethod
	def from_dict(obj):
		if isinstance(obj, dict):
			empleados = from_int(obj.get(u"empleados"))
			periodo = from_str(obj.get(u"periodo"))
			return Empleador(empleados, periodo)

	def to_dict(self):
		result = {}
		result[u"empleados"] = from_int(self.empleados)
		result[u"periodo"] = from_str(self.periodo)
		return result


class ImpuestosAfip:
	def __init__(self, activos, inactivos):
		self.activos = activos
		self.inactivos = inactivos

	@staticmethod
	def from_dict(obj):
		if isinstance(obj, dict):
			activos = from_list(lambda x: x, obj.get(u"activos"))
			inactivos = from_list(lambda x: x, obj.get(u"inactivos"))
			return ImpuestosAfip(activos, inactivos)

	def to_dict(self):
		result = {}
		result[u"activos"] = from_list(lambda x: x, self.activos)
		result[u"inactivos"] = from_list(lambda x: x, self.inactivos)
		return result


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

	def to_dict(self):
		result = {}
		result[u"ingresos"] = from_int(self.ingresos)
		result[u"ingresos_rol"] = from_int(self.ingresos_rol)
		result[u"ingresos_bruto"] = from_int(self.ingresos_bruto)
		result[u"ingresos_nse"] = from_str(self.ingresos_nse)
		return result


class Empleadore:
	def __init__(self, id, desde, hasta):
		self.id = id
		self.desde = desde
		self.hasta = hasta

	@staticmethod
	def from_dict(obj):
		if isinstance(obj, dict):
			id = from_int(obj.get(u"id"))
			desde = from_datetime(obj.get(u"desde"))
			hasta = from_datetime(obj.get(u"hasta"))
			return Empleadore(id, desde, hasta)

	def to_dict(self):
		result = {}
		result[u"id"] = from_int(self.id)
		result[u"desde"] = self.desde.isoformat()
		result[u"hasta"] = self.hasta.isoformat()
		return result


class RelacionDependencia:
	def __init__(self, empleadores):
		self.empleadores = empleadores

	@staticmethod
	def from_dict(obj):
		if isinstance(obj, dict):
			empleadores = from_list(Empleadore.from_dict, obj.get(u"empleadores"))
			return RelacionDependencia(empleadores)

	def to_dict(self):
		result = {}
		result[u"empleadores"] = from_list(lambda x: to_class(Empleadore, x), self.empleadores)
		return result


class Actividad:
	def __init__(self, empleado_publico, empleador, autonomo, anses, relacion_dependencia, actividades_afip, condicion_tributaria, impuestos_afip):
		self.empleado_publico = empleado_publico
		self.empleador = empleador
		self.autonomo = autonomo
		self.anses = anses
		self.relacion_dependencia = relacion_dependencia
		self.actividades_afip = actividades_afip
		self.condicion_tributaria = condicion_tributaria
		self.impuestos_afip = impuestos_afip

	@staticmethod
	def from_dict(obj):
		if isinstance(obj, dict):
			empleado_publico = from_bool(obj.get(u"empleado_publico"))
			empleador = Empleador.from_dict(obj.get(u"empleador"))
			autonomo = Autonomo.from_dict(obj.get(u"autonomo"))
			anses = Anses.from_dict(obj.get(u"anses"))
			relacion_dependencia = RelacionDependencia.from_dict(obj.get(u"relacion_dependencia"))
			actividades_afip = from_list(ActividadesAfip.from_dict, obj.get(u"actividades_afip"))
			condicion_tributaria = from_list(CondicionTributaria.from_dict, obj.get(u"condicion_tributaria"))
			impuestos_afip = ImpuestosAfip.from_dict(obj.get(u"impuestos_afip"))
			return Actividad(empleado_publico, empleador, autonomo, anses, relacion_dependencia, actividades_afip, condicion_tributaria, impuestos_afip)

	def to_dict(self):
		result = {}
		result[u"empleado_publico"] = from_bool(self.empleado_publico)
		result[u"empleador"] = to_class(Empleador, self.empleador)
		result[u"autonomo"] = to_class(Autonomo, self.autonomo)
		result[u"anses"] = to_class(Anses, self.anses)
		result[u"relacion_dependencia"] = to_class(RelacionDependencia, self.relacion_dependencia)
		result[u"actividades_afip"] = from_list(lambda x: to_class(ActividadesAfip, x), self.actividades_afip)
		result[u"condicion_tributaria"] = from_list(lambda x: to_class(CondicionTributaria, x), self.condicion_tributaria)
		result[u"impuestos_afip"] = to_class(ImpuestosAfip, self.impuestos_afip)
		return result


# class Entidad(Enum):
# 	BANCO_HIPOTECARIO_A = u"BANCO HIPOTECARIO A"
# 	BANCO_LA_PROVINCIA_CORDOBA_A = u"BANCO LA PROVINCIA CORDOBA A"
# 	BANCO_MACRO_A = u"BANCO MACRO A"
# 	BANCO_RIO_SANTANDER_RIO = u"BANCO RIO SANTANDER RIO"
# 	TARJETA_NARANJA_SA = u"TARJETA NARANJA SA"


class EntidadesHistorico:
	def __init__(self, entidad, periodo, situacion, monto):
		self.entidad = entidad
		self.periodo = periodo
		self.situacion = situacion
		self.monto = monto

	@staticmethod
	def from_dict(obj):
		if isinstance(obj, dict):
			entidad = from_str(obj.get(u"entidad"))
			periodo = from_str(obj.get(u"periodo"))
			situacion = from_int(obj.get(u"situacion"))
			monto = from_int(obj.get(u"monto"))
			return EntidadesHistorico(entidad, periodo, situacion, monto)

	def to_dict(self):
		result = {}
		result[u"entidad"] = from_str(self.entidad)
		result[u"periodo"] = from_str(self.periodo)
		result[u"situacion"] = from_int(self.situacion)
		result[u"monto"] = from_int(self.monto)
		return result


class EntidadesOnline:
	def __init__(self, entidad, periodo, situacion, monto):
			self.entidad = entidad
			self.periodo = periodo
			self.situacion = situacion
			self.monto = monto

	@staticmethod
	def from_dict(obj):
		if isinstance(obj, dict):
			entidad = from_str(obj.get(u"entidad"))
			periodo = from_str(obj.get(u"periodo"))
			situacion = from_int(obj.get(u"situacion"))
			monto = from_str(obj.get(u"monto"))
			return EntidadesOnline(entidad, periodo, situacion, monto)

	def to_dict(self):
			result = {}
			result[u"entidad"] = from_str(self.entidad)
			result[u"periodo"] = from_str(self.periodo)
			result[u"situacion"] = from_int(self.situacion)
			result[u"monto"] = from_str(self.monto)
			return result


class Bancarizacion:
	def __init__(self, entidades_historico, cheques_historico, sin_mora_desde, sin_mora_meses):
			self.entidades_historico = entidades_historico
			self.cheques_historico = cheques_historico
			self.sin_mora_desde = sin_mora_desde
			self.sin_mora_meses = sin_mora_meses

	@staticmethod
	def from_dict(obj):
		if isinstance(obj, dict):
			entidades_historico = from_list(EntidadesHistorico.from_dict, obj.get(u"entidades_historico"))
			cheques_historico = from_list(lambda x: x, obj.get(u"cheques_historico"))
			sin_mora_desde = from_str(obj.get(u"sin_mora_desde"))
			sin_mora_meses = from_int(obj.get(u"sin_mora_meses"))
			return Bancarizacion(entidades_historico, cheques_historico, sin_mora_desde, sin_mora_meses)

	def to_dict(self):
			result = {}
			result[u"entidades_historico"] = from_list(lambda x: to_class(EntidadesHistorico, x), self.entidades_historico)
			result[u"cheques_historico"] = from_list(lambda x: x, self.cheques_historico)
			result[u"sin_mora_desde"] = from_str(self.sin_mora_desde)
			result[u"sin_mora_meses"] = from_int(self.sin_mora_meses)
			return result


class AfipConstancia:
	def __init__(self, nombre, procesada):
		self.nombre = nombre
		self.procesada = procesada

	@staticmethod
	def from_dict(obj):
		if isinstance(obj, dict):
			nombre = from_str(obj.get(u"nombre"))
			procesada = from_bool(obj.get(u"procesada"))
			return AfipConstancia(nombre, procesada)

	def to_dict(self):
		result = {}
		result[u"nombre"] = from_str(self.nombre)
		result[u"procesada"] = from_bool(self.procesada)
		return result


class Consultas:
	def __init__(self, bcra, afip_constancia, afip_padron, afip_misaportes, anses, anses_certificacion, anses_cobro, sssalud_serviciodomestico):
			self.bcra = bcra
			self.afip_constancia = afip_constancia
			self.afip_padron = afip_padron
			self.afip_misaportes = afip_misaportes
			self.anses = anses
			self.anses_certificacion = anses_certificacion
			self.anses_cobro = anses_cobro
			self.sssalud_serviciodomestico = sssalud_serviciodomestico

	@staticmethod
	def from_dict(obj):
		if isinstance(obj, dict):
			bcra = AfipConstancia.from_dict(obj.get(u"bcra"))
			afip_constancia = AfipConstancia.from_dict(obj.get(u"afip_constancia"))
			afip_padron = AfipConstancia.from_dict(obj.get(u"afip_padron"))
			afip_misaportes = AfipConstancia.from_dict(obj.get(u"afip_misaportes"))
			anses = AfipConstancia.from_dict(obj.get(u"anses"))
			anses_certificacion = AfipConstancia.from_dict(obj.get(u"anses_certificacion"))
			anses_cobro = AfipConstancia.from_dict(obj.get(u"anses_cobro"))
			sssalud_serviciodomestico = AfipConstancia.from_dict(obj.get(u"sssalud_serviciodomestico"))
			return Consultas(bcra, afip_constancia, afip_padron, afip_misaportes, anses, anses_certificacion, anses_cobro, sssalud_serviciodomestico)

	def to_dict(self):
			result = {}
			result[u"bcra"] = to_class(AfipConstancia, self.bcra)
			result[u"afip_constancia"] = to_class(AfipConstancia, self.afip_constancia)
			result[u"afip_padron"] = to_class(AfipConstancia, self.afip_padron)
			result[u"afip_misaportes"] = to_class(AfipConstancia, self.afip_misaportes)
			result[u"anses"] = to_class(AfipConstancia, self.anses)
			result[u"anses_certificacion"] = to_class(AfipConstancia, self.anses_certificacion)
			result[u"anses_cobro"] = to_class(AfipConstancia, self.anses_cobro)
			result[u"sssalud_serviciodomestico"] = to_class(AfipConstancia, self.sssalud_serviciodomestico)
			return result


class Informe:
	def __init__(self, id, cliente, consultas_online, fecha_hora):
			self.id = id
			self.cliente = cliente
			self.fecha_hora = fecha_hora
			self.consultas_online = consultas_online

	@staticmethod
	def from_dict(obj):
		if isinstance(obj, dict):
			id = from_int(obj.get(u"id"))
			cliente = from_int(obj.get(u"cliente"))
			fecha_hora = from_int(obj.get(u"fecha_hora"))
			consultas_online = Consultas.from_dict(obj.get(u"consultas_online"))
			return Informe(id, cliente, consultas_online, fecha_hora)

	def to_dict(self):
			result = {}
			result[u"id"] = from_int(self.id)
			result[u"cliente"] = from_int(self.cliente)
			result[u"fecha_hora"] = from_int(self.fecha_hora)
			result[u"consultas_online"] = to_class(Consultas, self.consultas_online)
			return result


# class Provincia(Enum):
# 	CORDOBA = u"cordoba"


# class Rol(Enum):
# 	DIRECTOR_SUPLENTE_EDICTO_SOCIETARIO = u"director_suplente_edicto_societario"
# 	EMPTY = u""


class Juicio:
	def __init__(self, fecha, provincia, rol, texto):
			self.fecha = fecha
			self.provincia = provincia
			self.rol = rol
			self.texto = texto

	@staticmethod
	def from_dict(obj):
		if isinstance(obj, dict):
			fecha = from_str(obj.get(u"fecha"))
			provincia = from_str(obj.get(u"provincia"))
			rol = from_str(obj.get(u"rol"))
			texto = from_str(obj.get(u"texto"))
			return Juicio(fecha, provincia, rol, texto)

	def to_dict(self):
			result = {}
			result[u"fecha"] = from_str(self.fecha)
			result[u"provincia"] = from_str(self.provincia)
			result[u"rol"] = from_str(self.rol)
			result[u"texto"] = from_str(self.texto)
			return result

class Judicial:
	def __init__(self, juicios, concursos_y_quiebras):
			self.juicios = juicios
			self.concursos_y_quiebras = concursos_y_quiebras

	@staticmethod
	def from_dict(obj):
		if isinstance(obj, dict):
			juicios = from_list(Juicio.from_dict, obj.get(u"juicios"))
			concursos_y_quiebras = from_list(lambda x: x, obj.get(u"concursos_y_quiebras"))
			return Judicial(juicios, concursos_y_quiebras)

	def to_dict(self):
			result = {}
			result[u"juicios"] = from_list(lambda x: to_class(Juicio, x), self.juicios)
			result[u"concursos_y_quiebras"] = from_list(lambda x: x, self.concursos_y_quiebras)
			return result


class Domicilio:
	def __init__(self, domicilio, tipo):
			self.domicilio = domicilio
			self.tipo = tipo

	@staticmethod
	def from_dict(obj):
		if isinstance(obj, dict):
			domicilio = from_str(obj.get(u"domicilio"))
			tipo = from_str(obj.get(u"tipo"))
			return Domicilio(domicilio, tipo)

	def to_dict(self):
			result = {}
			result[u"domicilio"] = from_str(self.domicilio)
			result[u"tipo"] = from_str(self.tipo)
			return result


class DominiosNIC:
	def __init__(self, dominio, entidad, tipo, fecha):
			self.dominio = dominio
			self.entidad = entidad
			self.tipo = tipo
			self.fecha = fecha

	@staticmethod
	def from_dict(obj):
		if isinstance(obj, dict):
			dominio = from_str(obj.get(u"dominio"))
			entidad = from_str(obj.get(u"entidad"))
			tipo = from_str(obj.get(u"tipo"))
			fecha = from_datetime(obj.get(u"fecha"))
			return DominiosNIC(dominio, entidad, tipo, fecha)

	def to_dict(self):
			result = {}
			result[u"dominio"] = from_str(self.dominio)
			result[u"entidad"] = from_str(self.entidad)
			result[u"tipo"] = from_str(self.tipo)
			result[u"fecha"] = self.fecha.isoformat()
			return result


class ResolucionEnum(Enum):
	CONCEDIDA = u"Concedida"
	EMPTY = u""


class ActaTipo(Enum):
	MIXTA = u"Mixta"


class Acta:
	def __init__(self, numero, fecha_presentacion, tipo, clase, resolucion):
			self.numero = numero
			self.fecha_presentacion = fecha_presentacion
			self.tipo = tipo
			self.clase = clase
			self.resolucion = resolucion

	@staticmethod
	def from_dict(obj):
		if isinstance(obj, dict):
			numero = from_int(obj.get(u"numero"))
			fecha_presentacion = from_str(obj.get(u"fecha_presentacion"))
			tipo = ActaTipo(obj.get(u"tipo"))
			clase = from_int(obj.get(u"clase"))
			resolucion = from_union([from_int, ResolucionEnum], obj.get(u"resolucion"))
			return Acta(numero, fecha_presentacion, tipo, clase, resolucion)

	def to_dict(self):
			result = {}
			result[u"numero"] = from_int(self.numero)
			result[u"fecha_presentacion"] = from_str(self.fecha_presentacion)
			result[u"tipo"] = to_enum(ActaTipo, self.tipo)
			result[u"clase"] = from_int(self.clase)
			result[u"resolucion"] = from_union([from_int, lambda x: to_enum(ResolucionEnum, x)], self.resolucion)
			return result


class Marca:
	def __init__(self, nombre, actas):
			self.nombre = nombre
			self.actas = actas

	@staticmethod
	def from_dict(obj):
		if isinstance(obj, dict):
			nombre = from_str(obj.get(u"nombre"))
			actas = from_list(Acta.from_dict, obj.get(u"actas"))
			return Marca(nombre, actas)

	def to_dict(self):
			result = {}
			result[u"nombre"] = from_str(self.nombre)
			result[u"actas"] = from_list(lambda x: to_class(Acta, x), self.actas)
			return result


class Perfil:
	def __init__(self, letra, texto):
			self.letra = letra
			self.texto = texto

	@staticmethod
	def from_dict(obj):
		if isinstance(obj, dict):
			letra = from_str(obj.get(u"letra"))
			texto = from_str(obj.get(u"texto"))
			return Perfil(letra, texto)

	def to_dict(self):
			result = {}
			result[u"letra"] = from_str(self.letra)
			result[u"texto"] = from_str(self.texto)
			return result


class SexoEnum(Enum):
	EMPTY = u""
	F = u"F"
	FEMENINO = u"FEMENINO"
	MASCULINO = u"MASCULINO"


class Personas:
	def __init__(self, nombre, sexo, domicilio, id, relacion):
			self.nombre = nombre
			self.sexo = sexo
			self.domicilio = domicilio
			self.id = id
			self.relacion = relacion

	@staticmethod
	def from_dict(obj):
		if isinstance(obj, dict):
			nombre = from_str(obj.get(u"nombre"))
			sexo = SexoEnum(obj.get(u"sexo"))
			domicilio = from_str(obj.get(u"domicilio"))
			id = from_int(obj.get(u"id"))
			relacion = from_union([from_str, from_none], obj.get(u"relacion"))
			return Personas(nombre, sexo, domicilio, id, relacion)

	def to_dict(self):
			result = {}
			result[u"nombre"] = from_str(self.nombre)
			result[u"sexo"] = to_enum(SexoEnum, self.sexo)
			result[u"domicilio"] = from_str(self.domicilio)
			result[u"id"] = from_int(self.id)
			result[u"relacion"] = from_union([from_str, from_none], self.relacion)
			return result


class Telefono:
	def __init__(self, anio_guia, numero, titular, domicilio):
			self.anio_guia = anio_guia
			self.numero = numero
			self.titular = titular
			self.domicilio = domicilio

	@staticmethod
	def from_dict(obj):
		if isinstance(obj, dict):
			anio_guia = from_union([from_int, from_str], obj.get(u"anio_guia"))
			numero = from_str(obj.get(u"numero"))
			titular = from_str(obj.get(u"titular"))
			domicilio = from_str(obj.get(u"domicilio"))
			return Telefono(anio_guia, numero, titular, domicilio)

	def to_dict(self):
			result = {}
			result[u"anio_guia"] = from_union([from_int, from_str], self.anio_guia)
			result[u"numero"] = from_str(self.numero)
			result[u"titular"] = from_str(self.titular)
			result[u"domicilio"] = from_str(self.domicilio)
			return result


class Persona:
	def __init__(self, id, nombre, sexo, edad, tipo, fallecido, jubilado, jubilado_beneficio, domicilios, emails, telefonos, marcas, homonimos, vecinos, personas_igual_domicilio, personas_relacionadas, dominios_nic, perfil, actividad, bancarizacion):
			self.id = id
			self.nombre = nombre
			self.sexo = sexo
			self.edad = edad
			self.tipo = tipo
			self.fallecido = fallecido
			self.jubilado = jubilado
			self.jubilado_beneficio = jubilado_beneficio
			self.domicilios = domicilios
			self.emails = emails
			self.telefonos = telefonos
			self.marcas = marcas
			self.homonimos = homonimos
			self.vecinos = vecinos
			self.personas_igual_domicilio = personas_igual_domicilio
			self.personas_relacionadas = personas_relacionadas
			self.dominios_nic = dominios_nic
			self.perfil = perfil
			self.actividad = actividad
			self.bancarizacion = bancarizacion

	@staticmethod
	def from_dict(obj):
		if isinstance(obj, dict):
			id = from_int(obj.get(u"id"))
			nombre = from_str(obj.get(u"nombre"))
			sexo = from_str(obj.get(u"sexo"))
			edad = from_int(obj.get(u"edad"))
			tipo = SexoEnum(obj.get(u"tipo"))
			fallecido = from_bool(obj.get(u"fallecido"))
			jubilado = from_bool(obj.get(u"jubilado"))
			jubilado_beneficio = from_str(obj.get(u"jubilado_beneficio"))
			domicilios = from_list(Domicilio.from_dict, obj.get(u"domicilios"))
			emails = from_list(lambda x: x, obj.get(u"emails"))
			telefonos = from_list(Telefono.from_dict, obj.get(u"telefonos"))
			marcas = from_list(Marca.from_dict, obj.get(u"marcas"))
			homonimos = from_list(lambda x: x, obj.get(u"homonimos"))
			vecinos = from_list(lambda x: x, obj.get(u"vecinos"))
			personas_igual_domicilio = from_list(Personas.from_dict, obj.get(u"personas_igual_domicilio"))
			personas_relacionadas = from_list(Personas.from_dict, obj.get(u"personas_relacionadas"))
			dominios_nic = from_list(DominiosNIC.from_dict, obj.get(u"dominios_nic"))
			perfil = Perfil.from_dict(obj.get(u"perfil"))
			actividad = Actividad.from_dict(obj.get(u"actividad"))
			bancarizacion = Bancarizacion.from_dict(obj.get(u"bancarizacion"))
			return Persona(id, nombre, sexo, edad, tipo, fallecido, jubilado, jubilado_beneficio, domicilios, emails, telefonos, marcas, homonimos, vecinos, personas_igual_domicilio, personas_relacionadas, dominios_nic, perfil, actividad, bancarizacion)

	def to_dict(self):
			result = {}
			result[u"id"] = from_int(self.id)
			result[u"nombre"] = from_str(self.nombre)
			result[u"sexo"] = from_str(self.sexo)
			result[u"edad"] = from_int(self.edad)
			result[u"tipo"] = to_enum(SexoEnum, self.tipo)
			result[u"fallecido"] = from_bool(self.fallecido)
			result[u"jubilado"] = from_bool(self.jubilado)
			result[u"jubilado_beneficio"] = from_str(self.jubilado_beneficio)
			result[u"domicilios"] = from_list(lambda x: to_class(Domicilio, x), self.domicilios)
			result[u"emails"] = from_list(lambda x: x, self.emails)
			result[u"telefonos"] = from_list(lambda x: to_class(Telefono, x), self.telefonos)
			result[u"marcas"] = from_list(lambda x: to_class(Marca, x), self.marcas)
			result[u"homonimos"] = from_list(lambda x: x, self.homonimos)
			result[u"vecinos"] = from_list(lambda x: x, self.vecinos)
			result[u"personas_igual_domicilio"] = from_list(lambda x: to_class(Personas, x), self.personas_igual_domicilio)
			result[u"personas_relacionadas"] = from_list(lambda x: to_class(Personas, x), self.personas_relacionadas)
			result[u"dominios_nic"] = from_list(lambda x: to_class(DominiosNIC, x), self.dominios_nic)
			result[u"perfil"] = to_class(Perfil, self.perfil)
			result[u"actividad"] = to_class(Actividad, self.actividad)
			result[u"bancarizacion"] = to_class(Bancarizacion, self.bancarizacion)
			return result

class Rol:
	def __init__(self, informe, persona, experto):
			self.informe = informe
			self.persona = persona
			self.experto = experto

	@staticmethod
	def from_dict(obj):
		if isinstance(obj, dict):
			informe = Informe.from_dict(obj.get(u"informe"))
			persona = Persona.from_dict(obj.get(u"persona"))
			experto = from_bool(obj.get(u"experto"))
			return Rol(informe, persona, experto)

	def to_dict(self):
			result = {}
			result[u"informe"] = to_class(Informe, self.informe)
			result[u"persona"] = to_class(Persona, self.persona)
			result[u"experto"] = from_bool(self.experto)
			return result


def rol_from_dict(s):
	return Rol.from_dict(s)

def rol_to_dict(x):
	return to_class(Rol, x)
