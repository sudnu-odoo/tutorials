from odoo import models

class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    def get_product_info_pos(self, price, quantity, pos_config_id, product_variant_id=False):
        # Call the original method first
        res = super().get_product_info_pos(price, quantity, pos_config_id, product_variant_id)

        # Add weight and volume info
        res.update({
            'weight': self.weight or 0.0,
            'volume': self.volume or 0.0,
        })

        return res
