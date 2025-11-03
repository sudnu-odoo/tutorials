from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    branch_id = fields.Many2one('sale.branch', string='Sales Branch')

    @api.model
    def create(self, vals):
        # Only override name if branch is provided and name is default
        if vals[0].get('branch_id'):
            branch = self.env['sale.branch'].browse(vals[0]['branch_id'])
            if branch.sequence_id and (not vals[0].get('name') or vals[0]['name'] == 'New'):
                vals[0]['name'] = branch.sequence_id.next_by_id()
        return super(SaleOrder, self).create(vals)
