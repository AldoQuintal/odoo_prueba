# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.http import request

class LoginAutoWizard(models.TransientModel):
    _name = "login.app.wizard"
    _description = 'Wizard ventas en Ecommerce'
    
    def _obtener_rutas_vendedor(self):
        rute_id = []
        ruta_select = self.env['res.partner'].sudo().search([('user_id', '=', self.env.user.id)])
        print(f'ruta_select. {ruta_select}')
        for r in ruta_select:
            print(f'R {r}')
            rute_id.append(r.ruta_tag.id)

        print(f'ruta id_ {rute_id}')
        if rute_id:
            return [('id', 'in', rute_id)]

    name = fields.Char(string="Vendedor actual:", readonly=True)
    ruta_contacto = fields.Many2one('rutas.contacto', domain=_obtener_rutas_vendedor)
    clientes_ruta = fields.Many2one('res.partner')
    user_id = fields.Many2one('res.users', string="User", 
                              help="Select the user here",
                              store=True)

    @api.onchange('ruta_contacto')
    def onchange_data_ruta(self):
        self.name = f'Vendedor en curso {self.env.user.name}'
        self.clientes_ruta = ''
        for rec in self:
            print(f'Rec: {rec.ruta_contacto.id}')
            return {'domain': {'clientes_ruta': [('ruta_tag', '=', rec.ruta_contacto.id), ('user_id', '=', self.env.user.id)]}}

    @api.onchange('clientes_ruta')
    def onchange_clientes_ruta(self):
        print(f'Self: {self.clientes_ruta.id}')
        usuario = self.env['res.users'].sudo().search([('partner_id', '=', self.clientes_ruta.id)])
        
        self.user_id = usuario.id
        print(f'res_user: {self.user_id}')

    def action_switch(self):
        usuario = self.env['res.users'].sudo().search([('partner_id', '=', self.clientes_ruta.id)])
        print(f'Usuario: {usuario}')
        print("Action Switch************")
        print(f'dbname: {self.env.cr.dbname}')
        print(f'User_id.login: {usuario.login}')
        print(f'self.env {self.env}')

        self.ensure_one()
        session = request.session
        session.update({
            'previous_user': self.env.user.id,
        })
        
        session.authenticate_without_password(self.env.cr.dbname,
                                              usuario.login, self.env)
        return {
            'type': 'ir.actions.act_url',
            'url': '/',
            'target': 'self'
        }










    # rute = fields.Selection(selection=lambda self: self.dynamic_selection_ruta())
    # clients = fields.Selection(selection=lambda self: self.dynamic_selection())

    # def dynamic_selection_ruta(self):
    #     ruta_select = self.env['res.partner'].sudo().search([('user_id', '=', self.env.user.id)])
    #     data_ruta = []
    #     for r in ruta_select:
    #         data_ruta.append(((r.ruta_tag.id), (f'{r.ruta_list} {r.dia}')))
    #         print(f'data_ruta : {data_ruta}')
        
    #     return data_ruta

    # @api.depends('rute')
    # def dynamic_selection(self):
    #     print(f'self: {self}')
    #     prueba = self.env['res.partner'].sudo().search([('user_id', '=', self.env.user.id)])
    #     data = []
    #     print(f'Prueba en selection: {prueba}')
    #     for vendor in prueba:
    #         data.append((vendor.name, vendor.name))

    #     return data
    

    # @api.onchange('rute')
    # def onchange_data_ruta(self):
    #     self.name = self.env.user.name
    #     for rec in self:
    #         print(f'rec. {rec.rute}')
    #         return {'domain': {'clients' : [('rute', '=', rec.rute)]}}
        
    
