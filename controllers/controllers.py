# -*- coding: utf-8 -*-
from openerp import http

# class FinancieraBuroRolBase(http.Controller):
#     @http.route('/financiera_buro_rol_base/financiera_buro_rol_base/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/financiera_buro_rol_base/financiera_buro_rol_base/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('financiera_buro_rol_base.listing', {
#             'root': '/financiera_buro_rol_base/financiera_buro_rol_base',
#             'objects': http.request.env['financiera_buro_rol_base.financiera_buro_rol_base'].search([]),
#         })

#     @http.route('/financiera_buro_rol_base/financiera_buro_rol_base/objects/<model("financiera_buro_rol_base.financiera_buro_rol_base"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('financiera_buro_rol_base.object', {
#             'object': obj
#         })