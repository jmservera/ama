"""Cross-epic local stabilization journey (#440; Refs #165, #104, #149).

One constructed, synthetic-only journey over the real local HTTP surface: labelled
synthetic data reaches the workbench (#165), the bounded assistant proposal carries
its provenance and never changes controlled state, failing closed when AI is
unavailable (#104), and the workbench keeps its non-colour, plain-language and
manual-path cues (#149). Local evidence only: not live, hosted or accessibility
acceptance.
"""

from __future__ import annotations

import copy
import json
import os
import re
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from tests.test_mvp import DATA
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.synthetic import privacy, provenance

from zava_forward.api.server import App, make_handler

WEB = Path(__file__).resolve().parents[1] / "src" / "zava_forward" / "api" / "web"
PASSWORD = "synthetic-only"
ANCHOR_LABEL = "SYNTHETIC-ANCHOR-440"


class CrossEpicStabilizationJourney(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dataset: Path = Path(tmp.name) / "synthetic.json"
        payload: dict[str, Any] = copy.deepcopy(DATA)
        self.dataset.write_text(json.dumps(payload), encoding="utf-8")
        self.payload: dict[str, Any] = payload
        store: Any = SqlStore(str(self.dataset), os.path.join(tmp.name, "synthetic.sqlite"))
        self.addCleanup(store.db.close)
        self.store: Any = store
        app: Any = App(store, PASSWORD)  # type: ignore[no-untyped-call]
        http = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(app))
        thread = threading.Thread(target=http.serve_forever, daemon=True)
        thread.start()

        def stop() -> None:
            http.shutdown()
            http.server_close()
            thread.join(timeout=5)

        self.addCleanup(stop)
        self.base: str = f"http://127.0.0.1:{http.server_address[1]}"
        self.cookie: str = self.login(str(payload["staff"][0]["email"]))

    def login(self, email: str) -> str:
        request = Request(
            self.base + "/api/login",
            json.dumps({"email": email, "password": PASSWORD}).encode(),
        )
        with urlopen(request, timeout=10) as response:
            return str(response.headers["Set-Cookie"]).split(";")[0]

    def call(self, path: str, body: dict[str, Any] | None = None) -> tuple[int, Any]:
        request = Request(
            self.base + path,
            data=json.dumps(body).encode() if body is not None else None,
            headers={"Cookie": self.cookie, "Content-Type": "application/json", "X-ZF-CSRF": "1"},
        )
        try:
            with urlopen(request, timeout=10) as response:
                return int(response.status), json.loads(response.read())
        except HTTPError as error:
            return int(error.code), json.loads(error.read())

    def controlled_state(self) -> dict[str, Any]:
        """Case, gate, hazard, funding and document state as the staff API presents it."""
        state: dict[str, Any] = {}
        for case in self.payload["cases"]:
            case_id = str(case["id"])
            status, view = self.call(f"/api/cases/{case_id}")
            self.assertEqual(status, 200, case_id)
            state[case_id] = {
                key: view[key]
                for key in (
                    "stage",
                    "gate",
                    "can_advance",
                    "hazards",
                    "funding",
                    "documents",
                    "history",
                    "decision",
                )
            }
        return state

    def test_synthetic_provenance_and_anchors_reach_the_workbench(self) -> None:
        manifest: dict[str, Any] = {
            "is_synthetic": True,
            "contains_real_data": False,
            "source_type": "SYNTHETIC",
            "anchor_label": ANCHOR_LABEL,
            "dataset_sha256": provenance.file_hashes([self.dataset])[self.dataset.name],
        }
        self.assertEqual(privacy.record_issues(manifest), [])
        self.assertEqual(privacy.emission_issues(manifest), [])
        for case in self.payload["cases"]:
            resident = {k: case["resident"][k] for k in ("name", "formal", "email")}
            self.assertEqual(privacy.pattern_issues(resident), [], case["id"])
            home = case["home"]
            self.assertEqual(privacy.pattern_issues(home, scale_home=True), [], case["id"])
            self.assertEqual((home["lat"], home["lon"]), (0, 0), case["id"])
        self.assertTrue(provenance.source_revision([self.dataset]).startswith("sha256:"))
        self.assertEqual(
            manifest["dataset_sha256"], provenance.file_hashes([self.dataset])[self.dataset.name]
        )

        unlabelled = {k: v for k, v in manifest.items() if k != "is_synthetic"}
        self.assertEqual(privacy.record_issues(unlabelled), ["missing_synthetic_label"])
        self.assertEqual(privacy.pattern_issues({"contact": "someone@example.org"}), ["email"])

        status, listing = self.call("/api/cases")
        self.assertEqual(status, 200)
        loaded = {str(item["id"]) for item in listing["items"]}
        self.assertTrue(loaded)
        self.assertLessEqual(loaded, {str(case["id"]) for case in self.payload["cases"]})
        status, progress = self.call("/api/me")
        self.assertEqual(status, 200)
        scopes = [str(item["scope"]) for item in progress["navigation"]]
        self.assertIn("Synthetic programme progress", scopes)

    def test_assistant_proposal_is_bounded_attributed_and_read_only(self) -> None:
        before = self.controlled_state()
        recommendations_before = len(self.store.data["recommendations"])
        audit_before = len(self.store.data.get("audit", []))

        status, proposal = self.call("/api/ai/priority", {"n": 3})
        self.assertEqual(status, 200)
        self.assertEqual(proposal["status"], "Proposed")
        self.assertEqual(proposal["source"], "template")
        self.assertIsNone(proposal["model"])
        self.assertLessEqual(len(proposal["items"]), 3)
        self.assertEqual(
            [item["case_id"] for item in proposal["deterministic"]][:1],
            [proposal["items"][0]["case_id"]],
        )
        for item in proposal["items"]:
            self.assertTrue(item["cites"], item["case_id"])
            self.assertTrue(item["reason"].startswith("Because of"), item["case_id"])

        status, latest = self.call("/api/ai/priority")
        self.assertEqual(status, 200)
        self.assertEqual(latest["recommendation"]["id"], proposal["id"])

        self.assertEqual(self.controlled_state(), before)
        self.assertEqual(len(self.store.data["recommendations"]), recommendations_before + 1)
        self.assertGreaterEqual(len(self.store.data.get("audit", [])), audit_before)

    def test_ai_unavailable_fails_closed_to_manual_workflow(self) -> None:
        before = self.controlled_state()
        for mode in ("ai", "workflow-only"):
            status, proposal = self.call("/api/ai/priority", {"n": 3, "mode": mode})
            self.assertEqual(status, 200, mode)
            self.assertEqual(proposal["source"], "template", mode)
            self.assertIsNone(proposal["model"], mode)
            self.assertEqual(proposal["status"], "Proposed", mode)
            self.assertTrue(proposal["items"], mode)
            self.assertTrue(proposal["fallback_reason"], mode)
        self.assertEqual(self.controlled_state(), before)

        status, refusal = self.call("/api/chat/threads", {"title": "Stabilisation check"})
        self.assertEqual(status, 403)
        self.assertIn("refused until the DPIA", str(refusal["error"]))
        status, chat = self.call("/api/chat/status")
        self.assertEqual(status, 200)
        self.assertFalse(chat["storage_approved"])
        self.assertIn("disabled", str(chat["activation"]))
        self.assertEqual(chat["limits"]["calls_per_turn"], 1)
        self.assertEqual(chat["limits"]["retries"], 0)
        self.assertEqual(chat["limits"]["memory_used"], False)
        self.assertEqual(self.controlled_state(), before)

    def test_workbench_keeps_non_colour_plain_language_and_manual_cues(self) -> None:
        html = (WEB / "index.html").read_text(encoding="utf-8")
        css = (WEB / "style.css").read_text(encoding="utf-8")
        app_js = (WEB / "app.js").read_text(encoding="utf-8")
        workspace_js = (WEB / "case-workspace.js").read_text(encoding="utf-8")
        chat_js = (WEB / "chat.js").read_text(encoding="utf-8")

        self.assertIn('lang="en-GB"', html)
        self.assertIn('class="skip-link" href="#app"', html)
        self.assertRegex(html, r'id="workspace-status"[^>]*role="status"[^>]*aria-live="polite"')
        for selector, glyph in (
            (".status-line.danger:before", r"\26A0"),
            (".status-line.ok:before", r"\2713"),
            (".status-line.wait:before", r"\23F3"),
        ):
            self.assertIn(selector, css)
            self.assertIn(glyph, css)
        self.assertRegex(css, r"prefers-reduced-motion:reduce")

        self.assertIn("Workflow-only mode.", workspace_js)
        self.assertIn("Workflow-only help, no record changed", chat_js)
        self.assertRegex(app_js, r"the existing case and building screens remain the manual path")
        self.assertIsNotNone(re.search(r"Workflow-only mode: the person can choose rules", app_js))

        status, me = self.call("/api/me")
        self.assertEqual(status, 200)
        labels = [str(item["label"]) for item in me["navigation"]]
        self.assertIn("My cases", labels)
        self.assertIn("Assistant proposals", labels)
        self.assertTrue(all(item["scope"] for item in me["navigation"]))


if __name__ == "__main__":
    unittest.main()
