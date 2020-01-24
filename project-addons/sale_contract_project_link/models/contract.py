# Copyright (C) 2019 - Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError
import datetime
from dateutil.relativedelta import relativedelta



class ContractContract(models.Model):
    _inherit = "contract.contract"

    def _compute_task_issue_count(self):
        for contract in self:
            domain = [
                ('contract_id', '=', contract.id), ('is_issue', '=', True)]
            task_count = self.env['project.task'].search_count(domain)
            contract.task_issue_count = task_count

    project_id = fields.Many2one('project.project', string='Project')
    task_issue_count = fields.Integer(
        compute='_compute_task_issue_count', string="Task Count")
    description = fields.Text('Description')

    no_recurring = fields.Boolean('Not recurring')

    # No facturar líneas a 0 marcado por defecto
    skip_zero_qty = fields.Boolean(default=True)

    # Proyecto y cuenta analítica deben se unicos
    _sql_constraints = [
        ('unique_group_id', 'unique(group_id)', 
          _('Analytic account already assigned')),
        ('unique_project_id', 'unique(project_id)', 
         _('Projectt already assigned')),
    ]

    @api.multi
    def _get_project_vals(self):
        self.ensure_one()
        res = {
            'name': self.name,
            'partner_id': self.partner_id.id,
            'allow_timesheets': True,  # To create analytic account id
            'company_id': self.company_id.id,
        }

        return res

    @api.multi
    def link_project(self, recalc_closed=False):
        Project = self.env['project.project']
        for contract in self:
            if contract.project_id:
                continue
            vals = contract._get_project_vals()
            project = Project.create(vals)
            contract.write({
                'project_id': project.id,
                'group_id': project.analytic_account_id.id
            })
            project.get_contract_id()

        return True
    
    @api.multi
    def write(self, vals):
        """
        Propagar cuenta analítica a las líneas
        """
        res = super().write(vals)
        if 'group_id' in vals:
            self.mapped('contract_line_ids').write(
                {'analytic_account_id': vals['group_id']})
        return res
    
    @api.model
    def _get_contracts_to_invoice_domain(self, date_ref=None):
        """
        SOBREESCRITO PARA PERSONALIZAR EL DOMAIN DE BUSQUEDA DEL CRON
        """
        domain = []
        if not date_ref:
            date_ref = fields.Date.context_today(self)

            param = self.env.ref(
                'sale_contract_project_link.contract_invoice_days_before')
            if param and param.value:
                days = int(param.value)
                date_ref = date_ref + datetime.timedelta(days=days)

        domain.extend([
            ('recurring_next_date', '<=', date_ref),
            ('no_recurring', '=', False),
        ])
        return domain
    
    def _finalize_and_create_invoices(self, invoices_values):
        """
        Si las facturas creadas son desde no recurrentes, como no tienen la
        fecha actualizada de _update_recurring_next_date, lo calculo yo aquí.
        """
        invoices = super()._finalize_and_create_invoices(invoices_values)

        contract_lines = invoices.mapped('invoice_line_ids.contract_line_id').\
            filtered(lambda l: l.contract_id.no_recurring)
        
        if contract_lines:
            wzd_date = contract_lines[0].recurring_next_date
            contract_lines.write({
                "last_date_invoiced": wzd_date,
                "recurring_next_date": wzd_date + relativedelta(days=1)})
        return invoices
    
       # FIX!! OVERWRITE PORQUE EL MODULO DE SALE_CONTRACT_INVOICING NO
    # TIENE EN CUENTA QUE ES API MULTI, TODO PR A OCA
    # @api.multi
    def _recurring_create_invoice(self, date_ref=False):
        no_recurring_mode = self._context.get('no_recurring_mode', False)
        if any([c.no_recurring for c in self]) and not no_recurring_mode:
            raise UserError(_('You cant invoice not recurring invoices from \
                here.You mus utse the variable invoice wizard.'))


        invoices_values = self._prepare_recurring_invoices_values(date_ref)

        # No crear facturas si no hay líneas
        invoice_values_with_lines = []
        for dic in invoices_values:
            if dic.get('invoice_line_ids', []):
                invoice_values_with_lines.append(dic)
        if not invoice_values_with_lines:
            return self.env['account.invoice']

        invoices = self._finalize_and_create_invoices(
            invoice_values_with_lines)

        # CODIGO DE SALE_CONTRACT_INVOICING CON BUCLE (FIX OCA BUG)
        for contract in self:
            if not contract.invoicing_sales:
                continue
            sales = self.env['sale.order'].search([
                ('analytic_account_id', '=', contract.group_id.id),
                ('partner_invoice_id', 'child_of',
                contract.partner_id.commercial_partner_id.ids),
                ('invoice_status', '=', 'to invoice'),
                ('date_order', '<=',
                '{} 23:59:59'.format(contract.recurring_next_date)),
            ])
            if sales:
                invoice_ids = sales.action_invoice_create()
                invoices |= self.env['account.invoice'].browse(invoice_ids)[:1]
        return invoices
    
class ContractLine(models.Model):
    _inherit = "contract.line"

    last_date_invoiced = fields.Date(
        string='Last Date Invoiced', readonly=True, copy=False
    )

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.contract_id.group_id:
            res.write({'analytic_account_id': res.contract_id.group_id.id})
        return res
    
    def _get_period_to_invoice(self, last_date_invoiced, recurring_next_date, 
                               stop_at_date_end=True):
        """
        Esta función se va a eliminar, pero si next_period_date_end
        da False porque el proyecto está cerrado hay que fallar. 
        """
        res = super()._get_period_to_invoice(
            last_date_invoiced, recurring_next_date, 
            stop_at_date_end=stop_at_date_end)
        
        if res[1] == False:
            raise ValidationError(
                    _("No hay siguiente fecha de fin de periodo. \
                      Revise la fecha fin")
                )
        return res
    
    # FIX!!! overwrited NO INVOICE IF NOT NEXT RECURRING INTERVAL
    @api.depends('recurring_next_date', 'date_start', 'date_end')
    def _compute_create_invoice_visibility(self):
        """
        Si dejo crear factura sin next_period_date_end, falla en la
        función de insert markers y en la de update recurring invoice date,
        no espera esta situación
        """
        today = fields.Date.context_today(self)
        for rec in self:
            # ADDED AND Rec.next_period_date_end
            if rec.date_start and rec.next_period_date_end:
                if today < rec.date_start:
                    rec.create_invoice_visibility = False
                else:
                    rec.create_invoice_visibility = bool(
                        rec.recurring_next_date
                    )

    def _compute_next_period_date_start(self):
        """
        Facturación variable ne contratos no recurrentes debe dar el siguinte
        inicio de período la fecha de última factura
        """
        res = super()._compute_next_period_date_start()
        for line in self:
            if line.contract_id.no_recurring and line.last_date_invoiced:
                line.next_period_date_start = line.last_date_invoiced 
        return res
    
    @api.multi
    def _update_recurring_next_date(self):
        """
        Ignorar las líneas que vienen de facturación manual.
        Ya las actualizo yo manualmente en _finalize_and_create_invoices
        """
        recs2super = self.filtered(lambda x: not x.contract_id.no_recurring)
        return super(ContractLine, recs2super)._update_recurring_next_date()
       
# FIX BUG NO ME DEJA SUPRIMIR UNA LINEA SI HE USADO EL ASISTENTE POR CULPA DEL
# REQUIRED
class ContractLineWizard(models.TransientModel):

    _inherit = 'contract.line.wizard'
    contract_line_id = fields.Many2one(
        comodel_name="contract.line",
        string="Contract Line",
        required=False,
        index=True,
    )