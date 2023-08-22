# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_receipt_design = fields.Many2one(related='pos_config_id.receipt_design', string="Diseño de ticket",
                                         help="Selecciona una plantila para ticket", compute='_compute_pos_is_custom_receipt',
                                         readonly=False, store=True)
    pos_design_receipt = fields.Text(related='pos_config_id.design_receipt', string='Ticket XML')
    pos_is_custom_receipt = fields.Boolean(related='pos_config_id.is_custom_receipt', readonly=False, store=True)

    #Referencia interna.
    pos_display_default_code = fields.Boolean(related="pos_config_id.display_default_code", readonly=False)

    pos_display_price = fields.Boolean(
        related="pos_config_id.display_list_price", readonly=False
    )

    @api.depends('pos_is_custom_receipt', 'pos_config_id')
    def _compute_pos_is_custom_receipt(self):
        for res_config in self:
            if res_config.pos_is_custom_receipt:
                res_config.pos_receipt_design = res_config.pos_config_id.receipt_design
            else:
                res_config.pos_receipt_design = False
