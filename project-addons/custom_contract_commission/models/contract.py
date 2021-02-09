# Copyright (C) 2020 - Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _
from odoo.addons import decimal_precision as dp



class ContractLine(models.Model):
    _inherit = [
        "contract.line",
        "sale.commission.mixin"
    ]

    _name = "contract.line"

    agents = fields.One2many(
        string="Agents & commissions",
        comodel_name="contract.line.agent",
    )
    purchase_price = fields.Float(
        digits=dp.get_precision('Product Price'),
        string='Cost',
    )

    @api.multi
    def _prepare_invoice_line(self, invoice_id=False, invoice_values=False):
        """
        Propagate agents from contract line to invoice
        """
        vals = super()._prepare_invoice_line(invoice_id=invoice_id, 
                                             invoice_values=invoice_values)
        vals['agents'] = [
            (0, 0, {'agent': x.agent.id,
                    'commission': x.commission.id}) for x in self.agents]
        vals['purchase_price'] = self.purchase_price
        return vals

  

class ContractLineAgent(models.Model):
    _inherit = "sale.commission.line.mixin"
    _name = "contract.line.agent"

    object_id = fields.Many2one(
        comodel_name="contract.line",
    )
    currency_id = fields.Many2one(
        related="object_id.contract_id.company_id.currency_id",
        readonly=True,
    )

    @api.depends('object_id.price_subtotal')
    def _compute_amount(self):
        for line in self:
            contract_line = line.object_id
            line.amount = line._get_commission_amount(
                line.commission, contract_line.price_subtotal,
                contract_line.product_id, contract_line.quantity,
            )
