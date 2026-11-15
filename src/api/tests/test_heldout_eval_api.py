"""HTTP API integration and role-denial tests for offline held-out evaluation (Issue #108)."""

from __future__ import annotations

import copy
import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import dataset
from test_quality_procurement import STAFF
from zava_forward.core import heldout_eval
from zava_forward.core.sqlstore import SqlStore

from zava_forward.api.server import App, make_handler


class HeldoutEvalApiTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        data = copy.deepcopy(dataset.DATA)
        data["staff"] = copy.deepcopy(STAFF)
        path = Path(self.tmp.name) / "synthetic.json"
        path.write_text(json.dumps(data))
        self.store = SqlStore(str(path), str(path.with_suffix(".sqlite")))
        self.addCleanup(self.store.db.close)
        self.password = "SYN-heldout-108"
        self.app = App(self.store, self.password)
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(self.app))
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.shutdown)
        self.base = f"http://127.0.0.1:{self.httpd.server_port}"
        self.cookies: dict[str, str] = {}

    def shutdown(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=5)

    def email_for_role(self, role: str) -> str:
        return str(next(s["email"] for s in self.store.data["staff"] if s["role"] == role))

    def call(
        self,
        path: str,
        *,
        email: str | None,
        body: object = None,
    ) -> tuple[int, dict[str, Any]]:
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if email:
            if email not in self.cookies:
                login_req = Request(
                    self.base + "/api/login",
                    data=json.dumps({"email": email, "password": self.password}).encode(),
                    headers=headers,
                )
                with urlopen(login_req, timeout=10) as resp:
                    self.cookies[email] = resp.headers["Set-Cookie"].split(";")[0]
            headers["Cookie"] = self.cookies[email]
        req = Request(
            self.base + path,
            data=json.dumps(body).encode() if body is not None else None,
            headers=headers,
        )
        try:
            with urlopen(req, timeout=10) as resp:
                return resp.status, json.loads(resp.read())
        except HTTPError as error:
            return error.code, json.loads(error.read())

    def test_get_heldout_evaluation_returns_complete_suite_without_audit_side_effects(
        self,
    ) -> None:
        manager = self.email_for_role("Retrofit Programme Manager")
        self.call("/api/me", email=manager)
        before_audit = len(list(self.store.audit_entries()))
        status, payload = self.call("/api/ai/heldout-evaluation", email=manager)
        self.assertEqual(status, 200)
        self.assertEqual(len(list(self.store.audit_entries())), before_audit)

        held_out = payload["held_out"]
        self.assertEqual(held_out["outcome"], "pass")
        self.assertEqual(held_out["denominators"]["frozen_total"], 16)
        self.assertEqual(held_out["calibration"]["status"], "not_applicable")
        self.assertEqual(
            held_out["actual_serving_version"]["reported"],
            heldout_eval.OFFLINE_SERVING_VERSION,
        )
        comp = payload["tokenomics_comparison"]
        self.assertEqual(comp["summary"]["verified_saving_candidates"], 1)
        self.assertEqual(comp["summary"]["failed_candidates"], 2)

    def test_get_ai_report_preserves_top_level_keys_and_embeds_heldout_summaries(self) -> None:
        manager = self.email_for_role("Retrofit Programme Manager")
        status, report = self.call("/api/ai/report", email=manager)
        self.assertEqual(status, 200)
        self.assertEqual(set(report), {"evaluation", "live", "registry", "consumption"})
        self.assertEqual(report["evaluation"]["held_out"]["outcome"], "pass")
        self.assertEqual(report["evaluation"]["held_out"]["calibration_status"], "not_applicable")
        self.assertTrue(report["evaluation"]["tokenomics_comparison"]["suite_valid"])

    def test_non_managers_contractors_and_unauthenticated_callers_are_denied(self) -> None:
        self.assertEqual(self.call("/api/ai/heldout-evaluation", email=None)[0], 401)
        self.assertEqual(
            self.call("/api/ai/candidate-comparison", email=None, body={"candidates": []})[0],
            401,
        )
        for denied_role in ("Quality Inspector", "Resident Liaison Officer", "Contractor"):
            email = self.email_for_role(denied_role)
            self.assertEqual(
                self.call("/api/ai/heldout-evaluation", email=email)[0],
                403,
                denied_role,
            )
            self.assertEqual(
                self.call("/api/ai/candidate-comparison", email=email, body={})[0],
                403,
                denied_role,
            )

    def test_query_parameters_and_malformed_candidate_bodies_return_400(self) -> None:
        manager = self.email_for_role("Retrofit Programme Manager")
        self.assertEqual(self.call("/api/ai/heldout-evaluation?foo=", email=manager)[0], 400)
        self.assertEqual(self.call("/api/ai/heldout-evaluation?x=1", email=manager)[0], 400)
        self.assertEqual(self.call("/api/ai/candidate-comparison", email=manager, body={})[0], 400)
        self.assertEqual(
            self.call(
                "/api/ai/candidate-comparison?extra=1", email=manager, body={"candidates": []}
            )[0],
            400,
        )
        self.assertEqual(
            self.call(
                "/api/ai/candidate-comparison",
                email=manager,
                body={"candidates": [], "unexpected": True},
            )[0],
            400,
        )

    def test_post_candidate_comparison_evaluates_candidates_and_records_audit_entry(
        self,
    ) -> None:
        manager = self.email_for_role("Retrofit Programme Manager")
        suite = heldout_eval.canonical_offline_heldout_suite()
        baseline = suite["baseline_candidate"]
        base_levers = baseline["lever_config"]

        candidates = [
            {
                "candidate_id": "cheap-regresses-overrides",
                "declared_lever": "model",
                "lever_config": dict(base_levers, model="cheap-nano-v1"),
                "case_ids": list(baseline["case_ids"]),
                "accepted_case_ids": list(baseline["accepted_case_ids"]),
                "quality_counters": dict(baseline["quality_counters"], overrides=1),
                "usage": {"estimated_cost": "0.000300", "currency": "GBP"},
            },
            {
                "candidate_id": "single-lever-cache-pass",
                "declared_lever": "caching",
                "lever_config": dict(base_levers, caching="prefix-cache-v2"),
                "case_ids": list(baseline["case_ids"]),
                "accepted_case_ids": list(baseline["accepted_case_ids"]),
                "quality_counters": dict(baseline["quality_counters"]),
                "usage": {"estimated_cost": "0.000850", "currency": "GBP"},
            },
        ]
        status, result = self.call(
            "/api/ai/candidate-comparison",
            email=manager,
            body={"candidates": candidates},
        )
        self.assertEqual(status, 200, result)
        by_id = {c["candidate_id"]: c for c in result["candidates"]}
        self.assertEqual(by_id["cheap-regresses-overrides"]["outcome"], "failure")
        self.assertFalse(by_id["cheap-regresses-overrides"]["is_saving"])
        self.assertEqual(by_id["single-lever-cache-pass"]["outcome"], "pass")
        self.assertTrue(by_id["single-lever-cache-pass"]["is_saving"])

        last_audit = list(self.store.audit_entries())[-1]
        self.assertEqual(last_audit["action"], "ai_candidate_comparison")
        self.assertEqual(last_audit["who"], manager)


if __name__ == "__main__":
    unittest.main()
