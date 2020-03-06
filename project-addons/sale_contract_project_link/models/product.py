# Copyright (C) 2019 - Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"


    service_tracking = fields.Selection(selection_add=[
        ('sale_project', 'Project setted in sale order')])
