# -*- coding: utf-8 -*-
from odoo import http

# class FacturesMm(http.Controller):
#     @http.route('/factures_mm/factures_mm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/factures_mm/factures_mm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('factures_mm.listing', {
#             'root': '/factures_mm/factures_mm',
#             'objects': http.request.env['factures_mm.factures_mm'].search([]),
#         })

#     @http.route('/factures_mm/factures_mm/objects/<model("factures_mm.factures_mm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('factures_mm.object', {
#             'object': obj
#         })