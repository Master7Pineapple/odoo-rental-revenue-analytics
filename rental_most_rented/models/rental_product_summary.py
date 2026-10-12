from odoo import fields, models, tools


class RentalProductSummary(models.Model):
    """One row per product, aggregated over all confirmed rentals (all time).

    Correct distinct order count per product (impossible as a plain sum on the
    line-level report). Built for exporting product / quantity / lines / orders.
    """
    _name = 'rental.product.summary'
    _description = 'Rented Products Summary'
    _auto = False
    _rec_name = 'product_id'
    _order = 'total_qty desc'

    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    product_tmpl_id = fields.Many2one('product.template', string='Product Template', readonly=True)
    categ_id = fields.Many2one('product.category', string='Product Category', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    total_qty = fields.Float(string='Quantity Rented', readonly=True)
    line_count = fields.Integer(string='Rental Lines', readonly=True)
    order_count = fields.Integer(string='Rental Orders', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    ROW_NUMBER() OVER (ORDER BY sub.product_id, sub.company_id) AS id,
                    sub.product_id      AS product_id,
                    sub.product_tmpl_id AS product_tmpl_id,
                    sub.categ_id        AS categ_id,
                    sub.company_id      AS company_id,
                    sub.total_qty       AS total_qty,
                    sub.line_count      AS line_count,
                    sub.order_count     AS order_count
                FROM (
                    SELECT
                        l.product_id            AS product_id,
                        p.product_tmpl_id       AS product_tmpl_id,
                        t.categ_id              AS categ_id,
                        s.company_id            AS company_id,
                        SUM(l.product_uom_qty)  AS total_qty,
                        COUNT(l.id)             AS line_count,
                        COUNT(DISTINCT s.id)    AS order_count
                    FROM sale_order_line l
                    JOIN sale_order s        ON l.order_id = s.id
                    JOIN product_product p   ON l.product_id = p.id
                    JOIN product_template t  ON p.product_tmpl_id = t.id
                    WHERE s.is_rental_order = TRUE
                      AND s.state = 'sale'
                      AND l.product_id IS NOT NULL
                    GROUP BY l.product_id, p.product_tmpl_id, t.categ_id, s.company_id
                ) sub
            )
        """ % (self._table,))
