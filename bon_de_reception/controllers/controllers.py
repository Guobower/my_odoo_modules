# -*- coding: utf-8 -*-
from odoo import http

# class BonDeReception(http.Controller):
#     @http.route('/bon_de_reception/bon_de_reception/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bon_de_reception/bon_de_reception/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bon_de_reception.listing', {
#             'root': '/bon_de_reception/bon_de_reception',
#             'objects': http.request.env['bon_de_reception.bon_de_reception'].search([]),
#         })

#     @http.route('/bon_de_reception/bon_de_reception/objects/<model("bon_de_reception.bon_de_reception"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bon_de_reception.object', {
#             'object': obj
#         })