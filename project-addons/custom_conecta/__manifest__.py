# Copyright (C) 2020 - Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Custom Conecta',
    'summary': "Adds an agreement object",
    'version': '12.0.0.0.0',
    'category': 'Custom',
    'author': 'Comunitea, '
              'Javier Colmenero (javier@comunitea.com), ',
    'license': 'AGPL-3',
    'depends': [
        'product',
        'project',
        'stock',
        'account',
        'crm',
        'sale_order_revision',
        'sale_order_type',
        'account_financial_report',
        'account_payment_partner',
        'purchase',
        'account_banking_mandate_sale',

        # No real dependencies
        'sale_contract_project_link', 
        'custom_sla',
        'project_task_material',
        'project_task_default_stage',
        'stock_picking_report_valued',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/project_security.xml',
        'views/res_partner_view.xml',
        'views/product_template_view.xml',
        'views/stock_picking_view.xml',
        'views/sale_order_view.xml',
        'views/purchase_order_view.xml',
        'views/project_task_material_view.xml',
        'views/account_view.xml',
        'views/res_partner_bank_view.xml',
        'views/crm_view.xml',
        'wizard/account_invoice_send.xml',
        'wizard/mail_compose_mesage.xml',
        'data/mail_data.xml'
        ],
    'development_status': 'Beta',
    'maintainers': [
        'Javier Colmenero',
    ],
    'installable': True,
}
