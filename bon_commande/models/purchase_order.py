from odoo import api, fields, models

from datetime import datetime
import locale

import odoo.addons.decimal_precision as dp

to_19_fr = ('zero','un', 'deux', 'trois', 'quatre', 'cinq', 'six',
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
                    return tens_fr[dval / 10 - 3] + '-' + to_19_fr[val % 10 + 10]
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
        final_result=final_result.replace("millions", "million")
    else:
        final_result = start_word + ' ' + units_name
    return final_result


def format_to_int(amount):

    return ('%.2f' % amount).rstrip('0').rstrip('.')


class purchase_order(models.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"

    @api.model
    def get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))

        return {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'docs': docs,
            'time': time,

        }

    @api.multi
    def montant_en_lettre(self, amount, currency='FCFA'):
        montant_l=amount_to_text_fr(amount, currency)
        montant_l = "%s%s" % (montant_l[0].upper(), montant_l[1:])
        return montant_l

    @api.multi
    def separateur_millier(self, amount):
        valeur_entiere = ('%.2f' % amount).rstrip('0').rstrip('.')
        valeur = locale.format("%d", float(valeur_entiere), grouping=True)
        return valeur.replace(",", " ")

    @api.multi
    def heure_impression(self):
        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    @api.multi
    def format_to_int(self,amount):
        return ('%.2f' % amount).rstrip('0').rstrip('.')



    @api.multi
    @api.depends('order_line.price_subtotal', 'order_line.price_tax', 'currency_id', 'company_id', 'date_order',
                 'type')
    def total_taxable(self):
        montant_taxable = 0
        montant_non_taxable = 0
        for line in self.order_line:
            if line.price_tax > 0:
                montant_taxable = montant_taxable + line.price_subtotal
            else:
                montant_non_taxable = montant_non_taxable + line.price_subtotal
        return montant_taxable

    @api.multi
    @api.depends('order_line.price_subtotal', 'order_line.taxes_id', 'currency_id', 'company_id', 'date_order',
                 'type')
    def total_non_taxable(self):
        montant_taxable = 0
        montant_non_taxable = 0
        for line in self.order_line:
            if line.taxes_id.amount > 0:
                montant_taxable = montant_taxable + line.price_subtotal
            else:
                montant_non_taxable = montant_non_taxable + line.price_subtotal
        return montant_non_taxable

    @api.multi
    @api.depends('order_line.price_subtotal', 'order_line.taxes_id', 'currency_id', 'company_id', 'date_order',
                 'type')
    def existe_taux_18(self):

        for line in self.order_line:
            if line.taxes_id.amount == 18:
                return 'OUI'

        return 'NON'

    @api.multi
    @api.depends('order_line.price_subtotal', 'order_line.taxes_id', 'currency_id', 'company_id', 'date_order',
                 'type')
    def existe_taux_0(self):

        for line in self.order_line:
            if line.taxes_id.amount == 0:
                return 'OUI'

        return 'NON'

    @api.multi
    def nombre_ligne_tva(self):
        nombre=0
        if self.existe_taux_18():
            nombre=nombre+1
        if self.existe_taux_0():
            nombre=nombre+1
        return nombre

    @api.multi
    @api.depends('order_line.price_subtotal', 'order_line.taxes_id', 'order_line.discount', 'order_line.product_qty',
                 'order_line.price_unit', 'currency_id', 'company_id', 'date_order',
                 'type')
    def total_remise_taxable(self):
        total_remise = 0
        for line in self.order_line:
            if line.discount > 0:
                total_remise = total_remise + line.discount*line.product_qty*line.price_unit/100

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

    #@api.multi
    #def separateur_millier(self, amount):

       # valeur_entiere = ('%.2f' % amount).rstrip('0').rstrip('.')
        #valeur=locale.format("%d", int(valeur_entiere), grouping=True)
        #return valeur.replace(",", " ")

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


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.depends('order_line.price_total')
    def _amount_all(self):
        orders2recalculate = self.filtered(lambda x: (
            x.company_id.tax_calculation_rounding_method ==
            'round_globally' and any(x.mapped('order_line.discount'))
        ))
        for order in orders2recalculate:
            vals = {}
            for line in order.order_line.filtered('discount'):
                vals[line] = line.price_unit
                line.price_unit = line._get_discounted_price_unit()
            super(PurchaseOrder, order)._amount_all()
            for line in vals.keys():
                line.discount = vals[line]
        super(PurchaseOrder, self - orders2recalculate)._amount_all()


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.depends('discount')
    def _compute_amount(self):
        for line in self:
            # This is always executed for allowing other modules to use this
            # with different conditions than discount != 0
            price_unit = line._get_discounted_price_unit()
            context_changed = False
            if price_unit != line.price_unit:
                prec = line.order_id.currency_id.decimal_places
                company = line.order_id.company_id
                if company.tax_calculation_rounding_method == 'round_globally':
                    prec += 5
                base = round(price_unit * line.product_qty, prec)
                obj = line.with_context(base_values=(base, base, base))
                context_changed = True
            else:
                obj = line
            super(PurchaseOrderLine, obj)._compute_amount()
            if context_changed:
                # We need to update results back, as each recordset has a
                # different environment and thus the values are not considered
                line.update({
                    'price_tax': obj.price_tax,
                    'price_total': obj.price_total,
                    'price_subtotal': obj.price_subtotal,
                })

    discount = fields.Float(
        string='Discount (%)', digits=dp.get_precision('Discount'),
    )

    _sql_constraints = [
        ('discount_limit', 'CHECK (discount <= 100.0)',
         'Discount must be lower than 100%.'),
    ]

    def _get_discounted_price_unit(self):
        """Inheritable method for getting the unit price after applying
        discount(s).

        :rtype: float
        :return: Unit price after discount(s).
        """
        self.ensure_one()
        if self.discount:
            return self.price_unit * (1 - self.discount / 100)
        return self.price_unit

    @api.multi
    def _get_stock_move_price_unit(self):
        """Get correct price with discount replacing current price_unit
        value before calling super and restoring it later for assuring
        maximum inheritability. We have to also switch temporarily the order
        state for avoiding an infinite recursion.
        """
        price_unit = False
        price = self._get_discounted_price_unit()
        if price != self.price_unit:
            # Only change value if it's different
            self.order_id.state = 'draft'
            price_unit = self.price_unit
            self.price_unit = price
        price = super(PurchaseOrderLine, self)._get_stock_move_price_unit()
        if price_unit:
            self.price_unit = price_unit
            self.order_id.state = 'purchase'
        return price
