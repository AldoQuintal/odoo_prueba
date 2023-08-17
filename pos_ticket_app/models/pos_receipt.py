# -*- coding: utf-8 -*-

from odoo import fields, models


class PosReceipt(models.Model):
    _name = 'pos.receipt'

    name = fields.Char(string='Nombre')
    design_receipt = fields.Text(string='Ticket XML')
