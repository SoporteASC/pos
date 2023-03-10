# -*- coding: utf-8 -*-
# Copyright 2019 PlanetaTIC - Marc Poch <mpoch@planetatic.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models, tools


class PosOrderReport(models.Model):
    _inherit = "report.pos.order"
    _auto = False

    config_id = fields.Many2one('pos.config', string='Point of Sale',
                                readonly=True)
    product_brand_id = fields.Many2one(
        'product.brand',
        string='Brand',
    )

    @api.model_cr
    def init(self):
        # This method is fully rewritten and does not call its super.
        # In future versions of pos module it could be great to
        # split init method of report.pos.order model in different
        # methods like "_select" and "_from" to avoid overwrite the full method
        tools.drop_view_if_exists(self._cr, 'report_pos_order')
        self._cr.execute("""
            CREATE OR REPLACE VIEW report_pos_order AS (
                SELECT
                    MIN(l.id) AS id,
                    COUNT(*) AS nbr_lines,
                    s.date_order AS date,
                    SUM(l.qty) AS product_qty,
                    SUM(l.qty * l.price_unit) AS price_sub_total,
                    SUM(
(l.qty * l.price_unit) * (100 - l.discount) / 100) AS price_total,
                    SUM(
(l.qty * l.price_unit) * (l.discount / 100)) AS total_discount,
                    (SUM(
l.qty*l.price_unit)/SUM(l.qty * u.factor))::decimal AS average_price,
                    SUM(
cast(to_char(date_trunc('day',s.date_order) - date_trunc(
'day',s.create_date),'DD') AS INT)) AS delay_validation,
                    s.id as order_id,
                    s.partner_id AS partner_id,
                    s.state AS state,
                    s.user_id AS user_id,
                    s.location_id AS location_id,
                    s.company_id AS company_id,
                    s.sale_journal AS journal_id,
                    l.product_id AS product_id,
                    pt.categ_id AS product_categ_id,
                    p.product_tmpl_id,
                    ps.config_id,
                    pt.pos_categ_id,
                    pc.stock_location_id,
                    s.pricelist_id,
                    s.session_id,
                    s.invoice_id IS NOT NULL AS invoiced,
                    pt.product_brand_id
                FROM pos_order_line AS l
                    LEFT JOIN pos_order s ON (s.id=l.order_id)
                    LEFT JOIN product_product p ON (l.product_id=p.id)
                    LEFT JOIN product_template pt ON (p.product_tmpl_id=pt.id)
                    LEFT JOIN product_uom u ON (u.id=pt.uom_id)
                    LEFT JOIN pos_session ps ON (s.session_id=ps.id)
                    LEFT JOIN pos_config pc ON (ps.config_id=pc.id)
                GROUP BY
                    s.id, s.date_order, s.partner_id,s.state, pt.categ_id,
                    s.user_id, s.location_id, s.company_id, s.sale_journal,
                    s.pricelist_id, s.invoice_id, s.create_date, s.session_id,
                    l.product_id,
                    pt.categ_id, pt.pos_categ_id,
                    p.product_tmpl_id,
                    ps.config_id,
                    pc.stock_location_id,
                    pt.product_brand_id
                HAVING
                    SUM(l.qty * u.factor) != 0
            )
        """)
