# Rental analytics for Odoo

Most rented products and rental customer reports inside the **Odoo 19 Rental** app. Built for Sokoon Rental House in Damascus so management and investors get live numbers without rebuilding a spreadsheet every month.

Project page: [blasedoesit.com/projects/analytics](https://blasedoesit.com/projects/analytics/)

## What it does

Adds three menus to the Rental app (**Most Rented**, **Top Customers**, **Products Summary**), each backed by a read-only SQL view over confirmed rental order lines:

| Menu | Model | What it answers |
|---|---|---|
| Most Rented | `rental.analysis.report` | Which products are rented most, by month, year or all time |
| Products Summary | `rental.product.summary` | Totals per product |
| Top Customers | `rental.customer.report` | Who rents, how often and how much |

- **Views:** chart (bar, pie, line), pivot, list and calendar.
- **Filters:** This Month, This Year, All Time (the default).
- **Group by:** product, product category, customer, month or year.
- **Measures:** quantity rented and number of rental lines.
- Pivot results can be inserted straight into an Odoo spreadsheet.

Because the reports are SQL views (`_auto = False` with an `init()` that creates the view), nothing is stored twice and they stay fast on large order histories.

## Tech

Python, PostgreSQL views, Odoo reporting (graph and pivot views).

## Layout

```
rental_most_rented/
├── models/     three read-only report models, each creating its SQL view
├── views/      graph, pivot, list, calendar and search views, menus
└── security/   read access
```

## Install

Requires **Odoo 19 Enterprise** with the Rental app (`sale_renting`).

1. Copy `rental_most_rented` into a directory on your Odoo addons path.
2. Restart Odoo, then **Apps → Update Apps List**, and install **Most Rented Products**.
3. Open **Rental → Most Rented**, **Top Customers** or **Products Summary**.

## Author

Built by **Kosai Alhafez**, business systems developer.
[blasedoesit.com](https://blasedoesit.com) · kosai@blasedoesit.com

## License

LGPL-3. See [LICENSE](LICENSE).
