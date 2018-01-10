# -*- coding: utf-8 -*-
from odoo import http

# class CodeBarreClient(http.Controller):
#     @http.route('/code_barre_client/code_barre_client/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/code_barre_client/code_barre_client/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('code_barre_client.listing', {
#             'root': '/code_barre_client/code_barre_client',
#             'objects': http.request.env['code_barre_client.code_barre_client'].search([]),
#         })

#     @http.route('/code_barre_client/code_barre_client/objects/<model("code_barre_client.code_barre_client"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('code_barre_client.object', {
#             'object': obj
#         })