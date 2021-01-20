from odoo import api, models, fields


class ProductCategory(models.Model):
    _inherit = 'product.category'

    """def unlink(self):
        for binding in self.prestashop_bind_ids:
            with binding.backend_id.work_on('prestashop.product.category') as work:
                deleter = work.component(usage='record.export.deleter')
                deleter.run('categories', binding.id)
        super(ProductCategory, self).unlink()"""


class PrestashopProductCategory(models.Model):
    _inherit = 'prestashop.product.category'

    def unlink(self):
        for category in self:
            with category.backend_id.work_on('prestashop.product.category') as work:
                deleter = work.component(usage='record.export.deleter')
                deleter.run('categories', category.id)
        super(PrestashopProductCategory, self).unlink()

