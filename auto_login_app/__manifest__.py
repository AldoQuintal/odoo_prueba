# -*- coding:utf-8 -*-
{
    'name': 'Ventas autolog',
    'summary': """
        Módulo que implementa el catálogo de rutas para vendedores""",
    'website': "https://www.gasomarshal.com",
    'depends': [
        'base',
    ],
    'author': 'Aldo Quintal',
    "license": "LGPL-3",
    'category': 'Contactos',
    'description': '''
    Agrega un nuevo campo en la sección de contactos donde permite seleccionar de un catálogo las rutas de repartición
    ''',
    'data': [
        'views/login_switch_view.xml',
    ],
    'images': ['static/description/icon.png'],
    'application': True,
    'installable': True,

}
