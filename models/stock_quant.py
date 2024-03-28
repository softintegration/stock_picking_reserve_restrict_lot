# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.osv import expression


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def _gather(self, product_id, location_id, lot_id=None, package_id=None, owner_id=None, strict=False):
        removal_strategy = self._get_removal_strategy(product_id, location_id)
        removal_strategy_order = self._get_removal_strategy_order(removal_strategy)

        domain = [('product_id', '=', product_id.id)]
        if self.env.context.get('forced_lots',False):
            domain.append(('lot_id','in',self.env.context['forced_lots']))
        if not strict:
            if lot_id:
                domain = expression.AND([['|', ('lot_id', '=', lot_id.id), ('lot_id', '=', False)], domain])
            if package_id:
                domain = expression.AND([[('package_id', '=', package_id.id)], domain])
            if owner_id:
                domain = expression.AND([[('owner_id', '=', owner_id.id)], domain])
            domain = expression.AND([[('location_id', 'child_of', location_id.id)], domain])
        else:
            domain = expression.AND(
                [['|', ('lot_id', '=', lot_id.id), ('lot_id', '=', False)] if lot_id else [('lot_id', '=', False)],
                 domain])
            domain = expression.AND([[('package_id', '=', package_id and package_id.id or False)], domain])
            domain = expression.AND([[('owner_id', '=', owner_id and owner_id.id or False)], domain])
            domain = expression.AND([[('location_id', '=', location_id.id)], domain])

        return self.search(domain, order=removal_strategy_order).sorted(lambda q: not q.lot_id)