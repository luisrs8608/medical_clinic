# -*- coding: utf-8 -*-

import base64
import logging

import xlrd
from odoo import api, fields, models, Command, _
from odoo.exceptions import UserError

import datetime

from odoo.tools import config, DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, pycompat

_logger = logging.getLogger(__name__)


class ImportPacientsData(models.TransientModel):
    _name = "import.pacients.data"
    _description = u"Import pacients data"

    data_file = fields.Binary(u"Archivo Excel")

    def import_pacients(self):
        for s in self:
            try:
                data_file = base64.b64decode(s.data_file)
                book = xlrd.open_workbook(file_contents=data_file)
            except:
                raise UserError(u"Archivo excel no válido.")

            sheet = book.sheet_by_index(0)
            _date = fields.Date.today()

            for rowx, row in enumerate(map(sheet.row, range(sheet.nrows))):
                if rowx > 2255 and rowx < 2300:
                    if row[0].ctype is xlrd.XL_CELL_DATE:
                        _date = xlrd.xldate.xldate_as_datetime(row[0].value, book.datemode)
                    name = row[1].value
                    ci = str(row[2].value).split('.')[0]
                    treatment = str(row[3].value)
                    price = row[4].value
                    doctor = row[6].value
                    if name and name != '':
                        doctor_id = self.env['hr.employee'].search([('name', '=', doctor)])
                        product_id = self.env['product.product'].search([('name', '=', 'General treatment')])
                        partner_data = dict(
                            name = str(name)[:50],
                            vat = ci,
                            employee_id = doctor_id and doctor_id.id or False,
                            is_patient = True
                        )
                        try:
                            partner_id = self.env['res.partner'].create(partner_data)
                            if treatment:
                                if type(price) is float or type(price) is int:
                                    _price = price
                                else:
                                    _price = 0.0
                                if _price > 0.0:
                                    sale_order_data = dict(
                                        partner_id = partner_id.id,
                                        partner_invoice_id = partner_id.id,
                                        partner_shipping_id = partner_id.id,
                                        employee_id = doctor_id and doctor_id.id or False,
                                        date_order = _date,
                                        note = treatment,
                                        order_line = [Command.create(dict(
                                            name = 'Tratamiento general',
                                            product_id = product_id and product_id.id or False,
                                            product_uom_qty = 1,
                                            price_unit = price,
                                        ))],
                                    )

                                    order_id = self.env['sale.order'].create(sale_order_data)
                                    order_id.action_confirm()
                                    invoice_id = order_id._create_invoices(final=True)
                                    invoice_id.action_post()
                                    self.env['account.payment.register'].with_context(
                                        active_model='account.move', active_ids=invoice_id.ids
                                    ).create({'payment_date': invoice_id.date,})._create_payments()
                                else:
                                    treatment_data = dict(
                                        patient_id = partner_id.id,
                                        date = _date,
                                        employee_id = doctor_id and doctor_id.id or False,
                                        description = treatment,
                                    )
                                    treatment_id = self.env['clinic.history'].create(treatment_data)
                        except Exception as e:
                            _logger.exception('Error: {}'.format(e))

                if rowx % 100 == 0:
                    self.env.cr.commit()
                    _logger.info('Inserted records')
        self.env.cr.commit()

        return {'type': 'ir.actions.act_window_close'}
