# -*- coding: utf-8 -*-
# Copyright 2020-Today TechKhedut.
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
{
    'name': "Construction Management | Job Costing | Job Cost Sheet | Job Order | Construction Project | Project Planning | Job Contract | Construction Waste Management",
    'description': """
        - Construction Management
        - Job Costing 
        - Job Cost Sheet
        - Job Contract
        - Project Site
        - Construction Project Management
        - Job Budget Management
        - Construction Scrape Management
        - Construction Waste Management
    """,
    'summary': """Construction Management - Job Costing, Job Order, Job Cost Sheet, Project Site, & Scrape Order Management""",
    'version': "1.0",
    'author': 'TechKhedut Inc.',
    'company': 'TechKhedut Inc.',
    'maintainer': 'TechKhedut Inc.',
    'website': "https://www.techkhedut.com",
    'support': "info@techkhedut.com",
    'category': 'Industry',
    'depends': ['contacts', 'account', 'sale_management', 'purchase', 'hr', 'project', 'calendar', 'stock', 'mail',
                'hr_timesheet'],
    'data': [
        # security
        'security/ir.model.access.csv',
        # Data
        'data/sequence.xml',
        'data/construction_data.xml',
        # Wizard Views
        'wizard/construction_inspection_view.xml',
        # Views
        'views/assets.xml',
        'views/construction_details_view.xml',
        'views/construction_site_details.xml',
        'views/construction_equipment.xml',
        'views/construction_labour_inherit.xml',
        'views/construction_employee_role.xml',
        'views/construction_employee_inherit.xml',
        'views/document_type.xml',
        'views/construction_purchase_order.xml',
        'views/construction_project_inherit_view.xml',
        'views/construction_insurance_risk.xml',
        'views/scrap_order_view.xml',
        'views/construction_configuration.xml',
        'views/job_costing_view.xml',
        'views/job_type_view.xml',
        # menus
        'views/menus.xml',
        # Report views
        'report/construction_details_report.xml',
        'report/job_costing_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'tk_construction_management/static/src/xml/template.xml',
            'tk_construction_management/static/src/css/lib/dashboard.css',
            'tk_construction_management/static/src/css/lib/style.css',
            'tk_construction_management/static/src/css/style.scss',
            'tk_construction_management/static/src/js/lib/apexcharts.js',
            'tk_construction_management/static/src/js/construction.js',
        ],
    },
    'images': ['static/description/cover.gif'],
    'license': 'OPL-1',
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 299,
    'currency': 'USD',
}
