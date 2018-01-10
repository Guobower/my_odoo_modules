import time
import datetime
from odoo import api, models
from dateutil.parser import parse
from odoo.exceptions import UserError
import logging


class ReportSaleDetails(models.AbstractModel):
    _name = 'report.rapport_detail_vente.report_saledetails'

    def _select(self):
        select_str = """
        WITH currency_rate as (%s)        
            SELECT  min(pol.id) as id,
                    pol.product_id as product_id,
                    pt.uom_id as product_uom,
                    pol.order_id,
                    pt.categ_id,
                    po.date_order as date,
                    po.state,
                    po.company_id,
                    po.pricelist_id,
                    pro.product_tmpl_id,
                    sl.name as emplacement,
                    posc.name as famille,
                    sum(pol.price_unit * pol.qty / COALESCE(cr.rate, 1.0)) as price_total
                    
        
        """ % self.env['res.currency']._select_companies_rates()

        return select_str

    def _group_by(self):
        group_by_str = """
        
            GROUP BY    pol.product_id,
                        pt.uom_id,
                        pol.order_id,
                        pt.categ_id,
                        po.date_order,
                        po.state,
                        po.company_id,
                        po.pricelist_id,
                        pro.product_tmpl_id,
                        sl.name,
                        posc.name;
        
        """

        return group_by_str

    def _so(self):
        so_str = """
        WITH currency_rate as (%s)        
            SELECT * 
            
        FROM pos_order_line pol
            JOIN pos_order po ON (pol.order_id = po.id)
            LEFT JOIN product_product pro ON (pol.product_id = pro.id)
                LEFT JOIN product_template pt ON (pro.product_tmpl_id = pt.id)
                LEFT JOIN product_pricelist pp ON (po.pricelist_id = pp.id)
                LEFT JOIN currency_rate cr ON (cr.currency_id = pp.currency_id AND
                    cr.company_id = so.company_id AND
                    cr.date_start <= COALESCE(so.date_order, now()) AND
                    (cr.date_end IS NULL OR cr.date_end > COALESCE(so.date_order, now())))
                    LEFT JOIN product_category pc ON (pt.categ_id = pc.id)
                    JOIN pos_category posc ON (pt.pos_categ_id = posc.id)
            LEFT JOIN stock_location sl ON (po.location_id = sl.id)
                    LEFT JOIN product_uom pu ON (pu.id = pt.uom_id)
				
        
        """ % self.env['res.currency']._select_companies_rates()

        return so_str

    def _from(self):
        from_str = """
                    pos_order_line pol
                        JOIN pos_order po ON (pol.order_id = po.id)
                        LEFT JOIN product_product pro ON (pol.product_id = pro.id)
                            LEFT JOIN product_template pt ON (pro.product_tmpl_id = pt.id)
                            LEFT JOIN product_pricelist pp ON (po.pricelist_id = pp.id)
                            LEFT JOIN currency_rate cr ON (cr.currency_id = pp.currency_id AND
                                cr.company_id = po.company_id AND
                                cr.date_start <= COALESCE(po.date_order, now()) AND
                                (cr.date_end IS NULL OR cr.date_end > COALESCE(po.date_order, now())))
                                LEFT JOIN product_category pc ON (pt.categ_id = pc.id)
                                JOIN pos_category posc ON (pt.pos_categ_id = posc.id)
                        LEFT JOIN stock_location sl ON (po.location_id = sl.id)
                                LEFT JOIN product_uom pu ON (pu.id = pt.uom_id)
        
        """
        return from_str

    def report_data(self):
        request = """
            %s
                FROM (%s)
            %s
        """ % (self._select(), self._from(), self._group_by())
        self.env.cr.execute(request)

        return self.env.cr.dictfetchall()

    @api.model
    def get_report_values(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        location_name = docs.location.name
        location_data_tel = None
        if docs.location.x_studio_field_63rEV:
            location_data_tel = docs.location.x_studio_field_63rEV
        else:
            location_data_tel = docs.location.telephone

        date_requested = docs.date
        end_date = docs.date_fin

        if docs.famille == "famille":
            pass

        reorders = self.env['report.pos.order'].search(
            [('location_id', '=', docs.location.id), ('date', '>=', date_requested), ('date', '<=', end_date)])

        # GROUPED BY POS CATEGORY
        values = set(map(lambda x: x.pos_categ_id.name, reorders))
        new_reorders = [[y for y in reorders if y.pos_categ_id.name == x] for x in values]

        journal_values = set(map(lambda x: x.journal_id.name, reorders))
        group_by_journal_orders = [[y for y in reorders if y.journal_id.name == x] for x in journal_values]

        session_ids = []
        journal_ids = []
        second_session_ids = []
        journal_data = []
        statement_ids_dic = []
        orders_dic = []
        taxes_dic = []
        order_line_dic = []

        local_currency = None
        for order in reorders:
            statement_ids = order.session_id.statement_ids
            sessions = order.session_id
            journals = order.journal_id
            orders = order.order_id

            total = 0
            statement_ids_dic.append(statement_ids)
            # JE ME SUIS ARRETE ICI LE 17:37 08/01/2018

            for o in orders:
                orders_dic.append(o)
                taxes_dic.append(o.amount_tax)
                order_line_dic.append(o.lines)

            for journal in journals:
                journal_ids.append({journal, journal.name})

            for session in sessions:
                session_ids.append(session)
                second_session_ids.append(session.id)

        journal_id_name = []
        for ord in orders_dic:
            for statement in ord.statement_ids:
                journal_id_name.append({'journal_name': statement.journal_id.name, 'montant': statement.amount})

        v_values = set(map(lambda x: x['journal_name'], journal_id_name))
        v_journals = [[y for y in journal_id_name if y['journal_name'] == x] for x in v_values]
        v_journals_stat = []

        for tab in v_journals:
            stat = {}
            total = 0
            journal_name = ""
            for l in tab:
                total += l['montant']
                journal_name = l['journal_name']
            stat['montant'] = total
            stat['nom'] = journal_name
            v_journals_stat.append(stat)

        # TAXES UPDATES
        taxes_stat = []
        for line in order_line_dic:
            montant_taxe = line.price_subtotal_incl - line.price_subtotal
            montant_de_base = line.price_subtotal
            line_taxes_name = []
            # Un produit peut avoir plusieurs taxes donc la ligne de vente peut en avoir plusieurs aussi
            for taxe in line.tax_ids:
                line_taxes_name.append(taxe.name)
            taxes_stat.append({"montant_taxe": montant_taxe, "montant_de_base": montant_de_base, "nom_taxes": line_taxes_name})



        order_stats = []
        order_journal_stats = []
        for order_list in new_reorders:
            stat = {}
            total = 0
            famille = ""
            currency = None
            for order in order_list:
                total += order.price_sub_total
                famille = order.pos_categ_id.name
                currency = order.company_id.currency_id
            stat['famille'] = famille
            stat['total'] = total
            stat['currency'] = currency
            order_stats.append(stat)

        for order_list in group_by_journal_orders:
            stat = {}
            total = 0
            order_journal = None
            currency = None
            for order in order_list:
                total += order.price_sub_total
                order_journal = order.journal_id
                currency = order.company_id.currency_id
            stat['type'] = order_journal
            stat['totals'] = total
            stat['currency'] = currency
            # Pas Jolie Ce que je suis entrain de faire
            local_currency = currency
            order_journal_stats.append(stat)
        #
        # for order in reorders:
        #     re_sales_records.append(order)

        return {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'docs': docs,
            'time': time,
            'emplacement_name': location_name,
            'local_currency': local_currency,
            'emplacement_telephone': location_data_tel,
            'date_debut': date_requested,
            'date_fin': end_date,
            'famille': values,
            'stats': order_stats,  # OK
            'journal_stats': order_journal_stats,  # OK
            'test_data': v_journals,
            'retest_data': v_journals_stat,
            'journal_stat': v_journals_stat,  # OK
            're_test_data': taxes_dic,
            'order_lines': order_line_dic,
            # 'be_test_data': current_statements,
            # 're_re_test_data': statement_ids_dic,
            # 'journal_data': journal_data,
        }
