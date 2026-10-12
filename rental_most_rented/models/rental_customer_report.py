from odoo import fields, models, tools


class RentalCustomerReport(models.Model):
    """One row per confirmed rental ORDER, so counting rows = number of orders.

    Use to rank customers by how many rental orders they placed.
    """
    _name = 'rental.customer.report'
    _description = 'Rental Customers Analysis'
    _auto = False
    _rec_name = 'partner_id'
    _order = 'order_count desc'

    partner_id = fields.Many2one('res.partner', string='Customer', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    date = fields.Datetime(string='Rental Date', readonly=True)
    order_count = fields.Integer(string='Orders', readonly=True)
    total_qty = fields.Float(string='Total Quantity', readonly=True)
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
                    s.id                                 AS id,
                    s.partner_id                         AS partner_id,
                    s.company_id                         AS company_id,
                    COALESCE(s.start_date, s.date_order) AS date,
                    s.state                              AS state,
                    1                                    AS order_count,
                    (SELECT COALESCE(SUM(l.product_uom_qty), 0)
                       FROM sale_order_line l
                      WHERE l.order_id = s.id
                        AND l.product_id IS NOT NULL)    AS total_qty
                FROM sale_order s
                WHERE s.is_rental_order = TRUE
                  AND s.state = 'sale'
                  AND s.partner_id IS NOT NULL
            )
        """ % (self._table,))
