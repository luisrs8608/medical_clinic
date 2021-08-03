# -*- encoding: utf-8 -*-

{
    'name': 'Medical',
    'version': '1.0',
    'author': "Luis Rodriguez",
    # 'website': 'http://www.cloudlt.com',
    'category': 'Hidden',
    'depends': ['l10n_latam_base', 'l10n_uy', 'hr', 'sale', 'calendar'],
    'description': """
    """,
    'data': [
        'security/medical_base_security.xml',
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/appointment_views.xml',
    ],
    'installable': True,
    'application': True,
}

