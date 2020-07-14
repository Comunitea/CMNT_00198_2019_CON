# Copyright (C) 2019 - Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    def _prepare_invoice_line_from_po_line(self, line):
        res = super()._prepare_invoice_line_from_po_line(line)
        if line.customer_id:
            res['customer_id'] = line.customer_id.id
        return res


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    customer_id = fields.Many2one('res.partner', 'Cliente')
