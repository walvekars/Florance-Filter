# -*- coding: utf-8 -*-
{
    'name': "google_chat",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',  'mail', 'im_livechat', 'website', 'web', 'portal','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'views/views.xml',
        'views/templates.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
        # 'views/templates.xml',

    ],

    'assets': {
        'web.assets_frontend': [
            'google_chat/static/js/main.js',
            # 'google_chat/static/src/js/MainComponent.js',
            # 'google_chat/static/src/js/Popup.js',
        ],
        'web.assets_qweb': [
            # 'google_chat/views/templates.xml',
        ],
    },
}

