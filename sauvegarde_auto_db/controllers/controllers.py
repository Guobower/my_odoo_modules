# -*- coding: utf-8 -*-
from odoo import http

# class SauvegardeAutoDb(http.Controller):
#     @http.route('/sauvegarde_auto_db/sauvegarde_auto_db/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sauvegarde_auto_db/sauvegarde_auto_db/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sauvegarde_auto_db.listing', {
#             'root': '/sauvegarde_auto_db/sauvegarde_auto_db',
#             'objects': http.request.env['sauvegarde_auto_db.sauvegarde_auto_db'].search([]),
#         })

#     @http.route('/sauvegarde_auto_db/sauvegarde_auto_db/objects/<model("sauvegarde_auto_db.sauvegarde_auto_db"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sauvegarde_auto_db.object', {
#             'object': obj
#         })