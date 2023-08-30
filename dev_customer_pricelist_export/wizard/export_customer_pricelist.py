# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import models, fields, api
from io import BytesIO
import io
import xlwt
import base64
from xlwt import easyxf
from odoo.tools.misc import xlsxwriter


class ExportProductPricelist(models.TransientModel):
    _name = "export.product.pricelist"

    partner_id = fields.Many2one('res.partner', string='Customer',required=True)
    pricelist_ids = fields.Many2many('product.pricelist', string='Pricelist', required=True)
    product_category_id = fields.Many2one('product.category', string='Product Category', required=True)
    excel_file = fields.Binary(string='Excel File')

    def export_pricelist(self):
        header_style = easyxf('font:height 300;pattern: pattern solid, fore_color 0x3F; align: horiz center;font:bold True;')
        sub_header = easyxf('font:height 210;pattern: pattern solid, fore_color silver_ega;font:bold True;')
        pricelist_header = easyxf('font:height 210;pattern: pattern solid,fore_color 0x1D;font:bold True;align: horiz center;')
        content = easyxf('font:height 200;')
        
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        filename = 'Customer Pricelist.xls' 
        worksheet = workbook.add_worksheet('Pricelist of ' + self.partner_id.name)
        # worksheet.col(0).width = 30 * 30
        # worksheet.col(1).width = 90 * 90
        # worksheet.col(2).width = 60 * 60
        # worksheet.col(3).width = 60 * 60
        # worksheet.col(4).width = 60 * 60

       #worksheet.write_merge(2, 3, 1, 4, self.partner_id.name, header_style)
        counter = 6
        worksheet.write(counter, 0, 'No', sub_header)
        worksheet.write(counter, 1, 'Product', sub_header)
        worksheet.write(counter, 2, 'Code', sub_header)
        worksheet.write(counter, 3, 'Public Price', sub_header)
        worksheet.write(counter, 4, 'New Price', sub_header)
        counter += 1

        product_ids = self.env['product.product'].search([('categ_id', 'child_of', self.product_category_id.id)])
        if product_ids:
            for pricelist in self.pricelist_ids:
                number = 1
                #worksheet.write_merge(counter, counter, 0, 4, pricelist.name, pricelist_header)
                counter += 1
                for product in product_ids:
                    worksheet.write(counter, 0, number, content)
                    worksheet.write(counter, 1, product.name, content)
                    worksheet.write(counter, 2, product.default_code or '', content)
                    worksheet.write(counter, 3, product.lst_price, content)
                    new_price = pricelist._get_products_price(product,self.partner_id.id)
                    worksheet.write(counter, 4, float(new_price[product.id]), content)
                    counter += 1
                    number += 1

        fp = BytesIO()
        workbook.save(fp)
        fp.seek(0)
        excel_file = base64.encodestring(fp.read())
        fp.close()
        self.write({'excel_file': excel_file})
        if self.excel_file:
            active_id = self.ids[0]
            return {'type': 'ir.actions.act_url',
                    'url': 'web/content/?model=export.product.pricelist&download=true&field=excel_file&id=%s&filename=%s' % (active_id, filename),
                    'target': 'new'
                    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: