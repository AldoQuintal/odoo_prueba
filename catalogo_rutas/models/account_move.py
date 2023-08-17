from odoo import _, api, fields, models, tools
from odoo.osv import expression

class AccountMove(models.Model):
    """ Update partner to add a field about notification preferences. Add a generic opt-out field that can be used
       to restrict usage of automatic email templates. """
    _inherit = "account.move"

    ruta_tag = fields.Char(string="Ruta", store=True, readonly=True)
    dia_tag = fields.Char(string="Día", store=True, readonly=True)

    def action_post(self):
        self.write({
            'ruta_tag'  : self.partner_id.ruta_tag.ruta,
            'dia_tag'   : self.partner_id.ruta_tag.dia
        })
        moves_with_payments = self.filtered('payment_id')
        other_moves = self - moves_with_payments
        if moves_with_payments:
            moves_with_payments.payment_id.action_post()
        if other_moves:
            other_moves._post(soft=False)
        return False