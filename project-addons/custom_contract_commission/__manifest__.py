# Copyright (C) 2020 - Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Custom Contract Commission',
    'summary': "Adds commisoin on contracts",
    'version': '12.0.0.0.0',
    'category': 'Custom',
    'author': 'Comunitea, '
              'Javier Colmenero (javier@comunitea.com), ',
    'license': 'AGPL-3',
    'depends': [
        'contract',
        'sale_commission',
        'sale_commission_formula',
        'custom_sla',
        'account_invoice_merge'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/sale_commission_security.xml',
        'wizard/recompute_commission_wzd_view.xml',
        'views/contract.xml',
        'views/settlement_view.xml',
        
    ],
    'development_status': 'Beta',
    'maintainers': [
        'Javier Colmenero',
    ],
    'installable': True,
}
