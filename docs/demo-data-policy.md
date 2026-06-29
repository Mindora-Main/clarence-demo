# Demo Data Policy

## Principle

Odoo's native demo data is a useful baseline. Mindora data must augment,
connect, or carefully rename that baseline; it must not replace it with a
second artificial company full of duplicate records.

## Ownership

| Data | Owner | Rule |
|---|---|---|
| Standard Odoo demo records | Odoo | Preserve unless a documented demo step extends them |
| `mindora_demo_base` XML records | Custom addon | Stable XML IDs, `noupdate="1"` |
| `mindora_demo_seed.*` records | External seeders | Idempotent, safe to rerun |
| Manual Studio/dashboard/worksheet setup | Demo operator | Record exact steps in runbooks |
| Transactional rehearsal records | Demo operator | Reset or restore after each run |

## Duplicate-avoidance order

Seeders search in this order:

1. stable external ID;
2. business identifier such as internal reference/barcode;
3. email for partners;
4. exact scenario name scoped by parent record;
5. create only when no equivalent exists.

When an equivalent native demo record exists, the seeder attaches its stable
external ID where safe instead of creating a duplicate.

## Update versus create

Update an existing record only when all of the following are true:

- the record is clearly the same business object;
- the changed fields are scenario-owned and non-destructive;
- the change will not invalidate native demo flows;
- the operator can explain the reset path.

Create a new record when the scenario needs a distinct identity and a stable
business key exists.

Do not automatically:

- delete or archive native demo records;
- replace chart of accounts, taxes, journals, warehouses, or legal companies;
- overwrite prices or addresses on an ambiguous name match;
- create users with real email addresses;
- post invoices, receive stock, confirm purchases, or send messages unless the
  specific seeder/runbook says so.

## Company identity

`seed_al_noor.py` does not rename the active company by default. On a dedicated
single-company demo database, the operator may pass `--rename-company`.
Multi-company databases are never renamed automatically.

The holding seeder creates portfolio companies as tagged partner records by
default. On a dedicated holding database, `--create-companies` explicitly
creates four `res.company` records and grants the seeder user access. The
operator must still configure localization, journals, fiscal positions,
access, and consolidation.

## Seed volume

Prefer the smallest dataset that makes the workflow credible:

- three customers and two vendors for Al Noor;
- six products/services;
- one anchor opportunity and quotation;
- one project with a small task set;
- one manufacturing BoM and draft MO;
- a few governance placeholders.

Use Odoo's existing demo history for background density. Add transactional
history manually only where a dashboard would otherwise be empty.

## Dry-run and rerun contract

Every seeder supports `--dry-run`. Dry-run may authenticate and read data but
must not call create/write/unlink.

A real run followed by a second real run must not create duplicate business
records. The second run should report existing/skipped records. Any unavoidable
Enterprise-schema difference is reported as a note and handled manually.

## Reset boundary

Safe to reset:

- quotations, approval requests, deliveries, draft purchase orders, field
  tasks, and draft invoices created for a rehearsal;
- quantities changed solely for the demo, using an inventory adjustment;
- demo activities and worksheet answers;
- seeder-owned records in a disposable database after their dependencies are
  understood.

Do not reset by deleting:

- accounting entries, valuation layers, completed stock moves, payments, or
  signed documents in a shared database;
- Odoo native demo data;
- records with unknown ownership.

When a transaction has posted side effects, restore a clean database snapshot
instead of trying to reverse it record by record.

## Privacy and outbound effects

- Use `.demo` or `.invalid` addresses only.
- Do not use real customer names, documents, phone numbers, or barcodes.
- Keep mail in Odoo.sh's mail catcher.
- Keep payment, shipping, SMS, social, and IAP connectors in test/neutralized
  mode.
- AI sources must be sanitized and least-privilege; write-capable topics must
  be tested separately.
