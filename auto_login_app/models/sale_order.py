from odoo import fields, models, api, _
from odoo.http import request
from odoo.exceptions import AccessError, UserError, ValidationError
from logging import getLogger


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    @api.model_create_multi
    def create(self, vals_list):
        

        res = super(SaleOrder, self).create(vals_list)
        return res