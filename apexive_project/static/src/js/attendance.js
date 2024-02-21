odoo.define('apexive_project.inherit_my_attendance', function (require) {
    "use strict";

    var Attendances = require('hr_attendance.my_attendances');
    var session = require('web.session');

    Attendances.include({
        events: Object.assign({}, Attendances.prototype.events, {
            'change #project': '_onChangeProject',
        }),

        // onchange for project to get task
        _onChangeProject: function (ev) {
            if (this.$("#project")[0]) {
                const project_id= this.$("select[name='project_id']").val();
                var selectHtml = '<select class="col-7" name="project_task_id" id="projectTask"  style="min-width: 255px;border: 1px solid #ddd;height: 35px;border-radius: 3px;">';
                selectHtml = selectHtml + '<option selected="selected" value=""></option>';
                for (const task of this.projects.project_task_ids) {
                    if (task.project_id == project_id) {
                        selectHtml = selectHtml + "<option value='" + task.id + "'" + ">" + task.name + "</option>";
                    }
                }
                selectHtml += "</select>";
                this.$("#projectTask").replaceWith(selectHtml);
            }
        },

        willStart: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                return self._rpc({
                    model: 'hr.employee',
                    method: 'get_attendance_projects',
                    args: [[['user_id', '=', self.getSession().uid]]],
                    context: session.user_context,
                }).then(function (p) {
                    self.projects = p;
                });
            });
        },

        update_attendance: function () {
            var self = this;
            var context = session.user_context;
            var project_id = this.$("select[name='project_id']").val();
            var project_task_id = this.$("select[name='project_task_id']").val();
            var attend_description = this.$("textarea[id='attend_description']").val();
            context['project_id'] = project_id;
            context['project_task_id'] = project_task_id;
            context['attend_description'] = attend_description;

            this._rpc({
                model: 'hr.employee',
                method: 'attendance_manual',
                args: [[self.employee.id], 'hr_attendance.hr_attendance_action_my_attendances'],
                context: context,
            })
                .then(function (result) {
                    if (result.action) {
                        self.do_action(result.action);
                    } else if (result.warning) {
                        self.displayNotification({ title: result.warning, type: 'danger' });
                    }
                });
        },
    });
    return Attendances;
});
