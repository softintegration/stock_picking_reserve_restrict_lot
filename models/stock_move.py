# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_available_quantity(self, location_id, lot_id=None, package_id=None, owner_id=None, strict=False,
                                allow_negative=False):
        self.ensure_one()
        restricted_lots = []
        if self.sale_line_id and self.product_id.tracking == 'lot':
            lot_ids = self.sale_line_id.order_id._get_related_lot_ids()
            # if no lot have been found we should return 0 because this is a restriction filter not a preference one
            if not lot_ids:
                return 0
            else:
                self = self.with_context(forced_lots=lot_ids.ids)
        return super(StockMove, self)._get_available_quantity(location_id, lot_id=lot_id, package_id=package_id,
                                                              owner_id=owner_id, strict=strict,
                                                              allow_negative=allow_negative)

    def _update_reserved_quantity(self, need, available_quantity, location_id, lot_id=None, package_id=None,
                                      owner_id=None, strict=True):
        self.ensure_one()
        if self.sale_line_id and self.product_id.tracking == 'lot':
            lot_ids = self.sale_line_id.order_id._get_related_lot_ids()
            # if no lot have been found we should return 0 because this is a restriction filter not a preference one
            if not lot_ids:
                return 0
            else:
                self = self.with_context(forced_lots=lot_ids.ids)
        return super(StockMove,self)._update_reserved_quantity(need,available_quantity,location_id,lot_id=lot_id,
                                                                   package_id=package_id,owner_id=owner_id,strict=strict)