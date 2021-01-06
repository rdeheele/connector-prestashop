from odoo.addons.component.core import Component


class PrestashopProductCategoryListener(Component):
    _name = 'prestashop.product.category.listener'
    _inherit = 'base.connector.listener'
    _apply_on = ['prestashop.product.category']

    def on_record_write(self, record, fields=None):
        print('on_record_write prestashop.product.category')
        if not 'prestashop_id' in fields:
            with record.backend_id.work_on(record._name) as work:
                exporter = work.component(usage='record.exporter')
                return exporter.run(record)
                #record.export_record()


class ProductCategoryListener(Component):
    _name = 'product.category.listener'
    _inherit = 'base.connector.listener'
    _apply_on = ['product.category']

    def on_record_write(self, record, fields=None):
        print('on_record_write prestashop.product.category')
        for binding in record.prestashop_bind_ids:
            binding.with_delay().export_record()
