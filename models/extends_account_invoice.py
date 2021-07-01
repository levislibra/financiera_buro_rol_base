# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ExtendsAccountInvoice(models.Model):
	_name = 'account.invoice'
	_inherit = 'account.invoice'

	rol_state_id = fields.Many2one('res.country.state', "Provincia (ROL)", compute='_compute_rol_state')

	@api.one
	def _compute_rol_state(self):
		if self.partner_id.rol_domicilio:
			domicilio = self.partner_id.rol_domicilio.split(', ')
			if len(domicilio) > 2:
				state_obj = self.pool.get('res.country.state')
				state_ids = state_obj.search(self.env.cr, self.env.uid, [
					('name', '=ilike', domicilio[2])
				])
				if len(state_ids) > 0:
					self.rol_state_id = state_ids[0]
