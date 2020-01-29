# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class PrintProjectHoursWzd(models.TransientModel):

    _name = 'print.project.hours.wzd'

    date_start = fields.Date('Date Start')
    date_end = fields.Date('Date End')

    def print_report(self):
        report_name = 'custom_documents_conecta.report_project_hours'
        active_ids = self._context.get('active_ids')
        projects = self.env['project.project'].browse(active_ids)
        data_dic = {
            'date_start': self.date_start,
            'date_end': self.date_start,
            'project_ids': active_ids
        }
        # import ipdb; ipdb.set_trace()

        # domain = [('task_id', '!=', False)]
        # if self.date_start:
        #     domain.append(('date', '>=', self.date_start))
        # if self.date_end:
        #     domain.append(('date', '<=', self.date_end))

        # report_data = {}
        # for project in projects:
        #     p_id = project.id
        #     report_data[p_id] = { 'project': project,
        #         'issues': {}, 'tasks': {}, 'ch': project.quantity_max,
        #         'wh': 0.0, 'dh': 0.0, 'eh': 0.0, 'th': 0.0,
        #         'ref': project.contract_id and project.contract_id.code
        #         or ''
        #     }
        #     domain.append(('project_id', '=', project.id))
        #     a_lines = self.env['account.analytic.line'].search(domain)
            
        #     for line in a_lines:
        #         task_type = 'issues'
        #         if not line.task_id.is_issue:
        #             task_type = 'tasks'
        #         if line.task_id not in report_data[p_id][task_type]:
        #             task = line.task_id
        #             report_data[p_id][task_type][task.id] = {
        #                 'task': task,
        #                 'lines': [],
        #                 # 'num': line.task_id.id,
        #                 # 'state': line.task_id.stage_id.name,
        #                 # 'notice_person': line.task_id.notice_person,
        #                 # 'description':  line.task_id.description,
        #                 'total': 0.0
        #             }
        #         report_data[p_id][task_type][task.id]['lines'] += \
        #             line
        #         report_data[p_id][task_type][task.id]['total'] += \
        #             line.unit_amount - line.discount
        #         report_data[p_id]['wh'] += line.unit_amount
        #         report_data[p_id]['dh'] += line.discount
            
        #     wh = report_data[p_id]['wh']
        #     dh = report_data[p_id]['dh']
        #     th = wh - dh
        #     report_data[p_id]['th'] = th
        #     if th > project.quantity_max:
        #         report_data[p_id]['eh'] = th - project.quantity_max

        # # import ipdb; ipdb.set_trace()
        # data_dic['report_data'] = report_data
        # Esto devolverá el report pasando por el parser
        return {
            'type': 'ir.actions.report',
            'report_name': report_name,
            'report_type': 'qweb-pdf',
            'data': data_dic,
        }
