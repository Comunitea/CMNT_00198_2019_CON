# -*- coding: utf-8 -*-
db_name = 'conecta'
session.open(db=db_name)
import logging
from odoo import fields
_logger = logging.getLogger(__name__)

accs = session.env['res.partner.bank'].search([('bank_id', '=', False)])
for acc in accs:
     acc._onchange_acc_number_base_bank_from_iban()

_logger.info('DONE')    
session.cr.commit()
session.cr.close()
