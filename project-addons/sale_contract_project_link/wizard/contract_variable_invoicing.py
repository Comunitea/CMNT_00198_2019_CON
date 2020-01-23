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
    def make_invoices(self):
        res = False
        # import ipdb; ipdb.set_trace()
        self.ensure_one()
        active_ids = self._context.get('active_ids')
        ctx = self._context.copy()
        ctx.update(no_recurring_mode=True)
        contracts = self.env['contract.contract'].\
            with_context(ctx).browse(active_ids)
        
        if any([not c.no_recurring for c in contracts]):
            raise UserError(
            _('You can not invoice recurrent contracts from this wizard'))
        
        if contracts:
            contracts.mapped('contract_line_ids').write(
                {'recurring_next_date': self.invoice_to})
            invoices = contracts._recurring_create_invoice()
            
            # Actualizar solo la ultima fecha de factura a las que tienen 
            # factura asociada
            contracts2update = self.env['account.invoice.line']
            for contract in contracts:
                if contract._get_related_invoices():
                    contracts2update += contract

            if contracts2update:
                contracts2update.mapped('contract_line_ids').write(
                    {'last_date_invoiced': self.invoice_to,
                     'recurring_next_date':  self.invoice_to + 
                     relativedelta(1)
                    })
        return
