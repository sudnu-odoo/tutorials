from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'
    _order = 'name asc'

    name = fields.Char(string='Tag Name', required=True)
    description = fields.Text(string='Description')
    color = fields.Integer(string="Color")

    # SQL Constraints
    _check_unique_tag = models.Constraint(
        'UNIQUE(name)',
        'The tag name must be unique.'
    )