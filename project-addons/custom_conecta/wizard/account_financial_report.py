# Copyright (C) 2019 - Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class AbstractWizard(models.AbstractModel):
    _inherit = 'account_financial_report_abstract_wizard'
    _description = 'Abstract Wizard'

    def _get_partner_ids_domain(self):
        res = super()._get_partner_ids_domain()
        return [
            ('parent_id', '=', False),
            ('is_company', '=', True),
        ]