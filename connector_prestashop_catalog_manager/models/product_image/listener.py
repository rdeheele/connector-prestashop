from odoo.addons.component.core import Component
from odoo.addons.component_event import skip_if


class PrestashopProductImageBindingExportListener(Component):
    _name = 'prestashop.product.image.binding.export.listener'
    _inherit = 'base.connector.listener'
    _apply_on = ['prestashop.product.image']

    def on_record_create(self, record, fields=None):
        record.with_delay().export_record()

    def on_record_write(self, record, fields=None):
        print('w1')
        print(fields)
        if 'name' in fields:
            record.with_delay().export_record()


class PrestashopProductImageExportListener(Component):
    _name = 'prestashop.product.image.export.listener'
    _inherit = 'base.connector.listener'
    _apply_on = ['base_multi_image.image']

    def on_record_write(self, record, fields=None):
        print('w2')
        print(fields)
        if 'name' in fields:
            for binding in record.prestashop_bind_ids:
                binding.with_delay().export_record()
