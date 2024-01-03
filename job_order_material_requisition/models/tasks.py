from odoo import models, api, fields, _ 



class JobCostLine(models.Model): 
    _inherit = 'job.cost.line'
    plan_id = fields.Many2one('material.plan')

class ProjectTask(models.Model):
    _inherit = 'project.task'


    def action_create_planning(self):
        job_cost_ids = self.job_cost_ids
        job_cost = self.env['job.cost.line'].search([
            ('direct_id', 'in', job_cost_ids.ids),
            ('job_type', '=', 'material'),
            ])

        for rec in job_cost:
            description = rec.description
            if not description:
                description = rec.product_id.name
            vals = {
                'material_task_id': self.id,
                'job_cost_id': rec.direct_id.id,
                'cost_line_id': rec.id,
                'description': description,
                'product_id': rec.product_id.id,
                'product_uom_qty': rec.product_qty,
                'product_uom': rec.uom_id.id,
            }
            if rec.plan_id:
                rec.plan_id.write(vals)
            else:
                mp = self.env['material.plan'].create(vals)
                rec.plan_id = mp.id
