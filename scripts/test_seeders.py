#!/usr/bin/env python3
"""Offline regression tests for the shared seeder client."""
from __future__ import annotations

import unittest
from typing import Any

from seeders._client import OdooClient, OdooConfig


class RecordingProxy:
    def __init__(self, result: Any) -> None:
        self.result = result
        self.calls: list[tuple[Any, ...]] = []

    def execute_kw(self, *args: Any) -> Any:
        self.calls.append(args)
        return self.result


def connected_client(proxy: RecordingProxy, *, dry_run: bool = False) -> OdooClient:
    client = OdooClient(
        OdooConfig(
            url="https://example.invalid",
            db="demo",
            user="demo@example.invalid",
            password="not-a-real-secret",
            dry_run=dry_run,
        )
    )
    client._uid = 7  # noqa: SLF001 - deliberate isolated client test
    client._models = proxy  # noqa: SLF001 - deliberate isolated client test
    return client


class OdooClientTests(unittest.TestCase):
    def test_search_passes_limit_as_execute_kw_keyword(self) -> None:
        proxy = RecordingProxy([42])
        client = connected_client(proxy)

        result = client.search(
            "res.partner", [["name", "=", "Gulf Towers"]], limit=1
        )

        self.assertEqual(result, [42])
        self.assertEqual(
            proxy.calls[0],
            (
                "demo",
                7,
                "not-a-real-secret",
                "res.partner",
                "search",
                [[["name", "=", "Gulf Towers"]]],
                {"limit": 1},
            ),
        )

    def test_search_read_passes_fields_and_limit_as_keywords(self) -> None:
        proxy = RecordingProxy([{"id": 42, "name": "Gulf Towers"}])
        client = connected_client(proxy)

        result = client.search_read("res.partner", [], ["name"], limit=1)

        self.assertEqual(result[0]["name"], "Gulf Towers")
        self.assertEqual(proxy.calls[0][-2], [[]])
        self.assertEqual(
            proxy.calls[0][-1], {"fields": ["name"], "limit": 1}
        )

    def test_dry_run_upsert_does_not_create(self) -> None:
        proxy = RecordingProxy([])
        client = connected_client(proxy, dry_run=True)

        record_id = client.upsert(
            "res.partner",
            [["email", "=", "new@example.invalid"]],
            {"name": "New Demo Partner"},
            "new demo partner",
        )

        self.assertEqual(record_id, 0)
        self.assertEqual(client.summary.created, 1)
        self.assertEqual(len(proxy.calls), 1)
        self.assertEqual(proxy.calls[0][4], "search")


if __name__ == "__main__":
    unittest.main()
