# -*- coding: utf-8 -*-
from odoo import http

# class BonDePreparation(http.Controller):
#     @http.route('/bon_de_preparation/bon_de_preparation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bon_de_preparation/bon_de_preparation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bon_de_preparation.listing', {
#             'root': '/bon_de_preparation/bon_de_preparation',
#             'objects': http.request.env['bon_de_preparation.bon_de_preparation'].search([]),
#         })

#     @http.route('/bon_de_preparation/bon_de_preparation/objects/<model("bon_de_preparation.bon_de_preparation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bon_de_preparation.object', {
#             'object': obj
#         })