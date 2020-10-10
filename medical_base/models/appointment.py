# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
# from odoo.exceptions import UserError, ValidationError


class Appointment(models.Model):
    _description = 'Appointment'
    _name = 'appointment'
    _rec_name = 'patient_id'
    _order = 'start DESC'

    patient_id = fields.Many2one('res.partner', string='Patient', index=True, ondelete='cascade')
    state = fields.Selection([('draft', 'Unconfirmed'), ('open', 'Confirmed')], string='Status', readonly=True, tracking=True, default='draft')
    start = fields.Datetime('Start', required=True)
    stop = fields.Datetime('Stop', required=True)
    duration = fields.Float('Duration', states={'done': [('readonly', True)]})
    employee_id = fields.Many2one('hr.employee', string='Dr.(Dra)', index=True, ondelete='cascade')
