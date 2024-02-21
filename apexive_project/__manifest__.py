# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Check in Screen with select Project and Task',
    'version': '16.0.0.1',
    'category': 'HR',
    'sequence': 20,
    'author': 'Bansi Patel',
    'summary': 'Check in/Check out modification',
    'depends': ['hr_attendance','project'],
    'data': [
        'views/attendance_view.xml',
    ],
    'qweb': [],
    'installable': True,
    'auto_install': True,
    'license': 'LGPL-3',
    'assets': {
        'web.assets_backend': [
            'apexive_project/static/src/js/attendance.js',
            'apexive_project/static/src/xml/**/*',
        ],
    },
}
