from odoo.addons.component.core import Component


class PrestashopProductCombinationOptionListener(Component):
    _name = 'prestashop.product.combination.option.listener'
    _inherit = 'base.connector.listener'
    _apply_on = ['prestashop.product.combination.option']

    def on_record_write(self, record, fields=None):
        if not 'prestashop_id' in fields:
            with record.backend_id.work_on(record._name) as work:
                exporter = work.component(usage='record.exporter')
                return exporter.run(record)


class ProductAttributeListener(Component):
    _name = 'product.attribute.listener'
    _inherit = 'base.connector.listener'
    _apply_on = ['product.attribute']

    def on_record_write(self, record, fields=None):
        for binding in record.prestashop_bind_ids:
            binding.with_delay().export_record()


class PrestashopProductCombinationOptionValueListener(Component):
    _name = 'prestashop.product.combination.option.value.listener'
    _inherit = 'base.connector.listener'
    _apply_on = ['prestashop.product.combination.option.value']

    def on_record_write(self, record, fields=None):
        if not 'prestashop_id' in fields:
            with record.backend_id.work_on(record._name) as work:
                exporter = work.component(usage='record.exporter')
                return exporter.run(record)


class ProductAttributeValueListener(Component):
    _name = 'product.attribute.value.listener'
    _inherit = 'base.connector.listener'
    _apply_on = ['product.attribute.value']

    def on_record_write(self, record, fields=None):
        for binding in record.prestashop_bind_ids:
            binding.with_delay().export_record()
