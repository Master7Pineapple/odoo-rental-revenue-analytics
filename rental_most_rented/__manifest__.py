{
    'name': 'Most Rented Products',
    'version': '19.0.2.0.0',
    'category': 'Sales/Rental',
    'summary': 'Visual analytics for the most rented products (month, year, all time)',
    'description': """
Most Rented Products
====================

Adds a "Most Rented" analytics screen inside the Rental app.

It builds a read-only SQL report over confirmed rental order lines and lets you
visualise the most rented products as bar / pie / line charts (graph view),
cross-tabulate them (pivot view) or list them.

Time scoping is handled with search filters:
  * This Month
  * This Year
  * All Time (no date filter = default)

Measures available: quantity rented and number of rental lines.
Group by product, product category, customer, month or year.
""",
    'author': "Kosai Alhafez",
    "website": "https://blasedoesit.com",
    'depends': ['sale_renting'],
    'data': [
        'security/ir.model.access.csv',
        'views/rental_analysis_views.xml',
        'views/rental_customer_views.xml',
        'views/rental_product_summary_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
