from odoo import models, fields, api

class SaleBranch(models.Model): 
    _name = 'sale.branch' 
    _description = 'Sales Branch' 

    name = fields.Char(string='Branch Name', required=True) 
    sequence_id = fields.Many2one('ir.sequence', string='Sequence')
    code = fields.Char(string='Branch Code', required=True, unique=True)

    # SQL Constraints
    _check_unique_code = models.Constraint(
        'UNIQUE(code)',
        'The branch code must be unique.'
    )


    # Override methods
    @api.model
    def create(self, vals):
        if not vals[0].get('code'):
            raise ValueError("Branch code is required.")
        seq = self.env['ir.sequence'].create({
            'name': f"Sequence for {vals[0].get('name')}",
            'code': f"sale.order.{vals[0].get('code')}",
            'prefix': f"{vals[0].get('code')}/",
            'padding': 4,
        })
        vals[0]['sequence_id'] = seq.id
        return super(SaleBranch, self).create(vals)