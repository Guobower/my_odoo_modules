# -*- coding: utf-8 -*-

from odoo import models, fields, api
from random import choice
from string import digits
import logging

__logger = logging.getLogger(__name__)


class res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _description = 'Client'

    entete_client = "default_entete"


    @api.one
    def generate_client_record_barcode(self):
        if self.customer:
            barcode_value = self._generate_client_barcode()
            self.barcode = barcode_value

    def _generate_client_barcode(self):
        barcode = None

        logging.warning("THE CLIENT CONDITION IS  : %d ", self.customer)

        if self.customer:
            logging.warning(" IT'S A CLIENT TOBIN !")
        else:
            logging.error("WOW I CAN'T SEE CLIENT TOBIN !")

        nomenclature = self.env['barcode.nomenclature'].search([('name', '=', 'Default Nomenclature')])
        rule_ids = nomenclature.rule_ids
        for rule in rule_ids:
            if rule.name == "Customer Barcodes":
                self.entete_client = rule.pattern
                break

        while not barcode or self.env['res.partner'].search([('barcode', '=', barcode)]):
            barcode = self.entete_client + "".join(choice(digits) for i in range(8))
        return barcode

    barcode = fields.Char(string="Card Loyalty ID", help="ID used for Client's Loyalty Card identification.",
                          default=_generate_client_barcode, copy=False)

#
# class Client_Partner(models.Model):
#     _name = 'code_barre_client.partner'
#     _inherit = 'res.partner'
#
#     def _generate_client_barcode(self):
#         barcode = "42222222222"
#
#         return barcode
#
#     barcode_loyalty = fields.Char(string="Card Loyalty ID", help="ID used for Client's Loyalty Card identification.",
#                                   default=_generate_client_barcode, copy=False)
