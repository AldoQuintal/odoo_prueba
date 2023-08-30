# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from datetime import datetime
import time
import pytz

class InventoryAdminWizard(models.TransientModel):
    _name = "inventory.app.wizard"
    _description = 'Wizard para gestionar el responsable de los picking'

    ruta = fields.Many2many('rutas.contacto', required=True)
    date = fields.Char()
    user = fields.Many2one('res.users', string="Responsable", required=True)
    

    @api.onchange('ruta')
    def _get_today_date(self):
        #print(f'self.env.user_ {self.env.user}')
        tt = self.env['res.users'].search([('login', '=', '__system__')])
        #print(f'tt _ {tt}')
        if self.env.user.tz:
            # En ese caso, la recuperamos
            tz = pytz.timezone(self.env.user.tz)
        # En caso contrario
        else:
            # Utilizaremos la zona horaria de la zona centro de México
            tz = pytz.timezone('America/Mexico_City')
        #print(f'Timezon:{tz}')

        self.date = f'Validación al día de hoy {datetime.now(tz).date()}'
        #print(f'date: {self.date}')

    @api.model_create_multi
    def create(self, vals_list):
        #print(vals_list[0]['ruta'][0][2])
        for a in vals_list[0]['ruta'][0][2]:
            id_ruta = a
            rute = self.env['rutas.contacto'].search([('id', '=', id_ruta)])
            #print(f'Sale order, {sale_order}')
            #print(vals_list[0]['user'])
            rute.update({
                'user_id'   : vals_list[0]['user']
            })
            

            #print(f'Today: {today}')

            if self.env.user.tz:
                # En ese caso, la recuperamos
                tz = pytz.timezone(self.env.user.tz)
            # En caso contrario
            else:
                # Utilizaremos la zona horaria de la zona centro de México
                tz = pytz.timezone('America/Mexico_City')

            today = datetime.now(tz).date()
            
            sale_order = self.env['sale.order'].search([
                ('ruta', '=', rute.id),
                ])
            
            #print(f'Sale order: {sale_order}')

            for data in sale_order:
                pick = self.env['stock.picking'].search([
                    ('sale_id', '=', data.id),
                    ])
                    
                if pick:
                    for pi in pick:
                        #print(f'Pickeo: {pick}')
                        #print(pick.create_date.day) 
                        fecha = pytz.utc.localize(pi.create_date).astimezone(tz)
                        #print(f'Fecha con mi time zone {fecha}')
                        #print(f'Pick: {pick}')
                        #print(f'Fecha: {fecha.day}')
                        #print(f'Fecha today: {today.day}')

                        if fecha.day == today.day:
                            pick_update = self.env['stock.picking'].search([
                            ('sale_id', '=', data.id),
                            ('date_today', '=', fecha)
                            ])
                            #print(f'Es del día de hoy  {pick}')
                            #print(vals_list[0]['user'])
                            print(f'Pick a updata: {pick_update}')
                            pick_update.update({
                                'user_id'   : vals_list[0]['user']
                            })

        res = super(InventoryAdminWizard, self).create(vals_list)
        return res

class preciadorDetalle(models.Model):
    _inherit = "rutas.contacto"
    _description = 'Modelo que genera un catálogo de rutas'

    user_id = fields.Many2one('res.users')


class Picking(models.Model):
    _inherit = "stock.picking"
    _description = "Transfer"

    date_today = fields.Date(store=True)

    @api.model_create_multi
    def create(self, vals_list):

        #print(f'self.env.user_ {self.env.user}')
        if self.env.user.tz:
            # En ese caso, la recuperamos
            tz = pytz.timezone(self.env.user.tz)
        # En caso contrario
        else:
            # Utilizaremos la zona horaria de la zona centro de México
            tz = pytz.timezone('America/Mexico_City')

        #print(f'Time zone {tz}')
        #print(f'Insert en la base de datos day_today: {datetime.now(tz).date()}')

        vals_list[0].update({
            'date_today'    :   datetime.now(tz).date()
        })
        sale_order = self.env['sale.order'].search([('name', '=', vals_list[0]['origin'])])
        ruta = self.env['rutas.contacto'].search([('id', '=', sale_order.ruta.id)])
        #print(f'Rutaa: {ruta}')
        today = datetime.now(tz).date()
        if ruta:    
            fecha = pytz.utc.localize(ruta.write_date).astimezone(tz)
            
            if fecha.day == today.day:
                vals_list[0].update({
                    'user_id'   :   ruta.user_id.id
                })
            
        res = super(Picking, self).create(vals_list)
        return res
    
    
