# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class ContractVariableInvoicingWzd(models.TransientModel):

    _name = 'contract.variable.invoicing.wzd'

    invoice_to = fields.Date('Invoice To', default=fields.Date.today(), 
                             required=True)
    
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


    @api.multi
    def make_invoices(self):
        """
        Facturar horas de manera variable
        """
        res = False
        self.ensure_one()
        active_ids = self._context.get('active_ids')
        ctx = self._context.copy()
        ctx.update(no_recurring_mode=True)
        contracts = self.env['contract.contract'].\
            with_context(ctx).browse(active_ids)
        
        if any([not c.no_recurring for c in contracts]):
            raise UserError(
            _('You can not invoice recurrent contracts from this wizard'))
        
        # Fecha de creación de factura equivalente al asistente.
        # Para aquellos facturados se actualizarán despues sus fechas en
        # _finalize_invoice_creation
        contracts.mapped('contract_line_ids').write(
            {'recurring_next_date': self.invoice_to})
        
        invoices = contracts._recurring_create_invoice()
        if invoices:
            return self.show_invoices(invoices)
        return
