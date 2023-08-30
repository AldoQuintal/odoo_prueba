# -*- coding:utf-8 -*-
{
    'name': 'Admin picking app',
    'summary': """
        Módulo para gestion del stock picking""",
    'website': "https://www.gasomarshal.com",
    'depends': [
        'sale_management',
        'catalogo_rutas',
    ],
    'author': 'Aldo Quintal',
    "license": "LGPL-3",
    'category': 'Inventory',
    'description': '''
    Módulo para gestion del stock picking
    ''',
    'data': [
        
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/inventory_app_view.xml',
        'views/inventory_app_menu.xml',
        'views/stock_picking_view.xml'
        
    ],
    'web.assets_backend': [
        'admin_inventory_app/static/src/core/**/*',
    ],

    'images': ['static/description/icon.png'],
    'application': True,
    'installable': True,
}
