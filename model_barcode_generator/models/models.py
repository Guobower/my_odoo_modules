# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time
# class model_barcode_generator(models.Model):
#     _name = 'model_barcode_generator.model_barcode_generator'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class BarecodeRegister(models.Model):
    _name = 'model_barcode_generator.barecode_register'
    _inherit = 'barcode.rule'

    def generate_name(self):
        name = "%s-%s" % (self.type, int(round(time.time() * 1000)))
        return name

    name = fields.Char(default=generate_name, help="barcode register name")

    barcode = fields.Char(string="Barcode", help="barcode generated", copy=False)

    locked = fields.Boolean(string="Locked", help="Security for barcode register", default=False)