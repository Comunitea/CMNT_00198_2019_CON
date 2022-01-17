{
    'name': 'Send Grouped Invoice By Email',
    'version': '1.1',
    'summary': 'Send Grouped Invoice By Email',
    'description': "",
    'sequence': 13,
    'depends': [
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/send_grouped_invoice_view.xml',
        'data/stock_picking_mail.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}