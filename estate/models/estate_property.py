from odoo import api, models, fields
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare, float_is_zero
from odoo.exceptions import ValidationError

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = 'id desc'

    name = fields.Char(string='Property Name', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From', default=fields.Date.today() + relativedelta(days=90), copy=False)
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='Number of Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sq ft)')
    active = fields.Boolean(string='Active', default=True)
    facades = fields.Integer(string='Number of Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sq ft)')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string='Garden Orientation')
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], string='Status', default='new')

    # references to other models 
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    company_id = fields.Many2one(
        'res.company',
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )

    # # SQL Constraints
    _check_expected_price = models.Constraint(
        'CHECK(expected_price >= 0)',
        'The expected price must be positive.'
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price must be non-negative.'
    )

    # computed fields
    total_area = fields.Float(
        string='Total Area (sq ft)',
        compute='_compute_total_area'
    )

    best_price = fields.Float(
        string='Best Offer',
        compute='_compute_best_price'
    )

    # computed methods
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = (property.living_area or 0.0) + (property.garden_area or 0.0)

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            if property.offer_ids:
                property.best_price = max(property.offer_ids.mapped('price'))
            else:
                property.best_price = 0.0

    # onchange methods
    @api.onchange('garden')
    def _onchange_garden(self):
        for property in self:
            if property.garden:
                property.garden_area = 10
                property.garden_orientation = 'north'
            else:
                property.garden_area = 0
                property.garden_orientation = False

    
    # Action methods
    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Canceled properties cannot be sold.")
            
            # Is there any accepted offer
            accepted_offer = self.offer_ids.filtered(lambda o: o.status == 'accepted')
            if not accepted_offer:
                raise UserError("You cannot sell a property without an accepted offer.")

            record.state = 'sold'

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be canceled.")
            record.state = 'canceled'

    def action_print_sale_report(self):
        # Generate the PDF report for this property.
        return self.env.ref('estate.report_property_offers').report_action(self)

    # Constraint methods
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_vs_expected_price(self):
        for record in self:
            # Skip check if selling_price is zero (no offer validated yet)
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue

            # Compare selling_price vs 90% of expected_price
            min_allowed = record.expected_price * 0.9
            if float_compare(record.selling_price, min_allowed, precision_rounding=0.01) < 0:
                raise ValidationError(
                    "The selling price cannot be lower than 90%% of the expected price!\n"
                    "Expected price: %.2f, Minimum allowed: %.2f, Selling price: %.2f" %
                    (record.expected_price, min_allowed, record.selling_price)
                )

    # Override methods
    @api.ondelete(at_uninstall=False)
    def _unlink_if_allowed(self):
        for record in self:
            if record.state not in ['sold', 'canceled']:
                raise UserError(
                    f"Cannot delete property '{record.name}' because it is in state '{record.state}'. "
                    "Only 'New' or 'Cancelled' properties can be deleted."
                )
