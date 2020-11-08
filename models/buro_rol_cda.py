# -*- coding: utf-8 -*-

from openerp import models, fields, api

class FinancieraBuroRolCda(models.Model):
	_name = 'financiera.buro.rol.cda'

	_order = 'orden asc'
	config_id = fields.Many2one('financiera.buro.rol.configuracion', 'Configuracion')
	name = fields.Char('Nombre')
	activo = fields.Boolean("Activo")
	orden = fields.Integer("Orden")
	general_ids = fields.One2many('financiera.buro.rol.cda.general', 'cda_id', 'General')
	sexo_edad_ids = fields.One2many('financiera.buro.rol.cda.sexo_edad', 'cda_id', 'Sexo y edad')
	actividad_ids = fields.One2many('financiera.buro.rol.cda.actividad', 'cda_id', 'Actividad')
	bancarizacion_ids = fields.One2many('financiera.buro.rol.cda.bancarizacion', 'cda_id', 'Bancarizacion')
	# result
	partner_tipo_id = fields.Many2one('financiera.partner.tipo', 'Tipo de cliente')
	capacidad_pago_mensual = fields.Float('CPM')
	company_id = fields.Many2one('res.company', 'Empresa', required=False, default=lambda self: self.env['res.company']._company_default_get('financiera.buro.rol.cda'))

	def evaluar_cda(self, partner_id, fallecido, perfil_letra, sexo, edad, empleado_vigencia, monotributista_vigencia, autonomo_vigencia,
	 empleado_antiguedad, monotributista_antiguedad, autonomo_antiguedad, 
	 empleado_continuidad, monotributista_continuidad, autonomo_continuidad, jubilado_pensionado,
	 resumen_situaciones_bancarias):
		values = {
			'cda_id': self.id,
			'partner_id': partner_id,
		}
		reporte_id = self.env['financiera.buro.rol.cda.reporte'].create(values)

		condicion_generales = 'aprobado'
		for general_id in self.general_ids:
			if general_id.evaluar_general(reporte_id, fallecido, perfil_letra) == 'rechazado':
				condicion_generales = 'rechazado'
		
		condicion_sexo_edad = 'aprobado'
		for sexo_edad_id in self.sexo_edad_ids:
			if sexo_edad_id.evaluar_sexo_edad(reporte_id, sexo, edad) == 'rechazado':
				condicion_sexo_edad = 'rechazado'
		
		condicion_actividad = 'aprobado'
		for actividad_id in self.actividad_ids:
			if actividad_id.evaluar_actividad(reporte_id, empleado_vigencia, monotributista_vigencia, autonomo_vigencia,
	 		empleado_antiguedad, monotributista_antiguedad, autonomo_antiguedad, 
	 		empleado_continuidad, monotributista_continuidad, autonomo_continuidad, jubilado_pensionado) == 'rechazado':
				condicion_actividad = 'rechazado'
		
		condicion_bancarizacion = 'aprobado'
		for bancarizacion_id in self.bancarizacion_ids:
			if bancarizacion_id.evaluar_bancarizacion(reporte_id, resumen_situaciones_bancarias) == 'rechazado':
				condicion_bancarizacion = 'rechazado'
		
		ret = 'aprobado'
		if condicion_generales == 'rechazado' or condicion_sexo_edad == 'rechazado' or condicion_actividad == 'rechazado' or condicion_bancarizacion == 'rechazado':
			ret = 'rechazado'
		return ret

class FinancieraBuroRolCdaGeneral(models.Model):
	_name = 'financiera.buro.rol.cda.general'

	cda_id = fields.Many2one('financiera.buro.rol.cda', 'CDA')
	control = fields.Char('Codigo', compute='_compute_control')
	accion = fields.Selection([('rechazar', 'Rechazar')], 'Accion', default='rechazar')
	motivo = fields.Selection([
		('fallecido', 'Fallecido'),
		('A', 'Perfil A'), ('B', 'Perfil B'), ('C', 'Perfil C'),
		('D', 'Perfil D'), ('E', 'Perfil E'), ('F', 'Perfil F'),
		('G', 'Perfil G')], 'Motivo')

	@api.one
	def _compute_control(self):
		self.control = "GL/" + str(self.id).zfill(5)

	def evaluar_general(self, reporte_id, fallecido, perfil_letra):
		condicion1_rechazo = False
		if self.motivo == 'fallecido':
			condicion1_rechazo = fallecido
			if condicion1_rechazo:
				values = {
					'reporte_id': reporte_id.id,
					'control': self.control,
					'name': "Rechazado por: Persona fallecida.",
				}
				detalle_id = self.env['financiera.buro.rol.cda.reporte.detalle'].create(values)
				reporte_id.detalle_ids = [detalle_id.id]

		condicion2_rechazo = False
		if self.motivo != 'fallecido':
			condicion2_rechazo = self.motivo == perfil_letra
			if condicion2_rechazo:
				values = {
					'reporte_id': reporte_id.id,
					'control': self.control,
					'name': "Rechazado por: Ser perfil " + str(perfil_letra),
				}
				detalle_id = self.env['financiera.buro.rol.cda.reporte.detalle'].create(values)
				reporte_id.detalle_ids = [detalle_id.id]
		ret = 'aprobado'
		if condicion1_rechazo or condicion2_rechazo:
			ret = 'rechazado'
		return ret


class FinancieraBuroRolCdaSexoEdad(models.Model):
	_name = 'financiera.buro.rol.cda.sexo_edad'

	cda_id = fields.Many2one('financiera.buro.rol.cda', 'CDA')
	control = fields.Char('Codigo', compute='_compute_control')
	accion = fields.Selection([('rechazar', 'Rechazar')], 'Accion', default='rechazar')
	sexo = fields.Selection([('M', 'Masculino'), ('F', 'Femenino')], 'Sexo')
	edad_condicion = fields.Selection([('menor', 'menor'), ('mayor', 'mayor')], 'Condicion')
	edad = fields.Integer('Edad')
	company_id = fields.Many2one('res.company', 'Empresa', required=False, default=lambda self: self.env['res.company']._company_default_get('financiera.buro.rol.cda.edad_sexo'))

	@api.one
	def _compute_control(self):
		self.control = "SE/" + str(self.id).zfill(5)

	def evaluar_sexo_edad(self, reporte_id, sexo, edad):
		condicion1_rechazo = False
		if self.sexo == sexo and self.edad_condicion == 'menor':
			condicion1_rechazo = edad < self.edad
			if condicion1_rechazo:
				values = {
					'reporte_id': reporte_id.id,
					'control': self.control,
					'name': "Rechazado por: Sexo " + str(self.sexo) + " de edad menor a " + str(self.edad),
				}
				detalle_id = self.env['financiera.buro.rol.cda.reporte.detalle'].create(values)
				reporte_id.detalle_ids = [detalle_id.id]

		condicion2_rechazo = False
		if sexo == self.sexo and self.edad_condicion == 'mayor':
			condicion2_rechazo = edad > self.edad
			if condicion2_rechazo:
				values = {
					'reporte_id': reporte_id.id,
					'control': self.control,
					'name': "Rechazado por: Sexo " + str(self.sexo) + " de edad mayor a " + str(self.edad),
				}
				detalle_id = self.env['financiera.buro.rol.cda.reporte.detalle'].create(values)
				reporte_id.detalle_ids = [detalle_id.id]
		ret = 'aprobado'
		if condicion1_rechazo or condicion2_rechazo:
			ret = 'rechazado'
		return ret

class FinancieraBuroRolCdaActividad(models.Model):
	_name = 'financiera.buro.rol.cda.actividad'

	cda_id = fields.Many2one('financiera.buro.rol.cda', 'CDA')
	control = fields.Char('Codigo', compute='_compute_control')
	accion = fields.Selection([('rechazar', 'Rechazar')], 'Accion', default='rechazar')
	actividad = fields.Selection([
		('sin_actividad', 'Sin actividad vigente'),
		('jubilado_pensionado', 'Jubilado y/o pensionado'),
		('empleado', 'Empleado'),
		('monotributista', 'Monotributista'),
		('autonomo', 'Autonomo')], 'Actividad')
	# antiguedad_condicion = fields.Selection([('menor', 'con meses de antiguedad menor a')], 'Condicion', default='menor')
	antiguedad = fields.Integer('Con meses de antiguedad menor a')
	# continuidad_condicion = fields.Selection([('menor', 'y continuidad menor a')], 'Condicion', default='menor')
	continuidad = fields.Integer('Con meses de continuidad menor a')
	company_id = fields.Many2one('res.company', 'Empresa', required=False, default=lambda self: self.env['res.company']._company_default_get('financiera.buro.rol.cda.edad_sexo'))

	@api.one
	def _compute_control(self):
		self.control = "ACT/" + str(self.id).zfill(5)

	def evaluar_actividad(self, reporte_id, empleado_vigencia, monotributista_vigencia, autonomo_vigencia,
	 empleado_antiguedad, monotributista_antiguedad, autonomo_antiguedad, 
	 empleado_continuidad, monotributista_continuidad, autonomo_continuidad, jubilado_pensionado=False):
		condicion1_rechazo = False
		if self.actividad == 'sin_actividad':
			condicion1_rechazo = not empleado_vigencia and not monotributista_vigencia and not autonomo_vigencia
			if condicion1_rechazo:
				values = {
					'reporte_id': reporte_id.id,
					'control': self.control,
					'name': "Rechazado por: No registra actividad vigente como empleado, monotributista ni autonomo.",
				}
				detalle_id = self.env['financiera.buro.rol.cda.reporte.detalle'].create(values)
				reporte_id.detalle_ids = [detalle_id.id]
		
		condicion2_rechazo = False
		if self.actividad == 'jubilado_pensionado':
			condicion2_rechazo = jubilado_pensionado
			if condicion2_rechazo:
				values = {
					'reporte_id': reporte_id.id,
					'control': self.control,
					'name': "Rechazado por: Ser jubilado y/o pensionado.",
				}
				detalle_id = self.env['financiera.buro.rol.cda.reporte.detalle'].create(values)
				reporte_id.detalle_ids = [detalle_id.id]
		
		condicion3_rechazo = False
		if self.actividad == 'empleado' and empleado_vigencia:
			detalle_rechazo = ''
			if self.antiguedad == 0 or self.continuidad == 0:
				# Rechazar por ser empleado
				detalle_rechazo = "Rechazado por: Ser empleado."
				condicion3_rechazo = True
			elif empleado_antiguedad < self.antiguedad or empleado_continuidad < self.continuidad:
				detalle_rechazo = "Rechazado por: Ser empleado con antiguedad menor a " + str(self.antiguedad) + " meses o continuidad menor a " + str(self.continuidad) + " meses."
				condicion3_rechazo = True
			if condicion3_rechazo:
				values = {
					'reporte_id': reporte_id.id,
					'control': self.control,
					'name': detalle_rechazo,
				}
				detalle_id = self.env['financiera.buro.rol.cda.reporte.detalle'].create(values)
				reporte_id.detalle_ids = [detalle_id.id]
		
		condicion4_rechazo = False
		if self.actividad == 'monotributista' and monotributista_vigencia:
			detalle_rechazo = ''
			if self.antiguedad == 0 or self.continuidad == 0:
				# Rechazar por ser monotributista
				detalle_rechazo = "Rechazado por: Ser monotributista."
				condicion4_rechazo = True
			elif monotributista_antiguedad < self.antiguedad or monotributista_continuidad < self.continuidad:
				detalle_rechazo = "Rechazado por: Ser monotributista con antiguedad menor a " + str(self.antiguedad) + " meses o continuidad menor a " + str(self.continuidad) + " meses."
				condicion4_rechazo = True
			if condicion4_rechazo:
				values = {
					'reporte_id': reporte_id.id,
					'control': self.control,
					'name': detalle_rechazo,
				}
				detalle_id = self.env['financiera.buro.rol.cda.reporte.detalle'].create(values)
				reporte_id.detalle_ids = [detalle_id.id]
		
		condicion5_rechazo = False
		if self.actividad == 'autonomo' and autonomo_vigencia:
			detalle_rechazo = ''
			if self.antiguedad == 0 or self.continuidad == 0:
				# Rechazar por ser autonomo
				detalle_rechazo = "Rechazado por: Ser autonomo."
				condicion5_rechazo = True
			elif autonomo_antiguedad < self.antiguedad or autonomo_continuidad < self.continuidad:
				detalle_rechazo = "Rechazado por: Ser autonomo con antiguedad menor a " + str(self.antiguedad) + " meses o continuidad menor a " + str(self.continuidad) + " meses."
				condicion5_rechazo = True
			if condicion5_rechazo:
				values = {
					'reporte_id': reporte_id.id,
					'control': self.control,
					'name': detalle_rechazo,
				}
				detalle_id = self.env['financiera.buro.rol.cda.reporte.detalle'].create(values)
				reporte_id.detalle_ids = [detalle_id.id]
		ret = 'aprobado'
		if condicion1_rechazo or condicion2_rechazo or condicion3_rechazo or condicion4_rechazo or condicion5_rechazo:
			ret = 'rechazado'
		return ret

class FinancieraBuroRolCdaBancarizacion(models.Model):
	_name = 'financiera.buro.rol.cda.bancarizacion'

	cda_id = fields.Many2one('financiera.buro.rol.cda', 'CDA')
	control = fields.Char('Codigo', compute='_compute_control')
	accion = fields.Selection([('rechazar', 'Rechazar')], 'Accion', default='rechazar')
	situaciones_cantidad = fields.Integer('Si tiene cantidad de situaciones o mas de')
	situaciones_tipo = fields.Selection([
		(1, "1"), (2, "2"), (3, "3"),
		(4, "4"), (5, "5"),	(6, "6")], 'Tipo de situaciones mayor o igual a')
	periodo = fields.Selection([
		('ultimo_mes', 'Ultimo mes'),
		('tres_meses', 'Ultimos tres meses'),
		('seis_meses', 'Ultimos seis meses'),
		('doce_meses', 'Ultimos doce meses')], 'Periodo')
	company_id = fields.Many2one('res.company', 'Empresa', required=False, default=lambda self: self.env['res.company']._company_default_get('financiera.buro.rol.cda.edad_sexo'))

	@api.one
	def _compute_control(self):
		self.control = "BCN/" + str(self.id).zfill(5)

	def evaluar_bancarizacion(self, reporte_id, resumen_situaciones_bancarias):
		condicion1_rechazo = False
		detalle_rechazo = ""
		situaciones_periodo = resumen_situaciones_bancarias[self.periodo]
		situaciones_periodo_solicitadas = 0
		i = self.situaciones_tipo-1
		while i < 6:
			situaciones_periodo_solicitadas += situaciones_periodo[i]
			i += 1
		if self.situaciones_cantidad == 0:
			condicion1_rechazo = situaciones_periodo_solicitadas == 0
			detalle_rechazo = "Rechazado por: No poseer ninguna situacion mayor o igual a "+str(self.situaciones_tipo)  + " en los ultimo/s " + str(self.periodo).replace('_', ' ').replace('ultimo', ' ')
		else:
			condicion1_rechazo = situaciones_periodo_solicitadas >= self.situaciones_cantidad
			detalle_rechazo = "Rechazado por: Poseer " + str(situaciones_periodo_solicitadas) + " situaciones de tipo mayor o igual a " + str(self.situaciones_tipo) + " en los ultimo/s " + str(self.periodo).replace('_', ' ').replace('ultimo', ' ')
		if condicion1_rechazo:
			values = {
				'reporte_id': reporte_id.id,
				'control': self.control,
				'name': detalle_rechazo,
			}
			detalle_id = self.env['financiera.buro.rol.cda.reporte.detalle'].create(values)
			reporte_id.detalle_ids = [detalle_id.id]
		evaluacion = 'aprobado'
		if condicion1_rechazo:
			evaluacion = 'rechazado'
		return evaluacion

class FinancieraBuroRolCdaReporte(models.Model):
	_name = 'financiera.buro.rol.cda.reporte'

	_order = 'id desc'
	partner_id = fields.Many2one('res.partner', 'Cliente')
	cda_id = fields.Many2one('financiera.buro.rol.cda', 'CDA evaluado')
	detalle_ids = fields.One2many('financiera.buro.rol.cda.reporte.detalle', 'reporte_id')
	resultado = fields.Selection([
		('aprobado', 'Aprobado'),
		('rechazado', 'Rechazado')],
		'Resultado', compute='_compute_resultado')

	@api.one
	def _compute_resultado(self):
		self.resultado = 'aprobado'
		if len(self.detalle_ids) > 0:
			self.resultado = 'rechazado'

class FinancieraBuroRolCdaReporteDetalle(models.Model):
	_name = 'financiera.buro.rol.cda.reporte.detalle'

	_order = 'id desc'
	control = fields.Char('Codigo')
	reporte_id = fields.Many2one('financiera.buro.rol.cda.reporte', 'Reporte')
	name = fields.Char('Detalle')

