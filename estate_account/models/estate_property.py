from odoo import api, models
from odoo import Command

class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        res = super(EstateProperty, self).action_sold()

        # collect properties that actually have a buyer
        props = self.filtered(lambda p: p.buyer_id)

        if not props:
            return res

        props.check_access_rights('write')
        props.check_access_rule('write')

        property_list = []
        for property in self:            
            property_list.append({
                "partner_id": property.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create({
                        "name": f"Sale of property {property.name}",
                        "quantity": 1,
                        "price_unit": property.selling_price * 0.06,  # 6% fee
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1,
                        "price_unit": 100.0,
                    }),
                ]
            })

        self.env['account.move'].sudo().create(property_list)

        return res