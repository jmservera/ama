"""The Resident tab nomination section is read only and shows unknowns honestly (#130)."""

import json
import subprocess
import unittest
from pathlib import Path
from typing import Any

WEB = Path(__file__).resolve().parents[1] / "src/zava_forward/api/web"

SCRIPT = r"""
const fs = require("node:fs");
const src = fs.readFileSync(process.argv[1] + "/panels.js", "utf8");
const start = src.indexOf("function nominationPanel");
const end = src.indexOf("\nfunction affectedChallengePanel");
const c = JSON.parse(process.argv[2]);
const h = (tag, attrs, ...kids) => ({tag, attrs: attrs || {}, kids: kids.flat(Infinity)
  .filter((k) => k !== null && k !== undefined && k !== false)});
const text = (n) => typeof n === "string" ? n : n.tag === "dt" ? n.kids.map(text).join("") + ": "
  : n.kids.map(text).join(n.tag === "dl" || n.tag === "section" || n.tag === "details" ? "\n" : "");
const tags = (n, out) => {
  if (typeof n !== "string") { out.push(n.tag); n.kids.forEach((k) => tags(k, out)); }
  return out;
};
const inputs = ["button", "input", "form", "textarea", "select", "a"];
eval(src.slice(start, end) + "\nglobalThis.__panel = nominationPanel(c);");
const p = globalThis.__panel;
console.log(JSON.stringify(p === null ? null : {text: text(p), tags: tags(p, []),
  controls: tags(p, []).filter((t) => inputs.includes(t))}));
"""

IDENT = dict(name="Sam Officer", role="Resident Liaison Officer")


def render(case: dict[str, Any]) -> dict[str, Any] | None:
    result = subprocess.run(
        ["node", "-e", SCRIPT, str(WEB), json.dumps(case)],
        text=True,
        capture_output=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)  # type: ignore[no-any-return]


def record(**changes: Any) -> dict[str, Any]:
    base: dict[str, Any] = dict(
        id="NOM-1",
        version=1,
        kind="Self-referral",
        original=dict(
            reported_subject_ref="SYN-UNVERIFIED",
            account="SYN original account <b>bold</b>",
            source="SYN source",
            channel="Phone",
            recorded_by=IDENT,
            at="2026-11-01T10:00:00+00:00",
        ),
        identity_status="Unknown",
        support_needs="Unknown",
        risk_flags="Unknown",
        owner=IDENT,
        acknowledgement=dict(
            reference="SYN ack", delivery="Not verified by this system", recorded_by=IDENT
        ),
        next_update="2000-01-01",
        non_digital_route="SYN office route",
        review_status="Human identity and eligibility review required",
        corrections=[],
        follow_up=dict(
            route_ready=True,
            missing=[],
            next_update_overdue=True,
            re_review_pending=False,
            review_current=False,
            review_owner="Human identity and eligibility review; policy owner not yet appointed",
            not_inferred=["priority change", "eligibility"],
        ),
    )
    return dict(base, **changes)


REVIEW = dict(
    record_version=1,
    outcome="Accepted for human eligibility review",
    rationale="SYN reasons",
    evidence_ref="SYN evidence",
    competing_evidence_versions=[],
    reviewer=dict(name="Rex Reviewer", role="Retrofit Coordinator"),
    at="2026-11-02T10:00:00+00:00",
)


class NominationScreen(unittest.TestCase):
    def shown(self, *records: dict[str, Any]) -> dict[str, Any]:
        out = render(dict(id="ZF-1", challenge_targets=[], nomination_records=list(records)))
        assert out is not None
        self.assertEqual(out["controls"], [])
        return out

    def test_original_correction_and_stale_review_are_kept_apart(self) -> None:
        correction = dict(
            version=2,
            reported_subject_ref="SYN-CORRECTED",
            account="SYN competing account",
            source="SYN correction source",
            channel="Letter",
            recorded_by=IDENT,
            at="2026-11-03T10:00:00+00:00",
        )
        stale = dict(REVIEW, stale_from_version=2)
        follow = dict(record()["follow_up"], re_review_pending=True, next_update_overdue=False)
        out = self.shown(
            record(version=2, corrections=[correction], reviews=[stale], follow_up=follow)
        )
        text = out["text"]
        self.assertIn("Original supplied account", text)
        self.assertIn("SYN original account <b>bold</b>", text)
        self.assertIn(
            "Corrected account, version 2 (competing evidence; the original is kept)", text
        )
        self.assertIn("SYN competing account", text)
        self.assertIn("Stale: recorded for version 1; the record changed at version 2", text)
        self.assertIn("Correction awaiting human re-review.", text)
        self.assertIn("Accepted for human eligibility review", text)
        self.assertIn("not an approval or an eligibility decision", text)
        self.assertIn("Delivery unverified", text)
        self.assertIn("Not overdue", text)
        self.assertNotIn("Current for version", text)
        self.assertNotIn("b", out["tags"])

    def test_current_review_and_overdue_follow_up(self) -> None:
        text = self.shown(record(reviews=[REVIEW]))["text"]
        self.assertIn("Current for version 1", text)
        self.assertIn("Overdue", text)
        self.assertIn("Sam Officer (Resident Liaison Officer)", text)
        self.assertIn("Rex Reviewer (Retrofit Coordinator)", text)

    def test_legacy_missing_fields_stay_not_recorded_or_unknown(self) -> None:
        legacy = dict(id="NOM-OLD", version=1, original=dict(account="SYN old"))
        text = self.shown(legacy)["text"]
        self.assertIn("Not recorded. Delivery unverified.", text)
        self.assertIn("No human review recorded.", text)
        self.assertIn("Named owner: Unknown", text)
        self.assertIn("Support needs: Unknown", text)
        self.assertIn("Risk flags: Unknown", text)
        self.assertIn("Missing from this record: Unknown", text)
        self.assertNotIn(": None", text)
        self.assertNotIn("undefined", text)
        self.assertNotIn("null", text)

    def test_missing_items_and_unknown_values_are_not_turned_into_none(self) -> None:
        follow = dict(record()["follow_up"], missing=["named owner"], next_update_overdue="Unknown")
        text = self.shown(record(owner=None, risk_flags="Unknown", follow_up=follow))["text"]
        self.assertIn("Missing from this record: named owner", text)
        self.assertIn("1 Jan 2000. Unknown", text)
        self.assertNotIn("Overdue", text)
        self.assertIn("Risk flags: Unknown", text)

    def test_authorised_empty_and_role_denied_differ(self) -> None:
        empty = render(dict(id="ZF-1", challenge_targets=[]))
        assert empty is not None
        self.assertIn("No nomination or self-referral is recorded for this home.", empty["text"])
        self.assertIsNone(render(dict(id="ZF-1")))


if __name__ == "__main__":
    unittest.main()
