# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api, _, fields
from odoo.exceptions import UserError


class ReportcontractHours(models.AbstractModel):
    """
    Parser to get data of repòrt export catalog all
    """
    _name = 'report.custom_documents_conecta.report_sla'

    @api.model
    def _get_report_values(self, docids, data=None):
        contract_ids = data.get('contract_ids')
        contracts = self.env['contract.contract'].browse(contract_ids)

        date_start = ''
        date_end = ''
        domain = [('sla_state', '!=', False)]
        if data.get('date_start'):
            domain.append(('issue_date', '>=', data['date_start']))
            date_start = fields.Date.from_string(data['date_start']).strftime('%d-%m-%Y')
        if data.get('date_end'):
            domain.append(('issue_date', '<=', data['date_end']))
            date_end = fields.Date.from_string(data['date_end']).strftime('%d-%m-%Y')

        report_data = {}
        for contract in contracts:
            report_data[contract] = {
                'date_start': date_start,
                'date_end': date_end,
                'n_issues': 0,
                'n_archived': 0,
                'archived_percent': 0.0,
                'fail_tasks': []
            }

            if not contract.project_id:
                continue

            project = contract.project_id
            domain.append(('project_id', '=', project.id))
            tasks = self.env['project.task'].search(domain)
            if not tasks:
                continue
            archived_tasks = tasks.filtered(lambda t: t.sla_state == '1')
            no_archived_tasks = tasks.filtered(lambda t: t.sla_state != '1')

            num_total = len(tasks)
            num_archived = len(archived_tasks)
            percent = (num_archived / num_total) * 100.0
            report_data[contract].update({
                'n_issues': num_total,
                'n_archived': num_archived,
                'archived_percent': percent
            })

            for t in no_archived_tasks:
                response = 'No cumplido'
                resolution = 'No cumplido'
                for sla in t.sla_control_ids:
                    if 'Respuesta' in sla.sla_line_id.sla_id.name and \
                            sla.sla_state == '1':
                        response = 'Cumplido'
                    if 'Resolución' in sla.sla_line_id.sla_id.name and \
                            sla.sla_state == '1':
                        response = 'Cumplido'

                dic = {
                    'id': t.id,
                    'response': 'No cumplido',
                    'resolution': 'No cumplido'
                }
                report_data[contract]['fail_tasks'].append(dic)

      
        return {
            'doc_ids': contracts.ids,
            'data': data,
            'docs': contracts,
            'report_data': report_data
        }
