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
        data_dic = {
            'date_start': self.date_start,
            'date_end': self.date_start,
        }
        # Esto devolverá el report pasando por el parser
        return {
            'type': 'ir.actions.report',
            'report_name': report_name,
            'report_type': 'qweb-pdf',
            'data': data_dic,
            }
        return