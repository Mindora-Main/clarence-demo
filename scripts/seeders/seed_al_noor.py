#!/usr/bin/env python3
"""Seed / augment the Al Noor Integrated Solutions live-demo scenario.

Anchor demo (demo/01-al-noor-live-os). Idempotent and safe to re-run; it
augments Odoo's own demo data rather than replacing it. Advanced records are
created only when the relevant app is installed.

Usage:
    export ODOO_PASSWORD='***'
    python scripts/seeders/seed_al_noor.py --url https://db.odoo.com --db DB --user admin@x.com --dry-run
    python scripts/seeders/seed_al_noor.py --url https://db.odoo.com --db DB --user admin@x.com
"""
from __future__ import annotations

import logging
from dataclasses import dataclass

from _client import (OdooClient, build_arg_parser, config_from_args, setup_logging)

log = logging.getLogger("seeder")

COMPANY_NAME = "Al Noor Integrated Solutions"


@dataclass(slots=True)
class Partner:
    name: str
    email: str
    xmlid: str
    is_customer: bool = False
    is_vendor: bool = False


@dataclass(slots=True)
class Product:
    name: str
    ref: str
    xmlid: str
    kind: str  # "storable" | "service"
    price: float


CUSTOMERS = [
    Partner(
        "Gulf Towers Facilities LLC",
        "facilities@gulftowers.demo",
        "mindora_demo_seed.al_noor_customer_gulf_towers",
        is_customer=True,
    ),
    Partner(
        "Muscat Smart Properties",
        "info@muscatsmart.demo",
        "mindora_demo_seed.al_noor_customer_muscat_smart",
        is_customer=True,
    ),
    Partner(
        "Oman Industrial Services",
        "ops@omanindustrial.demo",
        "mindora_demo_seed.al_noor_customer_oman_industrial",
        is_customer=True,
    ),
]
VENDORS = [
    Partner(
        "Delta Security Supplies",
        "sales@deltasecurity.demo",
        "mindora_demo_seed.al_noor_vendor_delta_security",
        is_vendor=True,
    ),
    Partner(
        "Gulf Network Hardware",
        "sales@gulfnetwork.demo",
        "mindora_demo_seed.al_noor_vendor_gulf_network",
        is_vendor=True,
    ),
]
PRODUCTS = [
    Product(
        "Access Control Controller",
        "ANS-ACC-CTRL",
        "mindora_demo_seed.al_noor_product_access_controller",
        "storable",
        420.0,
    ),
    Product(
        "Smart Door Reader",
        "ANS-DOOR-RDR",
        "mindora_demo_seed.al_noor_product_door_reader",
        "storable",
        180.0,
    ),
    Product(
        "Network Cabinet",
        "ANS-NET-CAB",
        "mindora_demo_seed.al_noor_product_network_cabinet",
        "storable",
        650.0,
    ),
    Product(
        "Installation Service",
        "ANS-SVC-INST",
        "mindora_demo_seed.al_noor_service_installation",
        "service",
        1200.0,
    ),
    Product(
        "Preventive Maintenance Plan",
        "ANS-SVC-PMP",
        "mindora_demo_seed.al_noor_service_maintenance",
        "service",
        1800.0,
    ),
    Product(
        "Emergency Site Visit",
        "ANS-SVC-ESV",
        "mindora_demo_seed.al_noor_service_emergency_visit",
        "service",
        150.0,
    ),
]


def ensure_company_identity(cli: OdooClient, *, rename_company: bool) -> None:
    """Rename only when explicitly requested on a single-company demo DB."""
    companies = cli.search_read("res.company", [], ["name"], limit=2)
    if any(company["name"] == COMPANY_NAME for company in companies):
        log.info("  . company identity already '%s'", COMPANY_NAME)
        cli.summary.skipped += 1
        return
    if not rename_company:
        cli.summary.notes.append(
            "company identity unchanged; pass --rename-company on a dedicated "
            "single-company demo database"
        )
        return
    if len(companies) != 1:
        cli.summary.notes.append("multiple companies present; left company name unchanged")
        return
    if cli.cfg.dry_run:
        log.info("  ~ would rename company -> %s", COMPANY_NAME)
        cli.summary.updated += 1
        return
    cli.execute("res.company", "write", [companies[0]["id"]], {"name": COMPANY_NAME})
    log.info("  ~ renamed company -> %s", COMPANY_NAME)
    cli.summary.updated += 1


def upsert_partner(cli: OdooClient, p: Partner, demo_tag: int | None) -> int:
    values = {
        "name": p.name, "email": p.email, "is_company": True, "company_type": "company",
        "customer_rank": 1 if p.is_customer else 0,
        "supplier_rank": 1 if p.is_vendor else 0,
    }
    if demo_tag:
        values["category_id"] = [(4, demo_tag)]
    return cli.upsert(
        "res.partner",
        ["|", ["email", "=", p.email], ["name", "=", p.name]],
        values,
        f"partner {p.name}",
        xmlid=p.xmlid,
    )


def upsert_product(cli: OdooClient, pr: Product) -> int:
    return cli.upsert_product(
        pr.ref,
        pr.name,
        pr.price,
        service=pr.kind == "service",
        xmlid=pr.xmlid,
    )


def seed(cli: OdooClient, *, rename_company: bool = False) -> None:
    log.info("[1] Company identity")
    ensure_company_identity(cli, rename_company=rename_company)

    demo_tag = cli.tag_id("mindora_demo_base.tag_mindora_demo")

    log.info("[2] Customers")
    cust_ids = {p.name: upsert_partner(cli, p, demo_tag) for p in CUSTOMERS}
    log.info("[3] Vendors")
    for p in VENDORS:
        upsert_partner(cli, p, demo_tag)

    log.info("[4] Products & services")
    product_ids: dict[str, int] = {}
    for pr in PRODUCTS:
        product_ids[pr.ref] = upsert_product(cli, pr)

    log.info("[5] CRM opportunity")
    gulf = cust_ids.get("Gulf Towers Facilities LLC", 0)
    opportunity_name = "Gulf Towers — Access Control Upgrade"
    if cli.module_installed("crm"):
        opportunity_values = {"name": opportunity_name, "type": "opportunity"}
        if gulf:
            opportunity_values["partner_id"] = gulf
        cli.upsert(
            "crm.lead",
            [["name", "=", opportunity_name]],
            opportunity_values,
            "opportunity Gulf Towers",
            xmlid="mindora_demo_seed.al_noor_opportunity_gulf_towers",
        )
    else:
        cli.summary.notes.append("crm not installed -> skipped opportunity")

    log.info("[6] Draft quotation (if Sales installed)")
    if cli.module_installed("sale_management") and gulf:
        controller_variant = cli.product_variant_id(
            product_ids.get("ANS-ACC-CTRL", 0)
        )
        order_values = {
            "partner_id": gulf,
            "origin": "MINDORA-DEMO-ANCHOR",
        }
        if controller_variant:
            order_values["order_line"] = [
                (
                    0,
                    0,
                    {
                        "product_id": controller_variant,
                        "product_uom_qty": 4,
                    },
                )
            ]
        cli.upsert(
            "sale.order",
            [
                ["partner_id", "=", gulf],
                ["state", "=", "draft"],
                ["origin", "=", "MINDORA-DEMO-ANCHOR"],
            ],
            order_values,
            "anchor quotation",
            xmlid="mindora_demo_seed.al_noor_anchor_quotation",
        )
    else:
        cli.summary.notes.append("sale_management not installed -> skipped quotation")

    log.info("[7] Field Service task (if Field Service installed)")
    if cli.module_installed("industry_fsm"):
        project_fields = cli.fields("project.project")
        fsm_project = (
            cli.search("project.project", [["is_fsm", "=", True]], limit=1)
            if "is_fsm" in project_fields
            else []
        )
        if not fsm_project and "is_fsm" in project_fields:
            project_id = cli.upsert(
                "project.project",
                [["name", "=", "Field Service"]],
                {"name": "Field Service", "is_fsm": True},
                "Field Service project",
                xmlid="mindora_demo_seed.al_noor_fsm_project",
            )
        else:
            project_id = fsm_project[0] if fsm_project else 0
        if project_id:
            cli.upsert("project.task",
                       [["name", "=", "Gulf Towers — Access Control Site Visit"],
                        ["project_id", "=", project_id]],
                       {"name": "Gulf Towers — Access Control Site Visit",
                        "project_id": project_id,
                        **({"partner_id": gulf} if gulf else {})},
                       "FSM task Gulf Towers",
                       xmlid="mindora_demo_seed.al_noor_fsm_task")
        else:
            cli.summary.notes.append(
                "Field Service project schema not recognized -> skipped FSM task"
            )
    else:
        cli.summary.notes.append("industry_fsm not installed -> skipped FSM task")

    log.info("[8] Governance placeholders (if installed)")
    if cli.module_installed("approvals"):
        cli.upsert(
            "approval.category",
            [["name", "=", "Site Works Approval"]],
            {"name": "Site Works Approval"},
            "approval type Site Works",
            xmlid="mindora_demo_seed.al_noor_approval_site_works",
        )
    else:
        cli.summary.notes.append("approvals not installed -> skipped approval category")

    if cli.module_installed("documents"):
        cli.upsert(
            "ir.attachment",
            [["name", "=", "Gulf Towers — Site Scope and Drawings"]],
            {
                "name": "Gulf Towers — Site Scope and Drawings",
                "type": "url",
                "url": "https://example.invalid/mindora-demo/gulf-towers-scope",
                "description": "Demo placeholder; replace with a sanitized scope document.",
            },
            "document placeholder Gulf Towers scope",
            xmlid="mindora_demo_seed.al_noor_document_scope_placeholder",
        )
    else:
        cli.summary.notes.append("documents not installed -> skipped document placeholder")


def main() -> int:
    parser = build_arg_parser("Seed the Al Noor live-demo scenario (idempotent).")
    parser.add_argument(
        "--rename-company",
        action="store_true",
        help="rename the sole company; use only on a dedicated demo database",
    )
    args = parser.parse_args()
    setup_logging(args.verbose)
    cli = OdooClient(config_from_args(args))
    cli.connect()
    seed(cli, rename_company=args.rename_company)
    cli.summary.report()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
