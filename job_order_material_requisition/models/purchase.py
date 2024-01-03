from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"



    def _prepare_account_move_line(self, move=False):
        res = super()._prepare_account_move_line(move=move)
        res['plan_id'] = self.plan_id.id
        res['task_id'] = self.task.id
        res['job_cost_id'] = self.job_cost_id.id
        res['job_cost_line_id'] = self.job_cost_line_id.id
        return res

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    # job_cost_id = fields.Many2one('job.costing', string="Job Cost")
    # job_cost_line_id = fields.Many2one('job.cost.line')
    plan_id = fields.Many2one('material.plan')
    task_id = fields.Many2one('project.task')


