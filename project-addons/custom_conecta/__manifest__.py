# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
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

        # No real dependencies
        'sale_contract_project_link', 
        'custom_sla',
        'project_task_material',
        'project_task_default_stage'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_view.xml',
        'views/product_template_view.xml',
        'views/stock_picking_view.xml',
        'views/sale_order_view.xml',
        'views/project_task_material_view.xml',
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
