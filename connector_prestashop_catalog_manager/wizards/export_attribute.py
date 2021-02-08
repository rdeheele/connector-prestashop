# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class PrestashopExportAttribute(models.TransientModel):
    _name = 'wiz.prestashop.export.attribute'

    def _default_backend(self):
        return self.env['prestashop.backend'].search([], limit=1).id

    def _default_shop(self):
        return self.env['prestashop.shop'].search([], limit=1).id

    backend_id = fields.Many2one(
        comodel_name='prestashop.backend',
        default=_default_backend,
        string='Backend',
    )
    shop_id = fields.Many2one(
        comodel_name='prestashop.shop',
        default=_default_shop,
        string='Shop',
    )

    def export_attributes(self):
        self.ensure_one()
        attribute_obj = self.env['product.attribute']
        ps_attribute_obj = self.env['prestashop.product.combination.option']
        for attribute in attribute_obj.browse(self.env.context['active_ids']):
            ps_attribute = ps_attribute_obj.search([
                ('odoo_id', '=', attribute.id),
                ('backend_id', '=', self.backend_id.id)
            ])
            if not ps_attribute:
                ps_attribute = ps_attribute_obj.create({
                    'backend_id': self.backend_id.id,
                    'odoo_id': attribute.id,
                })

    def export_values(self):
        self.ensure_one()
        attribute_obj = self.env['product.attribute']
        ps_attribute_obj = self.env['prestashop.product.combination.option']
        value_obj = self.env['product.attribute.value']
        ps_value_obj = self.env['prestashop.product.combination.option.value']
        for attribute in attribute_obj.browse(self.env.context['active_ids']):
            ps_attribute = ps_attribute_obj.search([
                ('odoo_id', '=', attribute.id),
                ('backend_id', '=', self.backend_id.id)
            ])
            if ps_attribute:
                if attribute.value_ids:
                    for value in attribute.value_ids:
                        ps_value = ps_value_obj.search([('odoo_id','=',value.id)])
                        if not ps_value:
                            ps_value_obj.create({
                                'backend_id': self.backend_id.id,
                                'odoo_id': value.id})
