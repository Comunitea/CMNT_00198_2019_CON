# Copyright 2014-2018 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, exceptions, fields, models, _



class SettlementLine(models.Model):
    _inherit = "sale.commission.settlement.line"

    partner_id = fields.Many2one(
        comodel_name='res.partner', store=False, string="Customer",
        related='invoice.partner_id')