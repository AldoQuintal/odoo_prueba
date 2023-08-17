from odoo import _, api, fields, models, tools
from odoo.osv import expression
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_round


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    amount_total = fields.Monetary(string="Total", store=True, compute='_compute_amounts', tracking=4)

    @api.depends('order_line.price_subtotal', 'order_line.price_tax', 'order_line.price_total')
    def _compute_amounts(self):
        """Compute the total amounts of the SO."""
        print("Entra al compute")
        for order in self:
            order_lines = order.order_line.filtered(lambda x: not x.display_type)
            print(f'order_lines: {order_lines}')
            order.amount_untaxed = sum(order_lines.mapped('price_subtotal'))
            print(f'Order amount untax: {order.amount_untaxed}')

            price_total = float_round(sum(order_lines.mapped('price_total')), precision_rounding=0.25, rounding_method='UP')
            order.amount_total = price_total
            
            print(f'Order amount total: {order.amount_total}')
            order.amount_tax = sum(order_lines.mapped('price_tax'))
            print(f'Order amount tax: {order.amount_tax}')


    @api.depends('order_line.tax_id', 'order_line.price_unit', 'amount_total', 'amount_untaxed')
    def _compute_tax_totals(self):
        for order in self:
            order_lines = order.order_line.filtered(lambda x: not x.display_type)
            print(f'Order? : {order_lines} ')
            order.tax_totals = self.env['account.tax']._prepare_tax_totals(
                [x._convert_to_tax_base_line_dict() for x in order_lines],
                order.currency_id,
            )
            
            print(f'Order Tax_totals : {order.tax_totals}')

    # @api.onchange('partner_id')
    # def _onchange_amount_total(self):
    #     print("8*8*8*8*8*8*8*8*8*8*8*8*8*8*8")
    #     print(self.name)

 
    # @api.model_create_multi
    # def create(self, vals_list):
    #     print("Se creo una SO")
    #     print(self)
        
    #     print(vals_list)
    #     res = super(SaleOrder, self).create(vals_list)

        
        
    #     return res
    