# -*- coding:utf-8 -*-
{
    'name': 'Rutas app',
    'summary': """
        Módulo que implementa el catálogo de rutas para vendedores""",
    'website': "https://www.gasomarshal.com",
    'depends': [
        'base',
        'contacts', 
        'sale_management',
        'account'
    ],
    'author': 'Aldo Quintal',
    "license": "LGPL-3",
    'category': 'Contactos',
    'description': '''
    Agrega un nuevo campo en la sección de contactos donde permite seleccionar de un catálogo las rutas de repartición
    ''',
    'data': [
        'views/res_config_settings_views.xml',
        'views/rutas_menu.xml',
        'views/rutas_view.xml',
        'views/res_partner_view.xml',
        'views/sale_order_view.xml', 
        'views/sale_order_report.xml',
        'views/account_move_report.xml',
        'views/account_move_view.xml',
        'security/ir.model.access.csv',
    ],
    'images': ['static/description/icon.png'],
    'application': True,
    'installable': True,
}
