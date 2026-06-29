# Demo Reset Runbook

## Choose the reset method

| Situation | Reset method |
|---|---|
| Clean Development build needed | Rebuild the branch; then reinstall and reseed |
| Reusable Staging rehearsal database | Restore the approved manual backup |
| Only draft rehearsal records changed | Perform the transactional reset below |
| Posted accounting/stock/signature side effects | Restore a snapshot; do not delete piecemeal |

Odoo.sh Development databases are disposable and may be garbage-collected.
Staging databases are neutralized and can use manual backups, subject to the
project's retention/availability. Confirm current Odoo.sh controls before a
live event.

## Establish a clean baseline

1. Build the target branch.
2. Install only its matching meta module.
3. Complete the branch's post-install settings.
4. Run the relevant seeder with `--dry-run`.
5. Run it for real.
6. Run it again and confirm no duplicate business records are created.
7. Complete manual records such as worksheets, dashboards, approval steps, and
   sanitized history.
8. Rehearse once.
9. For Staging, create a manual backup named with branch, date, and
   `clean-baseline`.
10. Capture fallback screenshots/video.

## Al Noor transactional reset

Perform in dependency order:

1. **Invoice:** cancel/delete only the rehearsal draft invoice. If posted, use
   the approved accounting reversal or restore the baseline.
2. **Field task:** remove rehearsal worksheet answers, time, and products, or
   delete the disposable task. Preserve the master task.
3. **Delivery:** cancel the rehearsal delivery only while Odoo permits a clean
   cancellation. Restore snapshot after completed moves.
4. **Purchase:** cancel/delete the draft replenishment PO.
5. **Sales order:** return to quotation only if the database state allows it;
   otherwise delete the disposable copy or restore.
6. **Approval:** withdraw/delete the rehearsal request or revoke the Studio
   approval on the disposable order.
7. **CRM:** move the opportunity to its start stage and clear the rehearsal
   activity.
8. **Stock:** restore planned demo quantities through a documented inventory
   adjustment, never direct SQL.
9. **Dashboard:** leave seeded/read-only history untouched.

Use a master-record pattern: preserve a clearly named start-state record and
duplicate it for each rehearsal when Odoo supports a safe duplicate.

## Rebuild from branch

1. In Odoo.sh, select the target Development branch.
2. Request a rebuild/new build.
3. Confirm the build revision matches the intended Git commit.
4. Install the matching meta module through build settings or Apps.
5. Validate `mindora_demo_base` installation before seeding.
6. Run the seeder dry-run and real run.
7. Apply the manual checklist from `branch-installation.md`.

Do not assume manual settings from an old Development database will survive a
rebuild.

## Restore Staging baseline

1. Stop active rehearsal users.
2. In Odoo.sh, open the Staging branch's backup controls.
3. Select the approved `clean-baseline` backup or import the approved database
   archive.
4. Wait for the build to become ready.
5. Confirm neutralization and mail catcher.
6. Confirm the Git revision and module versions.
7. Run the scenario verification below.

If the baseline came from Production, verify that all data is authorized and
sanitized before using it in a public demo.

## Seeder rerun

PowerShell:

```powershell
$env:ODOO_PASSWORD = 'replace-with-api-key'
python -B scripts/seeders/seed_al_noor.py `
  --url https://BUILD.example.odoo.com `
  --db DATABASE `
  --user demo.admin@example.com `
  --dry-run
```

Bash:

```bash
export ODOO_PASSWORD='replace-with-api-key'
python -B scripts/seeders/seed_al_noor.py \
  --url https://BUILD.example.odoo.com \
  --db DATABASE \
  --user demo.admin@example.com \
  --dry-run
```

Review the summary, then rerun without `--dry-run`.

## Scenario verification

### Al Noor

- customer, vendors, six products/services, opportunity, and draft quotation
  exist once;
- service product creates a Field Service task on order confirmation;
- approval activity/chatter behavior works;
- delivery and replenishment show expected stock state;
- field worksheet, product usage, and invoice handoff work;
- dashboard is populated and one drill-down is valid.

### Services

- customer and project exist once;
- six tasks exist once;
- each seeded timesheet line exists once after repeated runs;
- profitability view has costs/revenue only after operator configuration.

### MRP

- components and finished product exist once;
- one normal BoM and one draft demo MO exist;
- operations appear only when Work Orders is installed;
- quality point is manually configured and verified on the target Enterprise
  build.

### Holding

- portfolio contacts, initiatives, opportunity, and CapEx approval type exist
  once;
- no `res.company` legal entities were created unless `--create-companies` was
  explicitly used;
- document placeholders contain no confidential content;
- board workspace and dashboard are manually verified.

## Demo-day pre-flight

- Wake the database at least 60 minutes early.
- Run the full path once, then reset.
- Pre-authenticate required personas.
- Turn developer mode and notifications off.
- Confirm no real outbound recipient/provider.
- Keep fallback assets on the presentation machine.
- Record the build URL, commit, reset owner, and last successful rehearsal time.
