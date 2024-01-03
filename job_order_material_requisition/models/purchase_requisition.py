from odoo import models, fields, api


class MaterialPurchaseRequisitionLine(models.Model):
    _inherit = "material.purchase.requisition.line"

    job_cost_id = fields.Many2one('job.costing', string="Job Cost")
    cost_line_id = fields.Many2one('job.cost.line')
    plan_id = fields.Many2one('material.plan')
    task_id = fields.Many2one('project.task')


class MaterialPurchaseRequisitionLine(models.Model):
    _inherit = "material.purchase.requisition"

    @api.model
    def _prepare_po_line(self, line=False, purchase_order=False):
        # seller = line.product_id._select_seller(
        #         partner_id=self._context.get('partner_id'), 
        #         quantity=line.qty,
        #         date=purchase_order.date_order and purchase_order.date_order.date(), 
        #         uom_id=line.uom
        #         )
        # po_line_vals = {
        #         'product_id': line.product_id.id,
        #         'name':line.product_id.name,
        #         'product_qty': line.qty,
        #         'product_uom': line.uom.id,
        #         'date_planned': fields.Date.today(),
        #          # 'price_unit': line.product_id.standard_price,
        #         'price_unit': seller.price or line.product_id.standard_price or 0.0,
        #         'order_id': purchase_order.id,
        #          # 'account_analytic_id': self.analytic_account_id.id,
        #         'analytic_distribution':  {self.sudo().analytic_account_id.id: 100} if self.analytic_account_id else False,
        #         'custom_requisition_line_id': line.id,
        # }
        res = super()._prepare_po_line(line=line,purchase_order=purchase_order)
        res['job_cost_id'] = line.job_cost_id.id
        res['job_cost_line_id'] = line.cost_line_id.id
        res['plan_id'] = line.task_id.id
        res['task_id'] = line.task_id.id
        
        return res