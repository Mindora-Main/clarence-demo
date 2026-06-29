#!/usr/bin/env python3
"""Print a human-readable report of demo branches from docs/branch-matrix.csv.

Cross-checks that each referenced meta module exists under addons/.
Lightweight; no Odoo runtime. Exit 0 on success, 1 if a module is missing.
"""
from __future__ import annotations

import csv
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("branch_report")

REPO = Path(__file__).resolve().parents[1]
MATRIX = REPO / "docs" / "branch-matrix.csv"
EXPECTED_BRANCH_COUNT = 17


def main() -> int:
    if not MATRIX.is_file():
        log.error("docs/branch-matrix.csv not found")
        return 1

    with MATRIX.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    missing = 0
    errors = 0
    seen_branches: set[str] = set()
    seen_modules: set[str] = set()
    log.info("%-32s %-34s %s", "BRANCH", "MODULE", "STATUS")
    log.info("%s", "-" * 90)
    for row in rows:
        branch = (row.get("branch") or "").strip()
        module = (row.get("module") or "").strip()
        ok = (REPO / "addons" / module / "__manifest__.py").is_file()
        duplicate = branch in seen_branches or module in seen_modules
        status = "ok" if ok and not duplicate else (
            "DUPLICATE" if duplicate else "MISSING ADDON"
        )
        if not ok:
            missing += 1
        if duplicate:
            errors += 1
        seen_branches.add(branch)
        seen_modules.add(module)
        log.info("%-32s %-34s %s", branch, module, status)
    log.info("%s", "-" * 90)
    if len(rows) != EXPECTED_BRANCH_COUNT:
        errors += 1
        log.error("expected %d branches, found %d", EXPECTED_BRANCH_COUNT, len(rows))
    log.info(
        "%d branches, %d missing addon(s), %d matrix error(s)",
        len(rows), missing, errors,
    )
    return 1 if missing or errors else 0


if __name__ == "__main__":
    sys.exit(main())
