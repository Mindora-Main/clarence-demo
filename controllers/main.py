from odoo import http


class ClarenceDemoController(http.Controller):
    """Main controller for Clarence demo."""

    @http.route('/clarence/demo', auth='public', website=True)
    def index(self, **kw):
        """Demo endpoint."""
        return http.request.render('clarence_demo.index', {})
