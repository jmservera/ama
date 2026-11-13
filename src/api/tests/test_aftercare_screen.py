"""Synthetic aftercare screens render the returned contract (issue 133, Stage A).

Real service payloads are produced here by AftercareService over a temporary synthetic store and
passed to node, beside hand-built adversarial cases. The module is not wired into any route yet,
so this runs the file alone in a node vm with stubs. It is not a served-browser or keyboard check.
"""

import json
import re
import subprocess
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from zava_forward.core import aftercare_intake as ai
from zava_forward.core.aftercare import neutral_text
from zava_forward.core.synthetic import sensor_scenarios as ss

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"

SCRIPT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const src = fs.readFileSync(process.argv[1] + "/aftercare.js", "utf8");
const real = JSON.parse(fs.readFileSync(0, "utf8"));
const h = (tag, attrs, ...kids) => ({tag, attrs, kids: kids.flat(Infinity).filter(
  kid => kid !== false && kid !== null && kid !== undefined)});
const context = vm.createContext({Intl, h});
vm.runInContext(src, context);
const s = context.aftercareScreens;
const err = (status, extra = {}) => {
  const e = new Error("boom"); e.status = status; Object.assign(e, extra); return e;
};
const fraction = (unresolved) => ({...real.evaluator, totals: {...real.evaluator.totals,
  concerns_unresolved: unresolved}});
const RID = real.receipt.request_id;
const send = (api, opts) => s.submit(api, {home_ref: "HM-1"}, RID, undefined, opts);
const fail = (e, opts) => send(async () => { throw e; }, opts);
const adversarial = {...real.receipt, original: {statement: "<img src=x onerror=alert(1)>",
  representative_basis: "Signed letter"}, recorded_by: {name: "<b>Sam</b>", role: "Liaison"}};
(async () => {
  const out = {
    formClean: s.formView(real.form, {values: {raised_by: "household"}, requestId: "req-1"}),
    formRep: s.formView(real.form, {values: {raised_by: "representative"}}),
    formErr: s.formView(real.form, {errors: {home_ref: "Choose a home."}, values: {}}),
    receipt: s.receiptView(real.receipt), replay: s.receiptView(real.receipt, true),
    adversarial: s.receiptView(adversarial),
    concern: s.concernView(real.concern), evaluator: s.evaluatorView(real.evaluator),
    emptyEval: s.evaluatorView(real.evaluatorEmpty),
    fracZero: s.evaluatorView(fraction({count: 0, denominator: 0})),
    fracNull: s.evaluatorView(fraction({count: 1, denominator: null})),
    fracScalar: s.evaluatorView(fraction(1)),
    fracMissing: s.evaluatorView(fraction(undefined)),
    fracOver: s.evaluatorView(fraction({count: 3, denominator: 2})),
    outcomesMixed: s.evaluatorView({...real.evaluator, rows: [
      {home_ref: "HM-A", comparison: {}, unresolved_count: 0, concerns: [
        {outcome: "advice_given"}, {outcome: "advice_given"}, {outcome: "no_outcome_yet"},
        {}, {outcome: "mystery_code"}]},
      {home_ref: "HM-B", comparison: {}, unresolved_count: 0, concerns: []}]}),
    saved: await send(async () => ({receipt: real.receipt, replayed: false})),
    replayed: await send(async () => ({receipt: real.receipt, replayed: true})),
    invalid: await fail(err(400, {errors: {home_ref: "Bad"}})),
    invalidNoMap: await fail(err(400)),
    denied: await fail(err(403)),
    signedOut: await fail(err(401)),
    conflict: await fail(err(409)),
    network: await fail(new TypeError("Failed to fetch")),
    server503: await fail(err(503)),
    server500: await fail(err(500)),
    empty: await send(async () => null),
    emptyObject: await send(async () => ({receipt: {}})),
    arrayReceipt: await send(async () => ({receipt: []})),
    mismatched: await send(async () => ({receipt: {...real.receipt, request_id: "other-0001"}})),
    refusedAfterUnconfirmed: await fail(err(400, {errors: {home_ref: "Bad"}}), {unresolved: true}),
    deniedAfterUnconfirmed: await fail(err(403), {unresolved: true}),
    savedAfterUnconfirmed: await send(async () => ({receipt: real.receipt, replayed: true}),
      {unresolved: true}),
  };
  console.log(JSON.stringify(out));
})();
"""

NOW = datetime(2026, 11, 9, 12, 0, tzinfo=UTC)
LIAISON = {"name": "Synthetic Liaison", "role": "Resident Liaison Officer"}
MANAGER = {"name": "Synthetic Manager", "role": "Retrofit Programme Manager"}


def real_payloads() -> dict[str, Any]:
    homes = [str(s["rows"][0]["home_id"]) for s in ss.retrofit_exercise_scenarios()]
    with tempfile.TemporaryDirectory() as tmp:
        svc = ai.AftercareService(
            ai.FileStateStore(Path(tmp) / "a.json"), homes=homes, now=lambda: NOW
        )
        empty = svc.evaluator_view(MANAGER)
        receipt, _ = svc.record_concern(
            LIAISON,
            {
                "request_id": "req-0000001",
                "raised_by": "representative",
                "representative_basis": "Signed letter from the tenant",
                "home_ref": homes[0],
                "kind": "discomfort",
                "statement": "The living room stays cold in the evening.",
                "channel": "phone",
                "next_update": "2026-11-20",
            },
        )
        return {
            "form": svc.form(LIAISON),
            "receipt": receipt,
            "concern": svc.concern(MANAGER, "AC-001"),
            "evaluator": svc.evaluator_view(MANAGER),
            "evaluatorEmpty": empty,
        }


def run() -> dict[str, Any]:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB)],
        input=json.dumps(real_payloads()),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    parsed: dict[str, Any] = json.loads(result.stdout)
    return parsed


JARGON = re.compile(r"\b(gates?|holds?|provenance|traces?|snapshots?|envelopes?)\b", re.I)
LITERAL = re.compile(r"""(["'`])((?:\\.|(?!\1)[^\\\n])*)\1""")


def static_strings(source: str) -> list[str]:
    source = re.sub(r"^\s*//.*$", "", source, flags=re.M)
    found = [re.sub(r"\$\{[^}]*\}", "", m.group(2)) for m in LITERAL.finditer(source)]
    return [t for t in found if re.search(r"[A-Za-z]{3}", t)]


def walk(node: object) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if isinstance(node, dict):
        found.append(node)
        for kid in node.get("kids", []):
            found += walk(kid)
    return found


def visible(node: object) -> str:
    return " ".join(kid for n in walk(node) for kid in n.get("kids", []) if isinstance(kid, str))


class AftercareScreens(unittest.TestCase):
    out: dict[str, Any]

    @classmethod
    def setUpClass(cls) -> None:
        cls.out = run()

    def text(self, key: str) -> str:
        return visible(self.out[key])

    def test_form_uses_native_labelled_controls_and_no_owner_field(self) -> None:
        nodes = walk(self.out["formClean"])
        labels = {n["attrs"].get("for") for n in nodes if n["tag"] == "label"}
        ids = ("input", "select", "textarea")
        controls = {n["attrs"].get("id") for n in nodes if n["tag"] in ids}
        self.assertTrue(controls and controls <= labels)
        self.assertNotIn("ac-owner_role", controls)
        self.assertIn("ac-channel", controls)
        self.assertIn("req-1", json.dumps(self.out["formClean"]))

    def test_representative_basis_only_when_representative(self) -> None:
        self.assertNotIn("ac-representative_basis", json.dumps(self.out["formClean"]))
        self.assertIn("ac-representative_basis", json.dumps(self.out["formRep"]))

    def test_errors_are_summarised_for_focus_and_shown_inline(self) -> None:
        nodes = walk(self.out["formErr"])
        summary = [n for n in nodes if n["attrs"].get("id") == "ac-error-summary"]
        self.assertEqual(summary[0]["attrs"]["tabindex"], "-1")
        self.assertIn("Problem: Choose a home.", self.text("formErr"))
        self.assertIn("#ac-home_ref", json.dumps(self.out["formErr"]))
        self.assertNotIn("ac-error-summary", json.dumps(self.out["formClean"]))

    def test_receipt_from_the_service_shows_original_and_unknown_owner_as_text(self) -> None:
        text = self.text("receipt")
        for phrase in ("Signed letter from the tenant", "No owner is named yet"):
            self.assertIn(phrase, text)
        self.assertIn("Saved. Keep this receipt reference.", text)
        self.assertIn("No second record was made.", self.text("replay"))
        self.assertNotIn("[object Object]", text)

    def test_user_text_is_data_not_markup(self) -> None:
        self.assertIn("<img src=x onerror=alert(1)>", self.text("adversarial"))
        for key in ("receipt", "adversarial", "concern", "evaluator"):
            for node in walk(self.out[key]):
                self.assertNotIn("onerror", node["attrs"] or {})
                self.assertNotEqual(node["tag"], "img")

    def test_concern_view_states_text_status_and_no_sensor_dismissal(self) -> None:
        text = self.text("concern")
        self.assertIn("Unresolved", text)
        self.assertNotIn("[object Object]", text)

    def test_evaluator_view_from_the_service_states_fraction_and_unknowns(self) -> None:
        text = self.text("evaluator")
        self.assertIn("1 of 1 concerns unresolved", text)
        self.assertNotIn("[object Object]", text)
        self.assertNotIn("undefined", text)
        nodes = walk(self.out["evaluator"])
        self.assertTrue(any(n["tag"] == "caption" for n in nodes))
        self.assertIn("do not show what caused a concern", text)
        self.assertNotIn("blame", text.lower())

    def test_unresolved_fraction_zero_unknown_and_malformed_denominators(self) -> None:
        zero = "0 of 0 concerns unresolved. No proportion is stated"
        self.assertIn(zero, self.text("emptyEval"))
        self.assertIn(zero, self.text("fracZero"))
        for key in ("fracNull", "fracScalar", "fracMissing", "fracOver"):
            with self.subTest(key=key):
                text = self.text(key)
                self.assertIn("Unresolved concerns: Unknown", text)
                self.assertNotIn("[object Object]", text)

    def test_evaluator_rows_show_recorded_outcome_counts_in_plain_words(self) -> None:
        text = self.text("outcomesMixed")
        self.assertIn("Advice given: 2; No outcome yet: 2; Unknown: 1", text)
        self.assertIn("No concerns raised", text)
        self.assertNotIn("mystery_code", text)
        self.assertNotIn("undefined", text)
        self.assertIn("No outcome yet: 1", self.text("evaluator"))

    def test_static_web_strings_pass_the_neutral_text_guard(self) -> None:
        literals = static_strings((WEB / "aftercare.js").read_text(encoding="utf-8"))
        self.assertGreater(len(literals), 50)
        for text in literals:
            with self.subTest(text=text):
                neutral_text(text)
                self.assertIsNone(JARGON.search(text))
        self.assertEqual(
            static_strings("a('Hold it'); b(\"Hold\"); `Cut ${y} bills`"),
            ["Hold it", "Hold", "Cut  bills"],
        )
        for jargon in ("Hold the line", "hold", "A snapshot"):
            self.assertIsNotNone(JARGON.search(jargon))
        for bad in ("You'll save money", "Cut your bills"):
            with self.assertRaises(ValueError):
                neutral_text(bad)

    def test_evaluator_table_is_named_scoped_and_scrolls_inside_a_region(self) -> None:
        nodes = walk(self.out["evaluator"])
        tables = [n for n in nodes if n["tag"] == "table"]
        self.assertEqual(len(tables), 1)
        table = tables[0]
        caption = table["kids"][0]
        self.assertEqual(caption["tag"], "caption")
        name = caption["kids"][0]
        wrappers = [n for n in nodes if table in n.get("kids", []) and n["tag"] == "div"]
        self.assertEqual(len(wrappers), 1)
        attrs = wrappers[0]["attrs"]
        self.assertEqual(attrs["class"], "table-scroll")
        self.assertEqual((attrs["role"], attrs["tabindex"]), ("region", "0"))
        self.assertTrue(name and attrs["aria-label"] == name)
        cells = walk(table)
        self.assertTrue(all(n["attrs"].get("scope") for n in cells if n["tag"] == "th"))
        columns = [n for n in cells if n["tag"] == "th" and n["attrs"]["scope"] == "col"]
        self.assertEqual(len(columns), 7)
        self.assertIn("Outcomes", [visible(c) for c in columns])
        rows = [n for n in cells if n["tag"] == "th" and n["attrs"]["scope"] == "row"]
        self.assertEqual(len(rows), len(real_payloads()["evaluator"]["rows"]))

    def test_saved_and_replayed_outcomes_clear_uncertainty(self) -> None:
        self.assertEqual(self.out["saved"]["outcome"], "saved")
        self.assertEqual(self.out["replayed"]["outcome"], "replayed")
        self.assertTrue(self.out["replayed"]["replay"])
        for key in ("saved", "replayed", "savedAfterUnconfirmed"):
            self.assertFalse(self.out[key]["unresolved"], key)

    def test_unknown_outcomes_never_claim_nothing_was_saved_and_keep_the_request_id(self) -> None:
        keys = (
            "network", "server503", "server500", "empty", "emptyObject", "arrayReceipt",
            "mismatched", "conflict",
        )  # fmt: skip
        for key in keys:
            with self.subTest(key=key):
                result = self.out[key]
                self.assertFalse(result["ok"])
                self.assertTrue(result["retainRequestId"])
                self.assertTrue(result["unresolved"])
                self.assertNotIn("nothing was saved", result["message"].lower())
                self.assertIn("may or may not have been saved", result["message"])
                self.assertIn("same details", result["message"])
                self.assertIn("Check the concerns list", result["message"])
        self.assertEqual(self.out["conflict"]["outcome"], "conflict")
        self.assertEqual(self.out["network"]["outcome"], "unconfirmed")

    def test_definite_refusals_are_separate_and_without_the_unconfirmed_text(self) -> None:
        self.assertEqual(self.out["invalid"]["outcome"], "refused")
        self.assertEqual(self.out["invalid"]["errors"], {"home_ref": "Bad"})
        self.assertEqual(self.out["invalidNoMap"]["errors"], {})
        self.assertTrue(self.out["invalidNoMap"]["message"])
        for key in ("invalid", "invalidNoMap", "denied"):
            with self.subTest(key=key):
                self.assertFalse(self.out[key]["retainRequestId"])
                self.assertFalse(self.out[key]["unresolved"])
                self.assertNotIn("may or may not", self.out[key]["message"])
        self.assertTrue(self.out["signedOut"]["retainRequestId"])
        self.assertIn("Sign in again", self.out["signedOut"]["message"])

    def test_a_refusal_after_an_unconfirmed_attempt_keeps_the_uncertainty(self) -> None:
        for key in ("refusedAfterUnconfirmed", "deniedAfterUnconfirmed"):
            with self.subTest(key=key):
                result = self.out[key]
                self.assertTrue(result["retainRequestId"])
                self.assertTrue(result["unresolved"])
                self.assertIn("earlier attempt may have been saved", result["message"])
                self.assertIn("original details", result["message"])


if __name__ == "__main__":
    unittest.main()
