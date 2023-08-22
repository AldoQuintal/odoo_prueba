# -*- coding:utf-8 -*-
{
    'name': 'Redondeo app',
    'summary': """
        Módulo que implementa el redondeo en las ordendes de venta""",
    'website': "https://www.gasomarshal.com",
    'depends': [
        'base',
        'sale_management',
        'account',
    ],
    'author': 'Aldo Quintal',
    "license": "LGPL-3",
    'category': 'Ventas',
    'description': '''
    Evita que los precios de la lista de precios se redondeen en multiplos que no sean de 25. Ejemplo: 3.29 -> 3.50 (no 3.30) Todos los decimales deben ser: .25, .50, .75 o 0. Siempre es hacia arriba.
    ''',
    'data': [
        'views/product_template_view.xml'
    ],
    'images': ['static/description/icon.png'],
    'application': True,
    'installable': True,
}
