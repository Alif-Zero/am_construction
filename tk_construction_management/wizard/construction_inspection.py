# -*- coding: utf-8 -*-
# Copyright 2020 - Today Techkhedut.
# Part of Techkhedut. See LICENSE file for full copyright and licensing details.
from odoo import models, api, fields


class ConstructionInspection(models.TransientModel):
    _name = "construction.inspection"
    _description = "Construction Inspection "

    name = fields.Char(string="Title")
    user_ids = fields.Many2many('res.users', string="Assignee")
    date = fields.Date(string="Date", default=fields.Date.today())
    deadline = fields.Date(string="Deadline")
    construction_id = fields.Many2one('construction.details', string="Construction")
    desc = fields.Html(string="Description")

    def action_create_task(self):
        record = {
            'name': self.name,
            'project_id': self.construction_id.project_id.id,
            'construction_id': self.construction_id.id,
            'is_inspection_task': True,
            'partner_id': self.construction_id.customer_company_id.id,
            'date_deadline': self.deadline,
            'description': self.desc,
            'user_ids': [(6, 0, self.user_ids.ids)]
        }
        task_id = self.env['project.task'].create(record)
        inspection_record = {
            'date': self.date,
            'note': self.name,
            'construction_id': self.construction_id.id,
            'date_deadline': self.deadline,
            'task_id': task_id.id
        }
        self.env['site.inspection'].create(inspection_record)
