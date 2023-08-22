# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_round


class SaleOrderLine(models.Model):
    _inherit = 'product.template'

    list_price = fields.Float(
        'Sales Price', default=1.0,
        digits='Product Price',
        help="Price at which the product is sold to customers.",
    )

    list_price_copia = fields.Float('Sales Price', default=1.0,
        digits='Product Price',
        help="Price at which the product is sold to customers.",)


    @api.onchange('list_price_copia')
    def _onchange_price_copy(self):
        self.write({
        'list_price': float_round(self.list_price_copia, precision_rounding=0.25, rounding_method='UP')
    })
