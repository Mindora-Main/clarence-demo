#!/usr/bin/env python3
"""Seed / augment the Meridian Digital services scenario (demo/07-client-work).

Idempotent; augments existing demo data. Timesheets are added only when
hr_timesheet is installed.

Usage:
    export ODOO_PASSWORD='***'
    python scripts/seeders/seed_services.py --url URL --db DB --user USER [--dry-run]
"""
from __future__ import annotations

import logging
from dataclasses import dataclass

from _client import (OdooClient, build_arg_parser, config_from_args, setup_logging)

log = logging.getLogger("seeder")


@dataclass(slots=True)
class TaskSpec:
    name: str
    hours: float


CUSTOMERS = [
    ("Bank Muscat Digital", "digital@bankmuscat.demo"),
    ("Oman Air eCommerce", "ecommerce@omanair.demo"),
    ("Renaissance Services", "digital@renaissance.demo"),
]
TASKS = [
    TaskSpec("Discovery", 16),
    TaskSpec("UX design", 24),
    TaskSpec("API build", 40),
    TaskSpec("App build", 56),
    TaskSpec("UAT", 8),
    TaskSpec("Go-live", 4),
]


def seed(cli: OdooClient) -> None:
    if not cli.module_installed("project"):
        cli.summary.notes.append("project not installed -> nothing to seed")
        return

    demo_tag = cli.tag_id("mindora_demo_base.tag_mindora_demo")

    log.info("[1] Customers")
    customer_ids: dict[str, int] = {}
    for index, (name, email) in enumerate(CUSTOMERS, start=1):
        customer_ids[name] = cli.upsert(
            "res.partner",
            ["|", ["email", "=", email], ["name", "=", name]],
            {
                "name": name,
                "email": email,
                "is_company": True,
                "company_type": "company",
                "customer_rank": 1,
                **({"category_id": [(4, demo_tag)]} if demo_tag else {}),
            },
            f"customer {name}",
            xmlid=f"mindora_demo_seed.services_customer_{index:02d}",
        )
    cust = customer_ids.get("Bank Muscat Digital", 0)

    log.info("[2] Service products")
    cli.upsert_product(
        "SV-CONSULT",
        "Consulting Day Rate",
        900.0,
        service=True,
        xmlid="mindora_demo_seed.services_product_consulting",
    )
    cli.upsert_product(
        "SV-IMPL",
        "Software Implementation (Fixed)",
        18000.0,
        service=True,
        xmlid="mindora_demo_seed.services_product_implementation",
    )
    cli.upsert_product(
        "SV-SUPPORT",
        "Managed Support (Monthly)",
        1200.0,
        service=True,
        xmlid="mindora_demo_seed.services_product_support",
    )

    log.info("[3] Project + tasks")
    project_values = {
        "name": "Bank Muscat — Mobile App",
        **({"partner_id": cust} if cust else {}),
    }
    if "allow_timesheets" in cli.fields("project.project"):
        project_values["allow_timesheets"] = True
    proj = cli.upsert(
        "project.project",
        [["name", "=", "Bank Muscat — Mobile App"]],
        project_values,
        "project Bank Muscat Mobile App",
        xmlid="mindora_demo_seed.services_project_bank_muscat_mobile",
    )

    task_ids: dict[str, int] = {}
    if proj:
        for index, t in enumerate(TASKS, start=1):
            tid = cli.upsert("project.task",
                             [["name", "=", t.name], ["project_id", "=", proj]],
                             {"name": t.name, "project_id": proj},
                             f"task {t.name}",
                             xmlid=f"mindora_demo_seed.services_task_{index:02d}")
            task_ids[t.name] = tid

    log.info("[4] Billable timesheets (if hr_timesheet installed)")
    if cli.module_installed("hr_timesheet") and proj:
        emp = cli.search("hr.employee", [], limit=1)
        for index, t in enumerate(TASKS, start=1):
            if t.hours <= 0 or not task_ids.get(t.name):
                continue
            try:
                cli.upsert(
                    "account.analytic.line",
                    [
                        ["name", "=", f"{t.name} work"],
                        ["project_id", "=", proj],
                        ["task_id", "=", task_ids[t.name]],
                    ],
                    {
                        "name": f"{t.name} work",
                        "project_id": proj,
                        "task_id": task_ids[t.name],
                        "unit_amount": t.hours,
                        **({"employee_id": emp[0]} if emp else {}),
                    },
                    f"timesheet {t.name}",
                    xmlid=f"mindora_demo_seed.services_timesheet_{index:02d}",
                )
            except Exception as exc:  # noqa: BLE001
                cli.summary.notes.append(f"timesheet {t.name}: {exc}")
    else:
        cli.summary.notes.append("hr_timesheet not installed -> skipped timesheets")


def main() -> int:
    args = build_arg_parser("Seed the project-services scenario (idempotent).").parse_args()
    setup_logging(args.verbose)
    cli = OdooClient(config_from_args(args))
    cli.connect()
    seed(cli)
    cli.summary.report()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
