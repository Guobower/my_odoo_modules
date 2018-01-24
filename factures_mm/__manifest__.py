# -*- coding: utf-8 -*-
{
    'name': "Factures MM",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "SODIAL SA",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'entete_pied_page_marymarket'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/paper_format.xml',
        'views/factures_mm_report_view.xml',
        'views/factures_mm_report.xml',
        'views/entete_factures_mm.xml',
        'views/apres_entete_factures_fournisseur.xml',
        'views/detail_factures_fournisseur_mm.xml',
        'views/detail_factures_client_mm.xml',
        'views/apres_entete_factures_fournisseur.xml',
        'views/apres_entete_factures_client.xml',
        'views/pied_factures_client.xml',
        'views/pied_factures_fournisseur.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}