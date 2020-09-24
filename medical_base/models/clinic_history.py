# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
# from odoo.exceptions import UserError, ValidationError


class ClinicHistory(models.Model):
    _description = 'Clinic history'
    _name = 'clinic.history'
    _rec_name='date'
    _order = 'date DESC'

    patient_id = fields.Many2one('res.partner', string='Patient', index=True, ondelete='cascade')
    date = fields.Date(string='Date', default=fields.Date.today)
    employee_id = fields.Many2one('hr.employee', string='Dr.(Dra)', index=True, ondelete='cascade')
    description = fields.Html(string='Description')
