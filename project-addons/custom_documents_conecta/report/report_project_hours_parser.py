# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api, _, fields
from odoo.exceptions import UserError


class ReportProjectHours(models.AbstractModel):
    """
    Parser to get data of repòrt export catalog all
    """
    _name = 'report.custom_documents_conecta.report_project_hours'

    @api.model
    def _get_report_values(self, docids, data=None):
        project_ids = data.get('project_ids')
        projects = self.env['project.project'].browse(project_ids)

        domain = [('task_id', '!=', False)]
        date_start = ''
        date_end = ''
        if data.get('date_start'):
            domain.append(('date', '>=', data['date_start']))
            date_start = fields.Date.from_string(data['date_start']).strftime('%d-%m-%Y')
        if data.get('date_end'):
            domain.append(('date', '<=', data['date_end']))
            date_end = fields.Date.from_string(data['date_end']).strftime('%d-%m-%Y')

        report_data = {}
        for project in projects:
            p_id = project
            report_data[project] = {
                'issues': {}, 'tasks': {}, 'ch': project.quantity_max,
                'wh': 0.0, 'dh': 0.0, 'eh': 0.0, 'th': 0.0,
                'ref': project.contract_id and project.contract_id.code
                or '',
                'date_start': date_start,
                'date_end': date_end
            }
            domain.append(('project_id', '=', project.id))
            a_lines = self.env['account.analytic.line'].search(domain)
            
            for line in a_lines:
                task_type = 'issues'
                if not line.task_id.is_issue:
                    task_type = 'tasks'
                if line.task_id not in report_data[project][task_type]:
                    task = line.task_id
                    report_data[p_id][task_type][task] = {
                        'lines': [],
                        'total': 0.0
                    }
                report_data[p_id][task_type][task]['lines'] += \
                    line
                report_data[p_id][task_type][task]['total'] += \
                    line.unit_amount - line.discount
                report_data[p_id]['wh'] += line.unit_amount
                report_data[p_id]['dh'] += line.discount
            
            wh = report_data[p_id]['wh']
            dh = report_data[p_id]['dh']
            th = wh - dh
            report_data[p_id]['th'] = th
            if th > project.quantity_max:
                report_data[p_id]['eh'] = th - project.quantity_max
        
        return {
            'doc_ids': project.ids,
            'data': data,
            'docs': projects,
            'report_data': report_data
        }
