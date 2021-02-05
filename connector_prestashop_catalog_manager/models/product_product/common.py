# -*- coding: utf-8 -*-
# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields
from odoo.addons.queue_job.job import job, related_action


class PrestashopProductCombination(models.Model):
    _inherit = 'prestashop.product.combination'
    minimal_quantity = fields.Integer(
        string='Minimal Quantity',
        default=1,
        help='Minimal Sale quantity',
    )

    @job(default_channel='root.prestashop')
    @related_action(action='related_action_unwrap_binding')
    def export_record(self):
        self.ensure_one()
        with self.backend_id.work_on(self._name) as work:
            exporter = work.component(usage='record.exporter')
            return exporter.run(self)
