from odoo.addons.component.core import Component


class ProductCategoryDeleter(Component):
    _name = 'prestashop.category.exporter.deleter'
    _inherit = 'prestashop.deleter'
    _apply_on = 'prestashop.product.category'
    _usage = 'record.export.deleter'
