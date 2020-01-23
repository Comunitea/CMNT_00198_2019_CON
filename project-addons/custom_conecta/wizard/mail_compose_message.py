# Copyright (C) 2019 - Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api

class MailComposer(models.TransientModel):
    _inherit = 'mail.compose.message'

    company_id = fields.Many2one('res.company', string='Company', 
        change_default=True,
        readonly=True,
        default=lambda self: 
        self.env['res.company']._company_default_get('account.invoice'))