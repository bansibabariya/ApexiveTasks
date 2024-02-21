# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, modules

class InheritHRAttendance(models.Model):
    _inherit = 'hr.attendance'

    project_id = fields.Many2one('project.project', string="Project")
    project_task_id = fields.Many2one('project.task', string="Task", domain="[('project_id','!=',False), ('project_id','=',project_id), ('is_closed','=',False)]")
    description = fields.Text(string="Descriptions")

class InheritHREmployee(models.Model):
    _inherit = 'hr.employee'

    attendance_project_id = fields.Many2one('project.project',
        string="Attendance Project", compute='_compute_project')
    attendance_project_task_id = fields.Many2one('project.task',
        string="Attendance Project Task", compute='_compute_project')
    attendance_description = fields.Text(string="Attendance Descriptions", compute='_compute_project')

    # Get Projects
    @api.model
    def get_attendance_projects(self, domain):
        projects = self.env['project.project'].search([])
        tasks = projects.mapped('task_ids')
        emp_id = self.search(domain, limit=1)
        return {
            'project_ids': [{'id': x.id, 'name': x.display_name} for x in projects if len(x.task_ids) > 0],
            'project_task_ids': [{'id': x.id, 'name': x.display_name, 'project_id': x.project_id.id} for x in tasks],
            'current_project_id': {'id': emp_id.attendance_project_id.id,
                                   'name': emp_id.attendance_project_id.display_name} if emp_id.attendance_project_id and emp_id.attendance_project_id.id in projects.ids else False,
            'current_project_task_id': {'id': emp_id.attendance_project_task_id.id,
                                        'name': emp_id.attendance_project_task_id.display_name} if emp_id.attendance_project_task_id and emp_id.attendance_project_task_id.id in tasks.ids else False,
            'current_description': emp_id.attendance_description or False,
        }

    # Compute for projects
    @api.depends('last_attendance_id.check_in', 'last_attendance_id.check_out', 'last_attendance_id')
    def _compute_project(self):
        for employee in self:
            att = employee.last_attendance_id.sudo()
            attendance_state = att and not att.check_out and 'checked_in' or 'checked_out'
            if attendance_state == 'checked_in':
                employee.attendance_project_id = att.project_id
                employee.attendance_project_task_id = att.project_task_id
                employee.attendance_description = att.description
            else:
                employee.attendance_project_id = False
                employee.attendance_project_task_id = False
                employee.attendance_description = False

    # Override this method for project, task and des to update
    def _attendance_action_change(self):
        rec = super(InheritHREmployee, self)._attendance_action_change()
        project_id = self.env.context.get('project_id', False)
        project_task_id = self.env.context.get('project_task_id', False)
        attend_description = self.env.context.get('attend_description', False)
        values = {
            'project_id': int(project_id) if project_id else False,
            'project_task_id': int(project_task_id) if project_task_id else False,
            'description': str(attend_description) if attend_description else False
        }
        rec.update(values)
        return rec