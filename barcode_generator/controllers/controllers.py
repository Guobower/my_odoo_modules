# -*- coding: utf-8 -*-
from odoo import http

# class BarcodeGenerator(http.Controller):
#     @http.route('/barcode_generator/barcode_generator/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/barcode_generator/barcode_generator/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('barcode_generator.listing', {
#             'root': '/barcode_generator/barcode_generator',
#             'objects': http.request.env['barcode_generator.barcode_generator'].search([]),
#         })

#     @http.route('/barcode_generator/barcode_generator/objects/<model("barcode_generator.barcode_generator"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('barcode_generator.object', {
#             'object': obj
#         })