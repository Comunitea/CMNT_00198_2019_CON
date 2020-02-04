# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta


class PrintProjectHoursWzd(models.TransientModel):

    _name = 'print.project.hours.wzd'

    date_start = fields.Date('Date Start')
    date_end = fields.Date('Date End')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_id = self.env.context.get('active_id', False)
        project = self.env['project.project'].browse(active_id)
        res['date_start'] = project.period_date_start
        res['date_end'] = project.period_date_end
        return res

    def print_report(self):
        report_name = 'custom_documents_conecta.report_project_hours'
        active_ids = self._context.get('active_ids')
        projects = self.env['project.project'].browse(active_ids)
        data_dic = {
            'date_start': self.date_start,
            'date_end': self.date_end,
            'project_ids': active_ids
        }
        # Esto devolverá el report pasando por el parser
        return {
            'type': 'ir.actions.report',
            'report_name': report_name,
            'report_type': 'qweb-pdf',
            'data': data_dic,
        }
