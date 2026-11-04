"""Inventory of model-provider call sites and their metering join status (#432).

A new chat-completions call site fails here until it is classified, so the
claim that each model call is joined cannot drift from the source.
"""

from __future__ import annotations

import unittest
from pathlib import Path

SRC = Path(__file__).resolve().parents[2]
ENDPOINT = "chat/completions"

# file -> (join status, what it records). "ledger" means the call is admitted,
# priced and completed in the core consumption ledger with its call context.
INVENTORY = {
    "core/src/zava_forward/core/ai.py": ("ledger", "admission, call context, counts, outcome"),
    "api/src/zava_forward/api/resident_demo/aoai.py": (
        "own-accounting",
        "reserved and closed token accounting for the resident demo; not the ledger",
    ),
    "api/src/zava_forward/api/resident_demo/assistant.py": (
        "counts-only-sink",
        "optional validated counts; no ledger, price or context; adapter disabled by default",
    ),
}
NOT_LEDGER_JOINED = {
    "api/src/zava_forward/api/resident_demo/aoai.py",
    "api/src/zava_forward/api/resident_demo/assistant.py",
}


def call_sites() -> set[str]:
    found = set()
    for project in sorted(SRC.iterdir()):
        root = project / "src"
        if not root.is_dir():
            continue
        for path in root.rglob("*.py"):
            if ENDPOINT in path.read_text(encoding="utf-8"):
                found.add(path.relative_to(SRC).as_posix())
    return found


class AiCallSiteInventoryTest(unittest.TestCase):
    def test_every_provider_call_site_is_classified(self) -> None:
        self.assertEqual(call_sites(), set(INVENTORY))

    def test_only_named_sites_lack_the_ledger_join(self) -> None:
        unjoined = {path for path, (status, _) in INVENTORY.items() if status != "ledger"}
        self.assertEqual(unjoined, NOT_LEDGER_JOINED)

    def test_ledger_site_carries_the_call_context_join(self) -> None:
        text = (SRC / "core/src/zava_forward/core/ai.py").read_text(encoding="utf-8")
        for needle in ("ai_consumption.usage(", "consumption.complete(", "configuration"):
            self.assertIn(needle, text)


if __name__ == "__main__":
    unittest.main()
