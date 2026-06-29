# -*- coding: utf-8 -*-
{
    "name": 'Mindora Demo 00 — Base Universal',
    "version": '19.0.1.0.0',
    "category": "Mindora/Demo",
    "summary": 'Universal reusable base environment for Mindora demos',
    "description": """Universal baseline: contacts, CRM, sales, purchase, stock, accounting, project, HR, timesheets and Studio.
Use as the reusable starting point for any Mindora demo branch.""",
    "author": 'Mindora',
    "website": 'https://github.com/Mindora-Main/clarence-demo',
    "license": 'LGPL-3',
    "depends": [
        'mindora_demo_base',
        'base_setup',
        'contacts',
        'mail',
        'calendar',
        'crm',
        'sale_management',
        'account',
        'purchase',
        'stock',
        'project',
        'hr',
        'hr_timesheet',
        'web_studio',
    ],
    "data": [

    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
