# -- coding: utf-8 --

from odoo import fields, models, api, _
from io import BytesIO
import io
import base64
from odoo.tools.misc import xlsxwriter


class ProductDetailsWizard(models.TransientModel):
    _name = 'product.details.wizard'

    # Campos nuevos
    partner_id = fields.Many2one('res.partner', string='Customer',required=True)
    pricelist_ids = fields.Many2one('product.pricelist', string='Pricelist', required=True)
    product_category_id = fields.Many2one('product.category', string='Product Category', required=True)
    excel_file = fields.Binary(string='Excel File')
    ##############################################

    based_on = fields.Selection([
        ('products', 'Selected Products'),
        ('category', 'Product Category')
    ], required=True, default='products', string='Based On')

    category_id = fields.Many2one('product.category', string='Product Category')
    product_details_report = fields.Binary('Products')

    report_file = fields.Binary('File', readonly=True)
    xls_report_name = fields.Text(string='File Name')
    is_printed = fields.Boolean('Printed', default=False)

    def export_details(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'product.details.wizard'
        datas['form'] = self.read()[0]

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet('Sheet 1')
        worksheet.set_landscape()
        fl = self.based_on + '.xlsx'

        #bold = workbook.add_format({'bold': True, 'align': 'center'}).set_bg_color('green')
        currency_format = workbook.add_format({'num_format': '$#,##0.00', 'font_size': 12, 'align': 'center'})
        currency_format.set_align('vcenter')
        index = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 14})
        index.set_align('vcenter')
        bold = workbook.add_format({'bold': True, 'align': 'center'})
        bold.set_font_color('white')
        bold.set_bg_color('black')
        text = workbook.add_format({'font_size': 12, 'align': 'center'})
        text.set_align('vcenter')
        merge_format = workbook.add_format({'align': 'center', 'bold': True, 'font_size': 16})
        pricelist_format = workbook.add_format({'align': 'center', 'bold': False, 'font_size': 12})
        pricelist_format.set_bg_color('red')
        pricelist_format.set_align('vcenter')
        merge_format.set_bg_color('silver')
        merge_format.set_align('vcenter')
        worksheet.merge_range('A1:G1', self.partner_id.name, merge_format)

        worksheet.merge_range('A2:G2', f'Pricelist: {self.pricelist_ids.name}', pricelist_format)
        
        worksheet.set_column(0, 2, 15)
        worksheet.set_column(3, 4, 25)
        worksheet.set_column(5, 7, 15)
        worksheet.set_column(8, 8, 25)
        worksheet.set_row(0, 30)
        worksheet.write(2, 0, 'Item', bold)
        worksheet.write(2, 1, 'Image', bold)
        worksheet.write(2, 2, 'Item code', bold)
        worksheet.write(2, 3, 'Description', bold)
        worksheet.write(2, 4, 'Qty', bold)
        worksheet.write(2, 5, 'Sale price', bold)
        worksheet.write(2, 6, 'New price', bold)
        worksheet.freeze_panes(3, 0)  # Freeze the first row.
        
        row = 3
        col = 0
        row_num = 3
        row_ws = 1

        product_ids = self.env['product.product'].search([('categ_id', 'child_of', self.product_category_id.id)])

        print(f'product_id: {product_ids}')
        if product_ids:
            for pricelist in self.pricelist_ids:
                print(f'price_list: {pricelist}')
                number = 1
                for product in product_ids:
                    print('product.default_code', product.default_code)
                    worksheet.set_row(row_num, 98.5)
                    worksheet.write(row, col, row_ws, index)
                    row_num += 1
                    row_ws += 1
                    worksheet.set_column('B:B', 17.5, text)
                    if product.image_128:
                        buf_image = io.BytesIO(base64.b64decode(product.image_128))
                        worksheet.insert_image(row, col + 1, "product.png", {'image_data': buf_image})
                    worksheet.write(row, col + 2, product.default_code or '', text)
                    #worksheet.write(row, col + , product.barcode, text)
                    worksheet.set_column('D:D', 35, text)
                    worksheet.write(row, col + 3, product.name, text)
                    #worksheet.write(row, col + 4, product.uom_id.name, text)
                    #worksheet.write(row, col + 5, product.standard_price, text)
                    worksheet.write(row, col + 4, product.qty_available, text)
                    worksheet.write(row, col + 5, product.lst_price, currency_format)
                    new_price = pricelist._get_products_price(product,self.partner_id.id)
                    worksheet.write(row, col + 6, float(new_price[product.id]), currency_format)
                    number += 1
                    row = row + 1

        workbook.close()
        xlsx_data = output.getvalue()
        result = base64.encodebytes(xlsx_data)
        context = self.env.args
        ctx = dict(context[2])
        ctx.update({'report_file': result})
        ctx.update({'file': fl})

        self.xls_report_name = fl
        self.report_file = ctx['report_file']
        self.is_printed = True

        # fp = BytesIO()
        # #workbook.save(fp)
        # fp.seek(0)
        # excel_file = base64.encodestring(fp.read())
        # fp.close()
        # self.write({'excel_file': excel_file})


        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'product.details.wizard',
            'target': 'new',
            'context': ctx,
            'res_id': self.id,
        }
    
        # if self.excel_file:
        #         active_id = self.ids[0]
        #         return {'type': 'ir.actions.act_url',
        #                 'url': 'web/content/?model=export.product.pricelist&download=true&field=excel_file&id=%s&filename=%s' % (active_id, filename),
        #                 'target': 'new'
        #                 }
