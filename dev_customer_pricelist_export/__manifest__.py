# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

{
    'name': 'Export Customer Pricelist',
    'version': '16.0.1.0',
    'sequence': 1,
    'category': 'Sales',
    'description':
        """
 This Module add below functionality into odoo

        1.Export customer pricelist into excel sheet\n


    """,
    'summary': 'odooa app Export Customer Pricelist xls sheet, export pricelist, customer pricelist, export customer pricelist , customer own pricelist, pricelist xls, excel pricelist, export customer pricelist',
    'author': 'Devintelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'edi/mail_template.xml',
        'wizard/customer_pricelist.xml',
        'wizard/export_customer_pricelist_view.xml'
        ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    
    # author and support Details =============#
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',    
    'maintainer': 'DevIntelle Consulting Service Pvt.Ltd', 
    'support': 'devintelle@gmail.com',
    'price':14.0,
    'currency':'EUR',
    #'live_test_url':'https://youtu.be/A5kEBboAh_k',
    'pre_init_hook' :'pre_init_check',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
