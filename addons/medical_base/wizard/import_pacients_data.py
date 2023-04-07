# -*- coding: utf-8 -*-

import base64
import logging

import xlrd
from odoo import api, fields, models, Command, _
from odoo.exceptions import UserError

import datetime

from odoo.tools import config, DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, pycompat


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
            vals_list = []
            for rowx, row in enumerate(map(sheet.row, range(sheet.nrows))):
                if rowx > 0:
                    _date = xlrd.xldate.xldate_as_datetime(row[0].value, book.datemode)
                    name = row[1].value
                    ci = str(row[2].value).split('.')[0]
                    treatment = str(row[3].value)
                    cost = str(row[4]).split('.')[0]
                    doctor = row[6].value
                    if name and name != '':
                        doctor_id = self.env['hr.employee'].search([('name', '=', doctor)])
                        partner_data = dict(
                            name = name,
                            vat = ci,
                            employee_id = doctor_id and doctor_id.id or False,
                            is_patient = True
                        )
                        if treatment:
                            treatment_data = dict(
                                date = _date,
                                employee_id = doctor_id and doctor_id.id or False,
                                description = treatment,
                            )
                            partner_data.update(dict(
                                clinic_history_ids = [Command.create(treatment_data)]
                            ))
                        vals_list.append(partner_data)

                if rowx == 3:
                    break

            try:
                partner_ids = self.env['res.partner'].create(vals_list)
            except Exception as e:
                a = e
                # raise ValidationError(_("."))

        return {'type': 'ir.actions.act_window_close'}
