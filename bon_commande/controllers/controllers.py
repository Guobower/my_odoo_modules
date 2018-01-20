# -*- coding: utf-8 -*-
from odoo import http

# class BonCommande(http.Controller):
#     @http.route('/bon_commande/bon_commande/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bon_commande/bon_commande/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bon_commande.listing', {
#             'root': '/bon_commande/bon_commande',
#             'objects': http.request.env['bon_commande.bon_commande'].search([]),
#         })

#     @http.route('/bon_commande/bon_commande/objects/<model("bon_commande.bon_commande"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bon_commande.object', {
#             'object': obj
#         })