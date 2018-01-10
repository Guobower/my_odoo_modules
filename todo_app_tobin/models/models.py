# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class todo_app_tobin(models.Model):
#     _name = 'todo_app_tobin.todo_app_tobin'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class TodoTask(models.Model):
    _name = "tobin_todo.task"
    _description = "To-do Task"

    name = fields.Char("Description", required=True)
    is_done = fields.Boolean(string="Fait ?")
    active = fields.Boolean(string="Active ?", default=True)

    @api.model
    def do_clear_done(self):
        dones = self.search([('is_done', '=', True)])
        dones.write({'active': False})
        return True

    @api.multi
    def do_toggle_done(self):
        for task in self:
            task.is_done = not task.is_done
        return True

