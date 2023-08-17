from odoo import _, api, fields, models, tools
from odoo.osv import expression


class Partner(models.Model):
   """ Update partner to add a field about notification preferences. Add a generic opt-out field that can be used
      to restrict usage of automatic email templates. """
   _inherit = "res.partner"

   ruta_tag = fields.Many2one('rutas.contacto',  string="Other")
   dia = fields.Char(string="Dia", readonly=True)
   ruta_list = fields.Char(string="Ruta")

   @api.onchange('ruta_tag')
   def _get_day_ruta(self):
      print(self.ruta_tag)
      self.write({
         'dia' : self.ruta_tag.dia,
         'ruta_list' : self.ruta_tag.ruta,
      })

   # @api.onchange('ruta_tag')
   # def _show_name_ruta(self):
   #    print(f'Ruta: {self.ruta_tag.ruta}')
   #    self.ruta_tag = self.ruta_tag.ruta
