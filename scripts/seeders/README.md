# Mindora demo seeders

External, idempotent Odoo seeders that **augment** an existing demo/staging
database over XML-RPC. They never run during module installation, never store
passwords, and detect installed modules so they skip advanced records gracefully.

## Golden rules

- Run against a **demo/staging** database, never production.
- Always `--dry-run` first (reads only, writes nothing).
- The password is read **only** from the `ODOO_PASSWORD` environment variable.
- Re-running is safe: records use business keys plus stable
  `mindora_demo_seed.*` external IDs.
- Odoo's own demo data is treated as a baseline — seeders extend it, they do not
  wipe or duplicate it.
- External RPC access must be available for the database plan and user.

## Usage
```bash
export ODOO_PASSWORD='your-api-key-or-password'

python scripts/seeders/seed_al_noor.py \
    --url https://your-branch.odoo.com \
    --db  your-database \
    --user admin@yourcompany.com \
    --dry-run        # preview, writes nothing

# then run for real (drop --dry-run)
python scripts/seeders/seed_al_noor.py --url ... --db ... --user ...
```
Generate an API key in Odoo: **Preferences → Account Security → New API Key**.

PowerShell:

```powershell
$env:ODOO_PASSWORD = 'your-api-key-or-password'
python -B scripts/seeders/seed_al_noor.py `
  --url https://your-branch.odoo.com `
  --db your-database `
  --user admin@example.com `
  --dry-run
```

On a dedicated single-company Al Noor database, pass `--rename-company`.
Without it, the script never renames the active company.

On a dedicated holding database, `seed_holding.py --create-companies` creates
Clarence Holding plus three subsidiary `res.company` records and grants the
seeder user access. Without the flag it creates only tagged portfolio contacts.
Localization, journals, access policy, and consolidation remain manual.

## Which seeder for which branch
| Seeder | Branch | What it augments |
|---|---|---|
| `seed_al_noor.py` | `demo/01-al-noor-live-os` | Customers, vendors, products, CRM opportunity, draft quotation, FSM task, approval type |
| `seed_services.py` | `demo/07-client-work` | Meridian customers, service products, project + tasks + billable timesheets |
| `seed_mrp.py` | `demo/09-workshop`, `demo/10-mrp` | Gulf Precision customer, components, finished product, work centres, BoM + operations |
| `seed_holding.py` | `demo/15-holding` | Portfolio structure, investment opportunity, initiatives, CapEx approval, document placeholders |

## Shared client

`_client.py` provides `OdooClient` with idempotent `upsert`, `upsert_product`,
`module_installed`, dry-run handling and a created/updated/skipped summary.
Seeders import it directly (run them from the repo root as shown above).

## Reset

See `docs/demo-reset-runbook.md`. In short: restore the branch database from a
clean Odoo.sh backup, or rely on the seeders' idempotency to re-converge state.

## API lifecycle

These scripts target Odoo 19's `/xmlrpc/2` API. Odoo 19 documentation marks
legacy XML-RPC/JSON-RPC services as deprecated in favor of JSON-2. Keep the
seeders for this Odoo 19 lab and plan a JSON-2 migration before the documented
removal release.
