"""HTTP API integration tests for Issue #220 Criterion 5: non-retaliation and zero hazard delay.

Exercises live loopback HTTP endpoints (/api/cases/<cid>/resident, /api/cases/<cid>,
/api/cases, /api/assistants/proposals/<tid>/challenge, and /api/audit-check) plus
static workbench checks on web/panels.js across digital, staff-recorded non-digital,
representative/nominee, AI task, form extraction, and SQLite assistant proposal challenge paths.
"""

from __future__ import annotations

import copy
import json
import os
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from typing import Any
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import release_support as _release_support
from tests.test_mvp import DATA
from zava_forward.core.assistants import canonical as _canonical
from zava_forward.core.challenges import build_non_retaliation_assurance
from zava_forward.core.sqlstore import SqlStore

from zava_forward.api.server import App as _App
from zava_forward.api.server import make_handler as _make_handler

RELEASE_SUPPORT: Any = _release_support
CANONICAL: Any = _canonical
APP_CLS: Any = _App
MAKE_HANDLER: Any = _make_handler
ROOT = Path(__file__).resolve().parents[3]
PANELS_JS = ROOT / "src" / "api" / "src" / "zava_forward" / "api" / "web" / "panels.js"


class HttpLocalAssistantProvider:
    configured = True
    sends_no_bytes = True
    provider = "local-test-double"
    endpoint = "local-test"
    fast = "test"

    def __init__(self, base_ai: Any) -> None:
        self._base_ai = base_ai

    def __getattr__(self, name: str) -> Any:
        return getattr(self._base_ai, name)

    def evidence(self, system: str, prompt: str, max_tokens: int, timeout: float) -> dict[str, Any]:
        del system, prompt, max_tokens, timeout
        out = {
            "summary": "SYN assistant summary requiring human review.",
            "findings": [
                {
                    "text": "SYN check appointment and home facts manually.",
                    "citations": ["source:home"],
                }
            ],
            "unknowns": [],
        }
        return {
            "text": str(CANONICAL(out)),
            "provider": "local-test-double",
            "deployment": "test",
            "model": "test-model",
            "source": "ai",
            "outcome": "returned",
            "usage": {"prompt_tokens": 70, "completion_tokens": 20, "total_tokens": 90},
        }


def _seed_api_case_invariants(case: dict[str, Any]) -> None:
    case["score"] = 91
    case["urgent"] = True
    case["awaiting_hazard_action"] = True
    case["hazards"] = [
        {
            "category": "Electrical",
            "priority": "Emergency",
            "noticed": "2026-01-14",
            "aware_at": "2026-01-14T07:30:00Z",
            "investigation_due_at": "2026-01-15T07:30:00Z",
            "make_safe_due_at": "2026-01-15T07:30:00Z",
            "source": "SYN existing 24h Awaabs Law emergency hazard",
            "recorded_at": "2026-01-14T07:35:00Z",
            "referred": None,
            "repaired": None,
            "released": False,
            "job": "",
            "owner": "Sam Officer",
            "note": "SYN 24h clock running",
            "hold": {
                "scope": "Home",
                "case_id": case["id"],
                "status": "Active",
                "accountable_role": "Building Safety Liaison",
                "decision": None,
            },
        },
        {
            "category": "Damp and mould",
            "priority": "Significant",
            "noticed": "2026-01-08",
            "aware_at": "2026-01-08T09:00:00Z",
            "investigation_due_at": "2026-01-22T09:00:00Z",
            "safety_works_due_at": "2026-01-29T09:00:00Z",
            "source": "SYN existing 7d/14d Awaabs Law damp hazard",
            "recorded_at": "2026-01-08T09:10:00Z",
            "referred": "2026-01-08",
            "repaired": None,
            "released": False,
            "job": "SYN-DAMP-14D",
            "owner": "Sam Officer",
            "note": "SYN 14d investigation clock running",
            "hold": {
                "scope": "Home",
                "case_id": case["id"],
                "status": "Active",
                "accountable_role": "Building Safety Liaison",
                "decision": None,
            },
        },
    ]
    case["safeguarding"] = [
        {
            "id": "SG-API-1",
            "status": "Open",
            "raised_at": "2026-11-13T10:00:00Z",
            "due_by": "2026-11-16T10:00:00Z",
            "escalate_by": "2026-11-17T10:00:00Z",
            "paused": False,
        }
    ]
    case["tasks"] = [{"id": "TSK-API-1", "title": "SYN open task", "done": False, "status": "Open"}]
    case["service_requests"] = [
        {
            "id": "SR-API-1",
            "kind": "Repair query",
            "status": "Open",
            "closed": False,
            "route": "Standard",
            "channel": "Phone",
            "summary": "SYN open repair follow-up",
            "source": "SYN-SR-API-1",
            "owner": {
                "email": "sam@example.test",
                "name": "Sam Officer",
                "role": "Resident Liaison Officer",
                "code": "RLO-1",
            },
            "next_update": "2026-11-25",
            "version": 1,
            "remedy": {
                "status": "Open",
                "owner": None,
                "at": None,
                "opened_at": "2026-11-13T10:00:00Z",
                "version": 1,
                "history": [],
            },
        }
    ]
    case["handoff"] = {"state": "Offered", "to_code": "RLO-1", "note": "SYN active handoff"}
    case["representative_authorities"] = {
        "SYN-CARER-AUTH-1": [
            {
                "version": 1,
                "representative_ref": "SYN-CARER-AUTH-1",
                "status": "Confirmed",
            }
        ]
    }
    case["form_staging"] = [
        {
            "id": "BATCH-API-1",
            "case_id": case["id"],
            "schema_id": "pas2035-ventilation",
            "schema_version": "1.0",
            "schema_digest": "sha256:syn-api-220",
            "source": {
                "id": "DOC-API-1",
                "kind": "Survey",
                "version": 1,
                "content_sha256": "synapisha256",
            },
            "processing": {
                "mode": "ai",
                "model": "syn-api-form-model",
                "prompt_version": "form-v1",
            },
            "verification": None,
            "candidates": [
                {
                    "id": "C-1",
                    "field_id": "trickle_vents",
                    "raw_value": "none",
                    "locator": {"page": 1},
                }
            ],
        }
    ]
    case["form_reviews"] = [
        {
            "id": "DRAFT-API-1",
            "version": 1,
            "schema_digest": "sha256:syn-api-220",
            "status": "Unapproved working notes",
            "fields": {
                "trickle_vents": {
                    "value": "none",
                    "state": "Accepted",
                    "evidence": {
                        "batch_id": "BATCH-API-1",
                        "candidate_id": "C-1",
                    },
                }
            },
            "recorded_by": "pam@example.test",
            "recorded_at": "2026-10-01T11:30:00+00:00",
        }
    ]


class ChallengeNoRetaliationApi220Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.env_patch = patch.dict(
            os.environ,
            {
                "ZF_ASSIST_AUTHORITY": "local-nonbillable-test-authority",
                "ZF_ASSIST_EXPIRES": "2099-01-01T00:00:00Z",
                "ZF_ASSIST_CALL_ALLOWANCE": "100",
                "ZF_ASSIST_TOKEN_ALLOWANCE": "2000000",
                "ZF_ASSIST_PROACTIVE": "0",
            },
        )
        self.env_patch.start()
        self.addCleanup(self.env_patch.stop)

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
        for c in data["cases"]:
            if c["id"] == "ZF-1":
                _seed_api_case_invariants(c)
        self.path.write_text(json.dumps(data))
        self.store = SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
        self.addCleanup(self.store.db.close)
        self.store.ai = HttpLocalAssistantProvider(self.store.ai)
        self.app = APP_CLS(self.store, "synthetic-only")
        RELEASE_SUPPORT.install(self.store)
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), MAKE_HANDLER(self.app))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.addCleanup(self.shutdown)
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"
        self.cookies: dict[str, str] = {}

    def shutdown(self) -> None:
        self.app.assistants.stop()
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)

    def call(self, path: str, actor: str = "", body: object = None) -> tuple[int, Any]:
        if actor and actor not in self.cookies:
            req = Request(
                self.base + "/api/login",
                json.dumps(
                    {"email": f"{actor}@example.test", "password": "synthetic-only"}
                ).encode(),
            )
            with urlopen(req, timeout=5) as response:
                self.cookies[actor] = response.headers["Set-Cookie"].split(";")[0]
        req = Request(
            self.base + path,
            data=json.dumps(body).encode() if body is not None else None,
            headers={"Cookie": self.cookies.get(actor, ""), "Content-Type": "application/json"},
        )
        try:
            with urlopen(req, timeout=5) as response:
                raw = response.read()
                return response.status, (
                    json.loads(raw)
                    if "application/json" in response.headers.get("Content-Type", "")
                    else raw.decode()
                )
        except HTTPError as error:
            return error.code, json.loads(error.read())

    def test_http_case_challenge_all_channels_reopen_immediate_hazard_and_audit(self) -> None:
        sam_staff = self.store.staff["sam@example.test"]
        prio = self.store.ai_priority(sam_staff, n=5, mode="workflow-only")
        msg = self.store.ai_run(sam_staff, "ZF-1", "message", mode="workflow-only")
        msg_id = str(msg["record_id"])

        code, cases_before = self.call("/api/cases?view=all", "pam")
        self.assertEqual(code, 200)
        order_before = [row["id"] for row in cases_before["items"]]

        code, case0 = self.call("/api/cases/ZF-1", "sam")
        self.assertEqual(code, 200)
        targets = {t["proposal_id"]: t for t in case0["challenge_targets"]}
        self.assertIn(prio["id"], targets)
        self.assertIn(msg_id, targets)
        self.assertIn("form:BATCH-API-1", targets)

        hazards_before = copy.deepcopy(case0["hazards"])
        safeguarding_before = copy.deepcopy(case0["safeguarding"])
        tasks_before = copy.deepcopy(case0["tasks"])
        service_before = copy.deepcopy(case0["service_requests"])

        # Open via /api/cases/ZF-1/resident across representative + Assisted visit on ai_task,
        # and via /api/cases/ZF-1/followup across Nominee + Trusted intermediary on form_staging!
        msg_t = targets[msg_id]
        code, res1 = self.call(
            "/api/cases/ZF-1/resident",
            "sam",
            {
                "action": "challenge_open",
                "proposal_id": msg_id,
                "proposal_version": msg_t["proposal_version"],
                "decision_version": msg_t["decision_version"],
                "target_kind": "proposal",
                "channel": "Assisted visit",
                "submitted_by": "Their representative",
                "representative_ref": "SYN-CARER-AUTH-1",
                "source": "SYN-HTTP-SRC-1",
                "request": "SYN representative challenges AI message wording.",
                "explanation": (
                    "SYN logged during assisted visit without consent or refusal inference."
                ),
                "owner": "sam@example.test",
                "non_digital_route": "SYN Phone Sam or request home visit.",
                "next_update": "2099-03-01",
            },
        )
        self.assertEqual(code, 200, res1)
        ch1 = res1["affected_challenges"][0]
        self.assertTrue(ch1["hazard_clock_preserved"])
        self.assertEqual(
            ch1["non_retaliation_assurance"],
            build_non_retaliation_assurance(hazard_concern=False, independent_hazard_routed=False),
        )

        form_t = targets["form:BATCH-API-1"]
        code, res2 = self.call(
            "/api/cases/ZF-1/resident",
            "sam",
            {
                "action": "challenge_open",
                "proposal_id": "form:BATCH-API-1",
                "proposal_version": form_t["proposal_version"],
                "decision_version": form_t["decision_version"],
                "target_kind": "source",
                "channel": "Trusted intermediary",
                "submitted_by": "Nominee",
                "representative_ref": "SYN-ADVOCATE-API-2",
                "source": "SYN-HTTP-SRC-2",
                "request": (
                    "SYN nominee challenges extracted ventilation value and flags black mould."
                ),
                "explanation": "SYN urgent damp hazard routed separately right now.",
                "owner": "sam@example.test",
                "non_digital_route": "SYN Phone Sam or drop letter at office.",
                "hazard_concern": True,
                "hazard_intake": {
                    "category": "Damp and mould",
                    "priority": "Emergency",
                    "source": "SYN trusted intermediary phone intake",
                    "aware_at": "2026-01-15T13:00:00Z",
                    "note": "SYN severe mould in child bedroom routed immediately",
                },
                "next_update": "2099-03-02",
            },
        )
        self.assertEqual(code, 200, res2)
        ch2 = res2["affected_challenges"][1]
        self.assertTrue(ch2["hazard_clock_preserved"])
        self.assertEqual(
            ch2["non_retaliation_assurance"],
            build_non_retaliation_assurance(hazard_concern=True, independent_hazard_routed=True),
        )
        self.assertEqual(len(res2["hazards"]), 3)
        self.assertEqual(res2["hazards"][:2], hazards_before)
        self.assertEqual(res2["safeguarding"], safeguarding_before)
        self.assertEqual(res2["tasks"], tasks_before)
        self.assertEqual(res2["service_requests"], service_before)

        # Resolve CH-1 as Correction recorded, then reopen CH-1 via HTTP and verify staleness holds!
        code, res_resolved = self.call(
            "/api/cases/ZF-1/resident",
            "sam",
            {
                "action": "challenge_resolve",
                "id": "CH-1",
                "expected_version": 1,
                "resolution": "Correction recorded",
                "resolution_ref": "SYN-HTTP-CORR-1",
                "explanation": "SYN confirmed wording used stale contact preference.",
                "next_update": "2099-03-03",
            },
        )
        self.assertEqual(code, 200, res_resolved)
        code, res_reopened = self.call(
            "/api/cases/ZF-1/resident",
            "sam",
            {
                "action": "challenge_reopen",
                "id": "CH-1",
                "expected_version": 2,
                "channel": "Letter",
                "submitted_by": "Their representative",
                "representative_ref": "SYN-CARER-AUTH-1",
                "source": "SYN-HTTP-REOPEN-1",
                "request": "SYN representative sent follow-up letter.",
                "explanation": "SYN reopened while keeping prior correction stale marker.",
                "owner": "rae@example.test",
                "next_update": "2099-03-05",
            },
        )
        self.assertEqual(code, 200, res_reopened)
        reopened_ch1 = res_reopened["affected_challenges"][0]
        self.assertEqual(reopened_ch1["status"], "Reopened")
        self.assertTrue(reopened_ch1["prior_correction_preserved"])
        after_targets = {t["proposal_id"]: t for t in res_reopened["challenge_targets"]}
        self.assertTrue(after_targets[msg_id]["stale"])

        # Case ranking order across /api/cases?view=all never dropped!
        code, cases_after = self.call("/api/cases?view=all", "pam")
        self.assertEqual(code, 200)
        self.assertEqual([row["id"] for row in cases_after["items"]], order_before)

        # Adverse field injection or unknown keys return HTTP 400; unauthorized roles get 403!
        code, bad_adverse = self.call(
            "/api/cases/ZF-1/resident",
            "sam",
            {
                "action": "challenge_update",
                "id": "CH-1",
                "expected_version": 3,
                "channel": "Phone",
                "source": "SYN",
                "request": "SYN",
                "explanation": "SYN",
                "next_update": "2099-03-06",
                "no_access": True,
            },
        )
        self.assertEqual(code, 400, bad_adverse)
        for denied_actor in ("rex", "bea", "kim"):
            self.assertEqual(
                self.call(
                    "/api/cases/ZF-1/resident",
                    denied_actor,
                    {
                        "action": "challenge_escalate",
                        "id": "CH-1",
                        "expected_version": 3,
                        "owner": "pam@example.test",
                        "reason": "SYN denied",
                        "next_update": "2099-03-07",
                    },
                )[0],
                403,
            )

        # Audit check endpoint confirms ledger intact & entries carry non-retaliation tags!
        code, ledger_status = self.call("/api/audit-check", "pam")
        self.assertEqual(code, 200)
        self.assertTrue(ledger_status["intact"])
        chal_audits = [
            row
            for row in self.store.audit_entries()
            if str(row.get("action", "")).startswith("resident_challenge_")
        ]
        self.assertGreaterEqual(len(chal_audits), 4)
        for row in chal_audits:
            self.assertIn("non_retaliation_assurance=verified", row["detail"])
            self.assertIn("hazard_clock_preserved=true", row["detail"])

    def test_http_assistant_proposal_challenge_endpoint_lifecycle_and_safety_routing(self) -> None:
        code, invoked = self.call(
            "/api/assistants/works-resident-coordination/invoke",
            "sam",
            {"case_id": "ZF-1"},
        )
        self.assertEqual(code, 202, invoked)
        tid = invoked["id"]
        self.assertTrue(self.app.assistants.execute(tid))
        code, ready = self.call(f"/api/assistants/proposals/{tid}", "sam")
        self.assertEqual(code, 200, ready)
        self.assertTrue(ready["actionable"])

        code, case_before = self.call("/api/cases/ZF-1", "sam")
        self.assertEqual(code, 200)
        hazards_before = copy.deepcopy(case_before["hazards"])

        # POST /api/assistants/proposals/<tid>/challenge: open with immediate hazard_intake!
        code, opened = self.call(
            f"/api/assistants/proposals/{tid}/challenge",
            "sam",
            {
                "action": "open",
                "revision": ready["revision"],
                "target_kind": "proposal",
                "channel": "Phone",
                "submitted_by": "Nominee",
                "representative_ref": "SYN-CARER-AUTH-1",
                "source": "SYN-API-ASSIST-1",
                "request": (
                    "SYN nominee disputes appointment slot and reports live electrical fault."
                ),
                "explanation": (
                    "SYN proposal held for human check; emergency hazard raised immediately."
                ),
                "owner": "sam@example.test",
                "non_digital_route": "SYN Phone Sam or emergency control room.",
                "hazard_concern": True,
                "hazard_intake": {
                    "category": "Electrical",
                    "priority": "Emergency",
                    "source": "SYN nominee telephone report",
                    "aware_at": "2026-01-15T14:00:00Z",
                    "note": "SYN immediate emergency attendance dispatched",
                },
                "next_update": "2099-03-10",
            },
        )
        self.assertEqual(code, 200, opened)
        self.assertTrue(opened["hazard_clock_preserved"])
        self.assertEqual(
            opened["non_retaliation_assurance"],
            build_non_retaliation_assurance(hazard_concern=True, independent_hazard_routed=True),
        )

        code, case_after = self.call("/api/cases/ZF-1", "sam")
        self.assertEqual(code, 200)
        self.assertEqual(len(case_after["hazards"]), 3)
        self.assertEqual(case_after["hazards"][:2], hazards_before)

        # Resolve as Correction recorded -> 200, proposal becomes stale & non-actionable;
        # stale revision -> 409; unauthorized role -> 403; reopen -> 200 keeping stale=True!
        code, resolved = self.call(
            f"/api/assistants/proposals/{tid}/challenge",
            "pam",
            {
                "action": "resolve",
                "revision": opened["revision"],
                "id": "ACH-1",
                "expected_version": 1,
                "resolution": "Correction recorded",
                "resolution_ref": "SYN-API-ASSIST-CORR",
                "explanation": "SYN confirmed slot conflicted with hospital visit.",
                "next_update": "2099-03-12",
            },
        )
        self.assertEqual(code, 200, resolved)
        self.assertTrue(resolved["stale"])
        self.assertFalse(resolved["actionable"])

        # Stale revision returns 409 Conflict
        code, conflict = self.call(
            f"/api/assistants/proposals/{tid}/challenge",
            "pam",
            {
                "action": "reopen",
                "revision": opened["revision"],
                "id": "ACH-1",
                "expected_version": 2,
                "reason": "SYN stale revision check",
                "source": "SYN-SRC",
                "next_update": "2099-03-14",
            },
        )
        self.assertEqual(code, 409, conflict)

        # Unauthorized role (rex - Retrofit Coordinator without recorded-reason rights) gets 403
        code, forbidden = self.call(
            f"/api/assistants/proposals/{tid}/challenge",
            "rex",
            {
                "action": "reopen",
                "revision": resolved["revision"],
                "id": "ACH-1",
                "expected_version": 2,
                "reason": "SYN unauthorized role check",
                "source": "SYN-SRC",
                "next_update": "2099-03-14",
            },
        )
        self.assertEqual(code, 403, forbidden)

        # Authorised reopen returns 200 and preserves stale=True
        code, reopened = self.call(
            f"/api/assistants/proposals/{tid}/challenge",
            "pam",
            {
                "action": "reopen",
                "revision": resolved["revision"],
                "id": "ACH-1",
                "expected_version": 2,
                "channel": "Trusted intermediary",
                "submitted_by": "Nominee",
                "representative_ref": "SYN-CARER-AUTH-1",
                "reason": "SYN nominee added care-worker schedule.",
                "source": "SYN-API-ASSIST-REOPEN",
                "next_update": "2099-03-15",
            },
        )
        self.assertEqual(code, 200, reopened)
        self.assertTrue(reopened["stale"])
        self.assertFalse(reopened["actionable"])
        self.assertEqual(reopened["challenges"][0]["status"], "Open")
        self.assertTrue(reopened["challenges"][0]["prior_correction_preserved"])

    def test_workbench_panels_js_exposes_representative_channels_reopen_and_safeguard_copy(
        self,
    ) -> None:
        js = PANELS_JS.read_text(encoding="utf-8")
        for expected in (
            '"Assisted visit"',
            '"Trusted intermediary"',
            '"Their representative"',
            '"Nominee"',
            '"representative_ref"',
            '"hazard_concern"',
            'action: "challenge_reopen"',
            "Safeguards verified: priority unchanged, no refusal or no-access recorded",
            "Safety concern flagged on receipt for separate urgent safety action",
        ):
            self.assertIn(expected, js)


if __name__ == "__main__":
    unittest.main()
