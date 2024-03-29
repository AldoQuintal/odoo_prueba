# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.addons.website.models import ir_http
from odoo.http import request


class ProductTemplate(models.Model):
	_inherit = "product.template"    
	
	quote_products = fields.Boolean('Quote Product',default=False)
	
class ProductProduct(models.Model):
	_inherit = "product.product"    
	
	quote_products = fields.Boolean('Quote Product',default=False)

class Website(models.Model):
	_inherit = 'website'

	send_quotation_automatic = fields.Boolean(string='Send Quotation Automatic')

	def get_quote_products(self):   
		quote_ids=self.env['product.template'].sudo().search([('quote_products','=','True')])
		
		return quote_ids  

	def get_qty(self):
		res = 0
		if request.session['uid']:
			quote_cart_ids = self.env['quote.order'].sudo().search([('partner_id','=',self.env.user.partner_id.id)])
			request.session['quote_order_id'] = quote_cart_ids.id
		else:
			if 'quote_order_id' in request.session.keys():
				quote_cart_ids = self.env['quote.order'].sudo().browse(request.session['quote_order_id'])
			else:
				quote_cart_ids = self.env['quote.order'].sudo().browse(None)
		
		for i in quote_cart_ids.quote_lines:
			res = res +i.qty
		return int(res)

	def get_quote_cart_products(self):
		order =  self.env['quote.order'].sudo().search([])
		quote_cart_ids = self.env['quote.order'].sudo().browse(request.session['quote_order_id'])

		return quote_cart_ids.quote_lines

class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	send_quotation_automatic = fields.Boolean("Send Quotation Automatic",related='website_id.send_quotation_automatic',readonly=False)

class QuoteOrderLine(models.Model):
	_name = 'quote.order.line'
	
	product_id = fields.Many2one('product.product')
	qty = fields.Float('Quantity')
	price = fields.Float('Price')
	quote_id = fields.Many2one('quote.order', 'Quote Order')
	
	def unlink(self):
		return super(QuoteOrderLine, self).unlink()
	
	
class QuoteOrder(models.Model):
	_name = 'quote.order'
	_rec_name = 'id'
	
	partner_id = fields.Many2one('res.partner')
	quote_lines = fields.One2many('quote.order.line', 'quote_id', 'Quote Lines')

	def unlink(self):
		for qt in self:
			qt.sudo().quote_lines.unlink()
		return super(QuoteOrder, self).unlink()

class SaleOrder(models.Model):
	_inherit = "sale.order"

	is_quote_order = fields.Boolean('Is Quote Order',default=False)

class ResPartner(models.Model):
	_inherit = 'res.partner'

	last_website_quote_id = fields.Many2one('quote.order', compute='_compute_last_website_quote_id', string='Last Online Sales Order')

	def _compute_last_website_quote_id(self):
		QuoteOrder = self.env['quote.order']
		for partner in self:
			is_public = any([u._is_public()
							 for u in partner.with_context(active_test=False).user_ids])
			website = ir_http.get_request_website()
			if website and not is_public:
				partner.last_website_quote_id = QuoteOrder.search([
					('partner_id', '=', partner.id),
				],order='id desc',  limit=1)
			else:
				partner.last_website_quote_id = QuoteOrder
