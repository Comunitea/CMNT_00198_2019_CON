# Copyright (C) 2019 - Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ContractLine(models.Model):
    _inherit = "contract.line"

    partner_id = fields.Many2one(
        'res.partner', related='contract_id.partner_id', store=True)