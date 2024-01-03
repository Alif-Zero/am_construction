# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MaterialPlanning(models.Model):
    _inherit = 'material.plan'
    
    
    requisition_line = fields.Many2one(
        'material.purchase.requisition.line',
        string='Requisition Line',
        readonly=True,
    )
    requisition_type = fields.Selection(
        selection=[
            ('internal','Internal Picking'),
            ('purchase','Purchase Order'),
        ],
        string='Requisition Action',
        default='internal',
        required=False,
    )
    partner_id = fields.Many2many('res.partner', string="Vendor")
    job_cost_id = fields.Many2one('job.costing', string="Job Cost")
    cost_line_id = fields.Many2one('job.cost.line')


