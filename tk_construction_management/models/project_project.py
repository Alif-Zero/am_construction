# -*- coding: utf-8 -*-
# Copyright 2020 - Today Techkhedut.
# Part of Techkhedut. See LICENSE file for full copyright and licensing details.
from odoo import fields, api, models


class ConstructionProject(models.Model):
    _inherit = 'project.project'

    construction_id = fields.Many2one('construction.details', string="Construction")
    image = fields.Binary(string='Company Logo')


class ConstructionProjectTask(models.Model):
    _inherit = 'project.task'

    construction_id = fields.Many2one(related="project_id.construction_id", string="Construction", store=True)
    labours_ids = fields.Many2many('hr.employee')
    color = fields.Integer(string="Color")
    is_inspection_task = fields.Boolean(string="Inspection Task")

    @api.onchange('construction_id')
    def onchange_construction_id(self):
        for rec in self:
            ids = []
            if rec.construction_id:
                for data in rec.construction_id.construction_labours_ids:
                    for id in data.labours_ids:
                        ids.append(id.id)
            return {'domain': {'labours_ids': [('id', 'in', ids)]}}


class ConstructionTaskStages(models.Model):
    _inherit = 'project.task.type'

    is_construction_stages = fields.Boolean(string="Construction Stage")


class ConstructionMeeting(models.Model):
    _inherit = 'calendar.event'

    construction_id = fields.Many2one('construction.details', string="Construction")
    is_construction_meeting = fields.Boolean(string="Construction Meeting")


