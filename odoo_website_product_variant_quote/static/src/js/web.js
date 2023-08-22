
odoo.define('odoo_website_product_variant_quote.web', function(require) {
	"use strict";
	var core = require('web.core');
	var QWeb = core.qweb;
	var _t = core._t;
	var sAnimations = require('website.content.snippets.animation');
	var rpc = require('web.rpc');
	var ajax = require('web.ajax');
	var session = require('web.session');
	var VariantMixin = require('sale.VariantMixin');
	var publicWidget = require('web.public.widget');
	require('website_sale.website_sale');

     publicWidget.registry.WebsiteSale.include({
        _toggleDisable: function ($parent, isCombinationPossible) {
        		this._super.apply(this, arguments);
            VariantMixin._toggleDisable.apply(this, arguments);
            $parent.find("#add_to_cart_quote").toggleClass('disabled', !isCombinationPossible);
            $parent.find("#add_to_cart").toggleClass('disabled', !isCombinationPossible);
            $parent.find("#product_quote_price").toggleClass('disabled', isCombinationPossible);
            $parent.find("#buy_now").toggleClass('disabled', !isCombinationPossible);
            $parent.find("#request_quote").toggleClass('disabled', isCombinationPossible);
        },
    });


	sAnimations.registry.websiteQuote=sAnimations.Class.extend({
		 selector: '.oe_website_sale',
		read_events: {
			'change #txt': '_onClickQuote',
			'click #bt_non':'_onNonlogin',
			'click .request_quote_btn':'_onRequestQuoteBtn',
		},
		_onClickQuote: function () {
				var jsonObj = [];
				$('#tbl tbody tr').each(function(){
					var in_val = $(this).find("#txt > input[type=text]").val();
					var x = $(this).find('#txt').attr('line_id');
					var item = {}
					item [x] = in_val;
					jsonObj.push(item);

				});
				var user = session.uid
				this._rpc({
					route: "/quote/cart/update_json",
					params: {
						jsdata: jsonObj,
					},
				}).then(function (data) {
					window.location.href = '/quote/cart';
				});
		},
		_onNonlogin: function () {
			var id1 = document.getElementById("txt1").value
			var obj = document.getElementById("obj").value
			ajax.jsonRpc("/shop/product/quote/confirm/nonlogin","call",{
				'id1' : id1,
				'obj':obj,
			}).then(function (data) {
				window.location.href = '/thank_you';
			});
		},
		_onRequestQuoteBtn: function () {
			var product_id = $(".product_id").val();
			$('.request_quote_form').attr('action','/quote/product/selected/'+product_id);
  			$('.request_quote_form').submit();
		}
	});

	$(document).ready(function (){

		$("select[name='country_id]'").change(function() {
			var $country = this.$('select[name="country_id"]');
	        var countryID = ($country.val() || 0);
	        this.$stateOptions.detach();
	        var $displayedState = this.$stateOptions.filter('[data-country_id=' + countryID + ']');
	        var nb = $displayedState.appendTo(this.$state).show().length;
	        this.$state.parent().toggle(nb >= 1);
		});
	});
});
