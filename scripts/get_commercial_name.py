# -*- coding: utf-8 -*-
db_name = 'conecta'
session.open(db=db_name)
import logging
from odoo import fields
_logger = logging.getLogger(__name__)

_logger.info('STARTING')    
partners = session.env['res.partner'].search([])
partners._compute_display_name()

_logger.info('DONE')    
session.cr.commit()
session.cr.close()