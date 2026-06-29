# Odoo.sh Demo Runbook

## Goal

Use each Git branch as a separate Odoo.sh demo database for a clear business operating model.

## First priority build order

1. `demo/00-base-universal`
2. `demo/01-al-noor-live-os`
3. `demo/04-trading-distribution-warehouse`
4. `demo/08-field-service-after-sales`
5. `demo/10-manufacturing-l2`
6. `demo/15-holding`

## How to create a database from a branch

1. Open Odoo.sh.
2. Select the `clarence-demo` project.
3. Open the branch.
4. Wait for the build to finish.
5. Create or open the database for that branch.
6. Activate developer mode.
7. Go to Apps.
8. Remove the default Apps filter if needed.
9. Search the technical meta module listed in `docs/branch-matrix.csv`.
10. Install it.
11. Configure the database using the branch checklist.

## Anchor demo: Al Noor

Use `demo/01-al-noor-live-os` for the live executive demo.

Demo path:

```text
Lead → Opportunity → Quotation → Sales Order → Inventory/Purchase/Delivery → Field Service → Invoice → Dashboard
```

## Demo narration

Do not say: “Here are the Odoo apps.”

Say:

```text
When a company is small, the owner can still manage through memory, WhatsApp and Excel.
When it grows, sales, purchasing, warehouse, service teams, documents and finance start moving at different speeds.
The question is not whether the company has software.
The question is whether the business has been designed as one operating system.
```

## Branch naming notes

Some long branch names were shortened because the GitHub connector wrapper blocked a few verbose names. The matrix keeps the business meaning intact.

## Data safety

Never run demo seeders against production. Use staging/demo databases only. Make a backup before heavy demo data import.
