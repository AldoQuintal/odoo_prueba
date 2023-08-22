# -*- coding: utf-8 -*-

from odoo import models


class PosSession(models.Model):
    _inherit = 'pos.session'


    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        print(f'Entral al loader: {result}')
        if self.config_id and self.config_id.display_default_code:
            result["context"]["display_default_code"] = True
        
        if self.config_id and self.config_id.display_list_price:
            result["context"]["display_list_price"] = True
            print(result["context"]["display_list_price"])

        result['search_params']['fields'].append('qty_available')
        print(f'Resultado ****** {result}')
        return result

    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        result += [
            'res.config.settings',
            'pos.receipt',
        ]
        return result

    def _loader_params_pos_receipt(self):
        return {
            'search_params': {
                'fields': ['design_receipt', 'name'],

            },
        }

    def _get_pos_ui_pos_receipt(self, params):
        return self.env['pos.receipt'].search_read(**params['search_params'])

    def _loader_params_res_config_settings(self):
        return {
            'search_params': {
                'fields': ['pos_receipt_design'],

            },
        }

    def _get_pos_ui_res_config_settings(self, params):
        return self.env['res.config.settings'].search_read(**params['search_params'])

    # #Referencia Interna
    # def _loader_params_product_product(self):
    #     print(f'------ {self.config_id.display_default_code}')
    #     result = super()._loader_params_product_product()
    #     if self.config_id and self.config_id.display_default_code:
    #         result["context"]["display_default_code"] = True
    #     return result
