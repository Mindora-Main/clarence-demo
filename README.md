# Clarence Demo Module

Odoo module providing infrastructure and base components for Clarence demonstration and integration.

## Installation

1. Clone the repository or add this module to your Odoo addons path
2. Install the module through Odoo's Apps menu

## Features

- Sample model with tracking and messaging
- Basic controller for HTTP routing
- Menu structure and views
- Security configuration

## Structure

```
clairence-demo/
├── __init__.py
├── __manifest__.py
├── README.md
├── models/
│   ├── __init__.py
│   └── sample_model.py
├── controllers/
│   ├── __init__.py
│   └── main.py
├── security/
│   └── ir.model.access.csv
└── views/
    └── views.xml
```

## License

LGPL-3
