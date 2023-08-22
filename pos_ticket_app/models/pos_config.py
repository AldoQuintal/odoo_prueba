# -*- coding: utf-8 -*-
from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    receipt_design = fields.Many2one('pos.receipt', string="Diseño de ticket", help="Selecciona una plantilla para el ticket")
    design_receipt = fields.Text(related='receipt_design.design_receipt', string='Diseño XML')
    is_custom_receipt = fields.Boolean(string='Plantilla para ticket?')

    #Referencia Interna. 
    display_default_code = fields.Boolean(default=False)
    display_list_price = fields.Boolean(default=False)