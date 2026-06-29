# -*- coding: utf-8 -*-
{
    "name": 'Mindora Demo 01 — Al Noor Live OS',
    "version": '19.0.1.0.0',
    "category": "Mindora/Demo",
    "summary": 'Anchor live demo: trading + installation + maintenance operating system',
    "description": """Anchor demo for Al Noor Integrated Solutions (Gulf B2B).
Lead -> Opportunity -> Quotation -> Sales Order -> Inventory/Purchase/Delivery -> Field Service -> Invoice -> Dashboard.
The most complete and stable scenario.""",
    "author": 'Mindora',
    "website": 'https://github.com/Mindora-Main/clarence-demo',
    "license": 'LGPL-3',
    "depends": [
        'mindora_demo_base',
        'crm',
        'sale_management',
        'sale_stock',
        'purchase',
        'purchase_stock',
        'stock',
        'stock_account',
        'stock_barcode',
        'account',
        'project',
        'hr',
        'hr_timesheet',
        'sale_timesheet',
        'industry_fsm',
        'industry_fsm_sale',
        'industry_fsm_stock',
        'helpdesk',
        'documents',
        'sign',
        'approvals',
        'spreadsheet_dashboard',
        'web_studio',
    ],
    "data": [

    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
