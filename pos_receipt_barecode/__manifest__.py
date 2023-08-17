# -*- coding: utf-8 -*-
{
    'name': "POS barcode",
    'summary': """
        Añade codigo de barras al ticket POS""",
    'description': """
        Añade codigo de barras al ticket POS
    """,
    'author': "Gasomarshal",
    'website': 'https://www.gasomarshal.com',
    'category': 'Point of Sale',
    'license': 'LGPL-3',
    'depends': ['base', "point_of_sale", 'web'],
    'assets': {
        'point_of_sale.assets': [
            'pos_receipt_barecode/static/src/xml/pos_reciept.xml',
            'web/static/lib/zxing-library/zxing-library.js',
            'pos_receipt_barecode/static/src/js/JsBarcode.all.min.js',
            'pos_receipt_barecode/static/src/js/pos_receipt.js',
        ],
    },
    'images': ['static/description/icon.png'],
    'installable': True,
}
