# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    def _get_related_lot_ids(self):
        self.ensure_one()
        domain = [('sale_order_id','=',self.id)]
        # FIXME : we have to avoid this "filtered" and find a solution to add the filter to the domain or to make a direct sql query for the sake of performance
        production_orders = self.env['mrp.production.sale.order'].search(domain).mapped("mrp_production_id")
        lot_ids = production_orders.mapped("finished_move_line_ids").mapped('lot_id')
        return lot_ids