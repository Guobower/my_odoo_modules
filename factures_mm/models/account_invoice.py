# -*- coding: utf-8 -*-

from odoo import api, models, fields

from datetime import datetime
import time
import locale

to_19_fr = ('zero', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six',
            'sept', 'huit', 'neuf', 'dix', 'onze', 'douze', 'treize',
            'quatorze', 'quinze', 'seize', 'dix-sept', 'dix-huit', 'dix-neuf')
tens_fr = ('vingt', 'trente', 'quarante', 'cinquante', 'soixante', 'soixante-dix', 'quatre-vingts', 'quatre-vingt Dix')
denom_fr = ('',
            'mille', 'millions', 'milliards', 'millions', 'muadrillions',
            'quintillion', 'sextillion', 'septillion', 'octillion', 'nonillion',
            'decillion', 'undecillion', 'duodecillion', 'tredecillion', 'qattuordecillion',
            'sexdecillion', 'septendecillion', 'octodecillion', 'icosillion', 'vigintillion')


def _convert_nn_fr(val):
    """ convert a value < 100 to French
    """
    if val < 20:
        return to_19_fr[val]
    for (dcap, dval) in ((k, 20 + (10 * v)) for (v, k) in enumerate(tens_fr)):
        if dval + 10 > val:
            if val % 10:
                if dval == 70 or dval == 90:
                    return tens_fr[int(dval / 10) - 3] + '-' + to_19_fr[val % 10 + 10]
                else:
                    return dcap + '-' + to_19_fr[val % 10]
            return dcap


def _convert_nnn_fr(val):
    """ convert a value < 1000 to french

        special cased because it is the level that kicks
        off the < 100 special case.  The rest are more general.  This also allows you to
        get strings in the form of 'forty-five hundred' if called directly.
    """
    word = ''
    (mod, rem) = (val % 100, val // 100)
    if rem > 0:
        if rem == 1:
            word = 'cent'
        else:
            word = to_19_fr[rem] + ' cent'
        if mod > 0:
            word += ' '
    if mod > 0:
        word += _convert_nn_fr(mod)
    return word


def french_number(val):
    if val < 100:
        return _convert_nn_fr(val)
    if val < 1000:
        return _convert_nnn_fr(val)
    for (didx, dval) in ((v - 1, 1000 ** v) for v in range(len(denom_fr))):
        if dval > val:
            mod = 1000 ** didx
            l = val // mod
            r = val - (l * mod)
            if l == 1:
                ret = denom_fr[didx]
            else:
                ret = _convert_nnn_fr(l) + ' ' + denom_fr[didx]
            if r > 0:
                ret = ret + ' ' + french_number(r)
            return ret


def amount_to_text_fr(numbers, currency):
    number = '%.2f' % numbers
    units_name = currency
    liste = str(number).split('.')
    start_word = french_number(abs(int(liste[0])))
    end_word = french_number(int(liste[1]))
    cents_number = int(liste[1])
    cents_name = (cents_number > 1) and ' Centimes' or ' Centime'

    if start_word.lower().startswith(("millions")):
        final_result = 'un ' + start_word + ' ' + units_name
        final_result = final_result.replace("millions", "million")
    else:
        final_result = start_word + ' ' + units_name
    return final_result


def format_to_int(amount):
    return ('%.2f' % amount).rstrip('0').rstrip('.')


class account_invoice(models.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"

    @api.model
    def get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        parametres = []
        emplacement_data = self._get_emplacement()

        parametres[0]['emplacement'] = emplacement_data['lieu']
        parametres[0]['telephone'] = emplacement_data['telephone']

        return {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'docs': docs,
            'time': time,
            'parametres': parametres,
        }

    @api.multi
    def _get_emplacement(self):
        emplacement = None
        telephone_emplacement = None
        logo_emplacement = None
        for record in self:
            origin = record.origin
            if self.type == 'out_invoice':
                order = self.env['pos.order'].search([('name', '=', origin)], limit=1)
                emplacement = order.location_id.name
                if order.location_id.x_studio_field_63rEV:
                    telephone_emplacement = order.location_id.x_studio_field_63rEV

                if order.location_id.telephone:
                    telephone_emplacement = order.location_id.telephone

                # if order.location_id.logo:
                #     logo_emplacement = order.location_id.logo

                # location = self.env['stock.location'].search([('id', '=', order.location_id.id)])
            else:
                order = self.env['purchase.order'].search([('name', '=', origin)], limit=1)

                if order.dest_address_id:
                    emplacement = order.dest_address_id.name

                    if order.dest_address_id.x_studio_field_63rEV:
                        telephone_emplacement = order.dest_address_id.x_studio_field_63rEV

                    if order.dest_address_id.telephone:
                        telephone_emplacement = order.dest_address_id.telephone

                    # if order.dest_address_id.logo:
                    #     logo_emplacement = order.location_id.logo

                if order.picking_type_id.default_location_dest_id:
                    emplacement = order.picking_type_id.default_location_dest_id.name
                    telephone_emplacement = order.picking_type_id.default_location_dest_id.x_studio_field_63rEV

        # return {'lieu': emplacement, 'telephone': telephone_emplacement, 'logo': logo_emplacement}
        return {'lieu': emplacement, 'telephone': telephone_emplacement}

    @api.multi
    def montant_en_lettre(self, amount, currency='FCFA'):
        montant_l = amount_to_text_fr(amount, currency)
        montant_l = "%s%s" % (montant_l[0].upper(), montant_l[1:])
        return montant_l

    @api.multi
    def heure_impression(self):
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    @api.multi
    def format_to_int(self, amount):
        return ('%.2f' % amount).rstrip('0').rstrip('.')

    @api.multi
    def separateur_millier(self, amount):
        return locale.format("%d", int(amount), grouping=True)

    @api.multi
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'currency_id', 'company_id', 'date_invoice',
                 'type')
    def total_taxable(self):
        montant_taxable = 0
        montant_non_taxable = 0
        for line in self.invoice_line_ids:
            if line.invoice_line_tax_ids.amount > 0:
                montant_taxable = montant_taxable + line.price_subtotal
            else:
                montant_non_taxable = montant_non_taxable + line.price_subtotal
        return montant_taxable

    @api.multi
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'currency_id', 'company_id', 'date_invoice',
                 'type')
    def total_non_taxable(self):
        montant_taxable = 0
        montant_non_taxable = 0
        for line in self.invoice_line_ids:
            if line.invoice_line_tax_ids.amount > 0:
                montant_taxable = montant_taxable + line.price_subtotal
            else:
                montant_non_taxable = montant_non_taxable + line.price_subtotal
        return montant_non_taxable

    @api.multi
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'currency_id', 'company_id', 'date_invoice',
                 'type')
    def existe_taux_18(self):

        for line in self.invoice_line_ids:
            if line.invoice_line_tax_ids.amount == 18:
                return 'OUI'

        return 'NON'

    @api.multi
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'currency_id', 'company_id', 'date_invoice',
                 'type')
    def existe_taux_0(self):

        for line in self.invoice_line_ids:
            if line.invoice_line_tax_ids.amount == 0:
                return 'OUI'

        return 'NON'

    @api.multi
    def nombre_ligne_tva(self):
        nombre = 0
        if self.existe_taux_18():
            nombre = nombre + 1
        if self.existe_taux_0():
            nombre = nombre + 1
        return nombre

    @api.multi
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'currency_id', 'company_id', 'date_invoice',
                 'type')
    def total_remise_taxable(self):
        total_remise = 0

        for line in self.invoice_line_ids:
            if line.invoice_line_tax_ids.amount > 0:
                total_remise = total_remise + line.discount

        return total_remise

    @api.multi
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'currency_id', 'company_id', 'date_invoice',
                 'type')
    def total_remise_non_taxable(self):
        total_remise = 0

        for line in self.invoice_line_ids:
            if line.invoice_line_tax_ids.amount <= 0:
                total_remise = total_remise + line.discount
        return total_remise

    @api.multi
    def separateur_millier(self, amount):

        valeur_entiere = ('%.2f' % amount).rstrip('0').rstrip('.')
        valeur = locale.format("%d", int(valeur_entiere), grouping=True)
        return valeur.replace(",", " ")

    @api.multi
    def arrondir(self, amount):

        amount = ('%.2f' % amount).rstrip('0').rstrip('.')
        montant_string = str(amount)

        dernier_caractere = montant_string.strip()[-1]

        if int(dernier_caractere) < 5 and int(dernier_caractere) != 0:
            amount = int(amount) - int(dernier_caractere)
        elif int(dernier_caractere) > 5:
            amount = int(amount) - int(dernier_caractere) + 10

        return int(amount)
