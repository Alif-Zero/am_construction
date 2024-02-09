# -*- coding: utf-8 -*-
# Copyright 2020 - Today Techkhedut.
# Part of Techkhedut. See LICENSE file for full copyright and licensing details.
from odoo import fields, api, models


class ConstructionPo(models.Model):
    _inherit = 'purchase.order'

    construction_id = fields.Many2one('construction.details', string='Construction')
    order_type = fields.Selection([('equipment', 'Equipment'), ('material', 'Material')], string="Order Type")
    material_id = fields.Many2one('construction.material', string='Material')
    equipment_id = fields.Many2one('construction.equipment', string='Equipment')

    def _prepare_invoice(self):
        res = super(ConstructionPo, self)._prepare_invoice()
        if self.construction_id:
            res['construction_id'] = self.construction_id.id
            res['order_type'] = self.order_type
        return res


class ConstructionBills(models.Model):
    _inherit = 'account.move'

    construction_id = fields.Many2one('construction.details', string="Construction")
    order_type = fields.Selection([('equipment', 'Equipment'), ('material', 'Material'), ('labour', 'Labour Bill'),
                                   ('eng_arc', 'Engineer & Architect'), ('expense', 'Expense'),
                                   ('insurance', 'Risk & Insurance')],
                                  string="Bill")
