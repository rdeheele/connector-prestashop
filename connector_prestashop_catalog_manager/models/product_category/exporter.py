# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.connector.components.mapper import mapping
from odoo.addons.component.core import Component

from odoo.addons.connector_prestashop.components.exporter import (
    PrestashopExporter,
)

from odoo.addons.connector_prestashop.components.mapper import (
    TranslationPrestashopExportMapper,
)
#from ...consumer import get_slug
#from openerp.addons.connector_prestashop.backend import prestashop


#@prestashop
class ProductCategoryExporter(Component):
    _name = 'prestashop.product.category.exporter'
    _inherit = 'prestashop.exporter'
    _apply_on = ['prestashop.product.category']

    """def _export_dependencies(self):
        category_binder = self.binder_for('prestashop.product.category')
        categories_obj = self.session.env['prestashop.product.category']
        for category in self.binding:
            self.export_parent_category(
                category.odoo_id.parent_id, category_binder, categories_obj)"""

    """def export_parent_category(self, category, binder, ps_categ_obj):
        if not category:
            return
        ext_id = binder.to_backend(category.id, wrap=True)
        if ext_id:
            return ext_id
        res = {
            'backend_id': self.backend_record.id,
            'odoo_id': category.id,
            'link_rewrite': get_slug(category.name),
        }
        category_ext_id = ps_categ_obj.with_context(
            connector_no_export=True).create(res)
        parent_cat_id = export_record(
            self.session, 'prestashop.product.category', category_ext_id.id)
        return parent_cat_id"""


class ProductCategoryExportMapper(Component):
    _name = 'prestashop.product.category.export.mapper'
    _inherit = 'translation.prestashop.export.mapper'
    _apply_on = ['prestashop.product.category']

    direct = [
        ('active', 'active')
    ]
    """
        ('sequence', 'position'),
        ('default_shop_id', 'id_shop_default'),
        ('active', 'active'),
        ('position', 'position')
    ]"""
    # handled by base mapping `translatable_fields`
    _translatable_fields = [
        ('name', 'name'),
        ('link_rewrite', 'link_rewrite'),
        ('description', 'description'),
        ('meta_description', 'meta_description'),
        ('meta_keywords', 'meta_keywords'),
        ('meta_title', 'meta_title'),
    ]

    @mapping
    def parent_id(self, record):
        category_binder = self.binder_for('prestashop.product.category')
        ext_categ_id = category_binder.to_external(
            record.parent_id.id, wrap=True)
        if ext_categ_id:
            import logging
            logging.info('id_parent:')
            logging.info(ext_categ_id)
            return {'id_parent': ext_categ_id}
