
# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api


class RecomputeCommissionWzd(models.TransientModel):

    _name = 'recompute.commission.wzd'

    @api.multi
    def recompute_commission(self):
        """
        Reclacula la comisionm por si han modificado el coste y con ello
        el margen
        tienen un menu de lineas de factura al vuelo para mopdificar el coste
        luego esto recalculará
        """
        self.ensure_one()
        active_ids = self._context.get('active_ids')
        invoices = self.env['account.invoice'].browse(active_ids)
        # if invoices:
            # invoices.recompute_lines_agents()
        for inv in invoices:
            for agent_line in inv.invoice_line_ids.mapped('agents'):
                agent_line._compute_amount()
        return
