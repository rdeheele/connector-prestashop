# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.connector.components.mapper import mapping
from odoo.addons.component.core import Component

from odoo.addons.connector_prestashop.components.exporter import (
    TranslationPrestashopExporter,
    PrestashopExporter,
)
from odoo.addons.connector_prestashop.components.mapper import \
    TranslationPrestashopExportMapper
#from openerp.addons.connector_prestashop.backend import prestashop
from collections import OrderedDict
import logging


_logger = logging.getLogger(__name__)


class ProductCombinationExporter(Component):
    _name = 'prestashop.product.combination.exporter'
    _inherit = 'prestashop.exporter'
    _apply_on = ['prestashop.product.combination']

    def _create(self, record):
        res = super(ProductCombinationExporter, self)._create(record)
        return res['prestashop']['combination']['id']

    """def _export_images(self):
        if self.binding.image_ids:
            image_binder = self.binder_for('prestashop.product.image')
            for image_line in self.binding.image_ids:
                image_ext_id = image_binder.to_backend(
                    image_line.id, wrap=True)
                if not image_ext_id:
                    image_ext_id = \
                        self.session.env['prestashop.product.image']\
                            .with_context(connector_no_export=True).create({
                                'backend_id': self.backend_record.id,
                                'odoo_id': image_line.id,
                            }).id
                    image_content = getattr(image_line, "_get_image_from_%s" %
                                            image_line.storage)()
                    export_record(
                        self.session,
                        'prestashop.product.image',
                        image_ext_id,
                        image_content)"""

    """def _export_dependencies(self):
        # TODO add export of category
        attribute_binder = self.binder_for(
            'prestashop.product.combination.option')
        option_binder = self.binder_for(
            'prestashop.product.combination.option.value')
        Option = self.env['prestashop.product.combination.option']
        OptionValue = self.env['prestashop.product.combination.option.value']
        for value in self.binding.attribute_value_ids:
            prestashop_option_id = attribute_binder.to_backend(
                value.attribute_id.id, wrap=True)
            if not prestashop_option_id:
                option_binding = Option.search(
                    [('backend_id', '=',  self.backend_record.id),
                     ('odoo_id', '=', value.attribute_id.id)])
                if not option_binding:
                    option_binding = Option.with_context(
                        connector_no_export=True).create({
                            'backend_id': self.backend_record.id,
                            'odoo_id': value.attribute_id.id})
                export_record(self.session,
                              'prestashop.product.combination.option',
                              option_binding.id)
            prestashop_value_id = option_binder.to_backend(
                value.id, wrap=True)
            if not prestashop_value_id:
                value_binding = OptionValue.search(
                    [('backend_id', '=',  self.backend_record.id),
                     ('odoo_id', '=', value.id)]
                )
                if not value_binding:
                    option_binding = Option.search(
                        [('backend_id', '=',  self.backend_record.id),
                         ('odoo_id', '=', value.attribute_id.id)])
                    value_binding = OptionValue.with_context(
                        connector_no_export=True).create({
                            'backend_id': self.backend_record.id,
                            'odoo_id': value.id,
                            'id_attribute_group': option_binding.id})
                export_record(
                    self.session,
                    'prestashop.product.combination.option.value',
                    value_binding.id)
        # self._export_images()"""

    def update_quantities(self):
        """self.binding.odoo_id.with_context(
            self.session.context).update_prestashop_qty()"""

    def _after_export(self):
        self.update_quantities()


class ProductCombinationExportMapper(Component):
    _name = 'prestashop.product.combination.export.mapper'
    _inherit = 'translation.prestashop.export.mapper'
    _apply_on = ['prestashop.product.combination']

    direct = [
        ('default_code', 'reference'),
        ('active', 'active'),
        ('barcode', 'ean13'),
        ('minimal_quantity', 'minimal_quantity'),
        ('weight', 'weight'),
    ]

    def _get_factor_tax(self, tax):
        factor_tax = tax.price_include and (1 + tax.amount / 100) or 1.0
        return factor_tax

    @mapping
    def combination_default(self, record):
        return {'default_on': int(record['default_on'])}

    def get_main_template_id(self, record):
        template_binder = self.binder_for('prestashop.product.template')
        return template_binder.to_external(record.main_template_id.id)

    @mapping
    def main_template_id(self, record):
        return {'id_product': self.get_main_template_id(record)}

    @mapping
    def _unit_price_impact(self, record):
        tax = record.taxes_id[:1]
        if tax.price_include and tax.amount_type == 'percent':
            # 6 is the rounding precision used by PrestaShop for the
            # tax excluded price.  we can get back a 2 digits tax included
            # price from the 6 digits rounded value
            return {
                'price': round(
                    record.impact_price / self._get_factor_tax(tax), 6)
            }
        else:
            return {'price': record.impact_price}

    @mapping
    def cost_price(self, record):
        return {'wholesale_price': record.standard_price}

    def _get_product_option_value(self, record):
        option_value = []
        option_binder = self.binder_for(
            'prestashop.product.combination.option.value')
        for value in record.product_template_attribute_value_ids:
            value_id = value.product_attribute_value_id.id
            value_ext_id = option_binder.to_external(value_id, wrap=True)
            if value_ext_id:
                option_value.append({'id': value_ext_id})
        return option_value

    def _get_combination_image(self, record):
        images = []
        image_binder = self.binder_for('prestashop.product.image')
        for image in record.image_ids:
            image_ext_id = image_binder.to_external(image.id, wrap=True)
            if image_ext_id:
                images.append({'id': image_ext_id})
        return images

    @mapping
    def associations(self, record):
        associations = OrderedDict([
            ('product_option_values',
                {'product_option_value':
                 self._get_product_option_value(record)}),
        ])
        image = self._get_combination_image(record)
        if image:
            associations['images'] = {
                'image': self._get_combination_image(record)
            }
        return {'associations': associations}


class ProductCombinationOptionExporter(Component):
    _name = 'prestashop.product.combination.option.exporter'
    _inherit = 'prestashop.exporter'
    _apply_on = ['prestashop.product.combination.option']

    def _create(self, record):
        res = super(ProductCombinationOptionExporter, self)._create(record)
        return res['prestashop']['product_option']['id']


class ProductCombinationOptionExportMapper(Component):
    _name = 'prestashop.product.combination.option.export.mapper'
    _inherit = 'translation.prestashop.export.mapper'
    _apply_on = ['prestashop.product.combination.option']

    direct = [
        ('prestashop_position', 'position'),
        ('display_type', 'group_type'),
    ]

    _translatable_fields = [
        ('name', 'name'),
        ('name', 'public_name'),
    ]


#@prestashop
class ProductCombinationOptionValueExporter(Component):
    _name = 'prestashop.product.combination.option.value.exporter'
    _inherit = 'prestashop.exporter'
    _apply_on = ['prestashop.product.combination.option.value']

    def _create(self, record):
        res = super(ProductCombinationOptionValueExporter, self)._create(record)
        return res['prestashop']['product_option_value']['id']

    """def _export_dependencies(self):
        attribute_id = self.binding.attribute_id.id
        # export product attribute
        binder = self.binder_for('prestashop.product.combination.option')
        if not binder.to_backend(attribute_id, wrap=True):
            exporter = self.get_connector_unit_for_model(
                TranslationPrestashopExporter,
                'prestashop.product.combination.option')
            exporter.run(attribute_id)
        return"""


class ProductCombinationOptionValueExportMapper(Component):
    _name = 'prestashop.product.combination.option.value.export.mapper'
    _inherit = 'translation.prestashop.export.mapper'
    _apply_on = ['prestashop.product.combination.option.value']

    direct = [('name', 'value')]
    # handled by base mapping `translatable_fields`
    _translatable_fields = [
        ('name', 'name'),
    ]

    """@mapping
    def prestashop_product_attribute_id(self, record):
        attribute_binder = self.binder_for(
            'prestashop.product.combination.option.value')
        return {
            'id_feature': attribute_binder.to_backend(
                record.attribute_id.id, wrap=True)
        }"""

    @mapping
    def prestashop_product_group_attribute_id(self, record):
        attribute_binder = self.binder_for(
            'prestashop.product.combination.option')
        return {
            'id_attribute_group': attribute_binder.to_external(
                record.attribute_id.id, wrap=True),
        }
