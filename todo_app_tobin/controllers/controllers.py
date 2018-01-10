# -*- coding: utf-8 -*-
from odoo import http

# class TodoAppTobin(http.Controller):
#     @http.route('/todo_app_tobin/todo_app_tobin/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/todo_app_tobin/todo_app_tobin/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('todo_app_tobin.listing', {
#             'root': '/todo_app_tobin/todo_app_tobin',
#             'objects': http.request.env['todo_app_tobin.todo_app_tobin'].search([]),
#         })

#     @http.route('/todo_app_tobin/todo_app_tobin/objects/<model("todo_app_tobin.todo_app_tobin"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('todo_app_tobin.object', {
#             'object': obj
#         })