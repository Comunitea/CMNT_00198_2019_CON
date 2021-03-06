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

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        """
        Al entrar aqui desde el .new del modulo sale en _prepare_invoice
        odoo no lo crea con compañía y el mñodulo de account_payment_partner
        no será capaz de obtener el modo de pago correcto.
        Esto también pasa en contratos, solo que ahí tengo pisado el
        _prepare_invoice entero. Que no es lo ideal.
        """
        if not self.company_id and self._context.get('active_model') and  \
            self._context.get('active_model') == 'sale.order':
            sale = self.env['sale.order'].browse(self._context['active_id'])
            self.company_id = sale.company_id
        res = super(AccountInvoice, self)._onchange_partner_id()
        
        return res

class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    customer_id = fields.Many2one('res.partner', 'Cliente')
