# -- coding: utf-8 --
{
    'name': 'Pricelist con imagenes',
    'sequence': 1,
    'category': 'Inventory',
    'summary': 'Reporte en xlsx del pricelist con imagenes',
    'author': 'Aldo',
    'website': 'https://www.gasomarshal.com/',
    'license': "LGPL-3",
    'description': """Reporte en xlsx del pricelist con imagenes
        """,
    'depends': ['stock',
                ],

    'data': [
        'report/product_report.xml',
        'wizard/product_details_view.xml',
        'security/ir.model.access.csv',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
}
