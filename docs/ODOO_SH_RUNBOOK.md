# Odoo.sh Runbook

## 1. Preconditions

- Odoo.sh project connected to `Mindora-Main/clarence-demo`.
- Odoo 19 Enterprise source entitlement is active.
- Primary Git branches from `PRIMARY_ODOO_SH_BRANCHES.md` exist remotely.
- A dedicated demo administrator is available.
- No production credentials or customer data are used.

Run the lightweight repository checks before pushing:

```bash
python -B scripts/verify_repo.py
python -B scripts/verify_odoo_manifests.py
python -B scripts/branch_report.py
```

## 2. Build the anchor branch first

Start with `demo/01-al-noor-live-os`. Keep it in Development while validating
module names and installation. Odoo.sh Development builds create fresh
databases with demo data and run tests by default, so treat native demo data as
the baseline rather than an error.

In the branch build settings, either:

- select **Install a list of modules** and enter
  `mindora_demo_01_al_noor_live_os`; or
- let the build start, update the Apps list, and install that technical module
  from Apps.

Do not install every `mindora_demo_*` module into the same database.

## 3. Confirm custom-addon discovery

Custom addons live under `addons/`. Before any scenario setup:

1. Open the build.
2. Enable developer mode temporarily.
3. Update the Apps list.
4. Remove the default **Apps** filter and search for
   `mindora_demo_base`.
5. If it is absent, inspect the build log and effective addons path before
   changing repository layout. Apply one repository-wide correction; do not
   move addons differently on individual branches.

The meta module must install `mindora_demo_base` and its standard dependencies
without importing data from another branch.

## 4. Validate Enterprise technical names

Before declaring a branch ready:

1. Open Apps with developer mode enabled.
2. Search each dependency from the matching manifest by technical name.
3. Record confirmed names and substitutions in
   `module-name-validation.md`.
4. If a name is absent, remove it from the manifest only after identifying the
   supported replacement or deciding that the feature is an optional manual
   install.
5. Re-run a clean Development build.

The current dependency lists are the best-known Odoo 19 names, not proof that
every Enterprise repository snapshot exposes every integration addon.

## 5. Seed the minimum scenario data

External RPC requires an eligible Odoo plan and a dedicated user's API
credential/password. On the operator machine:

```bash
export ODOO_PASSWORD='replace-with-api-key'
python -B scripts/seeders/seed_al_noor.py \
  --url https://BUILD.example.odoo.com \
  --db DATABASE \
  --user demo.admin@example.com \
  --dry-run
```

Review the created/updated/skipped summary. Then rerun without `--dry-run`.
Use `--rename-company` only for a dedicated, single-company Al Noor database.

Seeders create stable `mindora_demo_seed.*` external IDs for records they own.
They search by business key before creating, so reruns converge rather than
duplicate.

## 6. Complete UI-only configuration

The branch installation guide lists post-install settings. For Al Noor, the
minimum manual work is:

- enable CRM leads;
- configure the service product to create a Field Service task;
- configure the default field-service warehouse and worksheet;
- add a Studio approval step or a native Approvals request flow;
- configure one populated management dashboard;
- verify mail catcher behavior before sending a demo quotation.

Keep these steps in the runbook. Odoo.sh does not transfer manual database
configuration from one Git branch to another.

## 7. Promote and preserve

- Development databases are disposable and can be garbage-collected.
- Staging databases are neutralized copies; outgoing email and external
  connectors are disabled or intercepted.
- Take a manual Staging backup before a rehearsal reset when available.
- Keep the demo branch out of Production unless it is intentionally the
  project's production branch.
- Capture fallback screenshots/video after a successful rehearsal and store
  them outside this source repository unless approved assets are required.

## 8. Failure triage

| Failure | Action |
|---|---|
| Meta module absent | Check addons discovery and build log |
| Missing dependency | Validate technical name; document before editing manifest |
| Install traceback in base addon | Stop; fix XML/manifest compatibility before seeding |
| Seeder authentication failure | Verify database, login, plan eligibility, and API credential |
| Seeder would create duplicates | Stop; inspect business keys and existing external IDs |
| Field task not generated | Check service tracking and confirmed sale order |
| Live screen stalls | Switch to the prepared fallback asset; do not debug on stage |

## 9. Per-branch acceptance

A branch is ready only when:

- the matching meta module installs on a clean Odoo 19 Enterprise build;
- the seeder dry-run and real run both finish;
- the second real run creates no duplicate business records;
- the documented demo path is rehearsed;
- the reset procedure is timed and verified;
- uncertain technical names are resolved for that exact build.
