# -*- coding: utf-8 -*-

from datetime import date,time

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta


class CostingPlanningWizard(models.TransientModel):
    _name = 'costing.planning.wizard'


    # @api.model
    # def default_get(self, fields):
    #     rec = super(CostingPlanningWizard, self).default_get(fields)
    #     context = dict(self._context or {})
    #     active_model = context.get('active_model')
    #     active_ids = context.get('active_ids')
    #     picking = self.env[active_model].browse(active_ids)
    #     vals = []
    #     for line in picking.move_lines:
    #         vals.append((0,0,{'product_id': line.product_id.id,
    #                          'quantity': line.product_uom_qty,
    #                          'product_uom': line.product_uom.id,
    #                          'qty_available': line.product_id.qty_available,
    #                           }))
    #     rec.update({'product_line_ids': vals})
    #     return rec

    job_id = fields.Many2one('job.costing', required=True)
    planned_qty = fields.Float(string="Planned Qty")
    remaining_qty = fields.Float(string="Remaining Qty")
    qty_to_plan = fields.Float(string="Qty To Plan")
    start_date = fields.Date(
        string='Start Date',
        required=True,
    )
    end_date = fields.Date(
        string='End Date',
        required=True
        
    )
    picking_type_id = fields.Many2one('stock.picking.type', string="Operation")
    location_id = fields.Many2one('stock.location', string="From")
    dest_location_id = fields.Many2one('stock.location', string="To")

    def create_planning(self):
        job_id = self.job_id
        values = {
            'cost_id': job_id.id,
            'notes_job': job_id.notes_job,
            'user_id': job_id.user_id.id,
            'project_id': job_id.project_id.id,
            'product_id': job_id.product_id.id,
            'description': job_id.description,
            'partner_id': job_id.partner_id.id,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'picking_type_id': self.picking_type_id.id,
            'location_id': self.location_id.id,
            'dest_location_id': self.dest_location_id.id,
            'assumed_qty': self.qty_to_plan,
            'quantity': job_id.quantity,
            'uom_id': job_id.uom_id.id,
            # 'job_cost_line_ids': job_id.job_cost_line_ids.ids,
            # 'job_labour_line_ids': job_id.job_labour_line_ids.ids,
            # 'job_overhead_line_ids': job_id.job_overhead_line_ids.ids
        }
        self.env['job.costing.planning'].create(values)

    def _prepare_purchase_order(self, vendor):
        self.ensure_one()
        stock_pick_obj = self.env['stock.picking'].browse(self._context.get('active_ids', []))
        
        fpos = self.env['account.fiscal.position'].with_context(\
                company_id=vendor.company_id.id).get_fiscal_position(vendor.id)
        
        purchase_req_vals = {
            'partner_id': vendor.id,
            'company_id': vendor.company_id.id,
            'currency_id': vendor.property_purchase_currency_id.id \
                            or self.env.user.company_id.currency_id.id,
            'origin': stock_pick_obj.name,
            'payment_term_id': vendor.property_supplier_payment_term_id.id,
            'fiscal_position_id': fpos,
#            'date_order' : datetime.today(),
            #'picking_id':vendor.id
        }
        return purchase_req_vals

    #@api.multi
    def create_purchase_requistion(self):
        picking = self.env['stock.picking'].browse(self._context.get('active_ids', []))
        purchase_obj = self.env['purchase.order']
        order_lines = self.env['purchase.order.line']
        order_ids = []
        date_planned = datetime.today()
        for rec in self.supplier_ids:
            purchase_order = self._prepare_purchase_order(rec)
            purchase = purchase_obj.sudo().create(purchase_order)
            order_ids.append(purchase.id)
            for line in self.product_line_ids:
                # Create Purchase order Lines
                line_vals =  {
                         'product_id': line.product_id.id,
                         'name':line.product_id.name,
                         'product_qty': line.quantity,
                         'product_uom': line.product_uom.id,
                         'date_planned': datetime.today(),
                         'price_unit': line.product_id.standard_price,
#                          'qty_available': line.product_id.qty_available,
                         'order_id': purchase.id,
                         }
                purchase_order_line = order_lines.sudo().create(line_vals)
                purchase_order_line.order_id = purchase.id
        picking[0].purchase_order_ids = order_ids
