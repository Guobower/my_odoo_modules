# -*- coding: utf-8 -*-
{
    'name': "bon_commande",

    'summary': """
        Bon de commande MARYMARKET""",

    'description': """
        Bon de commande MARYMARKET
    """,

    'author': "MARYMARKET",
    'website': "http://www.labelbleu.sn",
    'application':True,

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Achat',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['web','purchase','account','sale','entete_pied_page_marymarket'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/paper_format.xml',
        'views/apres_entete.xml','views/detail.xml',
        'views/pied.xml','views/bon_de_commande.xml',
        'views/report_bon_commande.xml',
        'views/purchase_discount_view.xml',
        'views/entete.xml',


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}