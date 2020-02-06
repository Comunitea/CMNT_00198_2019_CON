# © 2017 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Custom Documents Conecta',
    'summary': "Custom documents",
    'version': '12.0.0.0.0',
    'category': 'Custom',
    'author': 'Comunitea, '
              'Javier Colmenero (javier@comunitea.com), ',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'sale',
        'account',
        'web',
        'account_due_dates_str',
        'custom_timecontrol_dates',
        'custom_sla'
    ],
    'data': [
        'views/report_templates.xml',
        'views/sale_report_templates.xml',
        'views/report_invoice.xml',
        'views/report_project.xml',
        'views/report_sla.xml',
        'views/res_company_views.xml',
        'views/report_menu.xml',
        'wizard/print_hours_report_view.xml',
        'wizard/print_sla_wzd_view.xml',

        ],
    'development_status': 'Beta',
    'maintainers': [
        'Javier Colmenero',
    ],
    'installable': True,
}
