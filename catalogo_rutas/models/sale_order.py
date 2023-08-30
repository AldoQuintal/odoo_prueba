from odoo import _, api, fields, models, tools
from odoo.osv import expression
from odoo.exceptions import AccessError, UserError, ValidationError


class SaleOrder(models.Model):
    """ Update partner to add a field about notification preferences. Add a generic opt-out field that can be used
       to restrict usage of automatic email templates. """
    _inherit = "sale.order"

    ruta_tag = fields.Char(string="Ruta")
    dia_tag = fields.Char(string="Día")
    ruta = fields.Many2one('rutas.contacto')



    # @api.model_create_multi
    # def create(self, vals_list):
    #     print("Se creo una SO")
    #     res = super(SaleOrder, self).create(vals_list)
        
    #     return res

    @api.onchange('partner_id')
    def _get_ruta_tag(self):
        print(self.partner_id.ruta_tag.id)
        
        self.write({
            'ruta_tag'  : self.partner_id.ruta_tag.ruta,
            'dia_tag'   : self.partner_id.ruta_tag.dia,
            'ruta'      : self.partner_id.ruta_tag.id
            
        })

        # self.ruta_tag = self.partner_id.ruta_tag.ruta
        # print(self.ruta_tag)

    def action_confirm(self):
        if self._get_forbidden_state_confirm() & set(self.mapped('state')):
            raise UserError(_(
                "It is not allowed to confirm an order in the following states: %s",
                ", ".join(self._get_forbidden_state_confirm()),
            ))

        for order in self:
            if order.partner_id in order.message_partner_ids:
                continue
            order.message_subscribe([order.partner_id.id])

        self.write(self._prepare_confirmation_values())

        self.write({
            'ruta_tag'  : self.partner_id.ruta_tag.ruta
        })

        # Context key 'default_name' is sometimes propagated up to here.
        # We don't need it and it creates issues in the creation of linked records.
        context = self._context.copy()
        context.pop('default_name', None)

        self.with_context(context)._action_confirm()
        if self.env.user.has_group('sale.group_auto_done_setting'):
            self.action_done()

        return True