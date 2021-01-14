# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = ['project.project']

    @api.multi
    def _hours_quantity(self):
        for project in self:
            hours_quantity = 0.0
            remaing_hours = 0.0
            discounted_hours = 0.0

            domain = [('project_id', '=', project.id), ('task_id', '!=', False)]

            if project.period_date_start:
                domain += [
                    ('date_start', '>=', 
                     project.period_date_start.strftime('%d-%m-%Y'))]
            if project.period_date_start:
                domain += [
                    ('date_end', '<=', project.period_date_end.strftime('%d-%m-%Y'))]
            a_lines = self.env['account.analytic.line'].search(domain)
            hours_quantity = \
                round(sum(a_lines.mapped('unit_amount')), 2)
            hours_discount = \
                round(sum(a_lines.mapped('discount')), 2)
            project.hours_quantity = hours_quantity
            project.remaining_hours = \
                project.quantity_max - hours_quantity
            project.total_discount = hours_discount
    
    @api.multi
    def _get_discounted(self):
        for project in self:
            domain = [
                ('task_id', 'in', project.task_ids.ids)]
            lines = self.env['account.analytic.line'].search(domain)
            tot_disc = round(sum(lines.mapped('discount')), 2)
            project.total_discount = tot_disc
    
    period_date_start = fields.Datetime('Period Date Start')
    period_date_end = fields.Datetime('Period Date End')
    quantity_max = fields.Float('Scheduled Time')
    hours_quantity = fields.Float(
        'Total Worked Time', compute='_hours_quantity')
    remaining_hours = fields.Float(
        'Remaining Time', compute='_hours_quantity')
    total_discount = fields.Float(
        'Total Discounted Time', compute='_get_discounted')
    
    def write(self, vals):
        res = super().write(vals)
        if vals.get('quantity_max'):
            qm = vals['quantity_max']
            if self.contract_id and self.contract_id.quantity_max != qm:
                self.contract_id.write({
                    'quantity_max': qm})
        return res

    
