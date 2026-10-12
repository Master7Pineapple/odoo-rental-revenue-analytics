from odoo import fields, models, tools


class RentalAnalysisReport(models.Model):
    _name = 'rental.analysis.report'
    _description = 'Most Rented Products Analysis'
    _auto = False
    _rec_name = 'product_id'
    _order = 'total_qty desc'

    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    product_tmpl_id = fields.Many2one('product.template', string='Product Template', readonly=True)
    categ_id = fields.Many2one('product.category', string='Product Category', readonly=True)
    order_id = fields.Many2one('sale.order', string='Rental Order', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    date = fields.Datetime(string='Rental Date', readonly=True)
    total_qty = fields.Float(string='Quantity Rented', readonly=True)
    order_count = fields.Integer(string='Rental Lines', readonly=True)
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Rental Order'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT
                    l.id                                 AS id,
                    l.product_id                         AS product_id,
                    p.product_tmpl_id                    AS product_tmpl_id,
                    t.categ_id                           AS categ_id,
                    l.order_id                           AS order_id,
                    s.partner_id                         AS partner_id,
                    s.company_id                         AS company_id,
                    COALESCE(s.start_date, s.date_order) AS date,
                    l.product_uom_qty                    AS total_qty,
                    1                                    AS order_count,
                    s.state                              AS state
                FROM sale_order_line l
                JOIN sale_order s        ON l.order_id = s.id
                JOIN product_product p   ON l.product_id = p.id
                JOIN product_template t  ON p.product_tmpl_id = t.id
                WHERE s.is_rental_order = TRUE
                  AND l.product_id IS NOT NULL
            )
        """ % (self._table,))
