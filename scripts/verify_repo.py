#!/usr/bin/env python3
"""Repository structure & content verification for the Mindora demo lab.

Verifies:
  * all expected addon folders exist (base + 17 branch meta modules)
  * required docs exist
  * required seeder + verification scripts exist
  * docs/branch-matrix.csv references addons that actually exist
  * no leftover placeholder text from the original sample module

Lightweight; no Odoo runtime. Exit 0 on success, 1 on failure.
"""
from __future__ import annotations

import csv
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger("verify_repo")

REPO = Path(__file__).resolve().parents[1]

EXPECTED_ADDONS = [
    "mindora_demo_base",
    "mindora_demo_00_base_universal",
    "mindora_demo_01_al_noor_live_os",
    "mindora_demo_02_sales",
    "mindora_demo_03_commerce",
    "mindora_demo_04_core",
    "mindora_demo_05_retail",
    "mindora_demo_06_online",
    "mindora_demo_07_client_work",
    "mindora_demo_08_field_service_after_sales",
    "mindora_demo_09_workshop",
    "mindora_demo_10_mrp",
    "mindora_demo_11_mrp_plus",
    "mindora_demo_12_team",
    "mindora_demo_13_marketing",
    "mindora_demo_14_board",
    "mindora_demo_15_holding",
    "mindora_demo_16_room",
]
EXPECTED_BRANCHES = [
    "demo/00-base-universal",
    "demo/01-al-noor-live-os",
    "demo/02-sales",
    "demo/03-commerce",
    "demo/04-core",
    "demo/05-retail",
    "demo/06-online",
    "demo/07-client-work",
    "demo/08-field-service-after-sales",
    "demo/09-workshop",
    "demo/10-mrp",
    "demo/11-mrp-plus",
    "demo/12-team",
    "demo/13-marketing",
    "demo/14-board",
    "demo/15-holding",
    "demo/16-room",
]

REQUIRED_DOCS = [
    "docs/PRIMARY_ODOO_SH_BRANCHES.md",
    "docs/ODOO_SH_RUNBOOK.md",
    "docs/branch-matrix.csv",
    "docs/branch-installation.md",
    "docs/al-noor-live-demo-script.md",
    "docs/demo-data-policy.md",
    "docs/demo-reset-runbook.md",
    "docs/module-name-validation.md",
    "docs/demo-data-dictionary.md",
]

REQUIRED_SCRIPTS = [
    "scripts/verify_repo.py",
    "scripts/verify_odoo_manifests.py",
    "scripts/branch_report.py",
    "scripts/test_seeders.py",
    "scripts/seeders/README.md",
    "scripts/seeders/seed_al_noor.py",
    "scripts/seeders/seed_services.py",
    "scripts/seeders/seed_mrp.py",
    "scripts/seeders/seed_holding.py",
]
REQUIRED_REPO_FILES = [
    "README.md",
    ".github/workflows/repo-check.yml",
]
FORBIDDEN_ROOT_PATHS = [
    "__init__.py",
    "__manifest__.py",
    "controllers",
    "models",
    "security",
    "views",
]

# Strings that must NOT survive from the original placeholder module.
FORBIDDEN_PLACEHOLDERS = [
    "clarence.demo.sample",
    "SampleModel",
    "Sample model for demonstration",
    "Clarence Demo Module",
]


def check_paths(paths: list[str], label: str) -> list[str]:
    errors = []
    for rel in paths:
        if not (REPO / rel).exists():
            errors.append(f"missing {label}: {rel}")
    return errors


def check_branch_matrix() -> list[str]:
    errors: list[str] = []
    matrix = REPO / "docs" / "branch-matrix.csv"
    if not matrix.is_file():
        return ["docs/branch-matrix.csv not found"]
    branches: list[str] = []
    modules: list[str] = []
    build_first: list[str] = []
    with matrix.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        required_columns = {
            "branch", "module", "database", "purpose", "seeder", "build_first"
        }
        missing_columns = required_columns - set(reader.fieldnames or [])
        if missing_columns:
            return [
                "branch-matrix.csv: missing columns "
                + ", ".join(sorted(missing_columns))
            ]
        for i, row in enumerate(reader, start=2):
            branch = (row.get("branch") or "").strip()
            module = (row.get("module") or "").strip()
            database = (row.get("database") or "").strip()
            if not branch or not module or not database:
                errors.append(
                    f"branch-matrix.csv line {i}: branch/module/database required"
                )
                continue
            branches.append(branch)
            modules.append(module)
            if (row.get("build_first") or "").strip().lower() == "yes":
                build_first.append(branch)
            if not (REPO / "addons" / module / "__manifest__.py").is_file():
                errors.append(
                    f"branch-matrix.csv line {i}: module '{module}' has no addon"
                )
    if branches != EXPECTED_BRANCHES:
        missing = sorted(set(EXPECTED_BRANCHES) - set(branches))
        extra = sorted(set(branches) - set(EXPECTED_BRANCHES))
        if missing:
            errors.append(f"branch-matrix.csv missing branches: {', '.join(missing)}")
        if extra:
            errors.append(f"branch-matrix.csv unexpected branches: {', '.join(extra)}")
        if not missing and not extra:
            errors.append("branch-matrix.csv branches are not in canonical order")
    if len(modules) != len(set(modules)):
        errors.append("branch-matrix.csv contains duplicate modules")
    if build_first != ["demo/01-al-noor-live-os"]:
        errors.append(
            "branch-matrix.csv must mark only demo/01-al-noor-live-os build_first=yes"
        )
    return errors


def check_placeholders() -> list[str]:
    errors: list[str] = []
    for path in REPO.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        if path.suffix not in {".py", ".xml", ".md", ".csv", ".txt"}:
            continue
        # the validation list itself is allowed to mention these tokens
        if path.name in {"verify_repo.py"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for token in FORBIDDEN_PLACEHOLDERS:
            if token in text:
                errors.append(f"placeholder '{token}' still present in {path.relative_to(REPO)}")
    return errors


def main() -> int:
    errors: list[str] = []
    errors += check_paths([f"addons/{a}/__manifest__.py" for a in EXPECTED_ADDONS], "addon")
    errors += check_paths(REQUIRED_DOCS, "doc")
    errors += check_paths(REQUIRED_SCRIPTS, "script")
    errors += check_paths(REQUIRED_REPO_FILES, "repository file")
    errors += check_branch_matrix()
    errors += check_placeholders()
    for rel in FORBIDDEN_ROOT_PATHS:
        if (REPO / rel).exists():
            errors.append(f"obsolete root sample path remains: {rel}")

    if errors:
        for err in errors:
            log.error(err)
        log.error("repo verification FAILED (%d issue(s))", len(errors))
        return 1
    log.info("repo verification PASSED (%d addons, %d docs)", len(EXPECTED_ADDONS), len(REQUIRED_DOCS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
