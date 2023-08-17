# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_round


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for a in self:
            a.price_unit = float_round(a.price_unit, precision_rounding=0.25, rounding_method='UP')

        for line in self:
            print(f'line_ {line}')
            tax_results = self.env['account.tax']._compute_taxes([line._convert_to_tax_base_line_dict()])
            print(f'Tax_resutls: {tax_results}')
            totals = list(tax_results['totals'].values())[0]
            print(f'total: {totals}')
            total_tax = tax_results['base_lines_to_update'][0][1]['price_total']
            print(f'Total _tax {total_tax}')
            amount_untaxed = totals['amount_untaxed'] 
            print(f'untax: {amount_untaxed}')
            amount_tax = totals['amount_tax']
            print(f'tax {amount_tax}')

            print(f'---------- {amount_untaxed + amount_tax}')

            cash_round = amount_untaxed + amount_tax
            redonde = float_round(cash_round, precision_rounding=0.25, rounding_method='UP')
            print(f'Cantidad redondeada ***: {redonde}')

            line.update({
                'price_subtotal': amount_untaxed,
                'price_tax': amount_tax,
                'price_total': cash_round,
                
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_recordset(['invoice_repartition_line_ids'])