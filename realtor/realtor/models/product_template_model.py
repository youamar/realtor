from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    apartment = fields.Many2one('realtor.apartment', string='Apartment',ondelete='set null')
    offerer = fields.Many2one('res.partner', string='Apartment',ondelete='set null')