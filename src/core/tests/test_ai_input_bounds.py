"""Input bounds stop a request before any provider call (#116). Constructed data only."""

from __future__ import annotations

import unittest
from typing import Any
from unittest import mock

from zava_forward.core.ai import MAX_IMAGE_BYTES, MAX_TEXT_BYTES
from zava_forward.core.ai import Ai as UntypedAi

Ai: Any = UntypedAi


class Meter:
    def __init__(self) -> None:
        self.reserved = 0

    def reserve(self, *args: Any, **kwargs: Any) -> str:
        self.reserved += 1
        raise RuntimeError("meter reached")


class InputBounds(unittest.TestCase):
    def setUp(self) -> None:
        self.ai = Ai()
        self.ai.endpoint = "https://provider.invalid"
        self.meter = Meter()
        self.ai.consumption = self.meter
        patcher = mock.patch("urllib.request.urlopen")
        self.urlopen = patcher.start()
        self.addCleanup(patcher.stop)

    def test_oversized_text_run_uses_template_and_names_the_error(self) -> None:
        out = self.ai.run("draft", "sys", "x" * (MAX_TEXT_BYTES + 1), "TEMPLATE")
        self.assertEqual(out["source"], "template")
        self.assertEqual(out["text"], "TEMPLATE")
        self.assertEqual(out["error"], "InputRefused")
        self.assertEqual(self.meter.reserved, 0)
        self.urlopen.assert_not_called()

    def test_oversized_evidence_is_refused_visibly(self) -> None:
        out = self.ai.evidence("sys", "x" * (MAX_TEXT_BYTES + 1))
        self.assertEqual(out["outcome"], "input-refused")
        self.assertEqual(out["reason"], "input-too-large")
        self.assertIsNone(out["text"])
        self.assertEqual(self.meter.reserved, 0)
        self.urlopen.assert_not_called()

    def test_bounded_text_still_reaches_the_meter(self) -> None:
        self.ai.run("draft", "sys", "short", "TEMPLATE")
        self.assertEqual(self.meter.reserved, 1)

    def test_oversized_image_is_stored_not_sent(self) -> None:
        out = self.ai.look_at("a.png", b"\0" * (MAX_IMAGE_BYTES + 1), "image/png")
        self.assertEqual(out["source"], "template")
        self.assertIn("manual route", out["reason"])
        self.assertEqual(self.meter.reserved, 0)
        self.urlopen.assert_not_called()

    def test_unapproved_image_type_is_stored_not_sent(self) -> None:
        out = self.ai.look_at("a.svg", b"<svg/>", "image/svg+xml")
        self.assertEqual(out["source"], "template")
        self.assertEqual(self.meter.reserved, 0)
        self.urlopen.assert_not_called()

    def test_approved_image_reaches_the_meter(self) -> None:
        self.ai.look_at("a.png", b"\x89PNG", "image/png")
        self.assertEqual(self.meter.reserved, 1)


if __name__ == "__main__":
    unittest.main()
