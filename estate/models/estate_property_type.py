from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'
    _order = 'sequence, name asc'

    name = fields.Char(string='Property Type Name', required=True)
    sequence = fields.Integer(string='Sequence', default=1)

    # reference to other models
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(compute="_compute_offer_count", string='Offer Count')

    # SQL Constraints
    _check_unique_property_type = models.Constraint(
        'UNIQUE(name)',
        'The property type name must be unique.'
    )

    # computed methods
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)