"""Synthetic aftercare screens render the returned contract (issue 133, Stage A).

All data is constructed synthetic text. The module is not wired into any route yet, so this
runs the file alone in a node vm with stubs. It is not a served-browser or keyboard check.
"""

import json
import subprocess
import unittest
from pathlib import Path
from typing import Any

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"

SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const src = fs.readFileSync(process.argv[1] + "/aftercare.js", "utf8");
const h = (tag, attrs, ...kids) => ({tag, attrs, kids: kids.flat(Infinity).filter(
  kid => kid !== false && kid !== null && kid !== undefined)});
const context = vm.createContext({Intl, h});
vm.runInContext(src, context);
const s = context.aftercareScreens;
const form = {title: "Raise a concern", intro: "Intro", owner_note: "No owner at intake.",
  synthetic_notice: "Synthetic demonstration.", manual_route: "Use paper.", protection: "Safe.",
  fields: [
    {name: "raised_by", label: "Who", required: true, options: [{value: "household", label: "H"}]},
    {name: "representative_basis", label: "Basis", required: false},
    {name: "home_ref", label: "Home", required: true},
    {name: "statement", label: "Statement", required: true}],
  staff_fields: [{name: "channel", label: "Channel", required: true,
    options: [{value: "phone", label: "By phone"}]},
    {name: "next_update", label: "Next", required: true}]};
const receipt = {receipt_id: "RC-AC-001", concern_id: "AC-001",
  received_at: "2026-11-09T10:00:00+00:00",
  recorded_by: {name: "<b>Sam</b>", role: "Resident Liaison Officer"}, channel: "phone",
  raised_by: "representative", home_ref: "HM-1", kind: "discomfort",
  original: {statement: "<img src=x onerror=alert(1)>", representative_basis: "Signed letter"},
  owner: {label: "Unknown (no owner named)", status: "unknown"}, next_update: "2026-11-20",
  what_happens_next: "Stays open.", accessible_route: "Phone route.", protection: "Safe.",
  synthetic_notice: "Synthetic."};
const concern = {id: "AC-001", kind: "discomfort", unresolved: true, overdue: false,
  owner: {label: "x", status: "unknown"}, investigation: "received", outcome: null,
  remedy: {status: "not_assessed"}, next_update: "2026-11-20", statement: "Cold",
  raised_by: "household", channel: "phone", closures: [{note: "Closure does not erase a remedy."}],
  sensor_note: "A normal reading does not dismiss a concern."};
const sufficient = {status: "sufficient", baseline: {temperature_c: 18.2},
  late: {temperature_c: 19.4}};
const view = {synthetic_notice: "Synthetic.", notice: "Neutral.", sensor_note: "Sensors.",
  totals: {homes_with_usable_comparison: {count: 1, denominator: 2}, concerns_raised: 1,
    concerns_unresolved: 1},
  rows: [{home_ref: "HM-1", comparison: sufficient, concerns: [{}], unresolved_count: 1},
    {home_ref: "HM-2", comparison: {status: "unknown"}, concerns: [], unresolved_count: 0}],
  unknowns: ["Evaluator role is Unknown."]};
const err = (status, extra = {}) => {
  const e = new Error("boom"); e.status = status; Object.assign(e, extra); return e;
};
(async () => {
  const out = {
    formClean: s.formView(form, {values: {raised_by: "household"}, requestId: "req-1"}),
    formRep: s.formView(form, {values: {raised_by: "representative"}}),
    formErr: s.formView(form, {errors: {home_ref: "Choose a home."}, values: {}}),
    receipt: s.receiptView(receipt), replay: s.receiptView(receipt, true),
    concern: s.concernView(concern), evaluator: s.evaluatorView(view),
    emptyEval: s.evaluatorView({...view, rows: [], unknowns: []}),
    ok: await s.submit(async () => ({receipt, replayed: false}), {home_ref: "HM-1"}, "req-1"),
    replayed: await s.submit(async () => ({receipt, replayed: true}), {}, "req-1"),
    invalid: await s.submit(async () => {
      throw err(400, {errors: {home_ref: "Bad"}});
    }, {}, "req-1"),
    denied: await s.submit(async () => { throw err(403); }, {}, "req-1"),
    network: await s.submit(async () => { throw new TypeError("Failed to fetch"); }, {}, "req-1"),
    server: await s.submit(async () => { throw err(503); }, {}, "req-1"),
    empty: await s.submit(async () => null, {}, "req-1"),
  };
  console.log(JSON.stringify(out));
})();
"""


def run() -> dict[str, Any]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB)], capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, result.stderr
    parsed: dict[str, Any] = json.loads(result.stdout)
    return parsed


def walk(node: object) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(node, dict):
        found.append(node)
        for kid in node.get("kids", []):
            found += walk(kid)
    return found


class AftercareScreens(unittest.TestCase):
    out: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.out = run()

    def text(self, key: str) -> str:
        return json.dumps(self.out[key])

    def test_form_uses_native_labelled_controls_and_no_owner_field(self) -> None:
        nodes = walk(self.out["formClean"])
        labels = {n["attrs"].get("for") for n in nodes if n["tag"] == "label"}
        controls = {
            n["attrs"].get("id") for n in nodes if n["tag"] in ("input", "select", "textarea")
        }
        self.assertTrue(controls and controls <= labels)
        self.assertNotIn("ac-owner_role", controls)
        self.assertIn("ac-channel", controls)
        self.assertIn("req-1", self.text("formClean"))

    def test_representative_basis_only_when_representative(self) -> None:
        self.assertNotIn("ac-representative_basis", self.text("formClean"))
        self.assertIn("ac-representative_basis", self.text("formRep"))

    def test_errors_are_summarised_for_focus_and_shown_inline(self) -> None:
        nodes = walk(self.out["formErr"])
        summary = [n for n in nodes if n["attrs"].get("id") == "ac-error-summary"]
        self.assertEqual(summary[0]["attrs"]["tabindex"], "-1")
        self.assertIn("Problem: Choose a home.", self.text("formErr"))
        self.assertIn("#ac-home_ref", self.text("formErr"))
        self.assertNotIn("ac-error-summary", self.text("formClean"))

    def test_receipt_shows_original_and_unknown_owner_as_text(self) -> None:
        text = self.text("receipt")
        for phrase in ("RC-AC-001", "Signed letter", "Unknown. No owner is named yet."):
            self.assertIn(phrase, text)
        self.assertIn("Saved. Keep this receipt reference.", text)
        self.assertIn("No second record was made.", self.text("replay"))

    def test_user_text_is_data_not_markup(self) -> None:
        self.assertIn("<img src=x onerror=alert(1)>", self.text("receipt"))
        for key in ("receipt", "concern", "evaluator"):
            for node in walk(self.out[key]):
                self.assertNotIn("onerror", node["attrs"] or {})
                self.assertNotEqual(node["tag"], "img")

    def test_concern_view_states_text_status_and_no_sensor_dismissal(self) -> None:
        text = self.text("concern")
        for phrase in ("Unresolved", "No outcome yet", "Not assessed yet", "does not dismiss"):
            self.assertIn(phrase, text)
        self.assertIn("does not erase a remedy", text)

    def test_evaluator_view_states_denominator_unknowns_and_caption(self) -> None:
        text = self.text("evaluator")
        for phrase in ("1 of 2 homes", "Evaluator role is Unknown.", "18.2 \\u00b0C"):
            self.assertIn(phrase, text)
        nodes = walk(self.out["evaluator"])
        self.assertTrue(any(n["tag"] == "caption" for n in nodes))
        self.assertTrue(any(n["attrs"].get("scope") == "row" for n in nodes if n["tag"] == "th"))
        self.assertEqual(text.count('"Unknown"'), 3)
        for banned in ("caused", "saved", "fault", "blame"):
            self.assertNotIn(banned, text.lower().replace("savings", ""))

    def test_empty_evaluator_cohort_is_stated(self) -> None:
        self.assertIn("No homes are in the synthetic cohort.", self.text("emptyEval"))

    def test_submit_outcomes_and_request_id_retention(self) -> None:
        self.assertTrue(self.out["ok"]["ok"])
        self.assertTrue(self.out["replayed"]["replay"])
        self.assertEqual(self.out["invalid"]["errors"], {"home_ref": "Bad"})
        self.assertFalse(self.out["invalid"]["retainRequestId"])
        self.assertFalse(self.out["denied"]["retainRequestId"])
        for key in ("network", "server", "empty"):
            self.assertFalse(self.out[key]["ok"], key)
            self.assertTrue(self.out[key]["retainRequestId"], key)
            self.assertIn("Nothing was saved", self.out[key]["message"], key)


if __name__ == "__main__":
    unittest.main()
