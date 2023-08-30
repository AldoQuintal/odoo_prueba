# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class LoginAutoWizard(models.TransientModel):
    _name = "login.app.wizard"
    _description = 'Wizard ventas en Ecommerce'

    name = fields.Char(string="Name")