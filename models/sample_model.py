from odoo import models, fields


class SampleModel(models.Model):
    """Sample model for demonstration purposes."""

    _name = 'clarence.demo.sample'
    _description = 'Sample Model for Clarence Demo'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Name',
        required=True,
        tracking=True,
    )
    description = fields.Text(
        string='Description',
        tracking=True,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    created_date = fields.Datetime(
        string='Created Date',
        default=fields.Datetime.now,
        readonly=True,
    )
