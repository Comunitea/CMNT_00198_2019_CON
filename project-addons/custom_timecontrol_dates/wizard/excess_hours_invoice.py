# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class ExcessHoursInvoiceWzd(models.TransientModel):

    _name = 'excess.hours.invoice.wzd'

    @api.multi
    def _get_journal(self):
        import ipdb; ipdb.set_trace()
        return self.env['account.journal'].search([('code', '=', 'T')], limit=1)

    product_id = fields.Many2one('product.product', 'Product to invoice')
    journal_id = fields.Many2one(
        'account.journal',required=True, default=_get_journal)
    
    @api.multi
    def show_invoices(self, invoices):
        self.ensure_one()
        tree_view_ref = ('account.invoice_tree_with_onboarding')
        form_view_ref = ('account.invoice_form')
        tree_view = self.env.ref(tree_view_ref, raise_if_not_found=False)
        form_view = self.env.ref(form_view_ref, raise_if_not_found=False)
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'res_model': 'account.invoice',
            'view_type': 'form',
            'view_mode': 'tree,kanban,form,calendar,pivot,graph,activity',
            'domain': [('id', 'in', invoices.ids)],
        }
        if tree_view and form_view:
            action['views'] = [(tree_view.id, 'tree'), (form_view.id, 'form')]
        return action
    
    @api.model
    def get_invoice_vals(self, contract):
        invoice_vals = {
            'partner_id': contract.invoice_partner_id.id,
            'type': 'out_invoice',
            'journal_id': contract.journal_id.id,
            'origin': contract.name,
            'company_id': contract.company_id.id,
            'user_id': contract.user_id.id,
            'account_id': 
            contract.partner_id.property_account_receivable_id.id,

        }
        if contract.payment_term_id:
            invoice_vals['payment_term_id'] = contract.payment_term_id.id
        if contract.fiscal_position_id:
            invoice_vals['fiscal_position_id'] = contract.fiscal_position_id.id
        if contract.pricelist_id:
            invoice_vals['pricelist_id'] = contract.pricelist_id.id
        return invoice_vals
    
    @api.model
    def get_invoice_line_vals(self, contract, inv):
        price_unit = 0.0
        qty = contract.remaining_hours * -1
        pronduct = False
        if self.product_id:
            product = self.product_id.with_context(
                quantity=qty,
                pricelist=contract.pricelist_id.id,
                partner=contract.invoice_partner_id.id,
                # date=fields.Date.context_today(),
            )
            price_unit = product.price

        line_vals = {
            'name': 'Excesos del contrato ' + contract.name,
            # 'partner_id': contract.invoice_partner_id.id,
            'product_id': product.id or False,
            'quantity': qty,
            # 'price_unit': price_unit,
            'invoice_id': inv.id,
            'account_id': 
            contract.partner_id.property_account_receivable_id.id,
        }
        invoice_line = self.env['account.invoice.line'].new(line_vals)
        invoice_line._onchange_product_id()
        invoice_line_vals = invoice_line._convert_to_write(invoice_line._cache)
        invoice_line_vals['price_unit'] = price_unit
        return invoice_line_vals

    @api.multi
    def make_invoice(self):
        """
        Facturar horas de manera variable
        """
        created_invoices = self.env['account.invoice']

        active_ids = self._context.get('active_ids')
    
        contracts = self.env['contract.contract'].browse(active_ids)
        for contract in contracts:
            if contract.remaining_hours >= 0:
                continue

            vals = self.get_invoice_vals(contract)
            invoice = self.env['account.invoice'].create(vals)
            created_invoices += invoice

            line_vals = self.get_invoice_line_vals(contract, invoice)
            self.env['account.invoice.line'].create(line_vals)
        
        if created_invoices:
            return self.show_invoices(created_invoices)
        return
