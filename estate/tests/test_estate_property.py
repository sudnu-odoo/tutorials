from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class TestEstate(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Property = cls.env['estate.property']
        cls.Offer = cls.env['estate.property.offer']

        cls.partner = cls.env['res.partner'].create({
            'name': 'Test Buyer Partner'
        })

        # Create a property for testing
        cls.property = cls.Property.create({
            'name': 'Beautiful Villa',
            'expected_price': 500000,
        })

    def test_create_offer_for_sold_property(self):
        """User should not be able to create an offer for a sold property."""
        # Simulate property being sold
        self.property.state = 'sold'

        # Attempt to create offer
        with self.assertRaises(UserError):
            self.Offer.create({
                'price': 100000,
                'partner_id': self.partner.id,
                'property_id': self.property.id,
            })

    def test_sell_property_without_accepted_offer(self):
        """Cannot sell a property with no accepted offer."""
        with self.assertRaises(UserError):
            self.property.action_sold()

    def test_sell_property_with_accepted_offer(self):
        """If there's an accepted offer, property should become sold."""
        # Create an accepted offer
        offer = self.Offer.create({
            'price': 500000,
            'partner_id': self.partner.id,
            'property_id': self.property.id,
        })
        offer.status = 'accepted'

        # Call the action
        self.property.action_sold()

        # Check property state
        self.assertEqual(self.property.state, 'sold', "Property should be marked as sold")

    def test_garden_reset(self):
        """Garden Area and Orientation must reset when garden is unchecked."""

        self.property.write({
            'garden': True,
            'garden_area': 10,
            'garden_orientation': 'north',
        })
        
        self.property.garden = False 

        self.property._onchange_garden() 
        
        self.assertEqual(self.property.garden, False, "Garden checkbox should be unchecked.")
        self.assertEqual(self.property.garden_area, 0, "Garden Area must be reset to 0.")
        self.assertFalse(self.property.garden_orientation, "Garden Orientation must be reset to False.")
