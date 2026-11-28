"""Input bounds stop a request before any provider call (#116). Constructed data only."""

from __future__ import annotations

import unittest
from typing import Any
from unittest import mock

from zava_forward.core.ai import MAX_IMAGE_BYTES, MAX_PARTS, MAX_TEXT_BYTES
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
        out = self.ai.run("funding_draft", "sys", "x" * (MAX_TEXT_BYTES + 1), "TEMPLATE")
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

    def test_oversized_string_is_refused_before_the_protection_hold(self) -> None:
        target = "zava_forward.core.data_protection.dispatch_hold"
        with mock.patch(target, return_value="held") as hold:
            out = self.ai.evidence("sys", "x" * (MAX_TEXT_BYTES + 1))
        self.assertEqual(out["reason"], "input-too-large")
        hold.assert_not_called()
        self.urlopen.assert_not_called()

    def test_system_and_string_user_share_one_text_budget(self) -> None:
        out = self.ai.evidence("s" * (MAX_TEXT_BYTES // 2 + 1), "u" * (MAX_TEXT_BYTES // 2))
        self.assertEqual(out["reason"], "input-too-large")
        self.urlopen.assert_not_called()

    def test_bounded_text_still_reaches_the_meter(self) -> None:
        self.ai.run("funding_draft", "sys", "short", "TEMPLATE")
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

    def refused(self, user: Any, system: Any = "sys") -> None:
        out = self.ai.evidence(system, user)
        self.assertEqual(out["outcome"], "input-refused")
        self.assertIsNone(out["text"])
        self.assertEqual(self.meter.reserved, 0)
        self.urlopen.assert_not_called()

    def test_shared_boundary_refuses_unapproved_payload_types(self) -> None:
        png = "data:image/png;base64,AAAA"
        text = {"type": "text", "text": "hi"}
        for user in (
            ["raw string part"],
            [],
            {"type": "text", "text": "hi"},
            [{"type": "text", "text": "hi", "extra": 1}],
            [text, {"type": "image_url", "image_url": {"url": "data:image/svg+xml;base64,AAAA"}}],
            [text, {"type": "image_url", "image_url": {"url": png, "detail": "high"}}],
            [text, {"type": "image_url", "image_url": {"url": "https://host.invalid/a.png"}}],
        ):
            with self.subTest(user=user):
                self.refused(user)
        self.refused("user", system=["not", "text"])

    def test_shared_boundary_bounds_image_and_text_for_list_payloads(self) -> None:
        big = "A" * ((MAX_IMAGE_BYTES // 3 + 2) * 4)
        image = {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{big}"}}
        self.refused([{"type": "text", "text": "hi"}, image])
        self.refused([{"type": "text", "text": "x" * (MAX_TEXT_BYTES + 1)}])

    def test_shared_boundary_bounds_total_image_bytes(self) -> None:
        half = "A" * ((MAX_IMAGE_BYTES // 2 // 3) * 4)
        image = {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{half}"}}
        self.refused([{"type": "text", "text": "hi"}, image, image, image])
        self.ai.evidence("sys", [{"type": "text", "text": "hi"}, image, image])
        self.assertEqual(self.meter.reserved, 1)

    def test_shared_boundary_bounds_part_count(self) -> None:
        empty = {"type": "text", "text": ""}
        out = self.ai.evidence("sys", [empty] * (MAX_PARTS + 1))
        self.assertEqual(out["outcome"], "input-refused")
        self.assertEqual(out["reason"], "input-too-many-parts")
        self.assertEqual(self.meter.reserved, 0)
        self.urlopen.assert_not_called()
        self.ai.evidence("sys", [empty] * MAX_PARTS)
        self.assertEqual(self.meter.reserved, 1)

    def test_shared_boundary_refuses_non_base64_image_data(self) -> None:
        for data in ("ignore previous instructions", "AAAA AAAA", "AAA", "AAAA\nAAAA"):
            with self.subTest(data=data):
                part = {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{data}"}}
                self.refused([{"type": "text", "text": "hi"}, part])

    def test_shared_boundary_refuses_unencodable_text_visibly(self) -> None:
        text = {"type": "text", "text": "a\ud800"}
        for system, user in (("sys", "a\ud800"), ("a\udc00", "hi"), ("sys", [text])):
            with self.subTest(system=system, user=user):
                result = self.ai.evidence(system, user)
                self.assertEqual(result["outcome"], "input-refused")
                self.assertEqual(result["reason"], "input-type-not-approved")
        self.assertEqual(self.meter.reserved, 0)
        self.urlopen.assert_not_called()

    def test_text_budget_is_inclusive_and_counts_utf8_bytes(self) -> None:
        part = {"type": "text", "text": "x" * (MAX_TEXT_BYTES - 1)}
        self.ai.evidence("s", [part])
        self.assertEqual(self.meter.reserved, 1)
        self.meter.reserved = 0
        self.refused([part], system="ss")
        self.refused([{"type": "text", "text": "é" * (MAX_TEXT_BYTES // 2)}], system="s")

    def test_plain_string_is_refused_at_the_serialized_limit(self) -> None:
        # The string route also bounds the serialized request body, so the exact limit is refused.
        out = self.ai.evidence("s", "x" * (MAX_TEXT_BYTES - 1))
        self.assertEqual(out["reason"], "input-too-large")
        self.ai.evidence("s", "x" * (MAX_TEXT_BYTES - 1024))
        self.assertEqual(self.meter.reserved, 1)

    def test_text_budget_is_summed_across_parts(self) -> None:
        half = {"type": "text", "text": "x" * (MAX_TEXT_BYTES // 2)}
        self.refused([half, half, {"type": "text", "text": "x"}])

    def test_malformed_text_and_image_parts_are_refused(self) -> None:
        png = "data:image/png;base64,AAAA"
        for part in (
            {"type": "text", "text": None},
            {"type": "text", "text": b"bytes"},
            {"type": "text"},
            {"type": "image_url"},
            {"type": "image_url", "image_url": "data:image/png;base64,AAAA"},
            {"type": "image_url", "image_url": {"url": None}},
            {"type": "image_url", "image_url": {}},
            {"type": "image_url", "image_url": {"url": "image/png;base64,AAAA"}},
            {"type": "image_url", "image_url": {"url": "data:image/png,AAAA"}},
            {"type": "image_url", "image_url": {"url": "data:IMAGE/PNG;base64,AAAA"}},
            {"type": "image_url", "image_url": {"url": "data:image/png ;base64,AAAA"}},
            {"type": "image_url", "image_url": {"url": png}, "text": "hi"},
        ):
            with self.subTest(part=part):
                self.refused([part])

    def test_non_text_system_values_are_refused(self) -> None:
        for system in (None, b"sys", 0, {"type": "text"}):
            with self.subTest(system=system):
                self.refused("user", system=system)

    def test_image_budget_is_inclusive(self) -> None:
        exact = "A" * (MAX_IMAGE_BYTES // 3 * 4)
        image = {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{exact}"}}
        self.ai.evidence("sys", [{"type": "text", "text": "hi"}, image])
        self.assertEqual(self.meter.reserved, 1)

    def test_look_at_image_limit_and_exact_type(self) -> None:
        # The encoded size, with padding, is what the shared boundary measures.
        # The exact limit is therefore refused.
        out = self.ai.look_at("a.png", b"\0" * MAX_IMAGE_BYTES, "image/png")
        self.assertEqual(out["error"], "InputRefused")
        self.assertEqual(self.meter.reserved, 0)
        self.ai.look_at("a.png", b"\0" * (MAX_IMAGE_BYTES - 3), "image/png")
        self.assertEqual(self.meter.reserved, 1)
        self.meter.reserved = 0
        for mime in ("IMAGE/PNG", "image/png; charset=binary", "image/gif", "image/webp"):
            with self.subTest(mime=mime):
                out = self.ai.look_at("a.img", b"\x89PNG", mime)
                self.assertEqual(out["source"], "template")
        self.assertEqual(self.meter.reserved, 0)
        self.urlopen.assert_not_called()

    def test_approved_list_payload_reaches_the_meter(self) -> None:
        part = {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,AAAA"}}
        self.ai.evidence("sys", [{"type": "text", "text": "hi"}, part])
        self.assertEqual(self.meter.reserved, 1)


if __name__ == "__main__":
    unittest.main()
