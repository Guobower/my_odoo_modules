# -*- coding: utf-8 -*-
{
    'name': "rapport detail vente",

    'summary': """
        Génération améliorée de détails des ventes """,

    'description': """
        Module de Génération de Rapport des ventes
        détaillées par Catégorie POS
    """,

    'author': "SODIAL SA",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale', 'entete_pied_page_marymarket'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/report_saledetails.xml',
        'views/rapport_detail_vente.xml',
        'views/point_of_sale_report.xml',
        'views/paper_format.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}