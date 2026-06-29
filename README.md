# Mindora × Clarence Odoo 19 Demo Lab

This repository contains the Odoo.sh branch architecture, lightweight Odoo
meta modules, seeders, and operator runbooks for the Mindora × Clarence demo
environments.

> Odoo provides the platform. Mindora designs the business operating system.

The repository is intentionally a thin orchestration layer. It does not
reimplement standard Odoo workflows. Each `mindora_demo_*` addon installs the
standard Odoo 19 applications needed for one coherent business story, while
the external seeders add a small set of recognizable records.

## Start here

Build `demo/01-al-noor-live-os` first. It is the anchor scenario:

`Lead → Opportunity → Quotation → Sales Order → Inventory / Purchase /
Delivery → Field Service → Invoice → Dashboard`

Use these documents in order:

1. [`docs/PRIMARY_ODOO_SH_BRANCHES.md`](docs/PRIMARY_ODOO_SH_BRANCHES.md)
2. [`docs/ODOO_SH_RUNBOOK.md`](docs/ODOO_SH_RUNBOOK.md)
3. [`docs/branch-installation.md`](docs/branch-installation.md)
4. [`docs/al-noor-live-demo-script.md`](docs/al-noor-live-demo-script.md)
5. [`docs/demo-reset-runbook.md`](docs/demo-reset-runbook.md)

## Repository layout

```text
.
├── addons/
│   ├── mindora_demo_base/
│   └── mindora_demo_00_base_universal/ ... mindora_demo_16_room/
├── docs/
├── scripts/
│   ├── seeders/
│   ├── branch_report.py
│   ├── verify_odoo_manifests.py
│   └── verify_repo.py
└── .github/workflows/repo-check.yml
```

The deleted root-level sample addon was a placeholder. All installable custom
addons now live below `addons/`.

## Odoo demo data policy

Odoo.sh development builds can already contain standard Odoo demo data. Keep
it: the seeders search before creating, attach stable external IDs to records
they own, and add only the minimum records required by the scenario. They do
not wipe data or bulk-create artificial history. Always run a seeder with
`--dry-run` first.

See [`docs/demo-data-policy.md`](docs/demo-data-policy.md) for ownership and
duplicate-avoidance rules.

## Local verification

No Odoo runtime is required:

```bash
python -B scripts/verify_repo.py
python -B scripts/verify_odoo_manifests.py
python -B scripts/branch_report.py
```

The same checks run in GitHub Actions.

## Seeder example

Set `ODOO_PASSWORD` to a dedicated demo user's API key or password. Never save
it in this repository.

```bash
python -B scripts/seeders/seed_al_noor.py \
  --url https://your-build.example.com \
  --db your_database \
  --user demo.admin@example.com \
  --dry-run
```

On a dedicated single-company database, add `--rename-company` to rename the
sole company to Al Noor. Without that explicit flag, the seeder leaves company
identity untouched.

## Important limitations

- Enterprise addon availability must be validated in the target Odoo.sh 19.0
  build before declaring a branch ready.
- The seeders use Odoo 19 XML-RPC. Odoo has deprecated the legacy RPC endpoints
  for a future release; migration to JSON-2 is tracked in
  [`docs/module-name-validation.md`](docs/module-name-validation.md).
- Studio approval rules, dashboards, worksheets, AI agents, and some
  Documents configuration remain deliberate post-install UI steps because
  their schemas are Enterprise-build-sensitive.

## License

LGPL-3
