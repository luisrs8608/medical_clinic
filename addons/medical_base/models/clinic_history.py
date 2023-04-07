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
    employee_id = fields.Many2one('hr.employee', string='Dr.(Dra)')
    description = fields.Text(string='Description')
    order_id = fields.Many2one('sale.order', string='Order', readonly=True)
    amount_total = fields.Float(string="To Invoice", compute='_compute_amount_total', readonly=True)
    paid = fields.Float(string="Paid", compute='_compute_amount_total', readonly=True)

    @api.depends('order_id')
    def _compute_amount_total(self):
        for rec in self:
            amount_total = rec.order_id and rec.order_id.amount_total or 0.0
            paid = 0.0
            if rec.order_id and rec.order_id.invoice_ids:
                amount_residual = sum(rec.order_id.invoice_ids.mapped('amount_residual'))
                paid = amount_total - amount_residual
            rec.paid = paid
            rec.amount_total = amount_total
