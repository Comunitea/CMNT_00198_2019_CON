# Copyright (C) 2019 - Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api



class Contract(models.Model):
    _inherit = "contract.contract"

    signature = fields.Binary("Customer signature")
    warn_percent = fields.Float(
        "Warning limit percent", default=0.7)
    quantity_max = fields.Float(
        'Scheduled Time')
    hours_quantity = fields.Float(
        'Total Worked Time', related='project_id.hours_quantity')
    remaining_hours = fields.Float(
        'Remaining Time', related='project_id.remaining_hours')
    total_discount = fields.Float(
        'Total DIscounted Time', related='project_id.total_discount')
    period_date_start = fields.Datetime('Period Date Start',
        related='project_id.period_date_start')
    period_date_end = fields.Datetime('Period Date End',
        related='project_id.period_date_end')
    

    @api.multi
    def check_limit(self):
        flag = False
        for contract in self:
            if contract.quantity_max:
                if contract.remaining_hours <= \
                        contract.quantity_max * (1 - contract.warn_percent) and \
                        contract.warn_percent > 0:
                    flag = True
        return flag
    
    @api.multi
    def _get_project_vals(self):
        res = super()._get_project_vals()
        res.update(quantity_max=self.quantity_max)
        self.ensure_one()
        res = {
            'name': self.name,
            'partner_id': self.partner_id.id,
            'allow_timesheets': True,  # To create analytic account id
            'company_id': self.company_id.id,
            'quantity_max': self.quantity_max,
        }
        return res
    
    def write(self, vals):
        res = super().write(vals)
        if vals.get('quantity_max'):
            qm = vals['quantity_max']
            if self.project_id and self.project_id.quantity_max != qm:
                self.project_id.write({
                    'quantity_max': qm})
        return res

