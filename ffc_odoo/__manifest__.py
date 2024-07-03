# -*- coding: utf-8 -*-
{
    'name': "ffc_odoo",

    'summary': "website issues for ffc",

    'description': """
    website issues for ffc
    """,

    'author': "DASARI RAMMOHAN",
    'website': " ",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services/services',
    'version': '1.o',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'assets': {
        'web.assets_frontend': [
            'ffc_odoo/static/src/js/website_hr_applicant_form.js'
        ],},

'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}


