# -*- coding: utf-8 -*-

from openerp import models, fields, api

class FinancieraRolInforme(models.Model):
	_name = 'financiera.rol.informe'
	
	_order = 'create_date desc'
	name = fields.Char('Nombre')
	partner_id = fields.Many2one('res.partner', 'Cliente')
	variable_ids = fields.One2many('financiera.rol.informe.variable', 'informe_id', 'Variables')
	cda_resultado_ids = fields.One2many('financiera.rol.cda.resultado', 'informe_id', 'Resultados')
	company_id = fields.Many2one('res.company', 'Empresa', required=False, default=lambda self: self.env['res.company']._company_default_get('financiera.rol.informe'))
	
	@api.model
	def create(self, values):
		rec = super(FinancieraRolInforme, self).create(values)
		id_informe = self.env.user.company_id.rol_configuracion_id.id_informe
		rec.update({
			'name': 'ROL/INFORME/' + str(id_informe).zfill(8),
		})
		return rec

	@api.one
	def ejecutar_cdas(self):
		cda_obj = self.pool.get('financiera.rol.cda')
		cda_ids = cda_obj.search(self.env.cr, self.env.uid, [
			('activo', '=', True),
			('company_id', '=', self.company_id.id),
		])
		if len(cda_ids) > 0:
			self.partner_id.rol_capacidad_pago_mensual = 0
			self.partner_id.capacidad_pago_mensual = 0
			self.partner_id.rol_partner_tipo_id = None
			self.partner_id.partner_tipo_id = None
		for _id in cda_ids:
			cda_id = cda_obj.browse(self.env.cr, self.env.uid, _id)
			ret = cda_id.ejecutar(self.id)
			if ret['resultado'] == 'aprobado':
				self.partner_id.rol_capacidad_pago_mensual = ret['cpm']
				self.partner_id.capacidad_pago_mensual = ret['cpm']
				self.partner_id.rol_partner_tipo_id = ret['partner_tipo_id']
				self.partner_id.partner_tipo_id = ret['partner_tipo_id']
				break

class FinancierarolInformeVariable(models.Model):
	_name = 'financiera.rol.informe.variable'
	
	_order = 'profundidad asc,id asc'
	informe_id = fields.Many2one('financiera.rol.informe', 'Informe')
	partner_id = fields.Many2one('res.partner', 'Cliente')
	name = fields.Char('Nombre')
	sub_name = fields.Char('Sub Nombre')
	valor = fields.Char('Valor')
	fecha = fields.Date('Fecha')
	descripcion = fields.Char('Descripcion')
	tipo = fields.Char('Tipo')
	profundidad = fields.Integer('Profundidad', default=0)
	company_id = fields.Many2one('res.company', 'Empresa', required=False, default=lambda self: self.env['res.company']._company_default_get('financiera.rol.informe'))
	