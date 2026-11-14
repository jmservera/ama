import copy
import unittest
from typing import Any

from zava_forward.core import journey_register as jr


def complete() -> dict[str, Any]:
    reg = jr.draft()
    for j in reg["journeys"]:
        j["owner"] = "Journey owner (fictional)"
        j["escalation"] = "Head of service (fictional)"
        for m in j["measures"].values():
            m.update(threshold="Set by owner (fictional)", approved_by="Owner (fictional)")
        j["manual_alternative"].update(tested_by="Tester (fictional)", tested_on="2026-11-03")
    return reg


class JourneyRegisterTests(unittest.TestCase):
    def test_draft_lists_every_journey_and_measure_but_is_blocked(self) -> None:
        reg = jr.draft()
        self.assertEqual({j["id"] for j in reg["journeys"]}, set(jr.JOURNEYS))
        self.assertTrue(all(set(j["measures"]) == set(jr.MEASURES) for j in reg["journeys"]))
        rec = jr.evaluate(reg)
        self.assertEqual(rec["status"], "blocked")
        self.assertFalse(rec["activation_allowed"])
        self.assertFalse(rec["usability_evidence"])
        self.assertIn("J1:owner_missing", rec["blockers"])
        self.assertIn("J4:manual_alternative_untested", rec["blockers"])

    def test_complete_register_is_ready_and_hash_is_stable(self) -> None:
        rec = jr.evaluate(complete())
        self.assertEqual(rec["status"], "ready")
        self.assertEqual(rec["blockers"], [])
        self.assertEqual(rec["record_hash"], jr.evaluate(complete())["record_hash"])

    def test_one_gap_blocks_only_that_journey(self) -> None:
        reg = complete()
        reg["journeys"][2]["measures"]["appointment_recovery"]["approved_by"] = "unknown"
        rec = jr.evaluate(reg)
        self.assertEqual(rec["blockers"], ["J3:appointment_recovery:threshold_unapproved"])
        self.assertFalse(rec["journeys"]["J3"]["ready"])
        self.assertTrue(rec["journeys"]["J1"]["ready"])

    def test_missing_journey_and_placeholder_values_block(self) -> None:
        reg = complete()
        reg["journeys"] = [j for j in reg["journeys"] if j["id"] != "R1"]
        reg["journeys"][0]["owner"] = "None"
        reg["journeys"][1]["manual_alternative"]["documented"] = False
        blockers = set(jr.evaluate(reg)["blockers"])
        self.assertEqual(
            blockers,
            {"R1:journey_missing", "J1:owner_missing", "J2:manual_alternative_undocumented"},
        )

    def test_malformed_input_blocks_without_raising(self) -> None:
        reg = copy.deepcopy(complete())
        reg["journeys"][0]["measures"] = "bad"
        reg["journeys"][1]["manual_alternative"] = None
        self.assertEqual(jr.evaluate(reg)["status"], "blocked")
        self.assertEqual(jr.evaluate({})["status"], "blocked")

    def test_missing_data_and_incomplete_appointments_go_to_a_person(self) -> None:
        cases = [
            {
                "id": "a",
                "source_record": "complete",
                "sensor_data": "present",
                "resident": {"priority_support": False},
                "appointment_history": "regular",
            },
            {
                "id": "b",
                "source_record": "stale",
                "sensor_data": "present",
                "resident": {"priority_support": False},
                "appointment_history": "regular",
            },
            {
                "id": "c",
                "source_record": "complete",
                "sensor_data": "declined",
                "resident": {"priority_support": None},
                "appointment_history": "no_response",
            },
        ]
        out = jr.route_cases(cases)
        by_id = {r["case_id"]: r for r in out["routes"]}
        self.assertEqual(by_id["a"]["route"], "none")
        self.assertEqual(by_id["b"]["reasons"], ["source_missing"])
        self.assertEqual(
            by_id["c"]["reasons"], ["sensor_missing", "support_unknown", "appointment_incomplete"]
        )
        self.assertTrue(all(r["rank_effect"] == "none" for r in out["routes"]))
        self.assertEqual((out["tested"], out["routed_to_human"]), (3, 2))
        self.assertEqual(out["reason_counts"]["sensor_missing"], 1)

    def test_routing_does_not_depend_on_other_cases_or_order(self) -> None:
        cases: list[dict[str, Any]] = [
            {"id": "x", "source_record": "missing"},
            {
                "id": "y",
                "source_record": "complete",
                "sensor_data": "present",
                "resident": {"priority_support": False},
                "appointment_history": "regular",
            },
        ]
        forward = {r["case_id"]: r for r in jr.route_cases(cases)["routes"]}
        backward = {r["case_id"]: r for r in jr.route_cases(cases[::-1])["routes"]}
        self.assertEqual(forward, backward)

    def test_routed_cases_name_a_human_and_none_are_dropped(self) -> None:
        cases: list[dict[str, Any]] = [{"id": "m"}, {"id": "n", "appointment_history": None}]
        out = jr.route_cases(cases, "Housing officer (fictional)")
        self.assertEqual(out["tested"], len(out["routes"]))
        self.assertEqual(out["dropped"], 0)
        self.assertTrue(all(r["reviewer"] == "Housing officer (fictional)" for r in out["routes"]))
        self.assertIn("appointment_incomplete", out["routes"][1]["reasons"])
        blocked = jr.route_cases(cases, "AI agent")
        self.assertEqual(blocked["unassigned"], 2)
        self.assertEqual(blocked["routed_to_human"], 2)
        self.assertTrue(all(r["rank_effect"] == "none" for r in blocked["routes"]))

    def test_usability_reports_aggregates_and_rejects_staff_level_data(self) -> None:
        obs = [{"measure": "appointment_recovery", "value": v} for v in (2, 4, 6)]
        ok = jr.aggregate_usability(obs, 3)
        self.assertEqual(ok["measures"]["appointment_recovery"]["mean"], 4)
        small = jr.aggregate_usability(obs, 4)
        self.assertTrue(small["measures"]["appointment_recovery"]["suppressed"])
        self.assertEqual(jr.aggregate_usability(obs)["blockers"], ["min_cell_unapproved"])
        bad = jr.aggregate_usability([*obs, {"measure": "hazard_action", "staff_id": "s1"}], 3)
        self.assertEqual(bad["status"], "blocked")
        self.assertEqual((bad["measures"], bad["rejected_fields"]), ({}, ["staff_id"]))
        self.assertFalse(bad["staff_surveillance"])


if __name__ == "__main__":
    unittest.main()
