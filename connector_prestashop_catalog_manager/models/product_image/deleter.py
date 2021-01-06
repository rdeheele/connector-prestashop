from odoo.addons.component.core import Component


class ProductImageDeleter(Component):
    _name = 'prestashop.image.exporter.deleter'
    _inherit = 'prestashop.deleter'
    _apply_on = 'prestashop.product.image'
    _usage = 'record.export.deleter'
