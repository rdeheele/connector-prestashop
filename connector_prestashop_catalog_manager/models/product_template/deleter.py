from odoo.addons.component.core import Component


class ProductTemplateDeleter(Component):
    _name = 'prestashop.template.exporter.deleter'
    _inherit = 'prestashop.deleter'
    _apply_on = 'prestashop.product.template'
    _usage = 'record.export.deleter'
