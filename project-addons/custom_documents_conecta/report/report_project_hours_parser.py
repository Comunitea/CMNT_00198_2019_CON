# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api, _
from odoo.exceptions import UserError


class ReportProjectHours(models.AbstractModel):
    """
    Parser to get data of repòrt export catalog all
    """
    _name = 'report.custom_documents_conecta.report_project_hours'

    @api.model
    def _get_report_values(self, docids, data=None):
        # import ipdb; ipdb.set_trace()
        doc_id = self.env['project.project'].browse(docids)
        return {
            'doc_ids': docids,
            'data': data,
            'docs': doc_id,
            'eee': 'EEEE69'
        }
