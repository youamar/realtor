# -*- coding: utf-8 -*-
# from odoo import http


# class Realtor(http.Controller):
#     @http.route('/realtor/realtor/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/realtor/realtor/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('realtor.listing', {
#             'root': '/realtor/realtor',
#             'objects': http.request.env['realtor.realtor'].search([]),
#         })

#     @http.route('/realtor/realtor/objects/<model("realtor.realtor"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('realtor.object', {
#             'object': obj
#         })
