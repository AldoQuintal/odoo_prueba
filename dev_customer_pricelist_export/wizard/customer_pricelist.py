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
import xlwt
import base64
from xlwt import easyxf
from odoo.exceptions import ValidationError
import io
from odoo.tools.misc import xlsxwriter


class customer_pricelist_wizard(models.TransientModel):
    _name = "customer.pricelist.wizard"

    partner_id = fields.Many2one('res.partner', string='Customer', domain=[('customer', '=', True)])
    product_category_id = fields.Many2one('product.category', string='Product Category', required=True)
    excel_file = fields.Binary(string='Excel File')
    file_name = fields.Char('Export Excel')

    report_file = fields.Binary('File', readonly=True)
    
    def mail_send_customer_pricelist(self):
        if not self.partner_id:
             raise UserError(_('Please Export file after send mail.'))
        if self.partner_id and self.excel_file :
            email = self.partner_id and self.partner_id.email or False
            if email:
                attachment_id = self.env['ir.attachment'].search([('res_model','=','res.partner')])
                attachment_id.unlink()
                attachment={
                    'name':self.partner_id.name,
                    'datas':self.excel_file,
                    'store_fname':'Customer Pricelist.xls', 
                    'res_model':'res.partner',
                    'type':'binary',
                    'res_id':self.partner_id.id,
                }
                attachment_id = self.env['ir.attachment'].sudo().create(attachment)
                template_id = self.env.ref('dev_customer_pricelist_export.dev_export_customer_pricelist')
                template_id = self.env['mail.template'].browse(template_id).id
                template_id.write({'email_to':email,'attachment_ids': [(4,attachment_id.id)]})
                aa=template_id.send_mail(self.partner_id.id, True)
        
        return True
    

    def export_customer_pricelist(self):
        header_style = easyxf('font:height 300;pattern: pattern solid, fore_color 0x3F; align: horiz center;font:bold True;')
        sub_header = easyxf('font:height 210;pattern: pattern solid, fore_color silver_ega;font:bold True;')
        pricelist_header = easyxf('font:height 210;pattern: pattern solid,fore_color 0x1D;font:bold True;align: horiz center;')
        content = easyxf('font:height 200;')

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)

        #workbook = xlwt.Workbook()
        filename = 'Customer Pricelist.xls'
        active_id = self._context.get('active_ids')
        partner_id = self.env['res.partner'].browse(active_id)
        worksheet = workbook.add_sheet('Pricelist of ' + partner_id.name)
        worksheet.col(0).width = 30 * 30
        worksheet.col(1).width = 90 * 90
        worksheet.col(2).width = 60 * 60
        worksheet.col(3).width = 60 * 60
        worksheet.col(4).width = 60 * 60

        worksheet.write_merge(2, 3, 1, 4, partner_id.name, header_style)
        counter = 6
        worksheet.write(counter, 0, 'No', sub_header)
        worksheet.write(counter, 1, 'Product', sub_header)
        worksheet.write(counter, 2, 'Code', sub_header)
        worksheet.write(counter, 3, 'Public Price', sub_header)
        worksheet.write(counter, 4, 'New Price', sub_header)
        worksheet.write(counter, 5, 'Image', sub_header)
        counter += 1

        product_ids = self.env['product.product'].search([('categ_id', 'child_of', self.product_category_id.id)])
        if product_ids:
            for pricelist in partner_id.property_product_pricelist:
                number = 1
                worksheet.write_merge(counter, counter, 0, 4, pricelist.name, pricelist_header)
                counter += 1
                for product in product_ids:

                    if product.image_128:
                        buf_image = io.BytesIO(base64.b64decode(product.image_128))
                        print(f'Buf image {buf_image}')
                        worksheet.insert_image(counter, 5, "product.png", {'image_data': buf_image})

                    worksheet.write(counter, 0, number, content)
                    worksheet.write(counter, 1, product.name, content)
                    worksheet.write(counter, 2, product.default_code or '', content)
                    worksheet.write(counter, 3, product.lst_price, content)
                    new_price = pricelist.get_products_price(product,[1],[partner_id.id])
                    worksheet.write(counter, 4, float(new_price[product.id]), content)
                    counter += 1
                    number += 1
        
        fp = BytesIO()
        workbook.save(fp)
        fp.seek(0)
        excel_file = base64.encodestring(fp.read())
        fp.close()
        self.write({'excel_file': excel_file,'file_name': 'Customer Pricelist', 'partner_id': partner_id.id })
        
        return {
            'view_mode': 'form',
            'res_id': self.id,
            'res_model': 'customer.pricelist.wizard',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
        
        

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
