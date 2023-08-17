from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo import models, fields, api, _, exceptions
from odoo.models import Model, NewId # Se importa el objeto modelo necesario de odoo


class ResCompany(Model):
    _inherit = 'res.company'

    check_ruta = fields.Boolean(string="Rutas de contacto")