"""HTTP, accessible HTML, permission, non-leakage, and keyboard tests for Issue #130 routes."""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import tempfile
import threading
import unittest
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from tests.test_mvp import DATA
from zava_forward.core.sqlstore import SqlStore

from zava_forward.api.server import App, make_handler


class _AccessibleFormInspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.labels_for: set[str] = set()
        self.control_ids: list[str] = []
        self.select_options: dict[str, list[str]] = {}
        self.live_regions: int = 0
        self.details_summaries: int = 0
        self._current_select_id: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {k: (v or "") for k, v in attrs}
        if tag == "label" and attr_map.get("for"):
            self.labels_for.add(attr_map["for"])
        elif tag in ("input", "select", "textarea"):
            if attr_map.get("type") != "hidden":
                cid = attr_map.get("id", "")
                self.control_ids.append(cid)
                if tag == "select":
                    self._current_select_id = cid
                    self.select_options.setdefault(cid, [])
        elif tag == "option" and self._current_select_id is not None:
            self.select_options[self._current_select_id].append(attr_map.get("value", ""))
        elif tag == "summary":
            self.details_summaries += 1
        if attr_map.get("role") in ("status", "alert") or attr_map.get("aria-live"):
            self.live_regions += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "select":
            self._current_select_id = None


def _playwright_available() -> bool:
    return importlib.util.find_spec("playwright") is not None


class NominationApiRoutesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "synthetic.json"
        data = copy.deepcopy(DATA)
        data["staff"].extend(
            [
                {
                    "code": "RLO-2",
                    "name": "Rae Reviewer",
                    "email": "rae@example.test",
                    "role": "Resident Liaison Officer",
                },
                {
                    "code": "CON-1",
                    "name": "Kim Contractor",
                    "email": "kim@example.test",
                    "role": "Contractor",
                    "contractor": "Test Ltd",
                },
                {
                    "code": "RC-1",
                    "name": "Rex Coordinator",
                    "email": "rex@example.test",
                    "role": "Retrofit Coordinator",
                },
                {
                    "code": "BSL-1",
                    "name": "Bea Safety",
                    "email": "bea@example.test",
                    "role": "Building Safety Liaison",
                },
            ]
        )
        self.path.write_text(json.dumps(data))
        self.store = SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
        self.addCleanup(self.store.db.close)
        app_cls: Any = App
        self.app = app_cls(self.store, "synthetic-only")
        from http.server import ThreadingHTTPServer

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.app))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.shutdown)
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"
        self.cookies: dict[str, str] = {}

    def shutdown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)

    def _login_cookie(self, actor: str) -> str:
        if actor not in self.cookies:
            req = Request(
                self.base + "/api/login",
                json.dumps(
                    {"email": f"{actor}@example.test", "password": "synthetic-only"}
                ).encode(),
            )
            with urlopen(req, timeout=5) as response:
                self.cookies[actor] = response.headers["Set-Cookie"].split(";")[0]
        return self.cookies[actor]

    def request_raw(self, path: str, actor: str = "", body: object = None) -> tuple[int, str, str]:
        headers: dict[str, str] = {}
        if actor:
            headers["Cookie"] = self._login_cookie(actor)
        payload: bytes | None = None
        if body is not None:
            payload = json.dumps(body).encode()
            headers["Content-Type"] = "application/json"
            headers["X-ZF-Request"] = "same-origin"
        req = Request(self.base + path, payload, headers=headers)
        try:
            with urlopen(req, timeout=10) as response:
                content_type = response.headers.get("Content-Type", "")
                return response.status, content_type, response.read().decode("utf-8")
        except HTTPError as err:
            content_type = err.headers.get("Content-Type", "")
            return err.code, content_type, err.read().decode("utf-8")

    def call_json(self, path: str, actor: str = "", body: object = None) -> tuple[int, Any]:
        status, _ctype, raw = self.request_raw(path, actor, body)
        return status, json.loads(raw)

    def nomination_payload(self, **overrides: Any) -> dict[str, Any]:
        base: dict[str, Any] = {
            "action": "nomination_record",
            "case_id": "ZF-1",
            "kind": "Self-referral",
            "reported_subject_ref": "SYN-SUBJ-130",
            "account": "SYN resident referral account",
            "source": "SYN intake note",
            "channel": "digital",
            "owner": "sam@example.test",
            "acknowledgement_ref": "SYN-ACK-INIT",
            "next_update": "2099-02-01",
            "non_digital_route": "Phone Sam or visit the local housing office",
            "hazard_concern": False,
        }
        base.update(overrides)
        return base

    def seed_priority_proposal(self, *, ai_mode: bool = False) -> dict[str, Any]:
        proposal = dict(
            self.store.ai_priority(self.store.staff["sam@example.test"], mode="workflow-only")
        )
        self.store.resolve_priority(
            self.store.staff["sam@example.test"], str(proposal["id"]), "accept"
        )
        if ai_mode:
            with self.store.lock:
                for rec in self.store.data.get("recommendations", ()):
                    if rec.get("id") == proposal["id"]:
                        rec["source"] = "ai"
                        rec["model"] = "gpt-4.1-mini"
                self.store.save()
        return proposal

    def test_ac1_plain_language_explanations_and_vulnerability_non_leakage_across_roles(
        self,
    ) -> None:
        code, created = self.call_json("/api/cases/ZF-1/resident", "sam", self.nomination_payload())
        self.assertEqual(code, 200, created)
        no_ai_exp = created["nomination_records"][0]["plain_language_explanation"]
        self.assertIs(no_ai_exp["permitted"], True)
        self.assertIs(no_ai_exp["ai_involved"], False)
        self.assertIn("No AI was involved", no_ai_exp["ai_involvement_explanation"])
        self.assertIn("Sam", no_ai_exp["human_decision_owner"])
        self.assertTrue(no_ai_exp["policy_reasons"])
        self.assertIn("Unknown", no_ai_exp["uncertainty_note"])

        proposal = self.seed_priority_proposal(ai_mode=True)
        target = next(
            item
            for item in self.call_json("/api/cases/ZF-1", "sam")[1]["challenge_targets"]
            if item["proposal_id"] == proposal["id"]
        )
        challenge_req = {
            "action": "challenge_open",
            "proposal_id": proposal["id"],
            "proposal_version": target["proposal_version"],
            "decision_version": target["decision_version"],
            "target_kind": "proposal",
            "channel": "staff_recorded_non_digital",
            "assisted_channel": "Phone",
            "source": "SYN-CH-SRC-130",
            "request": "SYN check home heating evidence",
            "explanation": "SYN plain-language summary given on call",
            "owner": "sam@example.test",
            "non_digital_route": "Phone Sam or write to staffed office",
            "next_update": "2099-02-10",
            "hazard_concern": False,
        }
        code, after_ch = self.call_json("/api/cases/ZF-1/resident", "sam", challenge_req)
        self.assertEqual(code, 200, after_ch)

        with self.store.lock:
            raw_case = self.store._case("ZF-1")
            raw_case["nomination_records"][0]["support_needs"] = "SYN-VULN-SUPPORT-SECRET"
            raw_case["nomination_records"][0]["risk_flags"] = "SYN-VULN-RISK-SECRET"
            raw_case["nomination_records"][0]["vulnerability_notes"] = "SYN-RESTRICTED-VULN-1"
            raw_case["nomination_records"][0]["safeguarding_detail"] = "SYN-RESTRICTED-SAFE-1"
            raw_case["affected_challenges"][0]["medical_detail"] = "SYN-RESTRICTED-MED-1"
            raw_case["affected_challenges"][0]["domestic_abuse_note"] = "SYN-RESTRICTED-DA-1"
            self.store.save()

        code, sam_case = self.call_json("/api/cases/ZF-1", "sam")
        self.assertEqual(code, 200)
        nom_exp = sam_case["nomination_records"][0]["plain_language_explanation"]
        ch_exp = sam_case["affected_challenges"][0]["plain_language_explanation"]
        tgt_exp = sam_case["challenge_targets"][0]["plain_language_explanation"]
        for exp in (nom_exp, ch_exp, tgt_exp):
            self.assertIs(exp["permitted"], True)
            self.assertIs(exp["ai_involved"], True)
            self.assertTrue(exp["human_decision_owner"])
            self.assertIn("gpt-4.1-mini", exp["ai_involvement_explanation"])
            self.assertTrue(exp["policy_reasons"])
            self.assertTrue(exp["uncertainty_note"])
            for secret in (
                "SYN-VULN-SUPPORT-SECRET",
                "SYN-VULN-RISK-SECRET",
                "SYN-RESTRICTED-VULN-1",
                "SYN-RESTRICTED-SAFE-1",
                "SYN-RESTRICTED-MED-1",
                "SYN-RESTRICTED-DA-1",
            ):
                self.assertNotIn(secret, json.dumps(exp))

        html_code, html_ctype, html_doc = self.request_raw(
            "/api/cases/ZF-1?view=nomination-routes-html", "sam"
        )
        self.assertEqual(html_code, 200)
        self.assertIn("text/html", html_ctype)
        self.assertIn("gpt-4.1-mini", html_doc)
        self.assertIn("Human decision owner", html_doc)

        for restricted in (
            "SYN-RESTRICTED-VULN-1",
            "SYN-RESTRICTED-SAFE-1",
            "SYN-RESTRICTED-MED-1",
            "SYN-RESTRICTED-DA-1",
        ):
            self.assertNotIn(restricted, json.dumps(sam_case))
            self.assertNotIn(restricted, html_doc)
        for secret in ("SYN-VULN-SUPPORT-SECRET", "SYN-VULN-RISK-SECRET"):
            self.assertNotIn(secret, html_doc)

        for denied in ("rex", "bea", "kim"):
            c_status, denied_case = self.call_json("/api/cases/ZF-1", denied)
            self.assertEqual(c_status, 200)
            denied_blob = json.dumps(denied_case)
            for secret in (
                "SYN-VULN-SUPPORT-SECRET",
                "SYN-VULN-RISK-SECRET",
                "SYN-RESTRICTED-VULN-1",
                "SYN-RESTRICTED-SAFE-1",
                "SYN-RESTRICTED-MED-1",
                "SYN-RESTRICTED-DA-1",
                "plain_language_explanation",
                "nomination_permissions",
            ):
                self.assertNotIn(secret, denied_blob)
            h_status, _, _ = self.request_raw("/api/cases/ZF-1?view=nomination-routes-html", denied)
            self.assertEqual(h_status, 403)

        with patch.dict(os.environ, ZF_REASON_ROLES="Building Safety Liaison"):
            _, limited_sam = self.call_json("/api/cases/ZF-1", "sam")
            self.assertNotIn("nomination_records", limited_sam)
            self.assertNotIn("SYN intake note", json.dumps(limited_sam))
            lh_status, _, _ = self.request_raw("/api/cases/ZF-1?view=nomination-routes-html", "sam")
            self.assertEqual(lh_status, 403)

    def test_ac2_digital_and_staff_recorded_non_digital_routes_and_field_permissions(
        self,
    ) -> None:
        code, detail = self.call_json(
            "/api/cases/ZF-1/resident",
            "sam",
            self.nomination_payload(
                channel="staff_recorded_non_digital",
                assisted_channel="Paper",
            ),
        )
        self.assertEqual(code, 200, detail)
        nom_id = detail["nomination_records"][0]["id"]

        bad_missing_medium = {
            "action": "nomination_acknowledge",
            "case_id": "ZF-1",
            "id": nom_id,
            "expected_version": 1,
            "channel": "staff_recorded_non_digital",
            "owner": "sam@example.test",
            "acknowledgement_ref": "SYN-ACK-FAIL",
            "non_digital_route": "Phone staffed office",
            "next_update": "2099-02-15",
            "hazard_concern": False,
        }
        self.assertEqual(
            self.call_json("/api/cases/ZF-1/resident", "sam", bad_missing_medium)[0], 400
        )

        bad_digital_with_medium = dict(
            bad_missing_medium,
            channel="digital",
            assisted_channel="Phone",
        )
        self.assertEqual(
            self.call_json("/api/cases/ZF-1/resident", "sam", bad_digital_with_medium)[0], 400
        )

        rlo_third_party_owner = dict(
            bad_missing_medium,
            channel="digital",
            owner="rae@example.test",
        )
        self.assertEqual(
            self.call_json("/api/cases/ZF-1/resident", "sam", rlo_third_party_owner)[0], 403
        )

        for denied in ("rex", "bea", "kim"):
            self.assertEqual(
                self.call_json(
                    "/api/cases/ZF-1/resident",
                    denied,
                    dict(bad_missing_medium, channel="digital"),
                )[0],
                403,
            )

        ack_digital = dict(
            bad_missing_medium,
            channel="digital",
            acknowledgement_ref="SYN-ACK-DIGITAL",
        )
        code, detail = self.call_json("/api/cases/ZF-1/resident", "sam", ack_digital)
        self.assertEqual(code, 200, detail)
        self.assertEqual(
            detail["nomination_records"][0]["acknowledgement"]["route_mode"], "digital"
        )

        ack_manager_reassign = {
            "action": "nomination_acknowledge",
            "case_id": "ZF-1",
            "id": nom_id,
            "expected_version": 2,
            "channel": "staff_recorded_non_digital",
            "assisted_channel": "In person",
            "owner": "rae@example.test",
            "owner_reassignment_reason": "SYN manager handoff to Rae",
            "acknowledgement_ref": "SYN-ACK-IN-PERSON",
            "non_digital_route": "Visit local hub or phone Rae",
            "next_update": "2099-02-20",
            "hazard_concern": False,
        }
        code, detail = self.call_json("/api/cases/ZF-1/resident", "pam", ack_manager_reassign)
        self.assertEqual(code, 200, detail)
        self.assertEqual(
            detail["nomination_records"][0]["acknowledgement"]["route_mode"],
            "staff_recorded_non_digital",
        )
        self.assertEqual(
            detail["nomination_records"][0]["acknowledgement"]["assisted_channel"],
            "In person",
        )
        self.assertEqual(detail["nomination_records"][0]["owner"]["code"], "RLO-2")

        hazard_ack = dict(ack_manager_reassign, expected_version=3, hazard_concern=True)
        h_code, h_payload = self.call_json("/api/cases/ZF-1/resident", "pam", hazard_ack)
        self.assertEqual(h_code, 400, h_payload)
        self.assertEqual(h_payload["route"], "independent_hazard_intake")
        self.assertIs(h_payload["queue_item_created"], False)

        proposal = self.seed_priority_proposal(ai_mode=False)
        target = next(
            item
            for item in self.call_json("/api/cases/ZF-1", "sam")[1]["challenge_targets"]
            if item["proposal_id"] == proposal["id"]
        )
        ch_base: dict[str, Any] = {
            "action": "challenge_open",
            "proposal_id": proposal["id"],
            "proposal_version": target["proposal_version"],
            "decision_version": target["decision_version"],
            "target_kind": "proposal",
            "source": "SYN-CH-SRC",
            "request": "SYN challenge request",
            "explanation": "SYN challenge explanation",
            "non_digital_route": "Phone staffed office",
            "next_update": "2099-02-25",
            "hazard_concern": False,
        }
        self.assertEqual(
            self.call_json(
                "/api/cases/ZF-1/resident",
                "sam",
                dict(ch_base, channel="digital", owner="rae@example.test"),
            )[0],
            403,
        )
        code, _ = self.call_json(
            "/api/cases/ZF-1/resident",
            "sam",
            dict(ch_base, channel="digital", owner="sam@example.test"),
        )
        self.assertEqual(code, 200)
        code, detail = self.call_json(
            "/api/cases/ZF-1/resident",
            "pam",
            dict(
                ch_base,
                channel="staff_recorded_non_digital",
                assisted_channel="Letter",
                owner="rae@example.test",
            ),
        )
        self.assertEqual(code, 200)
        ch_ids = [item["id"] for item in detail["affected_challenges"]]
        self.assertGreaterEqual(len(ch_ids), 2)

        corr_unauth_rlo = {
            "action": "nomination_correct",
            "case_id": "ZF-1",
            "id": nom_id,
            "expected_version": 3,
            "reported_subject_ref": "SYN-CORR-SUBJ",
            "account": "SYN corrected account",
            "source": "SYN correction note",
            "channel": "digital",
            "next_update": "2099-02-22",
            "raised_by": "Resident",
            "challenge_id": ch_ids[0],
            "hazard_concern": False,
        }
        self.assertNotEqual(
            self.call_json("/api/cases/ZF-1/resident", "sam", corr_unauth_rlo)[0], 200
        )
        code, detail = self.call_json("/api/cases/ZF-1/resident", "rae", corr_unauth_rlo)
        self.assertEqual(code, 200, detail)
        code, detail = self.call_json(
            "/api/cases/ZF-1/resident",
            "rae",
            dict(
                corr_unauth_rlo,
                expected_version=4,
                channel="staff_recorded_non_digital",
                assisted_channel="Trusted intermediary",
                challenge_id=ch_ids[1],
            ),
        )
        self.assertEqual(code, 200, detail)
        trail = detail["nomination_records"][0]["challenge_trail"]["competing_evidence"]
        self.assertEqual(
            [c["route_mode"] for c in trail], ["digital", "staff_recorded_non_digital"]
        )
        self.assertEqual(trail[1]["assisted_channel"], "Trusted intermediary")

    def test_accessible_html_route_fragment_labels_and_dual_channels(self) -> None:
        self.assertEqual(
            self.call_json("/api/cases/ZF-1/resident", "sam", self.nomination_payload())[0], 200
        )
        self.seed_priority_proposal(ai_mode=True)
        code, ctype, html_doc = self.request_raw(
            "/api/cases/ZF-1?view=nomination-routes-html", "sam"
        )
        self.assertEqual(code, 200)
        self.assertIn("text/html", ctype)
        inspector = _AccessibleFormInspector()
        inspector.feed(html_doc)
        self.assertGreaterEqual(len(inspector.control_ids), 10)
        for cid in inspector.control_ids:
            self.assertTrue(cid, "every visible form control must have a non-empty id")
            self.assertIn(cid, inspector.labels_for, f"missing <label for='{cid}'>")
        self.assertGreaterEqual(inspector.live_regions, 1)
        channel_selects = {
            cid: opts for cid, opts in inspector.select_options.items() if cid.endswith("-channel")
        }
        self.assertGreaterEqual(len(channel_selects), 3)
        for cid, opts in channel_selects.items():
            self.assertIn("digital", opts, cid)
            self.assertIn("staff_recorded_non_digital", opts, cid)

    def _launch_headless_chromium(self, pw: Any) -> Any:
        from playwright.sync_api import Error as PlaywrightError

        try:
            return pw.chromium.launch(headless=True)
        except PlaywrightError as error:
            if "Executable doesn't exist" in str(error):
                self.skipTest("Chromium is installed by the later browser-check step")
            raise

    @unittest.skipUnless(_playwright_available(), "playwright unavailable")
    def test_keyboard_operability_skips_when_chromium_executable_missing(self) -> None:
        from playwright.sync_api import Error as PlaywrightError

        class _MissingBinaryChromium:
            def launch(self, *, headless: bool) -> Any:
                raise PlaywrightError(
                    "BrowserType.launch: Executable doesn't exist at /tmp/ms-playwright/chromium"
                )

        class _BrokenChromium:
            def launch(self, *, headless: bool) -> Any:
                raise PlaywrightError("BrowserType.launch: sandbox crash")

        class _FakePlaywright:
            def __init__(self, chromium: Any) -> None:
                self.chromium = chromium

        with self.assertRaises(unittest.SkipTest) as skipped:
            self._launch_headless_chromium(_FakePlaywright(_MissingBinaryChromium()))
        self.assertIn(
            "Chromium is installed by the later browser-check step", str(skipped.exception)
        )

        with self.assertRaises(PlaywrightError):
            self._launch_headless_chromium(_FakePlaywright(_BrokenChromium()))

    @unittest.skipUnless(_playwright_available(), "playwright unavailable")
    def test_workbench_keyboard_operability_for_digital_and_non_digital_routes(self) -> None:
        from playwright.sync_api import sync_playwright

        self.assertEqual(
            self.call_json("/api/cases/ZF-1/resident", "sam", self.nomination_payload())[0], 200
        )
        nom_id = self.call_json("/api/cases/ZF-1", "sam")[1]["nomination_records"][0]["id"]

        with sync_playwright() as pw:
            browser = self._launch_headless_chromium(pw)
            try:
                context = browser.new_context(
                    viewport={"width": 1280, "height": 900}, reduced_motion="reduce"
                )
                context.route(
                    "**/*",
                    lambda route: (
                        route.continue_()
                        if route.request.url.startswith(self.base + "/")
                        else route.abort()
                    ),
                )
                page = context.new_page()
                page.goto(self.base + "/app")
                page.locator("#email").fill("sam@example.test")
                page.locator("#pw").fill("synthetic-only")
                page.keyboard.press("Enter")
                page.locator("#nav").wait_for(state="visible", timeout=10000)
                page.goto(self.base + "/app#/case/ZF-1?tab=resident")
                page.wait_for_selector("#nominations-title", timeout=10000)

                page.locator("#nominations-title").evaluate("e => { e.tabIndex = -1; e.focus(); }")
                page.keyboard.press("Tab")
                first_tag = page.evaluate("() => document.activeElement?.tagName")
                self.assertEqual(first_tag, "SUMMARY")

                ack_summary = page.locator(
                    "summary", has_text=f"Record acknowledgement for {nom_id}"
                )
                ack_summary.focus()
                page.keyboard.press("Enter")

                chan_id = f"#nomination-ack-{nom_id}-channel"
                ack_ref_id = f"#nomination-ack-{nom_id}-acknowledgement_ref"
                page.wait_for_selector(chan_id, state="visible", timeout=10000)
                page.select_option(chan_id, "digital")
                page.focus(ack_ref_id)
                page.keyboard.press("Control+A")
                page.keyboard.press("Backspace")
                page.keyboard.press("Enter")
                self.assertEqual(page.get_attribute(ack_ref_id, "aria-invalid"), "true")
                active_after_err = page.evaluate("() => document.activeElement?.id")
                self.assertEqual(active_after_err, f"nomination-ack-{nom_id}-acknowledgement_ref")

                page.keyboard.type("SYN-KB-DIGITAL-ACK")
                route_id = f"#nomination-ack-{nom_id}-non_digital_route"
                page.focus(route_id)
                page.keyboard.press("Control+A")
                page.keyboard.type("Phone Sam or visit housing hub")
                next_id = f"#nomination-ack-{nom_id}-next_update"
                page.locator(next_id).fill("2099-03-01")
                ack_submit = page.locator(
                    "button[type='submit']", has_text="Record acknowledgement"
                )
                ack_submit.focus()
                page.keyboard.press("Enter")
                page.wait_for_function(
                    "(expected) => document.querySelector('#nominations')"
                    "?.textContent?.includes(expected)",
                    arg="SYN-KB-DIGITAL-ACK",
                    timeout=10000,
                )

                ack_summary = page.locator(
                    "summary", has_text=f"Record acknowledgement for {nom_id}"
                )
                ack_summary.focus()
                page.keyboard.press(" ")
                page.wait_for_selector(chan_id, state="visible", timeout=10000)
                page.focus(chan_id)
                page.select_option(chan_id, "staff_recorded_non_digital")
                assist_id = f"#nomination-ack-{nom_id}-assisted_channel"
                page.focus(assist_id)
                page.select_option(assist_id, "phone")
                page.focus(ack_ref_id)
                page.keyboard.press("Control+A")
                page.keyboard.type("SYN-KB-PHONE-ACK")
                page.locator(next_id).fill("2099-03-05")
                ack_submit = page.locator(
                    "button[type='submit']", has_text="Record acknowledgement"
                )
                ack_submit.focus()
                page.keyboard.press("Enter")
                page.wait_for_function(
                    "(expected) => document.querySelector('#nominations')"
                    "?.textContent?.includes(expected)",
                    arg="SYN-KB-PHONE-ACK",
                    timeout=10000,
                )

                for width in (1280, 320):
                    page.set_viewport_size({"width": width, "height": 900})
                    overflow = page.evaluate(
                        "() => document.documentElement.scrollWidth"
                        " > document.documentElement.clientWidth + 1"
                    )
                    self.assertFalse(overflow, f"horizontal overflow at {width}px")
            finally:
                browser.close()

        stored_ack = self.call_json("/api/cases/ZF-1", "sam")[1]["nomination_records"][0][
            "acknowledgement"
        ]
        self.assertEqual(stored_ack["reference"], "SYN-KB-PHONE-ACK")
        self.assertEqual(stored_ack["route_mode"], "staff_recorded_non_digital")
        self.assertEqual(stored_ack["assisted_channel"], "Phone")

    @unittest.skipUnless(_playwright_available(), "playwright unavailable")
    def test_standalone_route_forms_submit_in_browser(self) -> None:
        from playwright.sync_api import sync_playwright

        self.assertEqual(
            self.call_json("/api/cases/ZF-1/resident", "sam", self.nomination_payload())[0], 200
        )
        nom_id = self.call_json("/api/cases/ZF-1", "sam")[1]["nomination_records"][0]["id"]
        self.seed_priority_proposal()
        statuses: list[int] = []

        with sync_playwright() as pw:
            browser = self._launch_headless_chromium(pw)
            try:
                context = browser.new_context()
                context.add_cookies(
                    [
                        {
                            "name": "zf_session",
                            "value": self._login_cookie("sam").split("=", 1)[1],
                            "url": self.base,
                        }
                    ]
                )
                page = context.new_page()
                page.on(
                    "response",
                    lambda r: statuses.append(r.status) if "/resident" in r.url else None,
                )
                page.goto(self.base + "/api/cases/ZF-1?view=nomination-routes-html")
                page.locator("summary", has_text=f"Record acknowledgement for {nom_id}").click()
                key = f"#nomination-ack-{nom_id}"
                page.select_option(f"{key}-channel", "digital")
                page.fill(f"{key}-acknowledgement_ref", "SYN-STANDALONE-ACK")
                page.fill(f"{key}-non_digital_route", "Phone Sam or visit housing hub")
                page.fill(f"{key}-next_update", "2099-03-01")
                with page.expect_navigation():
                    page.locator(f"{key} button[type='submit']").click()
                page.locator("summary", has_text=f"Record correction for {nom_id}").click()
                key = f"#nomination-correct-{nom_id}"
                page.select_option(f"{key}-channel", "digital")
                page.fill(f"{key}-account", "Synthetic corrected account")
                page.fill(f"{key}-source", "SYN-STANDALONE-CORRECTION")
                page.fill(f"{key}-reported_subject_ref", "SYN-SUBJECT")
                page.fill(f"{key}-next_update", "2099-03-02")
                with page.expect_navigation():
                    page.locator(f"{key} button[type='submit']").click()
                page.locator("summary", has_text="Record supplied challenge").click()
                key = "#challenge-open-route"
                page.select_option(f"{key}-channel", "digital")
                page.fill(f"{key}-source", "SYN-STANDALONE-CHALLENGE")
                page.fill(f"{key}-request", "Synthetic supplied challenge")
                page.fill(f"{key}-explanation", "Synthetic explanation")
                page.fill(f"{key}-non_digital_route", "Phone Sam or visit housing hub")
                page.fill(f"{key}-next_update", "2099-03-03")
                with page.expect_navigation():
                    page.locator(f"{key} button[type='submit']").click()
            finally:
                browser.close()

        self.assertEqual(statuses, [200, 200, 200])
        stored_ack = self.call_json("/api/cases/ZF-1", "sam")[1]["nomination_records"][0][
            "acknowledgement"
        ]
        self.assertEqual(stored_ack["reference"], "SYN-STANDALONE-ACK")
        detail = self.call_json("/api/cases/ZF-1", "sam")[1]
        record = detail["nomination_records"][0]
        self.assertEqual(record["owner"]["email"], "sam@example.test")
        self.assertEqual(record["original"]["account"], "SYN resident referral account")
        self.assertEqual(
            [c["source"] for c in record["corrections"]], ["SYN-STANDALONE-CORRECTION"]
        )
        self.assertIn("SYN-STANDALONE-CHALLENGE", json.dumps(detail["affected_challenges"]))

    def _ack_payload(self, nom_id: str, **overrides: Any) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "action": "nomination_acknowledge",
            "case_id": "ZF-1",
            "id": nom_id,
            "expected_version": 1,
            "channel": "digital",
            "owner": "sam@example.test",
            "acknowledgement_ref": "SYN-NEG",
            "non_digital_route": "Phone Sam or visit the local housing office",
            "next_update": "2099-03-01",
            "hazard_concern": False,
        }
        payload.update(overrides)
        return payload

    def test_route_writes_refuse_unauthenticated_unpermitted_malformed_and_cross_case(
        self,
    ) -> None:
        self.assertEqual(
            self.call_json("/api/cases/ZF-1/resident", "sam", self.nomination_payload())[0], 200
        )
        before = self.call_json("/api/cases/ZF-1", "sam")[1]
        nom_id = before["nomination_records"][0]["id"]
        path = "/api/cases/ZF-1/resident"

        self.assertEqual(self.request_raw(path, "", self._ack_payload(nom_id))[0], 401)
        self.assertEqual(
            self.call_json(path, "kim", self._ack_payload(nom_id, owner="kim@example.test"))[0],
            403,
        )
        self.assertEqual(self.request_raw(path, "sam", ["not", "an", "object"])[0], 400)
        for bad in (
            self._ack_payload(nom_id, id="NOM-DOES-NOT-EXIST"),
            self._ack_payload(nom_id, next_update="not-a-date"),
            self._ack_payload(nom_id, expected_version=99),
            self._ack_payload(nom_id, case_id="ZF-2"),
        ):
            self.assertGreaterEqual(self.call_json(path, "sam", bad)[0], 400, bad)
        status, _ = self.call_json("/api/cases/ZF-2/resident", "sam", self._ack_payload(nom_id))
        self.assertGreaterEqual(status, 400)
        self.assertEqual(self.call_json("/api/cases/ZF-1", "sam")[1], before)

    def test_native_form_encoding_is_refused_and_writes_nothing(self) -> None:
        self.assertEqual(
            self.call_json("/api/cases/ZF-1/resident", "sam", self.nomination_payload())[0], 200
        )
        before = self.call_json("/api/cases/ZF-1", "sam")[1]
        nom_id = before["nomination_records"][0]["id"]
        form = (
            f"action=nomination_acknowledge&case_id=ZF-1&id={nom_id}&expected_version=1"
            "&channel=digital&acknowledgement_ref=SYN-NATIVE&next_update=2099-03-01"
        ).encode()
        req = Request(
            self.base + "/api/cases/ZF-1/resident",
            form,
            headers={
                "Cookie": self._login_cookie("sam"),
                "Content-Type": "application/x-www-form-urlencoded",
                "X-ZF-CSRF": "1",
            },
        )
        with self.assertRaises(HTTPError) as refused:
            urlopen(req, timeout=10)
        self.assertEqual(refused.exception.code, 400)
        self.assertEqual(json.loads(refused.exception.read())["error"], "Could not read that.")
        self.assertEqual(self.call_json("/api/cases/ZF-1", "sam")[1], before)

    def test_correction_and_challenge_writes_refuse_unsafe_requests_and_write_nothing(
        self,
    ) -> None:
        self.assertEqual(
            self.call_json("/api/cases/ZF-1/resident", "sam", self.nomination_payload())[0], 200
        )
        proposal = self.seed_priority_proposal()
        detail = self.call_json("/api/cases/ZF-1", "sam")[1]
        nom_id = detail["nomination_records"][0]["id"]
        target = next(t for t in detail["challenge_targets"] if t["proposal_id"] == proposal["id"])
        before = detail
        correct: dict[str, Any] = {
            "action": "nomination_correct",
            "case_id": "ZF-1",
            "id": nom_id,
            "expected_version": 1,
            "channel": "digital",
            "owner": "sam@example.test",
            "account": "SYN corrected account",
            "source": "SYN-NEG-CORRECT",
            "reported_subject_ref": "SYN-SUBJ-130",
            "non_digital_route": "Phone Sam or visit the local housing office",
            "next_update": "2099-03-02",
            "hazard_concern": False,
        }
        challenge: dict[str, Any] = {
            "action": "challenge_open",
            "proposal_id": proposal["id"],
            "proposal_version": target["proposal_version"],
            "decision_version": target["decision_version"],
            "target_kind": "proposal",
            "channel": "digital",
            "source": "SYN-NEG-CHALLENGE",
            "request": "SYN challenge request",
            "explanation": "SYN challenge explanation",
            "owner": "sam@example.test",
            "non_digital_route": "Phone Sam or visit the local housing office",
            "next_update": "2099-03-03",
            "hazard_concern": False,
        }
        path = "/api/cases/ZF-1/resident"

        def native(payload: dict[str, Any]) -> int:
            from urllib.parse import urlencode

            req = Request(
                self.base + path,
                urlencode({k: str(v) for k, v in payload.items()}).encode(),
                headers={
                    "Cookie": self._login_cookie("sam"),
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-ZF-CSRF": "1",
                },
            )
            try:
                urlopen(req, timeout=10)
            except HTTPError as err:
                return err.code
            return 200

        for payload in (correct, challenge):
            action = payload["action"]
            self.assertEqual(self.request_raw(path, "", payload)[0], 401, action)
            self.assertEqual(self.call_json(path, "kim", payload)[0], 403, action)
            self.assertEqual(self.request_raw(path, "sam", [payload])[0], 400, action)
            self.assertEqual(native(payload), 400, action)
            with patch.object(self.app.provider, "name", "trusted-proxy"):
                status, body = self.call_json(path, "sam", payload)
                self.assertEqual((status, body["error"]), (403, "Missing request header."))
        self.assertGreaterEqual(
            self.call_json(path, "sam", dict(correct, expected_version=99))[0], 400
        )
        self.assertGreaterEqual(
            self.call_json(path, "sam", dict(challenge, proposal_version=99))[0], 400
        )
        self.assertGreaterEqual(self.call_json(path, "sam", dict(correct, case_id="ZF-2"))[0], 400)
        self.assertEqual(self.call_json("/api/cases/ZF-NOPE/resident", "sam", challenge)[0], 404)
        self.assertEqual(self.call_json("/api/cases/ZF-1", "sam")[1], before)

    def test_trusted_proxy_route_write_requires_csrf_header_and_writes_nothing_without_it(
        self,
    ) -> None:
        self.assertEqual(
            self.call_json("/api/cases/ZF-1/resident", "sam", self.nomination_payload())[0], 200
        )
        before = self.call_json("/api/cases/ZF-1", "sam")[1]
        nom_id = before["nomination_records"][0]["id"]
        payload = json.dumps(self._ack_payload(nom_id, acknowledgement_ref="SYN-CSRF")).encode()

        def post(extra: dict[str, str]) -> tuple[int, Any]:
            req = Request(
                self.base + "/api/cases/ZF-1/resident",
                payload,
                headers={
                    "Cookie": self._login_cookie("sam"),
                    "Content-Type": "application/json",
                    **extra,
                },
            )
            try:
                with urlopen(req, timeout=10) as response:
                    return response.status, json.loads(response.read())
            except HTTPError as err:
                return err.code, json.loads(err.read())

        with patch.object(self.app.provider, "name", "trusted-proxy"):
            status, body = post({})
            self.assertEqual((status, body["error"]), (403, "Missing request header."))
            self.assertEqual(self.call_json("/api/cases/ZF-1", "sam")[1], before)
            self.assertEqual(post({"X-ZF-CSRF": "1"})[0], 200)

    def test_route_form_failures_show_feedback_keep_form_usable_and_write_nothing(self) -> None:
        from playwright.sync_api import sync_playwright

        self.assertEqual(
            self.call_json("/api/cases/ZF-1/resident", "sam", self.nomination_payload())[0], 200
        )
        nom_id = self.call_json("/api/cases/ZF-1", "sam")[1]["nomination_records"][0]["id"]
        key = f"#nomination-ack-{nom_id}"

        with sync_playwright() as pw:
            browser = self._launch_headless_chromium(pw)
            try:
                context = browser.new_context()
                context.add_cookies(
                    [
                        {
                            "name": "zf_session",
                            "value": self._login_cookie("sam").split("=", 1)[1],
                            "url": self.base,
                        }
                    ]
                )
                page = context.new_page()
                page.goto(self.base + "/api/cases/ZF-1?view=nomination-routes-html")
                page.locator("summary", has_text=f"Record acknowledgement for {nom_id}").click()
                page.select_option(f"{key}-channel", "digital")
                page.fill(f"{key}-acknowledgement_ref", "SYN-FAIL-ACK")
                page.fill(f"{key}-non_digital_route", "Phone Sam or visit housing hub")
                page.fill(f"{key}-next_update", "2099-03-01")
                button = page.locator(f"{key} button[type='submit']")

                # Another session moves the record on, so the form's expected_version is stale.
                code, _ = self.call_json(
                    "/api/cases/ZF-1/resident",
                    "sam",
                    self._ack_payload(nom_id, acknowledgement_ref="SYN-OTHER-SESSION"),
                )
                self.assertEqual(code, 200)
                with page.expect_response("**/resident") as stale:
                    button.click()
                self.assertGreaterEqual(stale.value.status, 400)
                feedback = page.locator(f"{key}-feedback")
                self.assertEqual(feedback.inner_text().strip(), stale.value.json()["error"])
                self.assertTrue(feedback.evaluate("el => el === document.activeElement"))
                self.assertTrue(button.is_enabled())

                page.route("**/resident", lambda route: route.abort())
                button.click()
                page.wait_for_function(
                    "id => document.getElementById(id).textContent.includes('Nothing was')",
                    arg=f"nomination-ack-{nom_id}-feedback",
                )
                self.assertTrue(button.is_enabled())
            finally:
                browser.close()

        record = self.call_json("/api/cases/ZF-1", "sam")[1]["nomination_records"][0]
        self.assertEqual(record["acknowledgement"]["reference"], "SYN-OTHER-SESSION")

    def test_route_form_script_posts_json_with_csrf_header_and_page_loads_it(self) -> None:
        self.assertEqual(
            self.call_json("/api/cases/ZF-1/resident", "sam", self.nomination_payload())[0], 200
        )
        _, ctype, html = self.request_raw("/api/cases/ZF-1?view=nomination-routes-html", "sam")
        self.assertIn("text/html", ctype)
        self.assertIn('<script src="/nomination-routes.js" defer></script>', html)
        self.assertIn('<link rel="stylesheet" href="/style.css">', html)
        status, ctype, script = self.request_raw("/nomination-routes.js", "sam")
        self.assertEqual(status, 200)
        self.assertIn("javascript", ctype)
        self.assertIn('"Content-Type": "application/json"', script)
        self.assertIn('"X-ZF-CSRF": "1"', script)


if __name__ == "__main__":
    unittest.main()
