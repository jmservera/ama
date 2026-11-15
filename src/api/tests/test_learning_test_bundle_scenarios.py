"""Specialist role-screen and aftercare scenario verification for #129 learning-test bundles.

Constructed two-arm comparisons from `zava_forward.core.learning_test_bundles` are paired here
with real Node-VM renders of `role-screens.js` and `aftercare.js` (over `AftercareService`) across
all five candidate bundles (`story-once`, `pre-visit-pack`, `change-impact`, `handover-aftercare`,
`funding-evidence`), while verifying that `O10` and `O18` to `O20` stay out of scope and no
unapproved runtime bundle-runner screen or stored run endpoint is wired before Atlas-owner
confirmation and DPO retention approval.
"""

import json
import subprocess
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, ClassVar

from zava_forward.core import aftercare_intake as ai
from zava_forward.core import learning_test_bundles as ltb
from zava_forward.core.synthetic import sensor_scenarios as ss

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"
SERVER = Path(__file__).resolve().parents[1] / "src/zava_forward/api/server.py"
HOME_ID = "ZF-129"
NOW = datetime(2026, 11, 10, 12, 0, tzinfo=UTC)
LIAISON = {"name": "Synthetic Liaison", "role": "Resident Liaison Officer"}
MANAGER = {"name": "Synthetic Manager", "role": "Retrofit Programme Manager"}

SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const webDir = process.argv[1];
const appSrc = fs.readFileSync(webDir + "/app.js", "utf8");
const workSummarySrc = appSrc.slice(
  appSrc.indexOf("function workSummary("),
  appSrc.indexOf("function workSteps(")
);
const roleSrc = fs.readFileSync(webDir + "/role-screens.js", "utf8");
const aftercareSrc = fs.readFileSync(webDir + "/aftercare.js", "utf8");
const payload = JSON.parse(fs.readFileSync(0, "utf8"));

const h = (tag, attrs, ...kids) => {
  const node = {
    tag,
    attrs: attrs || {},
    kids: kids.flat(Infinity).filter((kid) => kid !== false && kid !== null && kid !== undefined)
  };
  Object.defineProperty(node, "replaceChildren", { value: (...k) => { node.kids = k; } });
  Object.defineProperty(node, "textContent", { set: (v) => { node.kids = [v]; } });
  return node;
};
const text = (node) => {
  if (!node || typeof node !== "object") return String(node ?? "");
  return (node.kids || []).map(text).join(" ");
};
const walk = (node, fn) => {
  if (node && typeof node === "object") {
    fn(node);
    (node.kids || []).forEach((kid) => walk(kid, fn));
  }
};

async function renderScreen(role, screenId, caseRecord, apiData) {
  let shown = [];
  const loc = { hash: `#/screens?screen=${screenId}&case=${encodeURIComponent(caseRecord.id)}` };
  const context = vm.createContext({
    location: loc,
    history: { replaceState: (_a, _b, url) => { loc.hash = url; } },
    URLSearchParams,
    Intl,
    AbortController,
    Date,
    routeController: new AbortController(),
    me: { user: { role } },
    workspaceStatus: {},
    h,
    api: async (url) => {
      if (url.startsWith("/api/cases?")) return { items: [caseRecord], total: 1 };
      if (url === `/api/cases/${encodeURIComponent(caseRecord.id)}`) return caseRecord;
      if (Object.hasOwn(apiData, url)) return apiData[url];
      throw Object.assign(new Error(`unmocked ${url}`), { status: 404 });
    },
    show: (...nodes) => { shown = nodes; }
  });
  vm.runInContext(
    workSummarySrc + "\n" + roleSrc + "\n;globalThis.__screens = roleScreens;",
    context
  );
  await vm.runInContext("roleScreensView()", context);
  const jumpLinks = [];
  const stageLinks = [];
  const captions = [];
  shown.forEach((root) => walk(root, (node) => {
    if (node.tag === "a" && node.attrs["data-jump"]) {
      jumpLinks.push(node.attrs["data-jump"]);
    }
    if (node.tag === "a" && typeof node.attrs.href === "string"
        && node.attrs.href.startsWith("#/screens?")) {
      stageLinks.push({ href: node.attrs.href, text: text(node) });
    }
    if (node.tag === "caption") {
      captions.push(text(node));
    }
  }));
  return {
    registeredIds: [...context.__screens.keys()],
    workspaceStatus: context.workspaceStatus.textContent || "",
    text: shown.map(text).join(" "),
    jumpLinks,
    stageLinks,
    captions
  };
}

function renderAftercare(aftercarePayload) {
  const context = vm.createContext({ Intl, h });
  vm.runInContext(aftercareSrc, context);
  const s = context.aftercareScreens;
  const form = s.formView(aftercarePayload.form, {
    values: { raised_by: "representative" },
    requestId: "req-zf129-001"
  });
  const receipt = s.receiptView(aftercarePayload.receipt);
  const concern = s.concernView(aftercarePayload.concern);
  const evaluator = s.evaluatorView(aftercarePayload.evaluator);
  return {
    formText: text(form),
    receiptText: text(receipt),
    concernText: text(concern),
    evaluatorText: text(evaluator)
  };
}

(async () => {
  const screens = {};
  for (const spec of payload.renders) {
    screens[spec.key] = await renderScreen(
      spec.role,
      spec.screen,
      payload.caseRecord,
      payload.apiData
    );
  }
  const aftercare = renderAftercare(payload.aftercare);
  console.log(JSON.stringify({ screens, aftercare }));
})().catch((err) => {
  console.error(err);
  process.exitCode = 1;
});
"""


def _constructed_case() -> dict[str, Any]:
    source_side = {
        "value": "D",
        "source_id": "EPC-REG",
        "version": "1",
        "date": "2024-03-01",
        "validation_state": "Reviewed",
    }
    return {
        "id": HOME_ID,
        "address": "14 Example Terrace",
        "town": "Northborough",
        "status": "In delivery",
        "measures": ["Loft insulation", "Heating controls"],
        "needs_notice": True,
        "named_contact": "Synthetic Liaison (Resident Liaison Officer)",
        "measure_decisions": [
            {
                "measure": "Loft insulation",
                "status": "Accepted",
                "readiness": "Ready on current scope",
                "context": {"scope": "PKG-129", "revision": 2, "design_version": 2},
                "versions": [
                    {
                        "version": 2,
                        "status": "Accepted",
                        "scope": "PKG-129",
                        "context_revision": 2,
                        "design_version": 2,
                        "answered_by": "Tenant via signed paper form",
                        "at": "2026-11-05T10:00:00Z",
                        "note": "Loft work agreed; morning visits requested.",
                    }
                ],
            },
            {
                "measure": "Heating controls",
                "status": "Paused",
                "readiness": "Paused by resident",
                "context": {"scope": "PKG-129", "revision": 2, "design_version": 2},
                "review": {"status": "Needs human review", "decision_version": 1},
                "versions": [
                    {
                        "version": 1,
                        "status": "Paused",
                        "scope": "PKG-129",
                        "context_revision": 2,
                        "design_version": 2,
                        "answered_by": "Representative with signed authority",
                        "at": "2026-11-06T11:30:00Z",
                        "note": "Hold heating controls until controls guide is in large print.",
                    }
                ],
            },
        ],
        "resident_update": {
            "status": "Outstanding",
            "purpose": "Confirm revised design dependency and large-print handover pack",
            "owner": "Synthetic Liaison",
            "due_at": "2026-11-18T12:00:00Z",
            "basis": "Agreed seven-day resident update rule",
            "safe_contact_ref": "SAFE-ROUTE-129",
            "version": 2,
        },
        "service_requests": [
            {
                "id": "SR-129",
                "route": "Assisted phone or paper request",
                "summary": "Keep representative copied and avoid repeat story questions",
                "desired_outcome": "Single named update owner and large-print guide",
                "status": "Open",
                "service_owner": "Synthetic Liaison",
                "redress_owner": "Resident Engagement Lead",
                "accessibility": ["Large print", "Morning notice before visit"],
                "representative_ref": "AUTH-LETTER-129",
                "next_update": "2026-11-18T12:00:00Z",
                "history": [
                    {
                        "status": "Open",
                        "by": "Synthetic Liaison",
                        "at": "2026-11-06T12:00:00Z",
                        "note": "Recorded with signed representative authority.",
                    }
                ],
            }
        ],
        "redress_route": {
            "commitments": ["Asking for a human review never delays urgent repairs or support."],
            "routes": [
                {
                    "route": "Independent review",
                    "who": "Resident, representative or staff",
                    "how": "By phone, paper, visit or workspace record",
                }
            ],
            "reviewable_decisions": [
                {"measure": "Heating controls", "version": 1, "status": "Paused"}
            ],
            "formal_requests": [],
            "send_note": "Nothing is sent from this reader screen.",
        },
        "work": {
            "owner": "Synthetic Coordinator",
            "resident_update_owner": "Synthetic Liaison",
            "queues": ["unowned", "blocked"],
            "reason": "Design revision requires building safety reassessment",
            "next_action": "Complete building safety reassessment on design version 2",
            "source": "WORK-129",
            "evidence": "EV-129",
            "version": "2",
            "recorded_at": "2026-11-10T09:00:00Z",
            "as_of": "2026-11-10T09:00:00Z",
            "hazard_clocks": [],
            "handoff": {
                "destination": "Building Safety Liaison",
                "sender": "Synthetic Coordinator",
                "proposed_receiver": "Synthetic Safety Reviewer",
                "confirmed_receiver": "Unconfirmed",
                "chase_owner": "Synthetic Coordinator",
                "resident_update_owner": "Synthetic Liaison",
                "state": "Awaiting receiver acceptance",
            },
            "blockers": [
                {
                    "step": "Technical review",
                    "reason": "Building dependency sign-off needs reassessment after v2 change.",
                    "owner": "Building Safety Liaison",
                    "responsible_role": "Building Safety Liaison",
                    "next_action": "Reassess building dependency on design version 2",
                    "source": "DES-129",
                    "version": "2",
                }
            ],
        },
        "stock_reconciliation": [
            {
                "id": "SQ-129",
                "field": "epc_band",
                "left": source_side,
                "right": source_side,
                "query_owner": {"name": "Data Steward"},
            }
        ],
        "stock_reconciliation_events": [{"query_id": "SQ-129", "status": "Reconciled"}],
        "technical": {
            "design_version": 2,
            "design_name": "Synthetic Designer",
            "design_at": "2026-11-08T14:00:00Z",
            "versions": [{"note": "Scoped flue clearance revision affecting building sign-off"}],
            "signoffs": {
                "assessment": {
                    "status": "Signed off",
                    "version": 1,
                    "by": "Synthetic Assessor",
                    "history": [],
                },
                "design": {
                    "status": "Signed off",
                    "version": 2,
                    "by": "Synthetic Coordinator",
                    "history": [],
                },
                "building": {
                    "status": "Needs reassessment",
                    "reason": "Scoped flue clearance revision in design version 2",
                    "history": [{"by": "Synthetic Coordinator"}],
                },
                "coordination": {
                    "status": "Signed off",
                    "version": 2,
                    "by": "Synthetic Manager",
                    "history": [],
                },
            },
        },
        "technical_missing": [],
        "quality": [
            {
                "measure": "Loft insulation",
                "state": "Returned",
                "checklist": "PAS-2035-LOFT",
                "checklist_version": "v1",
                "evidence_version": "ev-2",
                "source": "SITE-INSP-129",
                "submitted_by": "NorthContractor Ltd",
                "accepted_by": "",
                "resident_binding": {"measure": "Loft insulation", "context_revision": 2},
                "items": [
                    {"label": "Eaves ventilation maintained", "evidence": "Gap noted at north eave"}
                ],
                "defect": {
                    "description": "Ventilation baffle displaced at north eave",
                    "reason": "Airflow gap below checklist threshold",
                    "owner": "NorthContractor Remediation Lead",
                    "raised_by": "Synthetic Quality Inspector",
                    "fixed_by": "",
                    "remediation_evidence": "",
                },
            }
        ],
        "quality_handover_blockers": [
            {
                "measure": "Loft insulation",
                "reason": "Open returned defect blocks handover sign-off.",
            }
        ],
        "funding": {
            "route": "Warm Homes Social Housing Wave",
            "status": "Draft evidence in review",
            "reference": "WH-129",
        },
        "grants": [
            {
                "id": "GR-129",
                "scheme": "Warm Homes Social Housing Wave",
                "state": "Evidence assembly",
                "eligibility": {"outcome": "", "verified": False},
                "history": [
                    {
                        "state": "Baseline logged",
                        "source": "EPC-REG v1",
                        "approved_by": "Grants Reviewer",
                        "source_status": "Current",
                    }
                ],
            }
        ],
        "finance": {
            "budget": {"amount": 12000, "status": "Approved"},
            "commitments": [
                {
                    "id": "COM-129",
                    "status": "Approved",
                    "measure": "Loft insulation",
                    "quantity": 1,
                    "amount": 4500,
                }
            ],
            "invoices": [
                {
                    "id": "INV-129",
                    "kind": "Interim",
                    "ref": "SUP-129-A",
                    "supplier": "NorthContractor Ltd",
                    "work_order": "WO-129",
                    "commitment": "COM-129",
                    "status": "Matched",
                    "payment_status": "Not paid",
                    "hold": {"name": "Grants Officer", "reason": "Open quality defect on loft"},
                    "lines": [
                        {
                            "measure": "Loft insulation",
                            "quantity": 1,
                            "amount": 4500,
                            "milestone_ref": "MS-LOFT-1",
                        }
                    ],
                    "exceptions": [],
                }
            ],
        },
    }


def _api_routes() -> dict[str, Any]:
    work_orders = [
        {
            "id": "WO-129",
            "version": 2,
            "package": "PKG-129",
            "contractor": "NorthContractor Ltd",
            "state": "Issued",
            "measures": "Loft insulation",
            "scope": "Loft insulation only; heating controls paused by resident",
            "scope_version": 2,
            "appointment_control": {"status": "Offered", "missing": ["Resident confirmation"]},
            "appointments": [{"slot": "2026-11-21 AM", "state": "Offered"}],
            "versions": [
                {
                    "version": 2,
                    "resident_bindings": [{"measure": "Loft insulation", "context_revision": 2}],
                }
            ],
            "history": [],
            "corrections": [],
        }
    ]
    packages = [
        {
            "id": "PKG-129",
            "name": "North Terrace Fabric Lot",
            "period_from": "2026-11-01",
            "period_to": "2027-01-31",
            "scope": "Loft insulation",
            "scope_version": 2,
            "contract_ref": "CALL-129",
            "contract_version": 1,
            "leaseholder_consultation_status": "not_verified",
            "capacity": [
                {
                    "contractor": "NorthContractor Ltd",
                    "offered": 6,
                    "committed": 2,
                    "in_use": 1,
                    "headroom": 4,
                    "evidence_status": "Evidenced on supplier return",
                    "insurance_expiry": "2027-06-30",
                    "certification_expiry": "2027-06-30",
                }
            ],
        }
    ]
    form_review = {
        "held_download_enabled": True,
        "decision_holds": [{"id": "HOLD-129", "reason": "Awaiting v2 building reassessment"}],
        "drafts": [
            {
                "draft_id": "DR-129",
                "schema_id": "wh-claim",
                "schema_version": "1.0",
                "input_version": 2,
                "template": {"name": "Warm Homes Claim Pack"},
                "funding": {"route": "Warm Homes Social Housing Wave"},
                "rule_refs": ["WH-RULE-04"],
                "reviewed_ready": False,
                "approved_rule_validation": "Held until stale fields are re-reviewed",
                "unit_currency_verification": "GBP whole pounds",
                "stale_fields": ["building_clearance_signoff"],
                "dependency_impact": {
                    "approvals": [
                        {
                            "decision_id": "APR-DESIGN-V1",
                            "state": "Review required",
                            "fields": ["building_clearance_signoff"],
                        }
                    ]
                },
                "fields": {
                    "building_clearance_signoff": {
                        "state": "Held",
                        "effective_state": "Stale after design v2",
                        "value": "Design v1 reference",
                        "evidence": {
                            "source": {"id": "DES-129", "version": "1", "kind": "design_signoff"}
                        },
                    }
                },
                "issues": [
                    {
                        "field_id": "building_clearance_signoff",
                        "status": "Stale",
                        "reason": "Design updated to v2; prior v1 approval does not transfer.",
                    }
                ],
                "notice": "Held draft only: no submission or award is recorded or inferred.",
            }
        ],
    }
    freshness = {
        "proposals": [{"field_id": "building_clearance_signoff", "state": "Stale source v1"}]
    }
    finance_queue = [
        {
            "case_id": HOME_ID,
            "invoice": "INV-129",
            "supplier": "NorthContractor Ltd",
            "ref": "SUP-129-A",
            "status": "Matched",
            "exceptions": 0,
            "on_hold": True,
            "total": 4500,
        }
    ]
    return {
        "/api/resident/choice-queue?limit=100&offset=0": {
            "items": [_constructed_case()],
            "total": 1,
        },
        "/api/coordinator?view=all": {
            "as_of": "2026-11-10",
            "audit_integrity": "Intact",
            "funnel": [
                {
                    "stage": "Technical review",
                    "entries": 2,
                    "exits": 1,
                    "returns": 1,
                    "reopens": 0,
                    "denominator": 2,
                }
            ],
        },
        f"/api/workorders?case={HOME_ID}": work_orders,
        "/api/packages": packages,
        f"/api/cases/{HOME_ID}/form-review": form_review,
        f"/api/cases/{HOME_ID}/form-review/DR-129/proposal-freshness": freshness,
        "/api/finance": finance_queue,
        # Simulate AI report unavailable so manual-continuity fallbacks render cleanly.
        "/api/ai/report": None,
    }


def _aftercare_payload() -> dict[str, Any]:
    scenario_homes = [str(s["rows"][0]["home_id"]) for s in ss.retrofit_exercise_scenarios()]
    all_homes = [*scenario_homes, HOME_ID]
    with tempfile.TemporaryDirectory() as tmp:
        svc = ai.AftercareService(
            ai.FileStateStore(Path(tmp) / "aftercare.json"),
            homes=all_homes,
            cohort=all_homes,
            now=lambda: NOW,
        )
        receipt, _ = svc.record_concern(
            LIAISON,
            {
                "request_id": "req-zf129-001",
                "raised_by": "representative",
                "representative_basis": "Signed letter from the tenant",
                "home_ref": HOME_ID,
                "kind": "discomfort",
                "statement": "The hallway radiator stays cold after the heating check.",
                "channel": "phone",
                "next_update": "2026-11-20",
                "support_needed": ["large_print"],
            },
        )
        svc.record_closure(MANAGER, HOME_ID, "handover", "2026-11-12")
        svc.record_closure(MANAGER, HOME_ID, "financial", "2026-11-14")
        return {
            "form": svc.form(LIAISON),
            "receipt": receipt,
            "concern": svc.concern(MANAGER, "AC-001"),
            "evaluator": svc.evaluator_view(MANAGER),
        }


def _render_all() -> dict[str, Any]:
    payload = {
        "caseRecord": _constructed_case(),
        "apiData": _api_routes(),
        "aftercare": _aftercare_payload(),
        "renders": [
            {
                "key": "resident-choice",
                "role": "Resident Liaison Officer",
                "screen": "resident-choice",
            },
            {
                "key": "resident-service-issues",
                "role": "Resident Liaison Officer",
                "screen": "resident-service-issues",
            },
            {
                "key": "programme-queue",
                "role": "Retrofit Programme Manager",
                "screen": "programme-queue",
            },
            {
                "key": "procurement-packages",
                "role": "Retrofit Programme Manager",
                "screen": "procurement-packages",
            },
            {
                "key": "contractor-job-pack",
                "role": "Contractor",
                "screen": "contractor-job-pack",
            },
            {
                "key": "technical-queue",
                "role": "Retrofit Coordinator",
                "screen": "technical-queue",
            },
            {
                "key": "quality-queue",
                "role": "Quality Inspector",
                "screen": "quality-queue",
            },
            {
                "key": "finance-funding",
                "role": "Grants and Evidence Officer",
                "screen": "finance-funding",
            },
            {
                "key": "finance-invoices",
                "role": "Grants and Evidence Officer",
                "screen": "finance-invoices",
            },
        ],
    }
    done = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert done.returncode == 0, done.stderr
    parsed: dict[str, Any] = json.loads(done.stdout)
    return parsed


def _arm(
    prep: float,
    check: float,
    corr: float,
    coord: float,
    resident: float,
    support: float,
    counts: dict[str, int],
) -> dict[str, Any]:
    return {
        "effort": {
            "preparation": prep,
            "checking": check,
            "correction": corr,
            "coordination": coord,
            "resident_effort": resident,
            "support_cost": support,
        },
        "counts": counts,
    }


def _score(
    bundle_key: str,
    comparator_arm: dict[str, Any],
    workflow_arm: dict[str, Any],
    *,
    o16_owner: str | None = None,
) -> dict[str, Any]:
    run_payload: dict[str, Any] = {
        "bundle": bundle_key,
        "representative_data_retained": False,
        "cases": [
            {
                "case": HOME_ID,
                "arms": {"comparator": comparator_arm, "workflow": workflow_arm},
            }
        ],
    }
    if o16_owner is not None:
        run_payload["o16_counted_under"] = o16_owner
    out: dict[str, Any] = ltb.run_report(run_payload)
    return out


class LearningTestBundleRoleScreenScenarios(unittest.TestCase):
    rendered: ClassVar[dict[str, Any]]

    @classmethod
    def setUpClass(cls) -> None:
        cls.rendered = _render_all()

    def _screen_text(self, key: str) -> str:
        text: str = self.rendered["screens"][key]["text"]
        return text

    def test_bundle_1_story_once_and_promise_ownership_boundaries(self) -> None:
        choice_text = self._screen_text("resident-choice")
        issues_text = self._screen_text("resident-service-issues")
        programme_text = self._screen_text("programme-queue")
        receipt_text = str(self.rendered["aftercare"]["receiptText"])

        self.assertIn("Contact or access is never read as a yes.", choice_text)
        self.assertIn("Generic consent is not accepted.", choice_text)
        self.assertIn("Owner", choice_text)
        self.assertIn("SAFE-ROUTE-129", choice_text)
        self.assertIn("Representative reference", issues_text)
        self.assertIn("AUTH-LETTER-129", issues_text)
        self.assertIn("Chase owner (chases the receiver)", programme_text)
        self.assertIn("Resident-update owner (updates the resident)", programme_text)
        self.assertIn("Authority given", receipt_text)
        self.assertIn("Signed letter from the tenant", receipt_text)

        zero = {"authority_or_consent_breaches": 0, "promises_without_owner": 0}
        clean = _score(
            "story-once",
            _arm(10, 5, 4, 9, 6, 4, zero),
            _arm(5, 4, 2, 4, 2, 1, zero),
        )
        self.assertEqual(clean["bundle_title"], "Story once and promise ownership")
        self.assertEqual(clean["comparator_description"], "Manual re-asking and chase log")
        self.assertEqual(clean["direction"], "workflow lower")
        self.assertFalse(clean["stop"])

        blurred = _score(
            "story-once",
            _arm(10, 5, 4, 9, 6, 4, zero),
            _arm(
                4,
                3,
                1,
                3,
                2,
                1,
                {"authority_or_consent_breaches": 1, "promises_without_owner": 1},
            ),
        )
        self.assertTrue(blurred["stop"])
        self.assertEqual(
            blurred["breaches"],
            [
                f"{HOME_ID}/workflow/authority_or_consent_breaches",
                f"{HOME_ID}/workflow/promises_without_owner",
            ],
        )

    def test_bundle_2_pre_visit_pack_and_readiness_rehearsal_boundaries(self) -> None:
        packages_text = self._screen_text("procurement-packages")
        choice_text = self._screen_text("resident-choice")
        job_pack_text = self._screen_text("contractor-job-pack")

        self.assertIn(
            "Offered capacity is not a booking and not a promise to any resident.",
            packages_text,
        )
        self.assertIn("An offer is not a booking.", packages_text)
        self.assertIn(
            "A recorded choice, pause or withdrawal takes precedence over any offered contractor"
            " slot.",
            choice_text,
        )
        self.assertIn("Needs notice", job_pack_text)
        self.assertIn("The reason for any notice is not shared with contractors.", job_pack_text)
        self.assertIn("Submission is not acceptance.", job_pack_text)

        zero = {"offers_misread_as_commitments": 0}
        clean = _score(
            "pre-visit-pack",
            _arm(9, 5, 4, 7, 4, 3, zero),
            _arm(4, 4, 1, 3, 2, 1, zero),
        )
        self.assertEqual(clean["comparator_description"], "Current visit preparation")
        self.assertFalse(clean["stop"])
        self.assertEqual(clean["direction"], "workflow lower")

        misread = _score(
            "pre-visit-pack",
            _arm(9, 5, 4, 7, 4, 3, zero),
            _arm(4, 4, 1, 3, 2, 1, {"offers_misread_as_commitments": 1}),
        )
        self.assertTrue(misread["stop"])
        self.assertIn(f"{HOME_ID}/workflow/offers_misread_as_commitments", misread["breaches"])

    def test_bundle_3_change_impact_and_evidence_reuse_boundaries(self) -> None:
        technical_text = self._screen_text("technical-queue")
        funding_text = self._screen_text("finance-funding")

        self.assertIn("Action needed: Needs reassessment", technical_text)
        self.assertIn("Verified: Signed off on design version 1", technical_text)
        self.assertIn("Verified: Signed off on design version 2", technical_text)
        self.assertIn("Cannot confirm readiness", technical_text)
        self.assertIn("Proposals to check again", funding_text)
        self.assertIn("building_clearance_signoff (Stale source v1)", funding_text)
        self.assertIn("Approvals to review again", funding_text)
        self.assertIn("APR-DESIGN-V1 (fields building_clearance_signoff)", funding_text)

        zero = {"approvals_wrongly_carried_over": 0}
        clean = _score(
            "change-impact",
            _arm(8, 8, 5, 6, 2, 2, zero),
            _arm(4, 5, 1, 3, 1, 1, zero),
            o16_owner="change-impact",
        )
        self.assertEqual(clean["comparator_description"], "Manual dependency check")
        self.assertEqual(clean["o16_counted_under"], "change-impact")
        self.assertFalse(clean["stop"])

        carried_over = _score(
            "change-impact",
            _arm(8, 8, 5, 6, 2, 2, zero),
            _arm(4, 3, 1, 2, 1, 1, {"approvals_wrongly_carried_over": 1}),
            o16_owner="change-impact",
        )
        self.assertTrue(carried_over["stop"])
        self.assertIn(
            f"{HOME_ID}/workflow/approvals_wrongly_carried_over", carried_over["breaches"]
        )

    def test_bundle_4_accessible_handover_and_aftercare_keeps_open_remedies_visible(self) -> None:
        quality_text = self._screen_text("quality-queue")
        programme_text = self._screen_text("programme-queue")
        choice_screen = self.rendered["screens"]["resident-choice"]
        aftercare = self.rendered["aftercare"]

        self.assertIn("Open: awaiting a fix by the defect owner", quality_text)
        self.assertIn("Not ready: handover sign-off cannot be recorded", quality_text)
        self.assertIn("Open remedies are not closed by handover.", programme_text)
        self.assertGreaterEqual(len(choice_screen["jumpLinks"]), 4)
        self.assertIn(
            "Every state is written as words first: Confirmed, Waiting for resident or Action"
            " needed. Colour is never the only signal.",
            choice_screen["text"],
        )
        self.assertIn(
            "You can still raise it by phone, in person or on paper.",
            aftercare["receiptText"],
        )
        self.assertIn("Unresolved", aftercare["concernText"])
        self.assertIn(
            "Handover and financial closure are recorded separately. They do not change this"
            " concern, its outcome or its remedy.",
            aftercare["concernText"],
        )
        self.assertIn(
            "Unresolved concerns in homes with a handover or financial closure: 1.",
            aftercare["evaluatorText"],
        )

        zero = {"open_remedies_hidden": 0}
        workflow_lower = _score(
            "handover-aftercare",
            _arm(7, 5, 4, 6, 6, 4, zero),
            _arm(4, 4, 2, 3, 3, 2, zero),
        )
        self.assertEqual(workflow_lower["bundle_title"], "Accessible handover and aftercare")
        self.assertEqual(workflow_lower["comparator_description"], "Paper handover")
        self.assertEqual(workflow_lower["direction"], "workflow lower")
        self.assertFalse(workflow_lower["stop"])

        paper_lower = _score(
            "handover-aftercare",
            _arm(3, 3, 1, 2, 2, 1, zero),
            _arm(5, 4, 2, 4, 3, 2, zero),
        )
        self.assertEqual(paper_lower["direction"], "comparator lower or equal")
        self.assertFalse(paper_lower["stop"])

        hidden_remedy = _score(
            "handover-aftercare",
            _arm(7, 5, 4, 6, 6, 4, zero),
            _arm(4, 4, 2, 3, 3, 2, {"open_remedies_hidden": 1}),
        )
        self.assertTrue(hidden_remedy["stop"])
        self.assertIn(f"{HOME_ID}/workflow/open_remedies_hidden", hidden_remedy["breaches"])

    def test_bundle_5_review_ready_funding_evidence_and_o16_reconciliation(self) -> None:
        funding_text = self._screen_text("finance-funding")
        invoices_text = self._screen_text("finance-invoices")

        self.assertIn("Download Held draft (unreviewed)", funding_text)
        self.assertIn("Not submitted; eligibility Not assessed.", funding_text)
        self.assertIn("Submission, award and payment", funding_text)
        self.assertIn("Not recorded here. This screen never infers them.", funding_text)
        self.assertIn("No award is inferred from an invoice.", invoices_text)
        self.assertIn(
            "Finance decisions and invoice checks work the same when AI is unavailable.",
            invoices_text,
        )
        self.assertIn("No finance-defensible value is recorded.", invoices_text)

        zero_change = {"approvals_wrongly_carried_over": 0}
        zero_funding = {"inferred_submissions": 0}
        change_run = {
            "bundle": "change-impact",
            "o16_counted_under": "change-impact",
            "representative_data_retained": False,
            "cases": [
                {
                    "case": HOME_ID,
                    "arms": {
                        "comparator": _arm(8, 7, 4, 5, 2, 2, zero_change),
                        "workflow": _arm(4, 4, 1, 3, 1, 1, zero_change),
                    },
                }
            ],
        }
        funding_run = {
            "bundle": "funding-evidence",
            "o16_counted_under": "change-impact",
            "representative_data_retained": False,
            "cases": [
                {
                    "case": HOME_ID,
                    "arms": {
                        "comparator": _arm(11, 8, 5, 6, 1, 2, zero_funding),
                        "workflow": _arm(5, 5, 1, 3, 1, 1, zero_funding),
                    },
                }
            ],
        }
        owner: str | None = ltb.reconcile_o16([change_run, funding_run])
        self.assertEqual(owner, "change-impact")
        report: dict[str, Any] = ltb.run_report(funding_run)
        self.assertEqual(report["comparator_description"], "Manual evidence pack")
        self.assertIn("capacity", report["capacity_note"])
        self.assertFalse(report["stop"])

        inferred = _score(
            "funding-evidence",
            _arm(11, 8, 5, 6, 1, 2, zero_funding),
            _arm(5, 4, 1, 2, 1, 1, {"inferred_submissions": 1}),
            o16_owner="change-impact",
        )
        self.assertTrue(inferred["stop"])
        self.assertIn(f"{HOME_ID}/workflow/inferred_submissions", inferred["breaches"])

    def test_governance_gate_excludes_out_of_scope_and_unapproved_runner_wiring(self) -> None:
        self.assertEqual(set(ltb.OUT_OF_SCOPE), {"O10", "O18", "O19", "O20"})
        for bundle in ltb.BUNDLES.values():
            self.assertFalse(set(bundle.atlas_ids) & set(ltb.OUT_OF_SCOPE))

        registered_ids = list(self.rendered["screens"]["programme-queue"]["registeredIds"])
        self.assertGreaterEqual(len(registered_ids), 9)
        for screen_id in registered_ids:
            self.assertNotIn("learning", screen_id)
            self.assertNotIn("bundle", screen_id)

        server_source = SERVER.read_text(encoding="utf-8")
        self.assertNotIn("learning_test_bundles", server_source)
        self.assertNotIn("/api/learning", server_source)


if __name__ == "__main__":
    unittest.main()
