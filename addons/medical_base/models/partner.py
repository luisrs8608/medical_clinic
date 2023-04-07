# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
# from odoo.exceptions import UserError, ValidationError


class Patient(models.Model):
    _inherit = 'res.partner'

    clinic_history_ids = fields.One2many('clinic.history', 'patient_id', string='Clinic history')
    employee_id = fields.Many2one('hr.employee', string='Dr.(Dra)', index=True, ondelete='cascade')
    calendar_event_ids = fields.One2many('calendar.event', 'patient_id', string='Medical appointments')
    is_patient = fields.Boolean('Is patient?')

    def new_treatment(self):
        values = []
        values.append({
            'partner_id': self.id,
            'partner_invoice_id': self.id,
            'partner_shipping_id': self.id,
            'employee_id': self.employee_id.id,
            'order_line': [],
        })

        order_ids = self.env['sale.order'].create(values)
        action = self.env.ref('sale.action_orders').read()[0]
        form_view = [(self.env.ref('sale.view_order_form').id, 'form')]
        if 'views' in action:
            action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
        else:
            action['views'] = form_view
        action['res_id'] = order_ids.id

        return action

    def open_import_pacients(self):
        return {
            'name': 'Import pacients data',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'import.pacients.data',
            'view_id': self.env.ref('medical_base.import_pacients_data_form_view').id,
            'type': 'ir.actions.act_window',
            'target': 'new'
        }
