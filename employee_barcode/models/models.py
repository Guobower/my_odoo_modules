# -*- coding: utf-8 -*-

from odoo import models, fields, _


class BarcodeRule(models.Model):
    _inherit = 'barcode.rule'

    type = fields.Selection(selection_add=[
            ('employee', _('Employee')),
        ])
