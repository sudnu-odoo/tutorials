from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'

    price = fields.Float(string='Offer Price', required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string='Status', default='pending', copy=False)
    validity = fields.Integer(string='Validity (days)', default=7)

    # reference to other models
    partner_id = fields.Many2one('res.partner', string='Buyer', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    property_type_id = fields.Many2one(
        related='property_id.property_type_id'
    )

    # SQL Constraints
    _check_offer_price = models.Constraint(
        'CHECK(price >= 0)',
        'The offer price must be positive.'
    )

    # computed fields
    date_deadline = fields.Date(
        string='Deadline',
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )

    # computed methods
    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            # fallback to today if create_date isn't set yet
            create_date = offer.create_date or fields.Date.today()
            offer.date_deadline = create_date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Date.today()
            if offer.date_deadline:
                delta = offer.date_deadline - create_date.date()
                offer.validity = delta.days

    # action methods
    def action_accept(self):
        for offer in self:
            # If the property already has an accepted offer, reject this action
            existing_offer = offer.property_id.offer_ids.filtered(lambda o: o.status == 'accepted')
            if existing_offer and existing_offer != offer:
                raise UserError("This property already has an accepted offer.")

            offer.status = 'accepted'
            offer.property_id.state = 'offer_accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'

    @api.model
    def create(self, vals):
        for val in vals:
            property_id = val.get('property_id')
            property_rec = self.env['estate.property'].browse(property_id)

            # if property already sold, cannot make an offer
            if property_rec.state == 'sold':
                raise UserError("Cannot create an offer for a property that is already sold.")

            existing_highest = max(property_rec.offer_ids.mapped('price') or [0.0])
            new_price = val.get('price', 0.0)
            if new_price < existing_highest:
                raise ValidationError(
                    f"The new offer price {new_price} must be higher than the existing highest offer {existing_highest}."
                )

        offer = super().create(vals)
        property_rec.state = 'offer_received'

        return offer