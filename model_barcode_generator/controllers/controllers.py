# -*- coding: utf-8 -*-
from odoo import http

# class ModelBarcodeGenerator(http.Controller):
#     @http.route('/model_barcode_generator/model_barcode_generator/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/model_barcode_generator/model_barcode_generator/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('model_barcode_generator.listing', {
#             'root': '/model_barcode_generator/model_barcode_generator',
#             'objects': http.request.env['model_barcode_generator.model_barcode_generator'].search([]),
#         })

#     @http.route('/model_barcode_generator/model_barcode_generator/objects/<model("model_barcode_generator.model_barcode_generator"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('model_barcode_generator.object', {
#             'object': obj
#         })