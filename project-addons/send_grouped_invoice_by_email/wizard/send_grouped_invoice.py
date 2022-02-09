# from _typeshed import ReadOnlyBuffer
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import base64

class DeliveryManageWzd(models.TransientModel):
    _name = 'send.grouped.invoice'

    report_template = fields.Many2one('ir.actions.report', 'Optional report to print and attach')
    def confirm(self):
        invoices = self.env['account.invoice'].browse(
            self.env.context.get('active_ids'))
        
        attachments = self.env['ir.attachment']
        partners = invoices.mapped('partner_id')
        if len(partners) > 1:
            raise UserError(_("Can´t be more than one partner in the selected invoices"))

        report_invoice = self.env.ref('account.account_invoices_without_payment')
        for invoice in invoices:
            report_rendered = report_invoice.render_qweb_pdf(invoice.id)
            # repor
            # ReadOnlyBuffer

            data_record = base64.encodestring(report_rendered[0])
            
            ir_values = {
                'name': '%s.pdf' % invoice.number,
                # 'name': report_invoice.name,
                'type': 'binary',
                'datas': data_record,
                'datas_fname': '%s.pdf' % invoice.number,
                # 'store_fname': 'p0',
                'mimetype': 'application/pdf',
                'res_model': 'mail.compose.message',
                'res_id': 0,
            }
            data_id = self.env['ir.attachment'].create(ir_values)
            attachments |= data_id
            msg = _("Invoice has been send")
            invoice.message_post(body = msg)

        template = False
        if self._context.get('from_conecta'):
            template = self.env.ref(
                'send_grouped_invoice_by_email.grouped_email_template_account_invoice_conecta',
                False,
            )
        if self._context.get('from_external'):
            template = self.env.ref(
                'send_grouped_invoice_by_email.grouped_email_template_account_invoice_external',
                False,
            )
        if self._context.get('from_softdil'):
            template = self.env.ref(
                'send_grouped_invoice_by_email.grouped_email_template_account_invoice_softdil',
                False,
            )
        
        if not template:
            raise UserError(_('No mail template found'))
        # template.attachment_ids = [(6, 0, attachments.ids)]
        ctx = dict(
                default_model='res.partner',
                default_res_id=partners.id,
                default_use_template=bool(template),
                default_template_id=template and template.id or False,
                default_composition_mode='comment',
                user_id=self.env.user.id,
                default_attachment_ids=[(6, 0, attachments.ids)]
            )
        compose_form = self.env.ref(
            'mail.email_compose_message_wizard_form',
            False,
        )
        # TODO es necesario el sudo?
        composer_id = self.env["mail.compose.message"].sudo().with_context(ctx).create({})
        values = composer_id.onchange_template_id(
            template.id, "comment", 'res.partner', partners.id
        )["value"]
        composer_id.write(values)
        composer_id.attachment_ids = [(6, 0, attachments.ids)]
        # composer_id.with_context(ctx).send_mail()

        # report_name = self._render_template(template.report_name, template.model, self.env.user.id)
        # attachments.append((report_name,data_record))
        # template.with_context(ctx).send_mail(partners.id)
        # email_values = {'email_to': self.partner_id.email,
        #         'email_from': self.env.user.email}
        # template.send_mail(self.id, email_values=email_values, force_send=True)
        # template.attachment_ids = [(3, data_id.id)]
        
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }
        # return self.action_partner_show(partners)


    def action_partner_show(self,partners):
        action = self.env.ref('base.action_partner_form').read()[0]
        action["context"] = {}
        if len(partners) == 1:
            view_name = "base.view_partner_form"
            action["views"] = [(self.env.ref(view_name).id, "form")]
            action["res_id"] = partners.id
        else:
            action = {"type": "ir.actions.act_window_close"}
        return action