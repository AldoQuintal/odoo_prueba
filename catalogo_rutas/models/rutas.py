from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo import models, fields, api, _, exceptions
from odoo import _, api, fields, models, tools

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    check_ruta = fields.Boolean(string="Rutas de contacto", related="company_id.check_ruta", readonly=False)

class preciadorDetalle(models.Model):
    _name = "rutas.contacto"
    _description = 'Modelo que genera un catálogo de rutas'

    ruta = fields.Char(string="Nombre de la ruta", required=True, help="Identificador para la ruta")
    description = fields.Char(string="Descripción", required=False, help="Descripción")
    #partner_id = fields.Many2many('res.partner')
    dia = fields.Char(string="Día")




    def name_get(self):
        result = []
        for r in self:
            name = str(r.ruta) 
            name += ' (' + str(r.dia) + ')'
            result.append((r.id, name))
        return result

