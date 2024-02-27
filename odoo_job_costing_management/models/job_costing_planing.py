# -*- coding: utf-8 -*-

from datetime import date

from odoo import models, fields, api, _
from odoo.exceptions import Warning
from odoo.exceptions import UserError

class JobCostingPlanning(models.Model):
    _name = 'job.costing.planning'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin'] #odoo11
#    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _description = "Job Costing"
    _rec_name = 'name'

    @api.model
    def create(self,vals):
        number = self.env['ir.sequence'].next_by_code('job.costing.planning')
        vals.update({
            'name': number,
        })
        return super(JobCostingPlanning, self).create(vals) 

    #@api.multi
    def unlink(self):
        for rec in self:
            if rec.state not in ('draft', 'cancel'):
                raise UserError(_('You can not delete Job Cost Sheet which is not draft or cancelled.'))
        return super(JobCostingPlanning, self).unlink()

    @api.depends(
        'job_cost_line_ids',
        'job_cost_line_ids.product_qty',
        'job_labour_line_ids.hours',
        'job_cost_line_ids.cost_price',
    )
    def _compute_material_total(self):
        for rec in self:
            rec.material_total = sum([p.total_cost for p in rec.job_cost_line_ids])
            # rec.material_total = sum([(p.product_qty * p.cost_price) for p in rec.job_cost_line_ids])

    @api.depends(
        'job_labour_line_ids',
        'job_labour_line_ids.hours',
        'job_labour_line_ids.product_qty',
        'job_labour_line_ids.cost_price'
    )
    def _compute_labor_total(self):
        for rec in self:
            # rec.labor_total = sum([(p.hours * p.cost_price) for p in rec.job_labour_line_ids])
            rec.labor_total = sum([p.total_cost for p in rec.job_labour_line_ids])

    @api.depends(
        'job_overhead_line_ids',
        'job_labour_line_ids.hours',
        'job_overhead_line_ids.product_qty',
        'job_overhead_line_ids.cost_price'
    )
    def _compute_overhead_total(self):
        for rec in self:
            rec.overhead_total = sum([p.total_cost for p in rec.job_overhead_line_ids])
            # rec.overhead_total = sum([(p.product_qty * p.cost_price) for p in rec.job_overhead_line_ids])

    @api.depends(
        'material_total',
        'labor_total',
        'overhead_total'
    )
    def _compute_jobcost_total(self):
        for rec in self:
            rec.jobcost_total = rec.material_total + rec.labor_total + rec.overhead_total

    #@api.multi
    def _purchase_order_line_count(self):
        purchase_order_lines_obj = self.env['purchase.order.line']
        for order_line in self:
            order_line.purchase_order_line_count = purchase_order_lines_obj.search_count([('job_cost_id','=',order_line.id)])
    
    def _job_costsheet_line_count(self):
        job_costsheet_lines_obj = self.env['job.cost.line']
        for jobcost_sheet_line in self:
            jobcost_sheet_line.job_costsheet_line_count = job_costsheet_lines_obj.search_count([('direct_id','=',jobcost_sheet_line.id)])

    #@api.multi
    def _timesheet_line_count(self):
        hr_timesheet_obj = self.env['account.analytic.line']
        for timesheet_line in self:
            timesheet_line.timesheet_line_count = hr_timesheet_obj.search_count([('job_cost_id', '=', timesheet_line.id)])

    #@api.multi
    def _account_invoice_line_count(self):
#        account_invoice_lines_obj = self.env['account.invoice.line']
        account_invoice_lines_obj = self.env['account.move.line']
        for invoice_line in self:
            invoice_line.account_invoice_line_count = account_invoice_lines_obj.search_count([('job_cost_id', '=', invoice_line.id)])

    # @api.onchange('project_id')
    # def _onchange_project_id(self):
    #     for rec in self:
    #         rec.analytic_id = rec.project_id.analytic_account_id.id

    number = fields.Char(
        readonly=True,
        default='New',
        copy=False,
    )
    name = fields.Char(
        required=True,
        copy=True,
        default='New',
        string='Name',
    )
    cost_id = fields.Many2one('job.costing')
    notes_job = fields.Text(
        required=False,
        copy=True,
        string='Job Cost Details'
    )
    user_id = fields.Many2one(
        'res.users', 
        default=lambda self: self.env.user, 
        string='Created By', 
        readonly=True
    )
    description = fields.Char(
        string='Description',
    )
    parnter_id = fields.Many2one('res.partner', string="Contact Person")
    currency_id = fields.Many2one(
        'res.currency', 
        string='Currency', 
        default=lambda self: self.env.user.company_id.currency_id, 
        readonly=True
    )
    company_id = fields.Many2one(
        'res.company', 
        default=lambda self: self.env.company,
        string='Company', 
        readonly=True
    )
    project_id = fields.Many2one(
        'project.project',
        string='Project',
    )
    start_date = fields.Date(
        string='Start Date',
        required=True,
    )
    end_date = fields.Date(
        string='End Date',
        required=True
        
    )
    material_total = fields.Float(
        string='Total Material Cost',
        compute='_compute_material_total',
        store=True,
    )
    labor_total = fields.Float(
        string='Total Labour Cost',
        compute='_compute_labor_total',
        store=True,
    )
    overhead_total = fields.Float(
        string='Total Overhead Cost',
        compute='_compute_overhead_total',
        store=True,
    )
    jobcost_total = fields.Float(
        string='Total Cost',
        compute='_compute_jobcost_total',
        store=True,
    )
    job_cost_line_ids = fields.Many2many(
        'job.cost.line',
        'direct_id',
        string='Direct Materials',
        copy=False,
        domain=[('job_type','=','material')],
    )
    job_labour_line_ids = fields.Many2many(
        'job.cost.line',
        'direct_id',
        string='Direct Labours',
        copy=False,
        domain=[('job_type','=','labour')],
    )
    job_overhead_line_ids = fields.Many2many(
        'job.cost.line',
        'direct_id',
        string='Direct Overheads',
        copy=False,
        domain=[('job_type','=','overhead')],
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
#        domain=[('customer','=', True)],
    )
    product_id = fields.Many2one('product.product', string="BOQ Item")
    state = fields.Selection(
        selection=[
                    ('draft','Draft'),
                    ('confirm','Confirmed'),
                    ('approve','Approved'),
                    ('done','Done'),
                    ('cancel','Canceled'),
                  ],
        string='State',
        tracking=True,
        default='draft',
    )
    
    
    job_costsheet_line_count = fields.Integer(
        compute='_job_costsheet_line_count'
    )
    
    
    
    
    account_invoice_line_ids = fields.One2many(
#        "account.invoice.line",
        'account.move.line',
        'job_cost_id',
    )
    assumed_qty = fields.Float(string="Assumed Qty", related="cost_id.assumed_qty")
    quantity = fields.Float(string="Quantity")
    total_amount = fields.Float(string="Total Amount", compute='_compute_or_cost')
    notes_job = fields.Text(
        required=False,
        copy=True,
        string='Job Cost Details'
    )
    picking_type_id = fields.Many2one('stock.picking.type', string="Operation")
    location_id = fields.Many2one('stock.location', string="From")
    dest_location_id = fields.Many2one('stock.location', string="To")
    uom_id = fields.Many2one('uom.uom',string="UOM")

    @api.onchange('assumed_qty', 'overhead_profit',  'jobcost_total','quantity')
    def _compute_or_cost(self):
        for rec in self:
            # material_cost = sum(rec.job_cost_line_ids.mapped('total_cost'))
            # labour_cost = sum(rec.job_labour_line_ids.mapped('total_cost'))
            # oh_cost = sum(rec.job_overhead_line_ids.mapped('total_cost'))
            # basic_cost = material_cost + labour_cost + oh_cost
            if rec.assumed_qty != 0:
                cost_per_unit = rec.jobcost_total / rec.assumed_qty
                tax = 0
                cost_per_unit += cost_per_unit * (tax / 100)

                # rec.or_cost = cost_per_unit
            # else:
            #     # rec.or_cost = 0
            rec.total_amount =  rec.quantity

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_approve(self):
        for rec in self:
            rec.state = 'approve'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
            rec.complete_date = fields.date.today()

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'


    def action_view_planning(self):
        self.ensure_one()
        planning = self.env['job.costing.planning']
        # cost_ids = purchase_order_lines_obj.search([('job_cost_id','=',self.id)]).ids
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Planning',
            'res_model': 'job.costing.planning',
            'domain': [('cost_id','=', self.id)],
            'view_type': 'form',
            'view_mode': 'tree,form',
        }
        return action
    
    def action_view_transfer(self):
        self.ensure_one()
        planning = self.env['stock.picking']
        # cost_ids = purchase_order_lines_obj.search([('job_cost_id','=',self.id)]).ids
        action = {
            'type': 'ir.actions.act_window',
            'name': 'Transfer',
            'res_model': 'stock.picking',
            'domain': [('cost_planning_id','=', self.id)],
            'view_type': 'form',
            'view_mode': 'tree,form',
        }
        return action
    

    def action_create_transfer(self):
        stock_obj = self.env['stock.picking']
        move_obj = self.env['stock.move']

        for rec in self:
            if not rec.location_id.id:
                raise UserError(_('Select Source location under the picking details.'))
            
            if not rec.dest_location_id:
                raise UserError(_('Select Destination location under the picking details.'))

            picking_vals = {
                'partner_id' : rec.partner_id.id,
                        #'min_date' : fields.Date.today(),
                'location_id' : rec.location_id.id,
                'location_dest_id' : rec.dest_location_id and rec.dest_location_id.id or rec.employee_id.dest_location_id.id or rec.employee_id.department_id.dest_location_id.id,
                'picking_type_id' : rec.picking_type_id.id,#internal_obj.id,
                'note' : rec.notes_job,
                'cost_planning_id' : rec.id,
                'origin' : rec.name,
                'company_id' : rec.company_id.id,
                        
            }
            stock_id = stock_obj.sudo().create(picking_vals)
            # delivery_vals = {
            #         'delivery_picking_id' : stock_id.id,
            #     }
            # rec.write(delivery_vals)
            material_line = self.cost_id
            for line in material_line.job_cost_line_ids:
                pick_vals = rec._prepare_pick_vals(line, stock_id)
                move_id = move_obj.sudo().create(pick_vals)

#             po_dict = {}
#             for line in rec.requisition_line_ids:
#                 if line.requisition_type =='internal':
#                 #else:
#                 if line.requisition_type == 'purchase': #10/12/2019
#                     if not line.partner_id:
#                         raise UserError(_('Please enter atleast one vendor on Requisition Lines for Requisition Action Purchase'))
# #                        raise UserError(_('Please enter atleast one vendor on Requisition Lines for Requisition Action Purchase'))
#                     for partner in line.partner_id:
#                         if partner not in po_dict:
#                             po_vals = {
#                                 'partner_id':partner.id,
#                                 'currency_id':rec.env.user.company_id.currency_id.id,
#                                 'date_order':fields.Date.today(),
# #                                'company_id':rec.env.user.company_id.id,
#                                 'company_id':rec.company_id.id,
#                                 'custom_requisition_id':rec.id,
#                                 'origin': rec.name,
#                             }
#                             purchase_order = purchase_obj.create(po_vals)
#                             po_dict.update({partner:purchase_order})
#                             po_line_vals = rec.with_context(partner_id=partner)._prepare_po_line(line, purchase_order)
# #                            {
# #                                     'product_id': line.product_id.id,
# #                                     'name':line.product_id.name,
# #                                     'product_qty': line.qty,
# #                                     'product_uom': line.uom.id,
# #                                     'date_planned': fields.Date.today(),
# #                                     'price_unit': line.product_id.lst_price,
# #                                     'order_id': purchase_order.id,
# #                                     'account_analytic_id': rec.analytic_account_id.id,
# #                            }
#                             purchase_line_obj.sudo().create(po_line_vals)
#                         else:
#                             purchase_order = po_dict.get(partner)
#                             po_line_vals = rec.with_context(partner_id=partner)._prepare_po_line(line, purchase_order)
# #                            po_line_vals =  {
# #                                 'product_id': line.product_id.id,
# #                                 'name':line.product_id.name,
# #                                 'product_qty': line.qty,
# #                                 'product_uom': line.uom.id,
# #                                 'date_planned': fields.Date.today(),
# #                                 'price_unit': line.product_id.lst_price,
# #                                 'order_id': purchase_order.id,
# #                                 'account_analytic_id': rec.analytic_account_id.id,
# #                            }
#                             purchase_line_obj.sudo().create(po_line_vals)
#                 rec.state = 'stock'
            

    @api.model
    def _prepare_pick_vals(self, line=False, stock_id=False):
        pick_vals = {
            'product_id' : line.product_id.id,
            'name' : line.description,
            'product_uom_qty' : line.product_qty,
            'product_uom' : line.uom_id.id,
            'location_id' : self.location_id.id,
            'location_dest_id' : self.dest_location_id.id,
            'picking_type_id' : self.picking_type_id.id,
            'picking_id' : stock_id.id,
        }
        return pick_vals