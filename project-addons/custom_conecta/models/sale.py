# Copyright (C) 2019 - Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    supp_ref = fields.Char('Supplier Reference')


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        """
        Bug al tener sale_oprder_type y saler_oprder_revision, la secuencia
        debe ser la del tipo de venta al duplicar
        """
        if default is None:
            default = {}
        if self.type_id:
            default['name'] = self.type_id.sequence_id.next_by_id()
            default['revision_number'] = 0
            default['unrevisioned_name'] = default['name']
        return super(SaleOrder, self).copy(default=default)