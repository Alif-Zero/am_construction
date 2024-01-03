# -*- coding: utf-8 -*-

from odoo import models, fields


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    job_cost_id = fields.Many2one(
        'job.costing',
        string='Job Cost Center',
    )
    plan_id = fields.Many2one('material.plan')
    task_id = fields.Many2one('project.task')


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    plan_id = fields.Many2one('material.plan')
    task_id = fields.Many2one('project.task')

#    def _prepare_invoice_line_from_po_line(self, line): MOVE TO purchase.order.line _prepare_account_move_line
#        data = super(
#            AccountInvoice, self
#        )._prepare_invoice_line_from_po_line(line)
#        data.update({
#            'job_cost_id': line.job_cost_id.id,
#            'job_cost_line_id': line.job_cost_line_id.id,
#        })
#        return data
