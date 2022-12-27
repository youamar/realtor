from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    apartment_ids = fields.One2many('realtor.apartment', 'best_offer_buyer', string='Apartments')
    password = fields.Char(string='Password')