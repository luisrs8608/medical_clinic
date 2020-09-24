# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
# from odoo.exceptions import UserError, ValidationError


class Patient(models.Model):
    _inherit = 'res.partner'

    clinic_history_ids = fields.One2many('clinic.history', 'patient_id', string='Clinic history')
    employee_id = fields.Many2one('hr.employee', string='Dr.(Dra)', index=True, ondelete='cascade')
