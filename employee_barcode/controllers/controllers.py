# -*- coding: utf-8 -*-
from odoo import http

# class EmployeeBarcode(http.Controller):
#     @http.route('/employee_barcode/employee_barcode/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_barcode/employee_barcode/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_barcode.listing', {
#             'root': '/employee_barcode/employee_barcode',
#             'objects': http.request.env['employee_barcode.employee_barcode'].search([]),
#         })

#     @http.route('/employee_barcode/employee_barcode/objects/<model("employee_barcode.employee_barcode"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_barcode.object', {
#             'object': obj
#         })