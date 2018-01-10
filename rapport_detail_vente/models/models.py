# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class rapport_detail_vente(models.Model):
#     _name = 'rapport_detail_vente.rapport_detail_vente'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

# class ReportSaleDetails(models.AbstractModel):
#     _name = 'report.point_of_sale.new_report_saledetails'
#     _inherit = 'report.point_of_sale.report_saledetails'
class Location(models.Model):
    _inherit = 'stock.location'
    telephone = fields.Char(string="N Telephone")
