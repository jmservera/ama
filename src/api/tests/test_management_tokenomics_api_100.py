"""HTTP management endpoint tests for AI consumption economics (Issue #100)."""

from __future__ import annotations

import copy
import json
import tempfile
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlencode

from dataset import DATA
from zava_forward.core import tokenomics
from zava_forward.core.ai_consumption import COMPONENTS, CallContext, Consumption, reference
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store

from zava_forward.api.server import App, make_handler

COST_KEYS = (
    "token_cost",
    "total_cost_of_ai",
    "token_cost_per_accepted_outcome",
    "cost_per_accepted_outcome",
    "quality_qualified_cost_per_accepted_outcome",
    "booked_value",
)
START_DAY = "2026-03-02"
END_DAY = "2026-03-05"
START_ISO = "2026-03-02T00:00:00Z"
END_ISO = "2026-03-06T00:00:00Z"
MODEL = "api-mgmt-model"


def _synthetic_event(when: str, action: str) -> dict[str, Any]:
    return dict(at=when, action=action, source="year-one simulation", is_synthetic=True)


def _api_fixture() -> dict[str, Any]:
    data: dict[str, Any] = copy.deepcopy(DATA)
    data["as_of"] = "2026-03-07"
    data["staff"].append(
        dict(
            code="RC-100",
            name="Synthetic Coordinator",
            email="rc100@example.test",
            role="Retrofit Coordinator",
        )
    )
    for idx, case in enumerate(data["cases"]):
        if idx < 4:
            case["is_synthetic"] = True
            case["synthetic_source"] = "year-one simulation"
            case["history"] = [_synthetic_event("2026-03-01", "Identified")]
        else:
            case.pop("is_synthetic", None)
    data["cases"][0].update(
        stage="Contacting resident",
        returns=[
            dict(
                version=1,
                at="2026-03-03T12:00:00Z",
                from_stage="Survey booked",
                to_stage="Contact paused",
                reopened=False,
                by="SYN-ACTOR",
                source="SYN-REF",
                reason="SYN-REASON",
            )
        ],
    )
    syn_id = data["cases"][0]["id"]
    unmarked_id = data["cases"][4]["id"]
    data["recommendations"] = [
        dict(
            id="SYN-REC-ACCEPTED",
            kind="ai_task",
            task="briefing",
            source="ai",
            status="Accepted",
            verified=True,
            is_synthetic=True,
            case_ids=[syn_id],
            created="2026-03-03T10:00:00Z",
            resolved_at="2026-03-03T11:00:00Z",
            text="PRIVATE-DRAFT-BODY",
            reviewer_reason="PRIVATE-REVIEW-NOTE",
        ),
        dict(
            id="REAL-NON-SYNTHETIC",
            kind="ai_task",
            task="briefing",
            source="ai",
            status="Accepted",
            verified=True,
            is_synthetic=False,
            case_ids=[syn_id],
            created="2026-03-03T10:00:00Z",
            resolved_at="2026-03-03T11:00:00Z",
            text="SECRET-REAL-RECORD",
        ),
        dict(
            id="MIXED-UNMARKED-LINK",
            kind="ai_task",
            task="briefing",
            source="ai",
            status="Accepted",
            verified=True,
            is_synthetic=True,
            case_ids=[syn_id, unmarked_id],
            created="2026-03-03T10:00:00Z",
            resolved_at="2026-03-03T11:00:00Z",
        ),
    ]
    return data


class _ServerHarness:
    def __init__(self, store: Any) -> None:
        app_cls: Any = App
        self.app = app_cls(store, "synthetic-check")
        handler_factory: Any = make_handler
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), handler_factory(self.app))
        self.port = self.httpd.server_address[1]
        self._cookies: dict[str, str] = {}
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()

    def close(self) -> None:
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=5)

    def _cookie_for(self, user_email: str) -> str:
        if user_email not in self._cookies:
            payload = json.dumps({"email": user_email, "password": "synthetic-check"}).encode(
                "utf-8"
            )
            req = urllib.request.Request(
                f"http://127.0.0.1:{self.port}/api/login",
                data=payload,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                self.assert_200(resp.status)
                raw_cookie = resp.headers.get("Set-Cookie") or ""
                self._cookies[user_email] = raw_cookie.split(";", 1)[0]
        return self._cookies[user_email]

    def get_json(self, path: str, user_email: str) -> dict[str, Any]:
        cookie = self._cookie_for(user_email)
        req = urllib.request.Request(
            f"http://127.0.0.1:{self.port}{path}",
            headers={"Cookie": cookie},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            self.assert_200(resp.status)
            body: dict[str, Any] = json.loads(resp.read().decode("utf-8"))
            return body

    @staticmethod
    def assert_200(status: int) -> None:
        if status != 200:
            raise AssertionError(f"Expected HTTP 200, got {status}")


class ManagementTokenomicsApiTests(unittest.TestCase):
    """Verify HTTP management endpoints expose ai_consumption_economics safely."""

    def test_unpriced_http_management_endpoints_report_denominators_and_unknown_costs(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "store.json"
            path.write_text(json.dumps(_api_fixture()), encoding="utf-8")
            store_cls: Any = Store
            store = store_cls(path)
            srv = _ServerHarness(store)
            try:
                stats_resp = srv.get_json("/api/stats", "pam@example.test")
                prog_rep = srv.get_json(
                    "/api/stats?"
                    + urlencode(
                        {
                            "report": "progress",
                            "view": "all",
                            "start": START_ISO,
                            "as_of": END_ISO,
                        }
                    ),
                    "pam@example.test",
                )
                coord = srv.get_json(
                    "/api/coordinator?" + urlencode({"start": START_ISO, "as_of": END_ISO}),
                    "rc100@example.test",
                )
                prog = srv.get_json(
                    "/api/progress?" + urlencode({"start": START_DAY, "end": END_DAY}),
                    "pam@example.test",
                )
                ai_rep = srv.get_json(
                    "/api/ai/report?"
                    + urlencode({"start": START_ISO, "end": END_ISO, "as_of": END_ISO}),
                    "pam@example.test",
                )
            finally:
                srv.close()

            # Preserve /api/ai/report top-level keys while adding live.ai_consumption_economics
            self.assertEqual(
                set(ai_rep.keys()),
                {"evaluation", "chat_evaluation", "live", "registry", "consumption"},
            )

            econs = {
                "stats": stats_resp["ai_consumption_economics"],
                "progress_report": prog_rep["ai_consumption_economics"],
                "coordinator": coord["ai_consumption_economics"],
                "progress": prog["ai_consumption_economics"],
                "ai_report_live": ai_rep["live"]["ai_consumption_economics"],
            }
            for name, econ in econs.items():
                with self.subTest(endpoint=name):
                    tokenomics.assert_tokenomics_invariants(econ)
                    self.assertFalse(econ["price_source_configured"])
                    self.assertEqual(econ["od_51_status"], "open")
                    for cost_key in COST_KEYS:
                        self.assertEqual(econ[cost_key], "Unknown")

            # Synthetic isolation on /api/progress excludes REAL-NON-SYNTHETIC & MIXED-UNMARKED-LINK
            self.assertEqual(econs["progress"]["proposal_count"], 1)
            self.assertEqual(econs["progress"]["accepted_outcome_count"], 1)
            progress_blob = json.dumps(prog)
            for forbidden in ("PRIVATE-DRAFT-BODY", "PRIVATE-REVIEW-NOTE", "SECRET-REAL-RECORD"):
                self.assertNotIn(forbidden, progress_blob)

    def test_progress_window_bounds_ai_economics_denominators_and_keeps_costs_unknown(
        self,
    ) -> None:
        # The one synthetic accepted proposal is resolved on 2026-03-03; the end date is inclusive.
        windows = (
            ("2026-03-02", "2026-03-05", 1),
            ("2026-03-03", "2026-03-03", 1),
            ("2026-03-04", "2026-03-05", 0),
            ("2026-03-01", "2026-03-02", 0),
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "store.json"
            path.write_text(json.dumps(_api_fixture()), encoding="utf-8")
            store_cls: Any = Store
            srv = _ServerHarness(store_cls(path))
            try:
                results = {
                    (start, end): srv.get_json(
                        "/api/progress?" + urlencode({"start": start, "end": end}),
                        "pam@example.test",
                    )["ai_consumption_economics"]
                    for start, end, _ in windows
                }
            finally:
                srv.close()
        for start, end, expected in windows:
            with self.subTest(start=start, end=end):
                econ = results[(start, end)]
                tokenomics.assert_tokenomics_invariants(econ)
                self.assertEqual(econ["proposal_count"], expected)
                self.assertEqual(econ["accepted_outcome_count"], expected)
                for cost_key in COST_KEYS:
                    self.assertEqual(econ[cost_key], "Unknown")

    def test_priced_sql_http_endpoints_distinguish_zero_outcomes_from_accepted_outcomes(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            seed = Path(tmp) / "seed.json"
            db_path = Path(tmp) / "zf.sqlite"
            fixture = _api_fixture()
            syn_id = fixture["cases"][0]["id"]
            fixture["recommendations"] = []
            seed.write_text(json.dumps(fixture), encoding="utf-8")

            sql_cls: Any = SqlStore
            store = sql_cls(str(seed), str(db_path))
            store.tokenomics_governance = dict(
                od_51_status="approved",
                quality_floor_status="Pass",
                components={k: "0.000010" for k in COMPONENTS},
            )
            srv = _ServerHarness(store)
            try:
                srv.app.assistants.now = lambda _db=None: tokenomics.parse_record_timestamp(
                    "2026-03-03T12:00:00Z"
                )
                ledger: Consumption = srv.app.assistants.consumption
                cfg = reference("api-cfg-100")
                budget_id = reference("api-b-100")
                price_id = ledger.price(
                    source="https://prices.azure.com/api/retail/prices",
                    source_hash=reference("api-price-100"),
                    retrieved=START_ISO,
                    version="api-v1",
                    model=MODEL,
                    currency="GBP",
                    start=START_ISO,
                    end=END_ISO,
                    input_rate="1",
                    output_rate="2",
                    cached_rate="0.5",
                    synthetic=True,
                )
                ledger.authorize(
                    authority="api-spend-auth-100",
                    owner="api-alert-owner-100",
                    evidence="api-synthetic-evidence",
                    price=price_id,
                    capability="assessment",
                    configuration=cfg,
                    start=START_ISO,
                    end=END_ISO,
                    max_calls=4,
                    max_depth=2,
                    budgets=[dict(id=budget_id, calls=50, tokens=50000, amount="25")],
                )
                root = reference("api-root-100")
                ticket = ledger.reserve(
                    CallContext(
                        root=root,
                        attempt=reference("api-attempt-100"),
                        capability="assessment",
                        case_type="retrofit-case",
                        configuration=cfg,
                        prompt=reference("api-prompt-100"),
                    ),
                    MODEL,
                    1000,
                    100,
                )
                ledger.complete(
                    ticket,
                    dict(
                        prompt_tokens=100,
                        completion_tokens=20,
                        total_tokens=120,
                        cached_tokens=10,
                    ),
                    MODEL,
                    "returned",
                )
                ledger.output(root, "API-REC-100", eligible=True)
                ledger.billing(
                    source="api-synthetic-bill-100",
                    allocation="api-exact-tag-100",
                    budget=budget_id,
                    start=START_ISO,
                    end=END_ISO,
                    currency="GBP",
                    billed="0.000135",
                    tolerance="0.01",
                    complete=True,
                    synthetic=True,
                )
                with store.lock:
                    store.data["recommendations"].append(
                        dict(
                            id="API-REC-100",
                            kind="ai_task",
                            task="briefing",
                            source="ai",
                            status="Not reviewed",
                            verified=True,
                            is_synthetic=True,
                            meter_root=root,
                            case_ids=[syn_id],
                            created="2026-03-03T12:00:00Z",
                        )
                    )

                # Before acceptance: accepted_outcome_count == 0 -> unit costs Unknown
                prog_before = srv.get_json(
                    "/api/progress?" + urlencode({"start": START_DAY, "end": END_DAY}),
                    "pam@example.test",
                )
                econ_before = prog_before["ai_consumption_economics"]
                tokenomics.assert_tokenomics_invariants(econ_before)
                self.assertTrue(econ_before["price_source_configured"])
                self.assertEqual(econ_before["accepted_outcome_count"], 0)
                self.assertEqual(econ_before["token_cost"], "0.000135")
                self.assertEqual(econ_before["token_cost_per_accepted_outcome"], "Unknown")
                self.assertEqual(econ_before["cost_per_accepted_outcome"], "Unknown")
                self.assertEqual(
                    econ_before["quality_qualified_cost_per_accepted_outcome"],
                    "Unknown",
                )

                # Accept the proposal -> unit costs become exact positive Decimal strings
                ledger.review("API-REC-100", "accept")
                with store.lock:
                    store.data["recommendations"][0]["status"] = "Accepted"
                    store.data["recommendations"][0]["resolved_at"] = "2026-03-03T12:10:00Z"

                prog_after = srv.get_json(
                    "/api/progress?" + urlencode({"start": START_DAY, "end": END_DAY}),
                    "pam@example.test",
                )
                econ_after = prog_after["ai_consumption_economics"]
                tokenomics.assert_tokenomics_invariants(econ_after)
                self.assertEqual(econ_after["accepted_outcome_count"], 1)
                self.assertEqual(econ_after["token_cost"], "0.000135")
                self.assertEqual(econ_after["token_cost_per_accepted_outcome"], "0.000135")
                self.assertEqual(
                    econ_after["quality_qualified_cost_per_accepted_outcome"],
                    "0.000135",
                )
                self.assertNotEqual(econ_after["cost_per_accepted_outcome"], "Unknown")
            finally:
                srv.close()
                store.db.close()


if __name__ == "__main__":
    unittest.main()
