"""Resident choice screen separates choice, pause, access and commitment and offers no controls."""

import json
import subprocess
import unittest
from collections.abc import Mapping
from pathlib import Path

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"

SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const host = fs.readFileSync(process.argv[1] + "/role-screens.js", "utf8");
const context = vm.createContext({
  URLSearchParams, Intl, AbortController, Date,
  routeController: new AbortController(), me: {user: {role: "Resident Liaison Officer"}},
  h: (tag, attrs, ...kids) => ({tag, attrs, kids: kids.flat(Infinity).filter(
    kid => kid !== false && kid !== null && kid !== undefined)})
});
vm.runInContext(host + "\n;globalThis.__s = roleScreens.get('resident-choice');", context);
const c = JSON.parse(process.argv[2]);
console.log(JSON.stringify({roles: context.__s.roles, tree: context.__s.render(c)}));
"""

CASE = {
    "id": "C-1",
    "measure_decisions": [
        {
            "measure": "Loft insulation",
            "status": "Paused",
            "readiness": "Needs human review",
            "context": {"scope": "S-9", "revision": 2, "design_version": 3},
            "versions": [
                {
                    "version": 1,
                    "status": "Accepted",
                    "answered_by": "The resident",
                    "scope": "S-8",
                    "context_revision": 1,
                    "design_version": 2,
                },
                {
                    "version": 2,
                    "status": "Paused",
                    "answered_by": "The resident",
                    "scope": "S-9",
                    "context_revision": 2,
                    "design_version": 3,
                    "note": "Not before spring",
                },
            ],
        },
        {
            "measure": "Solar PV",
            "status": "Not recorded",
            "readiness": "Resident decision current",
            "versions": [],
        },
    ],
    "resident_update": {
        "status": "Outstanding",
        "purpose": "Explain damp query",
        "owner_identity": {"name": "Owner One"},
        "due_at": "2026-12-01T10:00:00+00:00",
        "basis": "Resident asked",
        "safe_contact_ref": "SC-77",
        "version": 2,
    },
    "service_requests": [
        {
            "id": "SR-1",
            "route": "Repair",
            "status": "Open",
            "accessibility": ["Phone only"],
            "next_update": "2026-12-02",
        }
    ],
}


QUEUE_SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const host = fs.readFileSync(process.argv[1] + "/role-screens.js", "utf8");
const queue = JSON.parse(process.argv[2]);
const urls = [];
const context = vm.createContext({
  URLSearchParams, Intl, AbortController, Date,
  routeController: new AbortController(), me: {user: {role: "Resident Liaison Officer"}},
  api: async (url) => {
    urls.push(url);
    if (queue === null) throw new Error("denied");
    return queue;
  },
  h: (tag, attrs, ...kids) => ({tag, attrs, kids: kids.flat(Infinity).filter(
    kid => kid !== false && kid !== null && kid !== undefined)})
});
vm.runInContext(host + "\n;globalThis.__s = roleScreens.get('resident-choice');", context);
context.__s.overview(new AbortController().signal)
  .then(tree => console.log(JSON.stringify({tree, urls})));
"""


def run_queue(queue: object) -> dict[str, object]:
    result = subprocess.run(
        ["node", "-e", QUEUE_SCRIPT, str(WEB), json.dumps(queue)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    parsed: dict[str, object] = json.loads(result.stdout)
    return parsed


def page(*items: object, total: int | None = None) -> dict[str, object]:
    rows = [{"address": "1 Test Road", "town": "Testville", **dict(i)} for i in items]  # type: ignore[call-overload]
    return {"items": rows, "total": len(items) if total is None else total}


def run(case: Mapping[str, object]) -> dict[str, object]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB), json.dumps(case)],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    parsed: dict[str, object] = json.loads(result.stdout)
    return parsed


def tags(node: object) -> list[str]:
    found: list[str] = []
    if isinstance(node, dict):
        found.append(node.get("tag", ""))
        for kid in node.get("kids", []):
            found += tags(kid)
    return found


class ResidentChoiceScreen(unittest.TestCase):
    def test_choice_pause_commitment_and_access_are_distinct(self) -> None:
        out = run(CASE)
        text = json.dumps(out["tree"])
        self.assertIn("Resident Liaison Officer", json.dumps(out["roles"]))
        self.assertNotIn("Resident Simulator", json.dumps(out["roles"]))
        for expected in (
            "Loft insulation",
            "scope S-9, revision 2, design 3",
            "v2 Paused (scope S-9, revision 2, design 3)",
            "Not before spring",
            "Not recorded",
            "Paused or withdrawn by the resident",
            "Human review before any restart",
            "Explain damp query",
            "Owner One",
            "SC-77",
            "Safe route reference",
            "Phone only",
            "Service requests and access needs (separate from choice)",
            "not a contact attempt",
        ):
            self.assertIn(expected, text)

    def test_stale_stop_with_unresolved_review_stays_visible_with_original_scope(self) -> None:
        case = {
            "id": "C-3",
            "measure_decisions": [
                {
                    "measure": "Solar PV",
                    "status": "Not recorded",
                    "readiness": "Needs human review",
                    "context": {"scope": "S-10", "revision": 3, "design_version": 4},
                    "review": {"status": "Needs human review", "decision_version": 1},
                    "versions": [
                        {
                            "version": 1,
                            "status": "Withdrawn",
                            "answered_by": "The resident",
                            "scope": "S-9",
                            "context_revision": 2,
                            "design_version": 3,
                            "note": "Changed my mind",
                        }
                    ],
                }
            ],
        }
        text = json.dumps(run(case)["tree"])
        self.assertNotIn("No measure is currently paused or withdrawn", text)
        self.assertIn(
            "Withdrawn (current answer Not recorded), scope S-9, revision 2, design 3", text
        )
        self.assertIn("Changed my mind", text)

    def test_stop_followed_by_waiting_keeps_stopped_answer_scope_and_note(self) -> None:
        case = {
            "id": "C-4",
            "measure_decisions": [
                {
                    "measure": "Solar PV",
                    "status": "Waiting",
                    "readiness": "Needs human review",
                    "context": {"scope": "S-11", "revision": 4, "design_version": 5},
                    "review": {"status": "Needs human review", "decision_version": 1},
                    "versions": [
                        {
                            "version": 1,
                            "status": "Paused",
                            "answered_by": "The resident",
                            "scope": "S-9",
                            "context_revision": 2,
                            "design_version": 3,
                            "note": "Not before spring",
                        },
                        {
                            "version": 2,
                            "status": "Waiting",
                            "answered_by": "The resident",
                            "scope": "S-11",
                            "context_revision": 4,
                            "design_version": 5,
                            "note": "Still thinking",
                        },
                    ],
                }
            ],
        }
        text = json.dumps(run(case)["tree"])
        self.assertNotIn("No measure is currently paused or withdrawn", text)
        self.assertIn("Paused (current answer Waiting), scope S-9, revision 2, design 3", text)
        self.assertIn("Not before spring", text)

    def test_queue_shows_stop_state_scope_and_review_for_stale_and_waiting(self) -> None:
        stale = {
            "id": "C-3",
            "measure_decisions": [
                {
                    "measure": "Solar PV",
                    "status": "Not recorded",
                    "readiness": "Needs human review",
                    "review": {"status": "Needs human review", "decision_version": 1},
                    "versions": [
                        {
                            "version": 1,
                            "status": "Withdrawn",
                            "scope": "S-9",
                            "context_revision": 2,
                            "design_version": 3,
                        }
                    ],
                }
            ],
        }
        waiting = {
            "id": "C-4",
            "measure_decisions": [
                {
                    "measure": "Solar PV",
                    "status": "Waiting",
                    "readiness": "Needs human review",
                    "review": {"status": "Needs human review", "decision_version": 1},
                    "versions": [
                        {
                            "version": 1,
                            "status": "Paused",
                            "scope": "S-9",
                            "context_revision": 2,
                            "design_version": 3,
                        },
                        {
                            "version": 2,
                            "status": "Waiting",
                            "scope": "S-11",
                            "context_revision": 4,
                            "design_version": 5,
                        },
                    ],
                }
            ],
        }
        stale_text = json.dumps(run_queue(page(stale))["tree"])
        waiting_text = json.dumps(run_queue(page(waiting))["tree"])
        self.assertIn(
            "Solar PV: current Not recorded; latest recorded v1 Withdrawn (scope S-9", stale_text
        )
        self.assertIn(
            "Solar PV: Withdrawn (current answer Not recorded) "
            "(v1, scope S-9, revision 2, design 3), needs human review",
            stale_text,
        )
        self.assertIn(
            "Solar PV: Paused (current answer Waiting) "
            "(v1, scope S-9, revision 2, design 3), needs human review",
            waiting_text,
        )

    def test_no_controls_and_no_contact(self) -> None:
        tree = run(CASE)["tree"]
        for control in ("button", "form", "input", "select", "textarea"):
            self.assertNotIn(control, tags(tree))
        self.assertIn("No message, call or letter is sent", json.dumps(tree))

    def test_empty_case_stays_unknown(self) -> None:
        text = json.dumps(run({"id": "C-2"})["tree"])
        self.assertIn("No records supplied", text)
        self.assertIn("No measure is currently paused or withdrawn", text)
        self.assertIn("No update commitment is recorded", text)

    def test_queue_summary_is_read_only_and_names_scope(self) -> None:
        result = run_queue(page(CASE, {"id": "C-2"}, total=7))
        tree = result["tree"]
        text = json.dumps(tree)
        self.assertEqual(result["urls"], ["/api/resident/choice-queue?limit=100&offset=0"])
        for expected in (
            "Choice and update commitments across open homes (portfolio scope, not this home)",
            "C-1, 1 Test Road, Testville",
            "Shows 2 of 7 open homes",
            "Loft insulation: current Paused; latest recorded v2 Paused "
            "(scope S-9, revision 2, design 3)",
            "Solar PV: current Not recorded",
            "Explain damp query",
            "Owner One",
            "SC-77",
            "No measure choices recorded",
            "No commitment recorded",
        ):
            self.assertIn(expected, text)
        for control in ("button", "form", "input", "select", "textarea", "a"):
            self.assertNotIn(control, tags(tree))

    def test_queue_failure_is_unknown_not_empty(self) -> None:
        text = json.dumps(run_queue(None)["tree"])
        self.assertIn("The cross-home queue could not be loaded.", text)
        self.assertNotIn("No measure choices recorded", text)


if __name__ == "__main__":
    unittest.main()
