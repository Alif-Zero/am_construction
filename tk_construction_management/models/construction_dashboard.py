# -*- coding: utf-8 -*-
# Copyright 2020 - Today Techkhedut.
# Part of Techkhedut. See LICENSE file for full copyright and licensing details.
from odoo import fields, api, models


class ConstructionDashboard(models.Model):
    _name = 'construction.dashboard'
    _description = "Construction Dashboard"

    @api.model
    def get_construction_stats(self):
        construction_obj = self.env['construction.details'].sudo()
        total_site = self.env['construction.site'].search_count([])
        planning_site = self.env['job.costing'].search_count([('state', '=', 'planning')])
        job_order = construction_obj.search_count([('stage', '=', 'confirm')])
        document_verified = construction_obj.search_count([('stage', '=', 'a_costing')])
        site_in_progress = construction_obj.search_count([('stage', '=', 'in_progress')])
        complete_site = construction_obj.search_count([('stage', '=', 'done')])
        close_site = construction_obj.search_count([('stage', '=', 'close')])
        cancel_site = construction_obj.search_count([('stage', '=', 'cancel')])
        site_state = [['Job Order', 'Document Verified', 'In Progress', 'Complete', 'Close', 'Cancel'],
                      [job_order, document_verified, site_in_progress, complete_site, close_site, cancel_site]]
        data = {
            'total_site': total_site,
            'planning_site': planning_site,
            'job_order': job_order,
            'site_in_progress': site_in_progress,
            'complete_site': complete_site + close_site,
            'site_state': site_state,
            'construction_time_line': self.construction_time_line(),
            'material_equipment_po': self.material_equipment_po()
        }
        site, site_count = [], []
        site_ids = self.env['site.type'].search([])
        if not site_ids:
            data['site_type'] = [[], []]
        for s in site_ids:
            site_data = self.env['construction.site'].sudo().search_count([('site_type_id', '=', s.id)])
            site_count.append(site_data)
            site.append(s.name)
        data['site_type'] = [site, site_count]

        return data

    def construction_time_line(self):
        site_data = []
        construction_site_data = self.env['construction.details'].search([])
        for site in construction_site_data:
            if site.stage == "in_progress":
                site_data.append({
                    'name': str(site.name) + " " + str(site.site_id.name),
                    'start_date': str(site.start_date),
                    'end_date': str(site.end_date),
                })
        return site_data

    def material_equipment_po(self):
        site_name = []
        equipment_po = []
        material_po = []
        construction_site = self.env['construction.details'].sudo().search([])
        for site in construction_site:
            if site.stage == "in_progress":
                site_name.append(site.site_id.name)
                equipment_po.append(site.equip_po_count)
                material_po.append(site.material_po_count)
        data = [site_name, equipment_po, material_po]
        return data
