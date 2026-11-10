import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from collections.abc import Callable
from typing import Any

from zava_forward.core import learning_test_bundles as ltb

EFFORT = dict.fromkeys(ltb.COMPONENTS, 2.0)


def case(
    name: str, comp: float = 2.0, flow: float = 1.0, counts: dict[str, int] | None = None
) -> dict[str, Any]:
    counts = counts or {}
    return {
        "case": name,
        "arms": {
            "comparator": {"effort": dict.fromkeys(ltb.COMPONENTS, comp), "counts": counts},
            "workflow": {"effort": dict.fromkeys(ltb.COMPONENTS, flow), "counts": counts},
        },
    }


class LearningTestBundles(unittest.TestCase):
    def test_five_bundles_exclude_out_of_scope(self) -> None:
        self.assertEqual(len(ltb.BUNDLES), 5)
        for bundle in ltb.BUNDLES.values():
            self.assertFalse(ltb.OUT_OF_SCOPE & set(bundle.atlas_ids))

    def test_net_effort_sums_six_components(self) -> None:
        self.assertEqual(ltb.case_net_effort(EFFORT), 12.0)

    def test_rejects_missing_unknown_or_negative(self) -> None:
        with self.assertRaises(ValueError):
            ltb.case_net_effort({"preparation": 1})
        with self.assertRaises(ValueError):
            ltb.case_net_effort({**EFFORT, "other": 1})
        with self.assertRaises(ValueError):
            ltb.case_net_effort({**EFFORT, "checking": -1})

    def test_median_range_and_capacity_label(self) -> None:
        zero = {"inferred_submissions": 0}
        out = ltb.compare_bundle(
            "funding-evidence",
            [case("a", 2, 1, zero), case("b", 3, 1, zero), case("c", 5, 2, zero)],
        )
        self.assertEqual(out["comparator"]["median_minutes"], 18.0)
        self.assertEqual(out["workflow"]["max_minutes"], 12.0)
        self.assertEqual(out["workflow"]["cases"], 3)
        self.assertFalse(out["stop"])
        self.assertIn("capacity", out["capacity_note"])
        self.assertEqual(out["evidence_label"], "constructed-case evidence")

    def test_comparator_win_is_valid_outcome(self) -> None:
        out = ltb.compare_bundle(
            "handover-aftercare", [case("a", 1, 3, {"open_remedies_hidden": 0})]
        )
        self.assertEqual(out["direction"], "comparator lower or equal")
        self.assertFalse(out["stop"])

    def test_nonzero_target_zero_count_stops_bundle(self) -> None:
        out = ltb.compare_bundle(
            "change-impact", [case("a", 2, 1, {"approvals_wrongly_carried_over": 1})]
        )
        self.assertTrue(out["stop"])
        self.assertIn("a/workflow/approvals_wrongly_carried_over", out["breaches"])

    def test_missing_count_arm_or_case_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ltb.compare_bundle("pre-visit-pack", [case("a")])
        with self.assertRaises(ValueError):
            ltb.compare_bundle("pre-visit-pack", [])
        with self.assertRaises(ValueError):
            ltb.compare_bundle("nope", [case("a")])
        one_arm = {"case": "x", "arms": {"comparator": case("x")["arms"]["comparator"]}}
        with self.assertRaises(ValueError):
            ltb.compare_bundle("pre-visit-pack", [one_arm])


def run(bundle: str, counts: dict[str, int], **extra: Any) -> dict[str, Any]:
    return {
        "bundle": bundle,
        "representative_data_retained": False,
        "cases": [case("a", 2, 1, counts)],
        **extra,
    }


class RunReports(unittest.TestCase):
    def test_o16_bundle_must_name_owner(self) -> None:
        zero = {"inferred_submissions": 0}
        with self.assertRaises(ValueError):
            ltb.run_report(run("funding-evidence", zero))
        with self.assertRaises(ValueError):
            ltb.run_report(run("funding-evidence", zero, o16_counted_under="other"))
        out = ltb.run_report(run("funding-evidence", zero, o16_counted_under="change-impact"))
        self.assertEqual(out["o16_counted_under"], "change-impact")

    def test_owner_rejected_for_bundle_without_o16(self) -> None:
        zero = {"offers_misread_as_commitments": 0}
        with self.assertRaises(ValueError):
            ltb.run_report(run("pre-visit-pack", zero, o16_counted_under="change-impact"))
        self.assertIsNone(ltb.run_report(run("pre-visit-pack", zero))["o16_counted_under"])

    def test_retention_must_be_stated_false(self) -> None:
        bad = run("pre-visit-pack", {"offers_misread_as_commitments": 0})
        bad["representative_data_retained"] = True
        with self.assertRaises(ValueError):
            ltb.run_report(bad)
        del bad["representative_data_retained"]
        with self.assertRaises(ValueError):
            ltb.run_report(bad)

    def test_reconcile_o16_rejects_conflict(self) -> None:
        a = {"bundle": "change-impact", "o16_counted_under": "change-impact"}
        b = {"bundle": "funding-evidence", "o16_counted_under": "funding-evidence"}
        c = {"bundle": "funding-evidence", "o16_counted_under": "change-impact"}
        self.assertEqual(ltb.reconcile_o16([a, c]), "change-impact")
        self.assertIsNone(ltb.reconcile_o16([{"bundle": "pre-visit-pack"}]))
        with self.assertRaises(ValueError):
            ltb.reconcile_o16([a, b])
        with self.assertRaises(ValueError):
            ltb.reconcile_o16([a, {"bundle": "funding-evidence"}, a])
        with self.assertRaises(ValueError):
            ltb.reconcile_o16([{"bundle": "change-impact"}])
        with self.assertRaises(ValueError):
            ltb.reconcile_o16([{"bundle": "change-impact", "o16_counted_under": "bogus"}])
        with self.assertRaises(ValueError):
            ltb.reconcile_o16([{"bundle": "pre-visit-pack", "o16_counted_under": "change-impact"}])
        with self.assertRaises(ValueError):
            ltb.reconcile_o16([{"bundle": "nope"}])

    def test_render_states_stop_first_and_capacity(self) -> None:
        report = ltb.run_report(
            run(
                "change-impact",
                {"approvals_wrongly_carried_over": 1},
                o16_counted_under="change-impact",
            )
        )
        lines = ltb.render_report(report).splitlines()
        self.assertTrue(lines[1].startswith("STOP:"))
        text = "\n".join(lines)
        self.assertIn("capacity", text)
        self.assertIn("constructed-case evidence", text)
        self.assertIn("O16 counted under: change-impact", text)
        ok = ltb.render_report(
            ltb.run_report(run("pre-visit-pack", {"offers_misread_as_commitments": 0}))
        )
        self.assertIn("no breach recorded", ok)


SCHEMA = "learning-bundle-constructed-input-v1"
ZERO = {b.key: dict.fromkeys(b.zero_measures, 0) for b in ltb.BUNDLES.values()}
MEASURE = "offers_misread_as_commitments"


def envelope(bundle: str, **extra: Any) -> dict[str, Any]:
    arm = {"counts": ZERO[bundle]}
    base: dict[str, Any] = {
        "schema_version": SCHEMA,
        "run": 1,
        "bundle": bundle,
        "representative_data_retained": False,
        "cases": [
            {
                "case": n,
                "arms": {
                    "comparator": {"effort": dict.fromkeys(ltb.COMPONENTS, 2 * n), **arm},
                    "workflow": {"effort": dict.fromkeys(ltb.COMPONENTS, n), **arm},
                },
            }
            for n in (1, 2, 3)
        ],
    }
    if "O16" in ltb.BUNDLES[bundle].atlas_ids:
        base["o16_counted_under"] = "change-impact"
    return {**base, **extra}


def command(payload: bytes | str | dict[str, Any]) -> tuple[int, str, str, list[str]]:
    if isinstance(payload, dict):
        payload = json.dumps(payload)
    data = payload.encode() if isinstance(payload, str) else payload
    with tempfile.TemporaryDirectory() as cwd:
        done = subprocess.run(
            [sys.executable, "-m", "zava_forward.core.learning_test_bundles"],
            input=data,
            capture_output=True,
            cwd=cwd,
            env={**os.environ, "ZF_DATA": os.path.join(cwd, "must-not-exist")},
            timeout=30,
        )
        left = os.listdir(cwd)
    return done.returncode, done.stdout.decode(), done.stderr.decode(), left


class ConstructedReportCommand(unittest.TestCase):
    def test_all_five_bundles_report_through_existing_scorer(self) -> None:
        for key, bundle in ltb.BUNDLES.items():
            with self.subTest(bundle=key):
                code, out, err, left = command(envelope(key))
                self.assertEqual((code, err, left), (0, "", []))
                expected = ltb.render_report(ltb.run_report(envelope(key)))
                self.assertIn(expected, out)
                self.assertIn(f"(comparator: {bundle.comparator})", out)
                self.assertIn("comparator: 3 cases, median 24 min", out)
                self.assertIn("workflow: 3 cases, median 12 min", out)

    def test_stop_is_stated_before_effort_and_exit_is_zero(self) -> None:
        run_input = envelope("change-impact")
        run_input["cases"][1]["arms"]["workflow"]["counts"] = {"approvals_wrongly_carried_over": 2}
        code, out, _, _ = command(run_input)
        lines = out.splitlines()
        self.assertEqual(code, 0)
        self.assertTrue(lines[0].startswith("CONSTRUCTED, UNVERIFIED INPUT (run 1)"))
        self.assertTrue(lines[2].startswith("STOP: 2/workflow/approvals_wrongly_carried_over"))
        self.assertLess(out.index("STOP:"), out.index("median"))

    def test_comparator_lower_is_reported_not_hidden(self) -> None:
        run_input = envelope("handover-aftercare")
        for item in run_input["cases"]:
            arms = item["arms"]
            arms["comparator"]["effort"], arms["workflow"]["effort"] = (
                arms["workflow"]["effort"],
                arms["comparator"]["effort"],
            )
        _, out, _, _ = command(run_input)
        self.assertIn("comparator lower or equal", out)
        self.assertIn("Stop rule: no breach recorded.", out)

    def test_qualifications_and_o16_choice_are_labelled(self) -> None:
        _, out, _, _ = command(envelope("funding-evidence"))
        for text in (
            "constructed-case evidence",
            "Saved minutes are capacity until Finance validates them",
            "not verified synthetic provenance",
            "mapping is unconfirmed",
            "retention decision is unsatisfied",
            "caller's constructed accounting choice, not owner mapping ratification",
            "Nothing is stored",
        ):
            self.assertIn(text, out)
        _, plain, _, _ = command(envelope("pre-visit-pack"))
        self.assertNotIn("accounting choice", plain)

    def test_refusals_exit_nonzero_with_no_report_or_files(self) -> None:
        def with_(
            mutate: Callable[[dict[str, Any]], object], bundle: str = "pre-visit-pack"
        ) -> dict[str, Any]:
            value = envelope(bundle)
            mutate(value)
            return value

        def first(v: dict[str, Any]) -> dict[str, Any]:
            arm: dict[str, Any] = v["cases"][0]["arms"]["workflow"]
            return arm

        refused: dict[str, Any] = {
            "empty": b"",
            "not json": b"{",
            "array": b"[]",
            "bad utf8": b"\xff",
            "nan": b'{"run": NaN}',
            "huge float": json.dumps(envelope("pre-visit-pack"))
            .replace('"checking": 2,', '"checking": 1e999,', 1)
            .encode(),
            "dup key": b'{"run": 1, "run": 2}',
            "deep": b"[" * 20000,
            "oversize": b" " * (ltb.MAX_INPUT_BYTES + 1),
            "schema": with_(lambda v: v.update(schema_version="v2")),
            "missing schema": with_(lambda v: v.pop("schema_version")),
            "unknown key": with_(lambda v: v.update(participant="A. Person")),
            "bool run": with_(lambda v: v.update(run=True)),
            "float run": with_(lambda v: v.update(run=1.0)),
            "unknown bundle": with_(lambda v: v.update(bundle="story")),
            "retained true": with_(lambda v: v.update(representative_data_retained=True)),
            "retained missing": with_(lambda v: v.pop("representative_data_retained")),
            "retained zero": with_(lambda v: v.update(representative_data_retained=0)),
            "no cases": with_(lambda v: v.update(cases=[])),
            "too many": with_(lambda v: v.update(cases=v["cases"][:1] * 51)),
            "dup case": with_(lambda v: v["cases"][1].update(case=1)),
            "text case": with_(lambda v: v["cases"][0].update(case="Mrs Jones")),
            "bool case": with_(lambda v: v["cases"][0].update(case=True)),
            "case note": with_(lambda v: v["cases"][0].update(note="free text")),
            "one arm": with_(lambda v: v["cases"][0]["arms"].pop("workflow")),
            "arm key": with_(lambda v: first(v).update(notes="x")),
            "bool effort": with_(lambda v: first(v)["effort"].update(checking=True)),
            "text effort": with_(lambda v: first(v)["effort"].update(checking="3")),
            "negative effort": with_(lambda v: first(v)["effort"].update(checking=-1)),
            "big effort": with_(lambda v: first(v)["effort"].update(checking=100001)),
            "missing effort": with_(lambda v: first(v)["effort"].pop("support_cost")),
            "extra effort": with_(lambda v: first(v)["effort"].update(other=1)),
            "float count": with_(lambda v: first(v)["counts"].update({MEASURE: 0.0})),
            "bool count": with_(lambda v: first(v)["counts"].update({MEASURE: False})),
            "negative count": with_(lambda v: first(v)["counts"].update({MEASURE: -1})),
            "missing count": with_(lambda v: first(v).update(counts={})),
            "foreign count": with_(lambda v: first(v)["counts"].update(inferred_submissions=0)),
            "o16 missing": with_(lambda v: v.pop("o16_counted_under"), "change-impact"),
            "o16 bad owner": with_(
                lambda v: v.update(o16_counted_under="story-once"), "funding-evidence"
            ),
            "o16 on other": with_(lambda v: v.update(o16_counted_under="change-impact")),
        }
        for name, payload in refused.items():
            with self.subTest(name):
                code, out, err, left = command(payload)
                self.assertNotEqual(code, 0)
                self.assertEqual((out, left), ("", []))
                self.assertTrue(err.startswith("Learning report refused: "), err)
                self.assertLessEqual(len(err), 260)

    def test_refusal_does_not_echo_long_caller_text(self) -> None:
        _, _, err, _ = command({**envelope("pre-visit-pack"), "bundle": "x" * 5000})
        self.assertLess(len(err), 260)

    def test_boundary_values_are_accepted_and_scorer_is_unchanged(self) -> None:
        edge = envelope("pre-visit-pack", run=1_000_000)
        edge["cases"] = edge["cases"][:1] * 1
        edge["cases"][0]["case"] = 1_000_000
        edge["cases"][0]["arms"]["workflow"]["effort"]["checking"] = 100000
        edge["cases"][0]["arms"]["comparator"]["effort"]["checking"] = 0.25
        code, out, _, _ = command(edge)
        self.assertEqual(code, 0)
        expected = ltb.render_report(ltb.run_report(copy.deepcopy(edge)))
        self.assertIn(expected, out)
        self.assertIn("(run 1000000)", out)
        many = envelope("pre-visit-pack")
        many["cases"] = [{**copy.deepcopy(many["cases"][0]), "case": n} for n in range(1, 51)]
        self.assertEqual(command(many)[0], 0)
        self.assertLess(len(json.dumps(many)), ltb.MAX_INPUT_BYTES)

    def test_importing_and_help_have_no_side_effects(self) -> None:
        with tempfile.TemporaryDirectory() as cwd:
            done = subprocess.run(
                [sys.executable, "-m", "zava_forward.core.learning_test_bundles", "-h"],
                capture_output=True,
                cwd=cwd,
                timeout=30,
            )
            self.assertEqual(done.returncode, 0)
            self.assertIn(b"learning-bundle-constructed-input-v1", done.stdout)
            self.assertEqual(os.listdir(cwd), [])


if __name__ == "__main__":
    unittest.main()
