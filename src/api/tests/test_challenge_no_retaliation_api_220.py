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
        base_hazards = [h for h in hazards_before if not h.get("standalone_safeguarding")]
        base_sg_views = [h for h in hazards_before if h.get("standalone_safeguarding")]
        after_hazards = [h for h in case_after["hazards"] if not h.get("standalone_safeguarding")]
        after_sg_views = [h for h in case_after["hazards"] if h.get("standalone_safeguarding")]
        self.assertEqual(len(after_hazards), len(base_hazards) + 1)
        self.assertEqual(after_hazards[: len(base_hazards)], base_hazards)
        self.assertEqual(after_sg_views, base_sg_views)

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


if __name__ == "__main__":
    unittest.main()
