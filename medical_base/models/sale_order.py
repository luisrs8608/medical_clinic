# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    employee_id = fields.Many2one('hr.employee', string='Dr.(Dra)', index=True)

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for so in self:
            if so.note:
                hc = self.env['clinic.history'].create({
                    'patient_id': so.partner_id.id,
                    'employee_id': so.employee_id.id,
                    'date': so.date_order,
                    'description': so.note,
                })
        return res
