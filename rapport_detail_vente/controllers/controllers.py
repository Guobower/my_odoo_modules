# -*- coding: utf-8 -*-
from odoo import http

# class RapportDetailVente(http.Controller):
#     @http.route('/rapport_detail_vente/rapport_detail_vente/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rapport_detail_vente/rapport_detail_vente/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rapport_detail_vente.listing', {
#             'root': '/rapport_detail_vente/rapport_detail_vente',
#             'objects': http.request.env['rapport_detail_vente.rapport_detail_vente'].search([]),
#         })

#     @http.route('/rapport_detail_vente/rapport_detail_vente/objects/<model("rapport_detail_vente.rapport_detail_vente"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rapport_detail_vente.object', {
#             'object': obj
#         })