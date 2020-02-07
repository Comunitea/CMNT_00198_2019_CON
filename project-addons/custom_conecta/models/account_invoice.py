from odoo import models, api, fields
from odoo.tools import formatLang, format_date

    
class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def _notify_get_groups(self, message, groups):
        """
        Que no salga el botón de ver factura nunca.
        """
        groups = super(AccountInvoice, self)._notify_get_groups(message, groups)

        if self.state not in ('draft', 'cancel'):
            for group_name, group_method, group_data in groups:
                group_data['has_button_access'] = False

        return groups