from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many(
        'estate.property',
        'salesperson_id',
        string='Properties'
    )

    def action_print_user_properties(self):
        return self.env.ref('estate.report_user_properties').report_action(self)