#!/usr/bin/env python3
"""Shared idempotent Odoo XML-RPC client for the Mindora demo seeders.

Design goals:
  * idempotent upsert (search first, then create or update)
  * never duplicate partners/products/projects
  * detect installed modules and let callers skip gracefully
  * dry-run support (reads allowed, no writes)
  * structured logging and a created/updated/skipped summary
  * password only ever comes from the ODOO_PASSWORD environment variable
"""
from __future__ import annotations

import argparse
import logging
import os
import sys
import xmlrpc.client
from dataclasses import dataclass, field
from typing import Any

log = logging.getLogger("seeder")
SEED_XMLID_MODULE = "mindora_demo_seed"


@dataclass(slots=True)
class OdooConfig:
    url: str
    db: str
    user: str
    password: str
    dry_run: bool = False


@dataclass(slots=True)
class Summary:
    created: int = 0
    updated: int = 0
    skipped: int = 0
    notes: list[str] = field(default_factory=list)

    def report(self) -> None:
        log.info("-" * 60)
        log.info("SUMMARY  created=%d  updated=%d  skipped=%d",
                 self.created, self.updated, self.skipped)
        for note in self.notes:
            log.info("  note: %s", note)


class OdooClient:
    """Thin, safe XML-RPC wrapper with upsert semantics."""

    def __init__(self, cfg: OdooConfig) -> None:
        self.cfg = cfg
        self.summary = Summary()
        self._uid: int | None = None
        self._models: xmlrpc.client.ServerProxy | None = None

    # -- connection -------------------------------------------------------
    def connect(self) -> None:
        common = xmlrpc.client.ServerProxy(f"{self.cfg.url}/xmlrpc/2/common")
        try:
            common.version()
        except Exception as exc:  # noqa: BLE001 - surface a clear message
            raise SystemExit(f"cannot reach {self.cfg.url}: {exc}") from exc
        uid = common.authenticate(self.cfg.db, self.cfg.user, self.cfg.password, {})
        if not uid:
            raise SystemExit("authentication failed (check db / user / ODOO_PASSWORD)")
        self._uid = uid
        self._models = xmlrpc.client.ServerProxy(f"{self.cfg.url}/xmlrpc/2/object")
        log.info("connected to %s (db=%s) as uid %s%s",
                 self.cfg.url, self.cfg.db, uid, "  [DRY-RUN]" if self.cfg.dry_run else "")

    # -- low level --------------------------------------------------------
    @property
    def uid(self) -> int:
        if self._uid is None:
            raise RuntimeError("call connect() first")
        return self._uid

    def execute(self, model: str, method: str, *args: Any, **kw: Any) -> Any:
        assert self._models is not None, "call connect() first"
        return self._models.execute_kw(
            self.cfg.db, self._uid, self.cfg.password, model, method, list(args), kw
        )

    def search(
        self, model: str, domain: list[Any], *, limit: int = 0
    ) -> list[int]:
        """Search with Odoo options passed as execute_kw keyword arguments."""
        return self.execute(model, "search", domain, limit=limit)

    def search_read(
        self,
        model: str,
        domain: list[Any],
        fields: list[str],
        *,
        limit: int = 0,
    ) -> list[dict[str, Any]]:
        return self.execute(
            model, "search_read", domain, fields=fields, limit=limit
        )

    def read(
        self, model: str, record_ids: list[int], fields: list[str]
    ) -> list[dict[str, Any]]:
        return self.execute(model, "read", record_ids, fields=fields)

    def fields(self, model: str) -> dict[str, dict[str, Any]]:
        return self.execute(
            model,
            "fields_get",
            attributes=["type", "required", "selection", "readonly"],
        )

    def model_available(self, model: str) -> bool:
        return bool(
            self.search("ir.model", [["model", "=", model]], limit=1)
        )

    def module_installed(self, technical_name: str) -> bool:
        ids = self.search(
            "ir.module.module",
            [["name", "=", technical_name], ["state", "=", "installed"]],
            limit=1,
        )
        return bool(ids)

    # -- idempotent upsert ------------------------------------------------
    def resolve_xmlid(
        self, xmlid: str, *, expected_model: str | None = None
    ) -> int | None:
        """Resolve an external ID without relying on private server methods."""
        module, name = xmlid.split(".", maxsplit=1)
        records = self.search_read(
            "ir.model.data",
            [["module", "=", module], ["name", "=", name]],
            ["model", "res_id"],
            limit=1,
        )
        if not records:
            return None
        if expected_model and records[0]["model"] != expected_model:
            raise RuntimeError(
                f"{xmlid} points to {records[0]['model']}, expected {expected_model}"
            )
        return int(records[0]["res_id"])

    def ensure_xmlid(self, xmlid: str, model: str, record_id: int) -> None:
        """Attach a stable external ID to a record created/found by a seeder."""
        if self.cfg.dry_run or not record_id or self.resolve_xmlid(xmlid):
            return
        module, name = xmlid.split(".", maxsplit=1)
        self.execute(
            "ir.model.data",
            "create",
            {
                "module": module,
                "name": name,
                "model": model,
                "res_id": record_id,
                "noupdate": True,
            },
        )

    def upsert(
        self,
        model: str,
        domain: list[Any],
        values: dict[str, Any],
        label: str,
        *,
        xmlid: str | None = None,
        update: bool = False,
    ) -> int:
        """Find by domain; create if missing (or update existing if update=True).

        Returns the record id, or 0 in dry-run when it would have created.
        """
        rid = self.resolve_xmlid(xmlid, expected_model=model) if xmlid else None
        if not rid:
            found = self.search(model, domain, limit=1)
            rid = found[0] if found else None
        if rid:
            if update:
                if self.cfg.dry_run:
                    log.info("  ~ would update %s", label)
                else:
                    self.execute(model, "write", [rid], values)
                    log.info("  ~ updated   %s [%d]", label, rid)
                self.summary.updated += 1
            else:
                log.info("  . exists    %s [%d]", label, rid)
                self.summary.skipped += 1
            if xmlid:
                self.ensure_xmlid(xmlid, model, rid)
            return rid
        if self.cfg.dry_run:
            log.info("  + would create %s", label)
            self.summary.created += 1
            return 0
        rid = self.execute(model, "create", values)
        if xmlid:
            self.ensure_xmlid(xmlid, model, rid)
        log.info("  + created   %s [%d]", label, rid)
        self.summary.created += 1
        return rid

    def upsert_product(
        self,
        default_code: str,
        name: str,
        price: float,
        *,
        service: bool = False,
        xmlid: str | None = None,
    ) -> int:
        """Upsert an Odoo 19 product template by its internal reference."""
        values: dict[str, Any] = {
            "name": name,
            "default_code": default_code,
            "list_price": price,
            "type": "service" if service else "consu",
        }
        product_fields = self.fields("product.template")
        if not service and "is_storable" in product_fields:
            values["is_storable"] = True
        return self.upsert(
            "product.template",
            [["default_code", "=", default_code]],
            values,
            f"product {default_code}",
            xmlid=xmlid,
        )

    def product_variant_id(self, template_id: int) -> int | None:
        if not template_id:
            return None
        records = self.read(
            "product.template", [template_id], ["product_variant_id"]
        )
        value = records[0].get("product_variant_id") if records else None
        return int(value[0]) if value else None

    def tag_id(self, xmlid: str) -> int | None:
        """Resolve a base-module demo tag external id, if present."""
        try:
            return self.resolve_xmlid(
                xmlid, expected_model="res.partner.category"
            )
        except Exception:  # noqa: BLE001
            return None


def build_arg_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--url", required=True, help="Odoo base URL, e.g. https://db.odoo.com")
    parser.add_argument("--db", required=True, help="database name")
    parser.add_argument("--user", required=True, help="login (email)")
    parser.add_argument("--dry-run", action="store_true", help="read only; write nothing")
    parser.add_argument("--verbose", action="store_true", help="debug logging")
    return parser


def config_from_args(args: argparse.Namespace) -> OdooConfig:
    password = os.environ.get("ODOO_PASSWORD")
    if not password:
        raise SystemExit("set the ODOO_PASSWORD environment variable (never store it in a file)")
    return OdooConfig(url=args.url.rstrip("/"), db=args.db, user=args.user,
                      password=password, dry_run=args.dry_run)


def setup_logging(verbose: bool = False) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(levelname)s %(message)s",
        stream=sys.stdout,
    )
