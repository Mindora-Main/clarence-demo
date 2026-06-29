# -*- coding: utf-8 -*-
{
    "name": 'Mindora Demo 10 — MRP',
    "version": '19.0.1.0.0',
    "category": "Mindora/Demo",
    "summary": 'Factory manufacturing: BoM, MO, work orders, quality, maintenance',
    "description": """Factory manufacturing (L2): bills of materials, manufacturing orders, work orders, quality control and maintenance.""",
    "author": 'Mindora',
    "website": 'https://github.com/Mindora-Main/clarence-demo',
    "license": 'LGPL-3',
    "depends": [
        'mindora_demo_base',
        'mrp',
        'mrp_workorder',
        'mrp_account',
        'stock',
        'stock_account',
        'purchase',
        'purchase_stock',
        'sale_management',
        'sale_stock',
        'quality_control',
        'quality_mrp',
        'maintenance',
        'mrp_maintenance',
        'account',
    ],
    "data": [

    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
