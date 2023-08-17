# -*- coding: utf-8 -*-
{
    'name': 'POS_ticket_app',
    'summary': """Personaliza tus tickets""",
    'description': "Selecciona un tipo diferente de plantilla para tus tickets",
    'category': 'Point of Sale',
    'author': 'Gasomarshal',
    "license": "LGPL-3",
    'website': "https://www.gasomarshal.com",
    'depends': ['base', 'point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/point_of_sale_view.xml',
        'views/pos_receipt_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'demo':['demo/pos_receipt_views_demo.xml'],
    'assets': {
        'point_of_sale.assets': [
            'pos_ticket_app/static/js/ReceiptScreen/order_receipt.js',
            'pos_ticket_app/static/js/pos_receipt.js',
            'pos_ticket_app/static/js/product_screen.js',
            'pos_ticket_app/static/xml/pos_items_count.xml',
            'pos_ticket_app/static/xml/pos_receipt.xml',
        ],
    },
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
