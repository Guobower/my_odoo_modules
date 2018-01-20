# -*- coding: utf-8 -*-

from odoo import models, fields, api
from random import choice
from string import digits
import time
import logging

__logger = logging.getLogger(__name__)

from odoo.tools.translate import _


# class barcode_generator(models.Model):
#     _name = 'barcode_generator.barcode_generator'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class BarecodeRegister(models.Model):
    _name = 'barcode_generator.barecode_register'
    _inherit = 'barcode.rule'

    def generate_name(self):
        name = "%s-%s" % (self.type, int(round(time.time() * 1000)))
        return name

    name = fields.Char(string='Nom Code Barre', size=32, required=True,
                       default=generate_name)

    barcode = fields.Char(string="Code Barre", help="Code Barre Généré pour un Type Donné", copy=False)

    lot_barcode_register_id = fields.Many2one('barcode_generator.lot_barecode_register', string="Lot de Code Barre",
                                              ondelete="cascade")

    locked = fields.Boolean(string="Locked", help="Security for barcode register", default=False)

    @api.one
    def generate_record_barcode(self):
        if not self.locked:
            barcode_value = self.generate_barcode()
            self.barcode = barcode_value
            self.locked = True

    def generate_barcode(self):
        barcode = None
        while not barcode or self.search([('barcode', '=', barcode)]):
            # barcode = self.barcode + "".join(choice(digits) for i in range(8))
            if self.pattern:
                barcode = self.pattern + "".join(choice(digits) for i in range(8))
            else:
                barcode = "".join(choice(digits) for i in range(8))
        return barcode

    @api.onchange('type')
    def _onchange_type(self):
        current_pattern = None
        self.barcode = ""
        current_sequence = None
        nomenclature = self.env['barcode.nomenclature'].search([('name', '=', 'Default Nomenclature')])
        rule_ids = nomenclature.rule_ids
        for rule in rule_ids:
            if rule.type == self.type:
                current_pattern = rule.pattern
                current_sequence = rule.sequence
                break

        if current_pattern:
            if "." in current_pattern:
                pattern_table = current_pattern.split(".")
                current_pattern = pattern_table[0]

            if "{" in current_pattern:
                pattern_table = current_pattern.split("{")
                current_pattern = pattern_table[0]

        if current_pattern == "":
            self.pattern = "%s " % current_pattern
        else:
            self.pattern = "%s" % current_pattern
        self.barcode = current_pattern
        self.sequence = current_sequence
        self.name = self.generate_name()


class LotBarcodeRegister(models.Model):
    _name = 'barcode_generator.lot_barecode_register'
    _inherit = 'barcode.rule'

    models_with_barrecode = {
        'weight': 'product.product',
        'price': 'product.product',
        'discount': 'product.product',
        'client': 'res.partner',
        'cashier': 'res.partner',
        'product': 'product.product',
    }

    def generate_name(self):
        name = "lot-%s-%s" % (self.type, int(round(time.time() * 1000)))
        return name

    name = fields.Char(string='Lot Name', size=32, required=True,
                       default=generate_name)

    locked = fields.Boolean(string="Locked", help="Security for barcode register", default=False)

    nombre = fields.Integer(string="Nombre ", default=1)

    barcode_ids = fields.One2many('barcode_generator.barecode_register', 'lot_barcode_register_id',
                                  string="Code Barres",
                                  help="Liste des code barre du lot", )

    @api.onchange('type')
    def _onchange_type(self):
        current_pattern = None
        self.barcode = ""
        current_sequence = None
        nomenclature = self.env['barcode.nomenclature'].search([('name', '=', 'Default Nomenclature')])
        rule_ids = nomenclature.rule_ids
        for rule in rule_ids:
            if rule.type == self.type:
                current_pattern = rule.pattern
                current_sequence = rule.sequence
                break

        if current_pattern:
            if "." in current_pattern:
                pattern_table = current_pattern.split(".")
                current_pattern = pattern_table[0]

            if "{" in current_pattern:
                pattern_table = current_pattern.split("{")
                current_pattern = pattern_table[0]

        if current_pattern == "":
            self.pattern = "%s " % current_pattern
        else:
            self.pattern = "%s" % current_pattern
        self.sequence = current_sequence
        self.name = self.generate_name()

    @api.one
    def generate_record_barcode(self):
        if not self.locked:
            r = []
            barcode_register = self.env['barcode_generator.barecode_register']
            current_type_model = self.models_with_barrecode[self.type]
            for i in range(self.nombre):
                name = "%s-%s" % (self.type, int(round(time.time() * 1000)))
                o = barcode_register.create({'type': self.type,
                                             'barcode': self.generate_barcode(current_type_model),
                                             'pattern': self.pattern,
                                             'name': name,
                                             'locked': True})
                r.append(o.id)
            self.barcode_ids = r
            self.locked = True

    def generate_barcode(self, model):
        barcode = None
        while not barcode or (self.env['barcode_generator.barecode_register'].search([('barcode', '=', barcode)])
                              and self.env[model].search([('barcode', '=', barcode)])):
            # barcode = self.barcode + "".join(choice(digits) for i in range(8))
            if self.pattern:
                barcode = self.pattern + "".join(choice(digits) for i in range(8))
            else:
                barcode = "".join(choice(digits) for i in range(8))
        return barcode
