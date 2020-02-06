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
        
      
        return {
            'doc_ids': contracts.ids,
            'data': data,
            'docs': contracts,
            'report_data': report_data
        }
