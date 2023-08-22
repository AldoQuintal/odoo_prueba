# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo import SUPERUSER_ID
import json

class websiteProductQuote(http.Controller):

	@http.route(['/request/quote'], type='http', auth="public", website=True)
	def requestQuote(self, **post):
		return request.render("website_product_variant_quote_av.request_quotation")

	@http.route(['/quote/cart'], type='http', auth="public", website=True)
	def quote_cart(self, **post):
		return request.render("website_product_variant_quote_av.quote_cart")
	
	@http.route(['/quote/product/selected/<model("product.product"):product_id>'], type='http', auth="public", website=True)
	def quote_multiple(self, product_id, **post):
		if post:
			new_qty = 1
			quote_obj = request.env['quote.order']
			quote_line_obj = request.env['quote.order.line']
			partner = request.env.user.partner_id
			quote_order_id = request.session.get('quote_order_id')
			if not quote_order_id:
				last_quote_order = partner.last_website_quote_id
				quote_order_id = last_quote_order.id

			quote_order = request.env['quote.order'].sudo().browse(quote_order_id).exists() if quote_order_id else None
			
			product_product_obj = request.env['product.product'].sudo().search([('id','=', product_id.id)], limit=1)
			request.session['quote_order_id'] = None
			if not quote_order:
				quote = quote_obj.sudo().create({'partner_id': partner.id})
				quote_line_ids = quote_line_obj.sudo().search([('product_id','=', product_id.id),('quote_id','=',quote.id)])
				
				if quote_line_ids:
					upd_qty = int(quote_line_ids.qty) + int(new_qty)
					quote_line_ids.update({'qty': upd_qty})
				else:
					quote_line = quote_line_obj.sudo().create({
						'product_id': product_product_obj.id,
						'qty': int(new_qty),
						'price': product_product_obj.lst_price,
						'quote_id': quote.id,	
					})
				request.session['quote_order_id'] = quote.id
			if quote_order:
				if not request.session.get('quote_order_id'):
					request.session['quote_order_id'] = quote_order.id
				
				quote_line_ids = quote_line_obj.sudo().search([('product_id','=', product_id.id),('quote_id','=',quote_order.id)])
				if quote_line_ids:
					upd_qty = int(quote_line_ids.qty) + int(new_qty)
					quote_line_ids.update({'qty': upd_qty})
				else:
					quote_line = quote_line_obj.sudo().create({
						'product_id': product_product_obj.id,
						'qty': int(new_qty),
						'price': product_product_obj.lst_price,
						'quote_id': quote_order.id,	
					})
			
		return request.render("website_product_variant_quote_av.quote_cart")	

	@http.route(['/quote/product/public/user'], type='http', auth="public", website=True)
	def quote_multiple_nonlogin(self, **post):
		countries = request.env['res.country'].sudo().search([])
		states = request.env['res.country.state'].sudo().search([])
		values ={}
		values.update({
			'countries': countries,
			'states': states,
		})
		return request.render("website_product_variant_quote_av.get_quotation_request",values)

	@http.route(['/quote/cart/update_json'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
	def upd_cart_qty(self, updated_val=None, product_id=None, **post):
		quote_cart_id =request.env['quote.order'].sudo().browse(request.session['quote_order_id'])
		if quote_cart_id:
			quote_line = quote_cart_id.quote_lines.filtered(lambda ql: ql.product_id.id == int(product_id))
			quote_line.write({'qty':updated_val})
		return True	
		
	@http.route(['/process/quote'], type='http', auth="public", website=True)
	def get_quote(self, **post):
		order =request.env['quote.order'].sudo().browse(request.session['quote_order_id'])
		val={'order':order}
		return request.render("website_product_variant_quote_av.get_billing_login_user",val)

	@http.route(['/process/quotation/public/user'], type='http', auth="public", website=True)
	def get_quote_nonlogin(self, **post):
		if not post:
			return request.redirect("/request/quote")
		if post.get('state_id'):
			state_id = int(post['state_id'])
		else:
			state_id = False

		partner_obj = request.env['res.partner']
		partner = partner_obj.sudo().create({ 
		  'name' : post.get('name',False),
		  'email' : post.get('email',False),
		  'phone' : post.get('phone',False),
		  'street': post.get('street',False),
		  'city':post.get('city',False),
		  'zip':post.get('zip',False),
		  'country_id':int(post.get('country_id')) if post.get('country_id') else False,
		  'state_id': state_id,
		})
		order = request.env['quote.order'].sudo().browse(request.session['quote_order_id'])
		order.update({'partner_id':partner.id})
		product_obj = request.env['product.template']        
		sale_order_obj = request.env['sale.order']
		sale_order_line_obj = request.env['sale.order.line']
		line_vals ={}
		pricelist_id = request.website.get_current_pricelist().id
		vals = {
				'partner_id': order.partner_id.id, 
				'pricelist_id': pricelist_id,
				'user_id': request.website.salesperson_id and request.website.salesperson_id.id,
				'team_id': request.website.salesteam_id and request.website.salesteam_id.id,
				'is_quote_order' : True,
			}    	
		sale_order_create = sale_order_obj.with_user(SUPERUSER_ID).create(vals)
		for i in order.quote_lines:
			line_vals = {    
						'product_id': i.product_id.id, 
						'name': i.product_id.name,#sale_order_line_obj.get_sale_order_line_multiline_description_sale(i.product_id),
						'product_uom_qty': i.qty, 
						'customer_lead':7, 
						'product_uom':i.product_id.uom_id.id,
						'order_id': sale_order_create.id  }		
			sale_order_line_create = sale_order_line_obj.with_user(SUPERUSER_ID).create(line_vals)
		
		# Send mail
		is_send_quote = request.website.send_quotation_automatic
		if is_send_quote == True:
			self.send_quotation_automatic(sale_order_create.id)
			sale_order_create.write({'state': 'sent'})
		else:
			template_id = request.env.ref('website_product_variant_quote_av.email_template_def_request_quotation')
			if sale_order_create.partner_id and sale_order_create.partner_id.email:
				template_id.sudo().with_context(email_to=sale_order_create.partner_id.email).send_mail(SUPERUSER_ID, force_send=True)
		
		order.sudo().unlink()
		request.session['quote_order_id'] = False
		return request.render("website_product_variant_quote_av.quotation_send_successfully")

	@http.route(['/shop/product/quote/confirm'], type='http', auth="public", website=True)
	def quote_confirm(self, **post):
		order = request.env['quote.order'].sudo().browse(request.session['quote_order_id'])
		if not order:
			order = request.env['quote.order'].sudo().search([],order='id desc', limit=1)
		product_obj = request.env['product.template']        
		partner_obj = request.env['res.partner']
		sale_order_obj = request.env['sale.order']
		sale_order_line_obj = request.env['sale.order.line']
		line_vals ={}
		pricelist_id = request.website.get_current_pricelist().id
		vals = {
				'partner_id': order.partner_id.id, 
				'pricelist_id': pricelist_id,
				'user_id': request.website.salesperson_id and request.website.salesperson_id.id,
				'team_id': request.website.salesteam_id and request.website.salesteam_id.id,
				'is_quote_order' : True,
			} 
		sale_order_create = sale_order_obj.sudo().create(vals)
		for i in order.quote_lines:
			line_vals = {    
						'product_id': i.product_id.id, 
						'name': i.product_id.name,#sale_order_line_obj.get_sale_order_line_multiline_description_sale(i.product_id),
						'product_uom_qty': i.qty, 
						'customer_lead':7, 
						'product_uom':i.product_id.uom_id.id,
						'order_id': sale_order_create.id  }			
			sale_order_line_create = sale_order_line_obj.sudo().create(line_vals)

		# Send mail
		is_send_quote = request.website.send_quotation_automatic
		if is_send_quote == True:
			self.send_quotation_automatic(sale_order_create.id)
			sale_order_create.write({'state': 'sent'})
		else:
			template_id = request.env.ref('website_product_variant_quote_av.email_template_def_request_quotation', raise_if_not_found=False)
			if sale_order_create.partner_id and sale_order_create.partner_id.email:
				template_id.sudo().with_context(email_to=sale_order_create.partner_id.email).send_mail(sale_order_create.id, force_send=True)

		order.sudo().unlink()
		request.session['quote_order_id'] = False
		return request.render("website_product_variant_quote_av.quotation_send_successfully")
	
	def send_quotation_automatic(self, sale_order_create):
		template_id = request.env.ref('website_product_variant_quote_av.email_template_request_quotation', raise_if_not_found=False)
		print(f'Template_id_: {template_id}')
		template_id.sudo().send_mail(sale_order_create, force_send=True)
		return True

	@http.route(['/quote/delete/<model("quote.order.line"):line>'], type='http', auth="public", website=True)
	def quotation_delete(self, **post):
		order = post.get('line')
		if order:
			order.sudo().unlink()
		return request.render("website_product_variant_quote_av.quote_cart")
	
	@http.route(['/get/quote/products/list'], type='json', auth="public", website=True)
	def get_cart_qty(self, **post):
		quote_products =request.env['product.template'].sudo().search([('quote_products','=',True)])
		if quote_products:
			return quote_products.ids
		return []	