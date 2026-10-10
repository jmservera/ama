"""Independent public-fixture and forecast tests; scratch state stays in the project."""
from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

from properwarm_mvp import controls, quality
from properwarm_mvp.exercise import (
    AS_OF, FIXTURE_VERSION, create_seed, dataset, forecast_input, iter_scale_events,
    iter_scale_homes, manifest,
)
from properwarm_mvp.forecast import SOURCE_MAX_AGE, compare_oracle, forecast
from properwarm_mvp.sqlstore import SqlStore
from properwarm_mvp.store import Store

ORACLE_PATH = Path(__file__).resolve().parents[1] / "evals" / "forecast_oracles.json"


class ForecastTests(unittest.TestCase):
    def setUp(self):
        with ORACLE_PATH.open(encoding="utf-8") as source:
            self.oracles = json.load(source)

    def test_six_frozen_scenarios_exact_rerun_and_independent_scores(self):
        for scenario, oracle in self.oracles["scenarios"].items():
            with self.subTest(scenario=scenario):
                inputs = forecast_input(scenario)
                untouched = copy.deepcopy(inputs)
                result = forecast(inputs)
                self.assertEqual(result, forecast(inputs))
                self.assertEqual(inputs, untouched)
                self.assertEqual(result["status"], oracle["status"])
                self.assertEqual(result["cumulative_handovers"], oracle["cumulative_handovers"])
                self.assertEqual(result["fixture_version"], self.oracles["fixture_version"])
                self.assertEqual(result["as_of"], self.oracles["as_of"])
                self.assertEqual(result["denominator"], self.oracles["denominator"])
                score = compare_oracle(result, oracle)
                if scenario == "missing_input":
                    self.assertEqual(result["tables"]["weekly"], [])
                    self.assertIn(oracle["unknown"], result["unknowns"][0]["reason"])
                    self.assertEqual(score["status"], "Not scored")
                    self.assertIsNone(score["weekly_cumulative_mae"])
                    self.assertIsNone(score["week_four_absolute_error"])
                    self.assertIsNone(score["within_thresholds"])
                else:
                    self.assertEqual([row["accepted_ids"] for row in result["tables"]["weekly"]],
                                     oracle["weekly_accepted_ids"])
                    self.assertTrue(score["within_thresholds"])
                    self.assertLessEqual(score["weekly_cumulative_mae"], 1)
                    self.assertLessEqual(score["week_four_absolute_error"], 2)

    def test_exact_capacity_and_duration_sensitivities(self):
        for name, capacity, duration in (("central", 2, 1), ("capacity_one", 1, 1),
                                         ("capacity_three", 3, 1), ("two_week_stages", 2, 2)):
            with self.subTest(name=name):
                inputs = forecast_input()
                for stage in ("installation", "qa_handover"):
                    inputs[stage] = {"slots": [capacity] * 4, "duration_weeks": duration}
                result = forecast(inputs)
                self.assertEqual(result["cumulative_handovers"], self.oracles["sensitivities"][name])
                self.assertTrue(all(row["installation_occupied"] <= capacity
                                    and row["qa_occupied"] <= capacity for row in result["tables"]["weekly"]))

    def test_two_week_slots_stay_occupied_and_stages_wait_until_following_week(self):
        inputs = forecast_input()
        for stage in ("installation", "qa_handover"):
            inputs[stage]["duration_weeks"] = 2
        result = forecast(inputs)
        rows = result["tables"]["weekly"]
        self.assertEqual([row["installation_occupied"] for row in rows], [2, 2, 2, 2])
        self.assertEqual([row["qa_occupied"] for row in rows], [0, 0, 2, 2])
        schedule = result["tables"]["schedule"]
        installation = [entry for entry in schedule if entry["stage"] == "installation"]
        self.assertEqual([entry["start_week"] for entry in installation], [1, 1, 3, 3])
        finishes = {entry["home_id"]: entry["end_week"] for entry in installation}
        for entry in schedule:
            if entry["stage"] == "qa_handover":
                self.assertGreater(entry["start_week"], finishes[entry["home_id"]])
        self.assertEqual(rows[-1]["accepted_ids"], ["EX-COHORT-001", "EX-COHORT-002"])

    def test_qa_capacity_is_separate_and_can_be_bottleneck(self):
        inputs = forecast_input()
        inputs["qa_handover"]["slots"] = [1, 1, 1, 1]
        result = forecast(inputs)
        self.assertEqual(result["cumulative_handovers"], [0, 1, 2, 3])
        self.assertEqual([row["installation_occupied"] for row in result["tables"]["weekly"]], [2, 2, 2, 2])
        self.assertEqual([row["qa_occupied"] for row in result["tables"]["weekly"]], [0, 1, 1, 1])

    def test_slot_reservations_respect_known_future_capacity_reduction(self):
        inputs = forecast_input()
        inputs["installation"] = {"slots": [2, 1, 2, 2], "duration_weeks": 2}
        inputs["qa_handover"] = {"slots": [0, 0, 2, 1], "duration_weeks": 2}
        result = forecast(inputs)
        self.assertEqual(result["status"], "forecast")
        self.assertEqual(result["cumulative_handovers"], [0, 0, 0, 1])
        self.assertEqual([row["installation_occupied"] for row in result["tables"]["weekly"]], [1, 1, 2, 2])
        self.assertEqual([row["qa_occupied"] for row in result["tables"]["weekly"]], [0, 0, 1, 1])
        for row in result["tables"]["weekly"]:
            self.assertLessEqual(row["installation_occupied"], row["installation_slots"])
            self.assertLessEqual(row["qa_occupied"], row["qa_slots"])

    def test_hold_cancels_only_its_active_slot_without_completing_installation(self):
        inputs = forecast_input("new_hold")
        inputs["installation"]["duration_weeks"] = 2
        result = forecast(inputs)
        self.assertEqual(result["status"], "forecast")
        self.assertEqual(result["tables"]["weekly"][1]["installed_ids"], ["EX-COHORT-002"])
        cancelled = [row for row in result["tables"]["schedule"] if "cancelled_at_start_week" in row]
        self.assertEqual([row["home_id"] for row in cancelled], ["EX-COHORT-001"])
        self.assertEqual(cancelled[0]["cancelled_at_start_week"], 2)
        self.assertTrue(all("EX-COHORT-001" not in row["accepted_ids"] for row in result["tables"]["weekly"]))

    def test_scenario_and_sibling_isolation(self):
        original = forecast(forecast_input())
        for scenario, home_id, kind in (("new_hold", "EX-COHORT-001", "hold"),
                                         ("withdrawal", "EX-COHORT-002", "withdrawal")):
            result = forecast(forecast_input(scenario))
            matching = [row for row in result["exclusions"] if row["kind"] == kind]
            self.assertEqual([row["home_id"] for row in matching], [home_id])
            self.assertEqual(len([row for row in result["exclusions"] if row["kind"] == "initial_hold"]), 4)
            self.assertNotIn(home_id, result["tables"]["weekly"][1]["accepted_ids"])
            self.assertEqual(forecast(forecast_input()), original)
        returned = forecast(forecast_input("qa_return"))["tables"]["schedule"]
        self.assertEqual([row["home_id"] for row in returned if row["stage"] == "qa_return"], ["EX-COHORT-001"])
        self.assertEqual([row["start_week"] for row in returned
                          if row["home_id"] == "EX-COHORT-001" and row["stage"] == "qa_handover"], [2, 3])

    def test_missing_future_stale_and_version_mismatch_abstain(self):
        for key in SOURCE_MAX_AGE:
            for invalid in ("missing", "future", "stale", "version", "date"):
                with self.subTest(source=key, invalid=invalid):
                    inputs = forecast_input()
                    if invalid == "missing":
                        inputs["sources"].pop(key)
                    else:
                        inputs["sources"][key].update({
                            "observed_at": "2026-10-11" if invalid == "future" else
                            "2025-01-01" if invalid == "stale" else
                            None if invalid == "date" else AS_OF,
                            "version": "" if invalid == "version" else f"{key}-1",
                        })
                    result = forecast(inputs)
                    self.assertEqual(result["status"], "abstained")
                    self.assertIsNone(result["cumulative_handovers"])
                    self.assertEqual(result["tables"]["weekly"], [])
                    self.assertEqual(compare_oracle(result, self.oracles["scenarios"]["steady"])["status"], "Not scored")
        self.assertEqual(forecast(forecast_input(), evaluated_as_of="2026-10-12")["status"], "abstained")

    def test_review_trigger_inclusive_boundary_and_no_latest_wins(self):
        from datetime import date, timedelta

        for key, days in SOURCE_MAX_AGE.items():
            inputs = forecast_input()
            inputs["sources"][key]["observed_at"] = (date.fromisoformat(AS_OF) - timedelta(days=days)).isoformat()
            self.assertEqual(forecast(inputs)["status"], "forecast")
            inputs["sources"][key]["observed_at"] = (date.fromisoformat(AS_OF) - timedelta(days=days + 1)).isoformat()
            self.assertEqual(forecast(inputs)["status"], "abstained")
        for version_key in ("version", "fixture_version"):
            inputs = forecast_input()
            inputs[version_key] = "unknown-version"
            self.assertEqual(forecast(inputs)["status"], "abstained")

    def test_unknown_home_input_reconciles_partial_coverage_not_zero_error(self):
        for missing in ("state", "source_versions"):
            inputs = forecast_input()
            if missing == "state":
                inputs["homes"][0].pop("state")
            else:
                inputs["homes"][0]["source_versions"] = {"stock": "obsolete-stock"}
            result = forecast(inputs)
            self.assertEqual(result["status"], "partial")
            self.assertEqual(result["coverage"], {
                "denominator": 16, "known": 15, "unknown": 1, "ready": 11, "held": 4, "fraction": 15 / 16,
            })
            self.assertEqual(result["unknowns"][0]["home_id"], "EX-COHORT-001")
            self.assertEqual(len(result["exclusions"]), 5)
            self.assertEqual(compare_oracle(result, self.oracles["scenarios"]["steady"])["status"], "Not scored")

    def test_bad_shapes_and_impossible_event_schedules_are_not_silent_success(self):
        bad_inputs = []
        for key in ("as_of", "installation", "qa_handover", "homes", "events", "denominator"):
            inputs = forecast_input()
            inputs.pop(key)
            bad_inputs.append(inputs)
        for slots in ([2], [2, True, 2, 2], [-1, 2, 2, 2]):
            inputs = forecast_input()
            inputs["installation"]["slots"] = slots
            bad_inputs.append(inputs)
        for changes in ({"week": 1, "kind": "qa_return"}, {"week": 5, "kind": "hold"},
                        {"week": 2, "kind": "hold", "home_id": "EX-HOME-001"}):
            inputs = forecast_input("new_hold")
            inputs["events"][0].update(changes)
            bad_inputs.append(inputs)
        inputs = forecast_input()
        inputs["homes"][1]["id"] = inputs["homes"][0]["id"]
        bad_inputs.append(inputs)
        inputs = forecast_input()
        inputs["homes"][-1]["release_week"] = 2
        bad_inputs.append(inputs)
        for inputs in bad_inputs:
            with self.subTest(inputs=inputs):
                result = forecast(inputs)
                self.assertEqual(result["status"], "abstained")
                self.assertIsNone(result["cumulative_handovers"])

    def test_priority_then_id_order_and_zero_capacity_are_deterministic(self):
        inputs = forecast_input()
        for home in inputs["homes"]:
            home["priority"] = 1
        inputs["homes"].reverse()
        self.assertEqual(forecast(inputs)["cumulative_handovers"], [0, 2, 4, 6])
        self.assertEqual(forecast(inputs)["tables"]["weekly"][1]["accepted_ids"],
                         ["EX-COHORT-001", "EX-COHORT-002"])
        inputs["installation"]["slots"] = [0, 0, 0, 0]
        result = forecast(inputs)
        self.assertEqual(result["status"], "forecast")
        self.assertEqual(result["cumulative_handovers"], [0, 0, 0, 0])

    def test_error_thresholds_are_not_exact_match_gate_and_abstention_is_not_zero(self):
        result = forecast(forecast_input())
        score = compare_oracle(result, {"cumulative_handovers": [0, 3, 5, 8]})
        self.assertTrue(score["within_thresholds"])
        self.assertEqual(score["week_four_absolute_error"], 2)
        self.assertEqual(score["weekly_cumulative_mae"], 1)
        self.assertFalse(compare_oracle(result, {"cumulative_handovers": [0, 3, 6, 9]})["within_thresholds"])


class ExerciseTests(unittest.TestCase):
    def setUp(self):
        self.work = Path.cwd() / f".exercise-test-state-{uuid.uuid4().hex}"
        self.work.mkdir()
        self.addCleanup(shutil.rmtree, self.work)
        environment = patch.dict(os.environ, {
            "PW_DOC_STORE": "local", "PW_DOC_DIR": str(self.work / "docs"),
            "PW_DIGEST_DIR": str(self.work / "digests"), "PW_AS_OF": AS_OF,
            "PYTHONDONTWRITEBYTECODE": "1",
        }, clear=True)
        environment.start()
        self.addCleanup(environment.stop)

    def test_fictional_dataset_populations_metadata_and_source_conflict(self):
        data = dataset()
        self.assertEqual(data, dataset())
        self.assertEqual(set(data), {"staff", "cases", "as_of"})
        self.assertEqual(data["as_of"], AS_OF)
        self.assertEqual(len(data["cases"]), 18)
        homes = {row["id"]: row for row in data["cases"]}
        self.assertEqual(len(homes), 18)
        lead, sibling = homes["EX-HOME-001"], homes["EX-HOME-002"]
        self.assertEqual(lead["exercise"]["building_id"], sibling["exercise"]["building_id"])
        self.assertEqual(lead["exercise"]["package_id"], sibling["exercise"]["package_id"])
        self.assertEqual(lead["exercise"]["package_applicability"], "Not reviewed independently")
        self.assertEqual(lead["home"]["epc"], "Unknown")
        candidates = lead["exercise"]["source_candidates"]
        self.assertEqual([source["version"] for source in candidates], ["epc-a-1", "epc-b-1"])
        self.assertIn("EPC rating: D", candidates[0]["raw_text"])
        self.assertIn("EX-HOME-001,E", candidates[1]["raw_text"])
        for source in candidates + sibling["exercise"]["source_candidates"]:
            self.assertEqual(source["sha256"], hashlib.sha256(source["raw_text"].encode()).hexdigest())
            self.assertTrue(source["fictional"])
            self.assertTrue(source["locator"] and source["parser"])
        cohort = [row for row in homes.values() if row["exercise"]["population"] == "forecast"]
        self.assertEqual(sum(row["exercise"]["forecast_state"] == "ready" for row in cohort), 12)
        self.assertEqual(sum(row["exercise"]["forecast_state"] == "held" for row in cohort), 4)
        for row in homes.values():
            self.assertEqual(row["exercise"]["fixture_version"], FIXTURE_VERSION)
            self.assertTrue(row["exercise"]["fictional"])
            self.assertTrue(row["resident"]["email"].endswith("@example.test"))
            self.assertRegex(row["resident"]["phone"], r"^01632 960\d{3}$")
            self.assertIn("Imaginary", row["home"]["address"])
            self.assertFalse(row["funding_ok"])
            self.assertEqual(row["decision"]["status"], "Not yet asked")
            self.assertEqual(row["hazards"], [])
        self.assertEqual(set(manifest()["populations"]), {"story", "forecast", "analytical", "scale"})
        lead["exercise"]["source_candidates"][0]["version"] = "changed"
        self.assertEqual(dataset()["cases"][0]["exercise"]["source_candidates"][0]["version"], "epc-a-1")

    def test_manifest_exact_workflows_profiles_and_existing_roles(self):
        public, data = manifest(), dataset()
        self.assertEqual(len(public["profiles"]), 11)
        self.assertEqual(len(public["workflows"]), 9)
        self.assertEqual({row["id"] for row in public["workflows"]},
                         {"stock", "technical", "resident", "procurement", "hazards",
                          "quality", "finance", "handoffs", "portfolio"})
        staff = {row["code"]: row for row in data["staff"]}
        self.assertEqual(len(staff), 12)
        self.assertEqual(len({row["email"] for row in staff.values()}), 12)
        self.assertEqual(set(public["roles"]), {row["role"] for row in staff.values()})
        self.assertEqual(len(public["roles"]), 8)
        existing = set(controls.FINANCE_ROLES + controls.RESIDENT_ROLES +
                       ("Quality Inspector", "Building Safety Liaison", "Contractor"))
        self.assertEqual(set(public["roles"]), existing)
        for profile in public["profiles"]:
            self.assertEqual(profile["role"], staff[profile["actor"]]["role"])
            self.assertIn(profile["default_queue"], ("mine", "all"))
            self.assertIn(profile["script"]["status"], ("Not run", "Blocked"))
            self.assertTrue(all(profile["script"][key] for key in
                                ("case", "endpoint", "permitted", "denied", "blocker", "evidence", "owner", "next_action")))
        for workflow in public["workflows"]:
            self.assertTrue(all(workflow[key] for key in ("fixture", "expected", "blocker", "owner", "next_action", "status")))
        self.assertIn("unimplemented", public["startup"]["database"])
        self.assertIn("Not run", public["populations"]["scale"]["execution"])
        self.assertEqual(public["lead_contract"]["milestones"], [3600, 12600, 1800])

    def test_explicit_seed_cli_no_implicit_state_or_overwrite(self):
        output = self.work / "seed.json"
        self.assertEqual(create_seed(output), output)
        before = output.read_bytes()
        with self.assertRaises(FileExistsError):
            create_seed(output)
        self.assertEqual(output.read_bytes(), before)
        create_seed(output, overwrite=True)
        self.assertEqual(output.read_bytes(), before)
        self.assertEqual(list(self.work.iterdir()), [output])
        with self.assertRaises(FileNotFoundError):
            create_seed(self.work / "absent" / "seed.json")
        result = subprocess.run(
            [sys.executable, "-m", "properwarm_mvp.exercise", "--output", str(self.work / "cli.json")],
            capture_output=True, text=True, check=False,
            env=dict(os.environ, PYTHONPATH=str(Path(__file__).resolve().parents[1])),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads((self.work / "cli.json").read_text()), dataset())

    def test_store_and_sqlstore_preserve_case_metadata_and_choice_isolation(self):
        seed = create_seed(self.work / "seed.json")
        for kind in ("json", "sql"):
            with self.subTest(kind=kind):
                root = self.work / kind
                root.mkdir()
                if kind == "json":
                    store = Store(str(seed), str(root / "live.json"), str(root / "audit.jsonl"))
                else:
                    store = SqlStore(str(seed), str(root / "state.sqlite"), str(root / "docs"))
                users = {row["code"]: row for row in dataset()["staff"]}
                initial = copy.deepcopy(store.detail("EX-HOME-001")["exercise"])
                store.set_decision(users["EX-RLO-01"], "EX-HOME-001", "Accepted")
                self.assertEqual(store.detail("EX-HOME-002")["decision"]["status"], "Not yet asked")
                self.assertEqual(store.detail("EX-HOME-001")["exercise"], initial)
                self.assertTrue(store.verify_audit())
                if kind == "sql":
                    store.db.close()
                    reopened = SqlStore(str(seed), str(root / "state.sqlite"), str(root / "docs"))
                    self.addCleanup(reopened.db.close)
                else:
                    reopened = Store(str(seed), str(root / "live.json"), str(root / "audit.jsonl"))
                self.assertEqual(reopened.detail("EX-HOME-001")["exercise"], initial)
                self.assertEqual(reopened.detail("EX-HOME-001")["decision"]["status"], "Accepted")
                self.assertEqual(reopened.as_of, AS_OF)

    def test_fixture_identities_support_real_independence_without_extra_permissions(self):
        seed = create_seed(self.work / "seed.json")
        store = Store(str(seed))
        users = {row["code"]: row for row in dataset()["staff"]}
        case_id = "EX-HOME-001"
        store.finance_action(users["EX-GEO-01"], case_id, {"action": "budget_propose", "amount": 22000})
        for code in ("EX-GEO-01", "EX-CON-01", "EX-RLO-01"):
            with self.assertRaises(PermissionError):
                store.finance_action(users[code], case_id, {"action": "budget_approve"})
        store.finance_action(users["EX-PM-02"], case_id, {"action": "budget_approve"})
        store.technical_action(users["EX-RC-01"], case_id, {"action": "design_submit", "note": "Fictional design"})
        with self.assertRaises(PermissionError):
            store.technical_action(users["EX-RC-01"], case_id, {"action": "signoff_give", "type": "design"})
        for key, code in (("assessment", "EX-QI-01"), ("design", "EX-RC-02"), ("building", "EX-BSL-01")):
            store.technical_action(users[code], case_id, {"action": "signoff_give", "type": key})
        for kind in ("EPC", "Survey", "Design", "Consent"):
            store.add_document(users["EX-GEO-01"], case_id, f"fictional-{kind}.txt", kind, b"Fictional evidence only")
        store.technical_action(users["EX-PM-01"], case_id, {"action": "signoff_give", "type": "coordination"})
        signoffs = store.detail(case_id)["technical"]["signoffs"]
        self.assertEqual(len({record["by_email"] for record in signoffs.values()}), 4)
        items = {label: "Fictional inspection evidence" for label in quality.checklist_for("Loft insulation")["items"]}
        index = store.submit_quality(users["EX-QI-01"], case_id, "Loft insulation",
                                     users["EX-CON-01"]["name"], "Provider submission", items)
        for code in ("EX-CON-01", "EX-QI-01"):
            with self.assertRaises(PermissionError):
                store.accept_quality(users[code], case_id, index)
        store.accept_quality(users["EX-QI-02"], case_id, index)
        self.assertEqual(store.detail(case_id)["quality"][0]["accepted_by"], users["EX-QI-02"]["name"])
        self.assertFalse(store.detail(case_id)["closed"])
        self.assertTrue(store.verify_audit())

    def test_separate_scale_stream_counts_and_distinct_namespaces_no_load_claim(self):
        home_ids = set()
        for home in iter_scale_homes():
            self.assertEqual(home["exercise"]["population"], "scale")
            home_ids.add(home["id"])
        self.assertEqual(len(home_ids), 60000)
        self.assertFalse(home_ids & {row["id"] for row in dataset()["cases"]})
        count, prior_id = 0, ""
        for event in iter_scale_events():
            self.assertIn(event["home_id"], home_ids)
            self.assertGreater(event["id"], prior_id)
            self.assertEqual(event["fixture_version"], "properwarm-scale-1")
            prior_id = event["id"]
            count += 1
        self.assertEqual(count, 600000)
        self.assertIn("Not run", manifest()["populations"]["scale"]["execution"])
        for kwargs in ({"home_count": 0}, {"home_count": True}, {"events_per_home": -1}):
            with self.assertRaises(ValueError):
                next(iter_scale_events(**kwargs))


if __name__ == "__main__":
    unittest.main()
