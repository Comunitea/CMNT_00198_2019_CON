# Copyright (C) 2019 - Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ProjectTaskMaterial(models.Model):
    _inherit = "project.task.material"

    description = fields.Char('Description')