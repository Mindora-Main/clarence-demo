{
    'name': 'Clarence Demo Module',
    'version': '1.0.0',
    'category': 'Tools',
    'summary': 'Demo module for Clarence integration',
    'description': """
        This module provides the infrastructure and base components
        for Clarence demonstration and integration.
    """,
    'author': 'Mindora',
    'website': 'https://github.com/Mindora-Main/clarence-demo',
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
    'depends': [
        'base',
    ],
    'data': [
        # security
        'security/ir.model.access.csv',
        # views
        'views/views.xml',
    ],
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
    'images': [],
    'sequence': 1,
}
