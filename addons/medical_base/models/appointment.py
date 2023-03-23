# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
# from odoo.exceptions import UserError, ValidationError


class Appointment(models.Model):
    _inherit = 'calendar.event'
    _rec_name = 'patient_id'
    # _order = 'start DESC'

    patient_id = fields.Many2one(
        'res.partner',
        string='Patient',
        domain=[('is_patient', '=', True)],
        index=True,
        ondelete='cascade'
    )
    employee_id = fields.Many2one('hr.employee', string='Dr.(Dra)', index=True, ondelete='cascade')

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        for rec in self:
            rec.name = rec.patient_id.name

    @api.onchange('name')
    def _onchange_name(self):
        for rec in self:
            if not rec.patient_id:
                partner_id = self.env['res.partner'].search([('name', 'ilike', rec.name)], limit=1)
                rec.patient_id = partner_id and partner_id.id or False

    @api.model_create_multi
    def create(self, vals_list):
        vals_list = [
            dict(vals, allday=False) for vals in vals_list
        ]
        res_ids = super(Appointment, self).create(vals_list)
        return res_ids
