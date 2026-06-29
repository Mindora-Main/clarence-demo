#!/usr/bin/env python3
"""Seed / augment the Clarence holding control-tower scenario (demo/15-holding).

Creates governance-flavoured records: holding initiatives (projects with codes),
an investment opportunity, a CapEx approval type, and a documents folder.
All advanced records are guarded by module detection. Idempotent.

Usage:
    export ODOO_PASSWORD='***'
    python scripts/seeders/seed_holding.py --url URL --db DB --user USER [--dry-run]
"""
from __future__ import annotations

import logging

from _client import (OdooClient, build_arg_parser, config_from_args, setup_logging)

log = logging.getLogger("seeder")

INITIATIVES = {
    "HLD-001": "Group Platform Build",
    "HLD-002": "Plant Expansion Phase 2",
    "HLD-003": "Logistics Park Development",
}
PORTFOLIO_COMPANIES = [
    ("Clarence Holding", "holding@clarence.demo"),
    ("Clarence Industrial", "industrial@clarence.demo"),
    ("Clarence Digital", "digital@clarence.demo"),
    ("Clarence Properties", "properties@clarence.demo"),
]


def ensure_demo_companies(
    cli: OdooClient,
    *,
    create_companies: bool,
    partner_ids: dict[str, int],
) -> dict[str, int]:
    """Optionally create accounting companies on an explicitly dedicated DB."""
    if not create_companies:
        cli.summary.notes.append(
            "legal companies not created; pass --create-companies only on a "
            "dedicated holding demo database"
        )
        return {}

    company_fields = cli.fields("res.company")
    company_ids: dict[str, int] = {}
    for index, (name, _email) in enumerate(PORTFOLIO_COMPANIES, start=1):
        values = {"name": name}
        if partner_ids.get(name) and "partner_id" in company_fields:
            values["partner_id"] = partner_ids[name]
        if (
            index > 1
            and company_ids.get("Clarence Holding")
            and "parent_id" in company_fields
        ):
            values["parent_id"] = company_ids["Clarence Holding"]
        company_ids[name] = cli.upsert(
            "res.company",
            [["name", "=", name]],
            values,
            f"accounting company {name}",
            xmlid=f"mindora_demo_seed.holding_res_company_{index:02d}",
        )

    linked_company_ids = [record_id for record_id in company_ids.values() if record_id]
    if linked_company_ids and not cli.cfg.dry_run:
        cli.execute(
            "res.users",
            "write",
            [cli.uid],
            {"company_ids": [(4, record_id) for record_id in linked_company_ids]},
        )
        log.info("  ~ granted current seeder user access to holding demo companies")
    cli.summary.notes.append(
        "configure localization, journals, access, consolidation, and opening "
        "balances manually for each created company"
    )
    return company_ids


def seed(cli: OdooClient, *, create_companies: bool = False) -> None:
    log.info("[1] Portfolio company contacts")
    demo_tag = cli.tag_id("mindora_demo_base.tag_clarence_group")
    portfolio_partner_ids: dict[str, int] = {}
    for index, (name, email) in enumerate(PORTFOLIO_COMPANIES, start=1):
        portfolio_partner_ids[name] = cli.upsert(
            "res.partner",
            ["|", ["email", "=", email], ["name", "=", name]],
            {
                "name": name,
                "email": email,
                "is_company": True,
                "company_type": "company",
                **({"category_id": [(4, demo_tag)]} if demo_tag else {}),
            },
            f"portfolio company {name}",
            xmlid=f"mindora_demo_seed.holding_company_{index:02d}",
        )

    log.info("[2] Optional multi-company structure")
    company_ids = ensure_demo_companies(
        cli,
        create_companies=create_companies,
        partner_ids=portfolio_partner_ids,
    )

    log.info("[3] Investment opportunity")
    if cli.module_installed("crm"):
        cli.upsert(
            "crm.lead",
            [["name", "=", "New Logistics Park — Feasibility"]],
            {"name": "New Logistics Park — Feasibility", "type": "opportunity"},
            "opportunity New Logistics Park",
            xmlid="mindora_demo_seed.holding_opportunity_logistics_park",
        )
    else:
        cli.summary.notes.append("crm not installed -> skipped opportunity")

    log.info("[4] Holding initiatives (projects with codes)")
    if cli.module_installed("project"):
        project_fields = cli.fields("project.project")
        for index, (code, name) in enumerate(INITIATIVES.items(), start=1):
            display_name = f"[{code}] {name}"
            values = {"name": display_name}
            subsidiary_names = (
                "Clarence Industrial",
                "Clarence Digital",
                "Clarence Properties",
            )
            subsidiary_id = company_ids.get(subsidiary_names[index - 1], 0)
            if subsidiary_id and "company_id" in project_fields:
                values["company_id"] = subsidiary_id
            if "description" in project_fields:
                values["description"] = (
                    f"Mindora demo governance initiative. Portfolio code: {code}."
                )
            cli.upsert(
                "project.project",
                [["name", "=", display_name]],
                values,
                f"initiative {code} {name}",
                xmlid=f"mindora_demo_seed.holding_project_{index:02d}",
            )
    else:
        cli.summary.notes.append("project not installed -> skipped initiatives")

    log.info("[5] CapEx approval type (governance)")
    if cli.module_installed("approvals"):
        cli.upsert(
            "approval.category",
            [["name", "=", "Capital Expenditure / Investment"]],
            {"name": "Capital Expenditure / Investment"},
            "approval type CapEx",
            xmlid="mindora_demo_seed.holding_approval_capex",
        )
    else:
        cli.summary.notes.append("approvals not installed -> skipped approval type")

    log.info("[6] Board document placeholders (if Documents installed)")
    if cli.module_installed("documents"):
        for index, name in enumerate(
            ("Board Pack — Current Quarter", "Investment Committee — Pipeline"),
            start=1,
        ):
            cli.upsert(
                "ir.attachment",
                [["name", "=", name]],
                {
                    "name": name,
                    "type": "url",
                    "url": f"https://example.invalid/mindora-demo/board-{index}",
                    "description": "Demo placeholder; replace with a sanitized document.",
                },
                f"document placeholder {name}",
                xmlid=f"mindora_demo_seed.holding_document_{index:02d}",
            )
        cli.summary.notes.append(
            "create the Board Pack workspace/folder in the Documents UI; "
            "the folder model varies by Enterprise build"
        )
    else:
        cli.summary.notes.append("documents not installed -> skipped document placeholders")


def main() -> int:
    parser = build_arg_parser(
        "Seed the holding control-tower scenario (idempotent)."
    )
    parser.add_argument(
        "--create-companies",
        action="store_true",
        help="create four res.company records; dedicated holding demo DB only",
    )
    args = parser.parse_args()
    setup_logging(args.verbose)
    cli = OdooClient(config_from_args(args))
    cli.connect()
    seed(cli, create_companies=args.create_companies)
    cli.summary.report()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
