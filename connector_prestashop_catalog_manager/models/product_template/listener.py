from odoo.addons.component.core import Component


class PrestashopTemplateBindingExportListener(Component):
    _name = 'prestashop.template.binding.export.listener'
    _inherit = 'base.connector.listener'
    _apply_on = ['prestashop.product.template']

    def on_record_write(self, record, fields=None):
        if not 'prestashop_id' in fields:
            with record.backend_id.work_on(record._name) as work:
                exporter = work.component(usage='template.exporter')
                return exporter.run(record)

    def on_record_create(self, record, fields=None):
        with record.backend_id.work_on(record._name) as work:
            exporter = work.component(usage='template.exporter')
            return exporter.run(record)


class PrestashopTemplateExportListener(Component):
    _name = 'prestashop.template.export.listener'
    _inherit = 'base.connector.listener'
    _apply_on = ['product.template']

    def on_record_write(self, record, fields=None):
        for binding in record.prestashop_bind_ids:
            with binding.backend_id.work_on('prestashop.product.template') as work:
                exporter = work.component(usage='template.exporter')
                return exporter.run(binding)
