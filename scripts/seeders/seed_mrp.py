#!/usr/bin/env python3
"""Seed / augment the Gulf Precision manufacturing scenario.

Creates a finished product, components, customer, work centres and a Bill of Materials
with operations. Manufacturing orders and quality points are only attempted
when the relevant apps are installed. Idempotent.

Usage:
    export ODOO_PASSWORD='***'
    python scripts/seeders/seed_mrp.py --url URL --db DB --user USER [--dry-run]
"""
from __future__ import annotations

import logging
from dataclasses import dataclass

from _client import (OdooClient, build_arg_parser, config_from_args, setup_logging)

log = logging.getLogger("seeder")


@dataclass(slots=True)
class Component:
    ref: str
    name: str
    qty: int
    cost: float


@dataclass(slots=True)
class Operation:
    name: str
    workcentre: str
    minutes: int


COMPONENTS = [
    Component("RM-SHEET", "Galvanised Steel Sheet 1.2 mm", 6, 32.0),
    Component("RM-ANGLE", "Steel Angle Profile", 8, 11.0),
    Component("RM-FAST", "Fastener & Bracket Set", 1, 24.0),
    Component("RM-COAT", "Powder Coat", 3, 9.0),
]
WORKCENTRES = {
    "Cutting": 45.0,
    "Welding & Assembly": 38.0,
    "Finishing / Powder Coat": 30.0,
    "Quality / QC": 25.0,
}
OPERATIONS = [
    Operation("Cut sheets & profiles", "Cutting", 30),
    Operation("Weld & assemble frame", "Welding & Assembly", 60),
    Operation("Powder coat", "Finishing / Powder Coat", 25),
    Operation("Dimensional check", "Quality / QC", 10),
]
FINISHED_REF = "FG-AHU-FRAME"


def seed(cli: OdooClient) -> None:
    if not cli.module_installed("mrp"):
        cli.summary.notes.append("mrp not installed -> nothing to seed")
        return

    log.info("[1] Customer")
    cli.upsert(
        "res.partner",
        [
            "|",
            ["email", "=", "projects@soharmall.demo"],
            ["name", "=", "Sohar Mall Developers"],
        ],
        {
            "name": "Sohar Mall Developers",
            "email": "projects@soharmall.demo",
            "is_company": True,
            "company_type": "company",
            "customer_rank": 1,
        },
        "customer Sohar Mall Developers",
        xmlid="mindora_demo_seed.mrp_customer_sohar_mall",
    )

    log.info("[2] Components")
    component_templates: dict[str, int] = {}
    for c in COMPONENTS:
        component_templates[c.ref] = cli.upsert_product(
            c.ref,
            c.name,
            round(c.cost * 1.4, 2),
            xmlid=f"mindora_demo_seed.mrp_product_{c.ref.lower().replace('-', '_')}",
        )
    log.info("[3] Finished product")
    fg = cli.upsert_product(
        FINISHED_REF,
        "Rooftop AHU Steel Frame",
        1450.0,
        xmlid="mindora_demo_seed.mrp_product_finished_ahu_frame",
    )

    log.info("[4] Work centres")
    wc_ids: dict[str, int] = {}
    if cli.model_available("mrp.workcenter"):
        for index, (name, rate) in enumerate(WORKCENTRES.items(), start=1):
            wc_ids[name] = cli.upsert(
                "mrp.workcenter",
                [["name", "=", name]],
                {"name": name, "costs_hour": rate},
                f"workcentre {name}",
                xmlid=f"mindora_demo_seed.mrp_workcenter_{index:02d}",
            )
    else:
        cli.summary.notes.append(
            "mrp.workcenter unavailable -> skipped work centres and operations"
        )

    log.info("[5] Bill of Materials + operations")
    if not fg:
        cli.summary.notes.append(
            "finished product would be created -> dependent BoM/MO checked on real run"
        )
        return

    component_variants = {
        ref: cli.product_variant_id(template_id)
        for ref, template_id in component_templates.items()
        if template_id
    }
    lines = [
        (
            0,
            0,
            {
                "product_id": component_variants[c.ref],
                "product_qty": c.qty,
            },
        )
        for c in COMPONENTS
        if component_variants.get(c.ref)
    ]
    ops = []
    if cli.module_installed("mrp_workorder"):
        ops = [
            (
                0,
                0,
                {
                    "name": operation.name,
                    "workcenter_id": wc_ids[operation.workcentre],
                    "time_cycle_manual": operation.minutes,
                },
            )
            for operation in OPERATIONS
            if wc_ids.get(operation.workcentre)
        ]
    bom_values = {
        "product_tmpl_id": fg,
        "product_qty": 1,
        "type": "normal",
        "bom_line_ids": lines,
        **({"operation_ids": ops} if ops else {}),
    }
    try:
        bom = cli.upsert(
            "mrp.bom",
            [["product_tmpl_id", "=", fg], ["type", "=", "normal"]],
            bom_values,
            f"BoM for {FINISHED_REF}",
            xmlid="mindora_demo_seed.mrp_bom_finished_ahu_frame",
        )
    except Exception as exc:  # noqa: BLE001
        cli.summary.notes.append(f"BoM create failed (build in UI): {exc}")
        return

    log.info("[6] Draft manufacturing order")
    finished_variant = cli.product_variant_id(fg)
    if bom and finished_variant:
        product_data = cli.read(
            "product.product", [finished_variant], ["uom_id"]
        )
        uom_value = product_data[0].get("uom_id") if product_data else None
        if uom_value:
            try:
                cli.upsert(
                    "mrp.production",
                    [["origin", "=", "MINDORA-DEMO-MRP"]],
                    {
                        "origin": "MINDORA-DEMO-MRP",
                        "product_id": finished_variant,
                        "product_qty": 2,
                        "product_uom_id": uom_value[0],
                        "bom_id": bom,
                    },
                    "draft manufacturing order",
                    xmlid="mindora_demo_seed.mrp_production_demo",
                )
            except Exception as exc:  # noqa: BLE001
                cli.summary.notes.append(
                    f"manufacturing order create failed (build in UI): {exc}"
                )

    if cli.module_installed("quality_control"):
        cli.summary.notes.append(
            "quality_control installed -> configure the dimensional-check "
            "quality point in the UI; required point fields vary by Enterprise build"
        )


def main() -> int:
    args = build_arg_parser("Seed the manufacturing scenario (idempotent).").parse_args()
    setup_logging(args.verbose)
    cli = OdooClient(config_from_args(args))
    cli.connect()
    seed(cli)
    cli.summary.report()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
