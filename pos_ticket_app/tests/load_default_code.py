# -*- coding: utf-8 -*-
import odoo

from odoo.addons.point_of_sale.tests.common import TestPoSCommon


@odoo.tests.tagged("post_install", "-at_install")
class TestPosDisplayDefaultCode(TestPoSCommon):
    def setUp(self):
        print("Test Setup")
        super(TestPosDisplayDefaultCode, self).setUp()
        self.config = self.basic_config
        self.config.display_default_code = True
        self.pos_session = self.env["pos.session"].create({"config_id": self.config.id})
        

    def test_load_params_products(self):
        result = self.pos_session._loader_params_product_product()
        print(f'resutl del test: {result}')
        self.assertTrue(result["context"]["display_default_code"])

