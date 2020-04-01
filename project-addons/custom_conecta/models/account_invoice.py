# Copyright (C) 2019 - Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    # Esto provoca error al crear factura proveedor
    # @api.model
    # def _default_journal(self):
    #     res = super()._default_journal()
    #     inv_type = self._context.get('type', 'out_invoice')
    #     if inv_type in ('in_invoice', 'in_refund'):
    #         return False
    #     return res
    
    # @api.model
    # def _default_currency(self):
    #     journal = self._default_journal()
    #     res = False
    #     if journal:
    #         res = journal.currency_id or journal.company_id.currency_id
    #     else:
    #         self.env.user.company_id.currency_id
    #     return res
        