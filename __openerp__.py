# -*- coding: utf-8 -*-
{
    'name': "Riesgo Online",

    'summary': """
        Modulo base para conectar con buro Riesgoonline.""",

    'description': """

    """,

    'author': "Librasoft",
    'website': "https://libra-soft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'finance',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'financiera_base', 'financiera_prestamos',
								'financiera_cobranza_mora'],

    # always loaded
    'data': [
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/buro_rol_configuracion.xml',
				'views/buro_rol_cda.xml',
        'views/buro_rol_informe.xml',
        'views/extends_res_company.xml',
        # 'data/defaultdata.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}