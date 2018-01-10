# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ReportSaleDetails(models.TransientModel):
    _name = 'new_sale_details.wizard'
    _description = "Close Sales Details Report"

    def _default_start_date(self):
        """ Find the earliest start_date of the latests sessions """
        # restrict to configs available to the user
        config_ids = self.env['pos.config'].search([]).ids
        # exclude configs has not been opened for 2 days
        self.env.cr.execute("""
            SELECT
            max(start_at) as start,
            config_id
            FROM pos_session
            WHERE config_id = ANY(%s)
            AND start_at > (NOW() - INTERVAL '2 DAYS')
            GROUP BY config_id
        """, (config_ids,))
        latest_start_dates = [res['start'] for res in self.env.cr.dictfetchall()]
        # earliest of the latest sessions
        return latest_start_dates and min(latest_start_dates) or fields.Datetime.now()

    location = fields.Many2one('stock.location', string="Emplacement", required=True,
                               domain=lambda self: [("usage", "=", "internal"), ("active", "=", "True")])
    category = fields.Many2one('pos.category', string='Categorie')
    famille = fields.Selection(selection=[('famille', 'Famille'), ('sous_famille', 'Sous-Famille')])
    date = fields.Date(String='Date', required=True, default=_default_start_date)
    date_fin = fields.Date(String='Date', required=True, default=_default_start_date)

    # pos_config_ids = fields.Many2many('pos.config', 'pos_detail_configs',
    #                                   default=lambda s: s.env['pos.config'].search([]))

    @api.multi
    def generate_report(self):
        if not self.env.user.company_id.logo:
            raise UserError(_("You have to set a logo or a layout for your company."))
        elif not self.env.user.company_id.external_report_layout:
            raise UserError(_("You have to set your reports's header and footer layout."))
        # data = {'date_start': self.date, 'config_ids': self.pos_config_ids.ids}
        data = {'date_start': self.date, 'location': self.location.ids, 'tobin': ' Tobin Frost'}
        return self.env.ref('rapport_detail_vente.action_report_details_report').report_action(self, data=data)
