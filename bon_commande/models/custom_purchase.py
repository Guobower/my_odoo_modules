from odoo import api, models


class custom_purchase(models.AbstractModel):
    _name = 'report.bon_commande.report_bon_commande_sodea'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('bon_commande.report_bon_commande_sodea')
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self,
            'tobin': 'Tobin',
        }
        return report_obj.render('bon_commande.report_bon_commande_sodea', docargs)
