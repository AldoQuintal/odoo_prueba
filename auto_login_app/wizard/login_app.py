# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.http import request
from odoo.exceptions import AccessError, UserError, ValidationError
from logging import getLogger

LOGGER = getLogger(__name__)
class LoginAutoWizard(models.TransientModel):
    _name = "login.app.wizard"
    _description = 'Wizard ventas en Ecommerce'

    
    
    is_vendor = fields.Boolean(string="No es usted?")
    new_vendor = fields.Many2one('res.users', string="Otro vendedor")
    name = fields.Char(string="Vendedor actual:", readonly=True)

    # @api.depends('name')
    # def _obtener_rutas_vendedor(self):
    #     print("Cambio el select?")
    #     rute_id = []
    #     if not self.is_vendor:
    #         ruta_select = self.env['res.partner'].sudo().search([('user_id', '=', self.env.user.id)])
    #     else:
    #         ruta_select = self.env['res.partner'].sudo().search([('user_id', '=', self.new_vendor.id)])


    #     print(f'ruta_select. {ruta_select}')
    #     for r in ruta_select:
    #         print(f'R {r}')
    #         rute_id.append(r.ruta_tag.id)

    #     print(f'ruta id_ {rute_id}')
    #     if rute_id:
    #         return [('id', 'in', rute_id)]
        
    

    



    name = fields.Char(string="Vendedor actual:", readonly=True)
    ruta_contacto = fields.Many2one('rutas.contacto')
    clientes_ruta = fields.Many2one('res.partner')
    user_id = fields.Many2one('res.users', string="User", 
                              help="Select the user here",
                              store=True)
    is_vendor = fields.Boolean(string="No es usted?")
    space = fields.Char(string=" ", readonly=True)
    alert = fields.Char()

    @api.onchange('name')
    def onchange_data_contacto(self):

        LOGGER.info("Esta es una prueba de log")
        print("Se afecto el name")
        self.clientes_ruta = ''
        rute_ids = []

        LOGGER.info(f'Usuario Self : {self.env.user.id}')

        LOGGER.info(f'Nuevo usuario : {self.new_vendor.id}')

        
        if not self.is_vendor:
            ruta_select = self.env['res.partner'].sudo().search([('user_id', '=', self.env.user.id)])
        else:
            ruta_select = self.env['res.partner'].sudo().search([('user_id', '=', self.new_vendor.id)])
            
        
        LOGGER.info(f'Vendedor : {ruta_select}')
        # if not ruta_select:
        #      raise UserError(_(
        #             f'El vendedor {self.new_vendor.name} no cuenta con rutas asignadas'))

        # for rec in ruta_select:
        #     rute_ids.append(rec.ruta_tag.id)
            
            
        #     domai = {'domain': {'ruta_contacto': [('id', 'in', rute_ids)]}}

        # return domai
    
    def name_get(self):
        print("Prueba odoo")
        self.name = f'Vendedor en curso {self.env.user.name}'
        return [(session.id, session.display_name) for session in self]


    @api.onchange('new_vendor')
    def onchange_new_vendor(self):
        if not self.is_vendor:
            self.name = f'Vendedor en curso {self.env.user.name}'
        else:
            self.name = f'Se encuentra supliendo a {self.new_vendor.name}'

    @api.onchange('is_vendor')
    def onchange_is_vendor(self):
        self.new_vendor = ''
        self.ruta_contacto = ''
        self.clientes_ruta = ''

    @api.onchange('ruta_contacto')
    def onchange_data_ruta(self):
        print("Onchange ruta contacto")

        self.clientes_ruta = ''
        if not self.is_vendor:
            print("Vendedor logeuado")
            actual_vendor = self.env.user.id
        else:
            actual_vendor = self.new_vendor.id

        print(f'Actual vendor? : {actual_vendor}')

        for rec in self:
            print(f'Rec: {rec.ruta_contacto.id}')
            do = {'domain': {'clientes_ruta': [('ruta_tag', '=', rec.ruta_contacto.id), ('user_id', '=', actual_vendor)]}}
            print(f'do: {do}')
            return do

    def action_switch(self):
        if not self.clientes_ruta:
            self.alert = "Elija un cliente antes de aceptar"
            self.ruta_contacto = ''
            self.clientes_ruta = ''
            self.is_vendor = False
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
                # 'view_type': 'form',
                # 'view_mode': 'form',
                # 'res_model': 'login.app.wizard',
                # 'target': 'current',
            }
        else:
            self.alert = False

        usuario = self.env['res.users'].sudo().search([('partner_id', '=', self.clientes_ruta.id)])
        print(f'Usuario : {usuario}')

        if not usuario:
            self.alert = f'Este usuario {self.clientes_ruta.name} no cuenta con permisos para entrar al portal.'
            self.ruta_contacto = ''
            self.clientes_ruta = ''
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
        else:
            self.alert = False
        
        
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
        
    
