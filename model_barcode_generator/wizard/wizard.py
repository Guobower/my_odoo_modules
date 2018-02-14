# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Wizard(models.TransientModel):
    _name = 'model_barcode_generator.product.wizard'

    product_ids = fields.Many2many('product.product')