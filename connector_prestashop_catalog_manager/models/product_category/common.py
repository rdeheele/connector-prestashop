from odoo import api, models, fields


class ProductCategory(models.Model):
    _inherit = 'product.category'

    def unlink(self):
        for binding in self.prestashop_bind_ids:
            with binding.backend_id.work_on('prestashop.product.category') as work:
                deleter = work.component(usage='record.export.deleter')
                deleter.run('categories', binding.id)
        super(ProductCategory, self).unlink()
