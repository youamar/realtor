# -*- coding: utf-8 -*-
{
    'name': "Realtor Application",

    'summary': """
        Real estate management.""",

    'description': """
        Manage real estate properties and their sales.""",

    'author': "Yahya Ouamar",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/realtor_menu.xml',
        'views/realtor_view.xml',
        'views/product_template_view.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'application': True,
}
