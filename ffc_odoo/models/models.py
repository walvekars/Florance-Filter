# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class ffc_odoo(models.Model):
#     _name = 'ffc_odoo.ffc_odoo'
#     _description = 'ffc_odoo.ffc_odoo'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

