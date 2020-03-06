# Copyright (C) 2019 - Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    extra_project_id = fields.Many2one('project.project', 'Extra project')

    @api.multi
    def action_confirm(self):
        """ If we have a contract in the order, set it up """
        res = super().action_confirm()
        for order in self:
            contracts = (
                self.env['contract.line']
                .search([('sale_order_line_id', 'in', order.order_line.ids)])
                .mapped('contract_id')
            )
            projects = self.project_ids
            if projects and projects[0].analytic_account_id and contracts:
                project = projects[0]
                contracts.write(
                    {'group_id': projects[0].analytic_account_id.id,
                     'project_id':project.id
                    })
        return res



class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def _timesheet_service_generation(self):
        res = super()._timesheet_service_generation()
        project = self[0].order_id.extra_project_id
        if not project:
            return res

        so_line_sale_global_project = self.filtered(
            lambda sol: sol.is_service and 
            sol.product_id.service_tracking == 'sale_project')
        
        for line in so_line_sale_global_project:
            if not line.task_id:
                line._timesheet_create_task(project=project)
        
        aa_id = project.analytic_account_id.id
        if aa_id:
            self[0].order_id.write({'analytic_account_id': aa_id})
        return res
