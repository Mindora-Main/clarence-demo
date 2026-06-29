# -*- coding: utf-8 -*-
{
    "name": 'Mindora Demo 04 — Core Warehouse',
    "version": '19.0.1.0.0',
    "category": "Mindora/Demo",
    "summary": 'Warehouse, barcode, replenishment, stock discipline',
    "description": """Core warehouse discipline: barcode, batch picking, replenishment, delivery, landed costs and expiry.""",
    "author": 'Mindora',
    "website": 'https://github.com/Mindora-Main/clarence-demo',
    "license": 'LGPL-3',
    "depends": [
        'mindora_demo_base',
        'sale_management',
        'sale_stock',
        'purchase',
        'purchase_stock',
        'stock',
        'stock_account',
        'stock_barcode',
        'stock_picking_batch',
        'delivery',
        'stock_landed_costs',
        'product_expiry',
    ],
    "data": [

    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
