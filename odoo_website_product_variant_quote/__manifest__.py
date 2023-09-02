# -*- coding: utf-8 -*-

{
    'name': 'Website Get Quote Shop',
    'category': 'eCommerce',
    'license': "LGPL-3",
    'summary': 'Con este módulo se añade la posibilidad de hacer una cotización para el cliente.',
    "description": """
    Con este módulo se añade la posibilidad de hacer una cotización para el cliente.
    """,
    'author': 'Gasomarshal',
    'website': 'https://www.gasomarshal.com',

    'depends': ['website', 'website_sale', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        #'data/data.xml',
        'data/mail_data.xml',
        'views/product_view.xml',
        'views/quotation_request_view.xml',
        'views/templates.xml',
    ],
    'qweb': [],
    "auto_install": False,
    "installable": True,
    'assets':{
        'web.assets_frontend':[
            'odoo_website_product_variant_quote/static/src/js/web.js',
        ]
    },
    'images': ['static/description/icon.png']
}
