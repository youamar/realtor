from odoo import models, fields, api

from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)

class RealtorApartment(models.Model):
    _name = 'realtor.apartment'
    
    name = fields.Char(string='Name', required=True, unique=True)
    description = fields.Text(string='Description')
    apartment_picture = fields.Binary(string='Apartment Picture', widget='image')
    availability_date = fields.Date(string='Availability Date', required=True, default=fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(string='Expected Price', required=True)
    apartment_area = fields.Float(string='Apartment Area', required=True)
    terrace_area = fields.Float(string='Terrace Area', required=True)
    total_area = fields.Float(compute='_compute_total_area', string='Total Area')
    best_offer_buyer = fields.Many2one('res.partner', string='Best Offer Buyer')
    best_offer_price = fields.Float(string='Best Offer Price')
    
    @api.depends('apartment_area', 'terrace_area')
    def _compute_total_area(self):
        for apartment in self:
            apartment.total_area = apartment.apartment_area + apartment.terrace_area
            
    @api.constrains('availability_date')
    def _check_availability_date(self):
        for apartment in self:
            if apartment.availability_date < fields.Date.today() + relativedelta(months=3):
                raise ValidationError("The availability date must be at least 3 months after the creation of the apartment")

    _sql_constraints = [
        ('expected_price_check',
            'CHECK(expected_price > 0)',
            'The expected price should be above 0'),
        ('apartment_area_check',
            'CHECK(apartment_area > 0)',
            'The apartment area should be above 0'),
        ('terrace_area_check',
            'CHECK(terrace_area >= 0)',
            'The terrace area should be positive'),
        ('best_offer_price_check',
            'CHECK(best_offer_price >= expected_price * 90 / 100)',
            'The best offer price should be at least 90% of the expected price')
    ]