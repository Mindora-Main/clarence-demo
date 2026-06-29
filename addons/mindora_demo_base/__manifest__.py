# -*- coding: utf-8 -*-
{
    "name": 'Mindora Demo — Base',
    "version": '19.0.1.0.0',
    "category": "Mindora/Demo",
    "summary": 'Shared base for the Mindora x Clarence Odoo 19 demo lab',
    "description": """Lightweight shared base for all Mindora demo branches.
Provides shared demo tags and reference markers.
No invasive changes; data is idempotent and marked noupdate.""",
    "author": 'Mindora',
    "website": 'https://github.com/Mindora-Main/clarence-demo',
    "license": 'LGPL-3',
    "depends": [
        'base',
        'mail',
        'contacts',
    ],
    "data": [
        'data/mindora_demo_tags.xml',
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
