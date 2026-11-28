"""Provider spy across every Ai family: a refused payload never reaches the transport (Refs #116).

Constructed payloads only. Each family is driven with input outside the approved
type or size allowlist; the transport, the meter and the data-protection hold
must see nothing.
"""

from __future__ import annotations

import base64
import unittest
from typing import Any
from unittest import mock

from zava_forward.agents import heldout_aoai  # type: ignore[import-untyped]
from zava_forward.core import ai_consumption
from zava_forward.core.ai import MAX_IMAGE_BYTES, MAX_TEXT_BYTES
from zava_forward.core.ai import Ai as UntypedAi

Ai: Any = UntypedAi

OVERSIZE = "x" * (MAX_TEXT_BYTES + 1)
PNG = "data:image/png;base64," + base64.b64encode(b"png").decode()
UNAPPROVED_PAYLOADS: dict[str, Any] = {
    "oversized-text": OVERSIZE,
    "extra-part-key": [{"type": "text", "text": "ok", "extra": "hidden"}],
    "gif-image": [{"type": "image_url", "image_url": {"url": "data:image/gif;base64,AAAA"}}],
    "image-url-extra-key": [{"type": "image_url", "image_url": {"url": PNG, "detail": "high"}}],
    "remote-image": [{"type": "image_url", "image_url": {"url": "https://x.invalid/a.png"}}],
    "not-a-list": {"type": "text", "text": "ok"},
    "empty-list": [],
}


class Meter:
    def __init__(self) -> None:
        self.reserved = 0

    def reserve(self, *args: Any, **kwargs: Any) -> str:
        self.reserved += 1
        raise RuntimeError("meter reached")


class ProviderBoundaryZeroTransport(unittest.TestCase):
    def setUp(self) -> None:
        self.ai = Ai()
        self.ai.endpoint = "https://provider.invalid"
        self.meter = Meter()
        self.ai.consumption = self.meter
        patcher = mock.patch("urllib.request.urlopen")
        self.urlopen = patcher.start()
        self.addCleanup(patcher.stop)
        hold = mock.patch("zava_forward.core.data_protection.dispatch_hold", return_value=None)
        self.hold = hold.start()
        self.addCleanup(hold.stop)

    def assert_nothing_sent(self, *, hold_checked: bool = False) -> None:
        self.urlopen.assert_not_called()
        self.assertEqual(self.meter.reserved, 0)
        if not hold_checked:  # run() consults the hold itself before it reaches the shared boundary
            self.hold.assert_not_called()

    def test_evidence_refuses_every_unapproved_shape_visibly(self) -> None:
        for label, payload in UNAPPROVED_PAYLOADS.items():
            with self.subTest(label):
                out = self.ai.evidence("sys", payload)
                self.assertEqual(out["outcome"], "input-refused")
                self.assertIsNone(out["text"])
        self.assert_nothing_sent()

    def test_run_falls_back_to_the_template_for_every_unapproved_shape(self) -> None:
        for label, payload in UNAPPROVED_PAYLOADS.items():
            with self.subTest(label):
                out = self.ai.run("funding_draft", "sys", payload, "TEMPLATE")
                self.assertEqual(out["source"], "template")
                self.assertEqual(out["error"], "InputRefused")
        self.assert_nothing_sent(hold_checked=True)

    def test_private_chat_enforces_the_same_boundary(self) -> None:
        for label, payload in UNAPPROVED_PAYLOADS.items():
            with self.subTest(label), self.assertRaises(ValueError):
                self.ai._chat(self.ai.fast, "sys", payload)
        self.assert_nothing_sent()

    def test_non_text_system_prompt_is_refused(self) -> None:
        out = self.ai.evidence(["system"], "ok")
        self.assertEqual(out["outcome"], "input-refused")
        self.assert_nothing_sent()

    def test_look_at_stores_unapproved_bytes_without_sending(self) -> None:
        cases = {
            "oversized-image": ("scan.png", b"\0" * (MAX_IMAGE_BYTES + 1), "image/png"),
            "gif": ("scan.gif", b"GIF89a", "image/gif"),
            "pdf": ("scan.pdf", b"%PDF-1.4", "application/pdf"),
        }
        for label, (name, data, mime) in cases.items():
            with self.subTest(label):
                out = self.ai.look_at(name, data, mime)
                self.assertEqual(out["source"], "template")
        self.assert_nothing_sent()

    def test_refusal_precedes_the_simulation_seal_and_captured_readings(self) -> None:
        seal = ai_consumption.SIMULATION_SEAL.set(object())
        readings = ai_consumption.CAPTURED_READINGS.set(True)
        try:
            out = self.ai.evidence("sys", OVERSIZE)
        finally:
            ai_consumption.CAPTURED_READINGS.reset(readings)
            ai_consumption.SIMULATION_SEAL.reset(seal)
        self.assertEqual(out["outcome"], "input-refused")
        self.assert_nothing_sent()

    def test_held_out_provider_refuses_before_building_a_request(self) -> None:
        opener = mock.Mock()
        call = heldout_aoai.make_provider(
            "https://aoai-demo.openai.azure.com", "dep", "model", "token", opener
        )
        out = call("sys", OVERSIZE, 10, 5)
        self.assertEqual(out, {"outcome": "failed"})
        opener.assert_not_called()


if __name__ == "__main__":
    unittest.main()
