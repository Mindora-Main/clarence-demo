#!/usr/bin/env python3
"""Validate every Odoo addon manifest under addons/.

Checks, per addon:
  * __manifest__.py exists and parses as a Python literal dict
  * required keys present (name, version, license, depends, installable)
  * `depends` is a list of non-empty strings
  * `data` files referenced actually exist on disk
  * the addon package has an __init__.py
  * addon technical names (folder names) are unique

Exit code 0 on success, 1 on any failure. Lightweight: no Odoo runtime needed.
"""
from __future__ import annotations

import ast
import logging
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger("verify_manifests")

REPO = Path(__file__).resolve().parents[1]
ADDONS = REPO / "addons"
REQUIRED_KEYS = ("name", "version", "license", "depends", "installable")


def parse_manifest(path: Path) -> dict[str, Any]:
    """Parse an Odoo __manifest__.py into a dict using a safe literal eval."""
    text = path.read_text(encoding="utf-8")
    return ast.literal_eval(text)


def check_addon(addon_dir: Path) -> list[str]:
    """Return a list of error strings for one addon (empty == OK)."""
    errors: list[str] = []
    name = addon_dir.name
    manifest_path = addon_dir / "__manifest__.py"

    if not manifest_path.is_file():
        return [f"{name}: missing __manifest__.py"]
    if not (addon_dir / "__init__.py").is_file():
        errors.append(f"{name}: missing __init__.py")

    try:
        data = parse_manifest(manifest_path)
    except (ValueError, SyntaxError) as exc:
        return [f"{name}: manifest does not parse ({exc})"]

    if not isinstance(data, dict):
        return [f"{name}: manifest is not a dict"]

    for key in REQUIRED_KEYS:
        if key not in data:
            errors.append(f"{name}: manifest missing required key '{key}'")

    depends = data.get("depends", [])
    if not isinstance(depends, list) or not all(
        isinstance(d, str) and d for d in depends
    ):
        errors.append(f"{name}: 'depends' must be a list of non-empty strings")

    manifest_data = data.get("data", [])
    if not isinstance(manifest_data, list) or not all(
        isinstance(rel, str) and rel for rel in manifest_data
    ):
        errors.append(f"{name}: 'data' must be a list of non-empty strings")
        manifest_data = []
    for rel in manifest_data:
        data_path = addon_dir / rel
        if not data_path.is_file():
            errors.append(f"{name}: data file not found -> {rel}")
        elif data_path.suffix == ".xml":
            try:
                ET.parse(data_path)
            except ET.ParseError as exc:
                errors.append(f"{name}: invalid XML {rel} ({exc})")

    if data.get("license") != "LGPL-3":
        errors.append(f"{name}: license must be LGPL-3")
    version = data.get("version")
    if not isinstance(version, str) or not version.startswith("19.0."):
        errors.append(f"{name}: version must start with 19.0.")
    for flag in ("installable", "application", "auto_install"):
        if flag in data and not isinstance(data[flag], bool):
            errors.append(f"{name}: '{flag}' must be a boolean")
    if data.get("installable") is not True:
        errors.append(f"{name}: installable must be True")
    if data.get("application") is not False:
        errors.append(f"{name}: application must be False")
    if data.get("auto_install") is not False:
        errors.append(f"{name}: auto_install must be False")
    if name != "mindora_demo_base" and "mindora_demo_base" not in depends:
        errors.append(f"{name}: branch module must depend on mindora_demo_base")

    return errors


def main() -> int:
    if not ADDONS.is_dir():
        log.error("addons/ directory not found at %s", ADDONS)
        return 1

    addon_dirs = sorted(
        p for p in ADDONS.iterdir() if p.is_dir() and (p / "__manifest__.py").exists()
    )
    if not addon_dirs:
        log.error("no addons with a manifest found under %s", ADDONS)
        return 1

    seen: dict[str, Path] = {}
    all_errors: list[str] = []
    for addon in addon_dirs:
        if addon.name in seen:
            all_errors.append(f"duplicate addon technical name: {addon.name}")
        seen[addon.name] = addon
        all_errors.extend(check_addon(addon))

    log.info("checked %d addons", len(addon_dirs))
    if all_errors:
        for err in all_errors:
            log.error(err)
        log.error("manifest verification FAILED (%d issue(s))", len(all_errors))
        return 1
    log.info("manifest verification PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
