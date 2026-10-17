"""Exact fictional coordinator populations, never generated historical backfill."""

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from dataset import DATA
from test_progress_reports import AS_OF, disposition
from zava_forward.core import coordinator, insights, ranking
from zava_forward.core.sqlstore import SqlStore
from zava_forward.core.store import Store


def fixture() -> dict[str, Any]:
    data = copy.deepcopy(DATA)
    data["staff"].extend(
        [
            dict(
                code="CON-101",
                name="Synthetic Provider",
                email="con@example.test",
                role="Contractor",
                contractor="Test Ltd",
            ),
            dict(
                code="RC-101",
                name="Synthetic Coordinator",
                email="rex@example.test",
                role="Retrofit Coordinator",
            ),
        ]
    )
    data["cases"][0].update(
        stage="Contacting resident",
        building_id="SYN-B101",
        returns=[
            disposition(1, "2026-10-01T12:00:00Z", "Survey booked", "Contact paused"),
            disposition(2, "2026-10-03T12:00:00Z", "Contact paused", "Contacting resident"),
        ],
    )
    data["cases"][0]["home"].update(lat=55.5, lon=-1.7)
    data["cases"][1]["home"]["lat"] = None
    data["cases"][2]["home"].update(lat=54.9, lon=-1.6)
    data["cases"][3]["home"].update(lat=54.91, lon=-1.61)
    data["cases"][4]["home"].update(lat=55.2, lon=-1.5, area="Other")
    data["cases"][4].update(
        stage="Aftercare issue",
        returns=[disposition(1, "2026-10-02T12:00:00Z", "Completed", "Aftercare issue", True)],
    )
    return data


class Coordinator(unittest.TestCase):
    backend = "json"
    store: Any

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / "synthetic.json"
        self.path.write_text(json.dumps(fixture()))
        self.store = (
            SqlStore(str(self.path), str(self.path.with_suffix(".sqlite")))
            if self.backend == "sqlite"
            else Store(str(self.path))
        )
        if self.backend == "sqlite":
            self.addCleanup(self.store.db.close)
        self.sam, self.pam = DATA["staff"]

    def read(self, **query: str) -> dict[str, Any]:
        return coordinator.read(self.store, self.pam, dict(as_of=AS_OF, view="all", **query))

    def test_denominators_missing_geocodes_and_no_mutation(self) -> None:
        before = copy.deepcopy(self.store.cases)
        audit = list(self.store.audit_entries())
        result = self.read()
        self.assertEqual(result["cohort"]["selected_cases"], 5)
        self.assertEqual(result["map"]["total"], 5)
        self.assertEqual(result["map"]["mapped"], 4)
        self.assertEqual(result["map"]["missing_geocode"], 1)
        self.assertEqual(result["records"]["total"], 5)
        self.assertEqual(sum(x["count"] for x in result["heatmap"]), 5)
        self.assertEqual(sum(x["current"] for x in result["funnel"]), 5)
        self.assertEqual(result["coverage"]["stage_history_partial"], 2)
        self.assertEqual(result["coverage"]["stage_history_unknown"], 3)
        self.assertIsNone(result["coverage"]["lifecycle_exclusions"])
        self.assertEqual(self.store.cases, before)
        self.assertEqual(list(self.store.audit_entries()), audit)

    def test_own_scope_and_combined_source_filters_match_existing_list(self) -> None:
        for actor in (self.sam, self.pam):
            for view in ("mine", "all"):
                for filters in (
                    {},
                    {"area": "Test"},
                    {"stage": "Final checks before ordering"},
                    {"flag": "hazard"},
                    {"queue": "blocked"},
                    {"area": "Test", "wave": "Wave 1", "owner": "RLO-01", "q": "ZF"},
                    {"flag": "fundingprog"},
                    {"flag": "nodecision"},
                ):
                    with self.subTest(view=view, filters=filters):
                        result = coordinator.read(
                            self.store, actor, dict(as_of=AS_OF, view=view, **filters)
                        )
                        query = {k: v for k, v in filters.items() if k != "q"}
                        page = self.store.page_cases(
                            actor, view, filters.get("q", ""), query, limit=2
                        )
                        self.assertEqual(result["records"]["total"], page["total"])
                        self.assertEqual(result["map"]["total"], page["total"])

    def test_exit_stage_is_not_current_stage_filter_and_drills_exactly(self) -> None:
        result = self.read(metric="exits", metric_stage="Contact paused")
        self.assertEqual([x["id"] for x in result["records"]["items"]], ["ZF-1"])
        self.assertEqual(result["map"]["total"], 1)
        self.assertEqual(result["cohort"]["selected_cases"], 5)
        result = self.read(
            metric="exits", metric_stage="Contact paused", stage="Contacting resident"
        )
        self.assertEqual(result["records"]["total"], 1)
        self.assertEqual(result["cohort"]["selected_cases"], 2)
        self.assertEqual(
            self.read(
                metric="exits", metric_stage="Contact paused", stage="Final checks before ordering"
            )["records"]["total"],
            0,
        )

    def test_distinct_cases_period_reopens_and_unknown_legacy(self) -> None:
        self.assertEqual(self.read(metric="entries")["records"]["total"], 2)
        self.assertEqual(self.read(metric="returns")["records"]["total"], 1)
        self.assertEqual(self.read(metric="reopens")["records"]["items"][0]["id"], "ZF-5")
        self.assertEqual(
            self.read(start="2026-10-02T12:00:00Z", metric="entries")["records"]["total"], 2
        )
        unknown = self.read(metric="unknown_history")
        self.assertEqual([r["id"] for r in unknown["records"]["items"]], ["ZF-2", "ZF-3", "ZF-4"])
        self.assertTrue(all(x["conversion"] is None for x in unknown["funnel"]))

    def test_malformed_contradictory_and_precision_history_stays_unknown(self) -> None:
        for change in (
            {"at": "not-a-time"},
            {"version": 99},
            {"to_stage": "Unknown"},
            {"at": "2026-10-01T12:00Z"},
            {"source": ""},
        ):
            with self.subTest(change=change):
                with self.store.lock:
                    self.store._case("ZF-1")["returns"] = copy.deepcopy(
                        fixture()["cases"][0]["returns"]
                    )
                    self.store._case("ZF-1")["returns"][0].update(change)
                    self.store.save()
                result = self.read(metric="returns")
                self.assertEqual(result["records"]["total"], 0)
                self.assertEqual(result["coverage"]["stage_history_unknown"], 4)

    def test_unknown_coordinate_values_remain_in_population(self) -> None:
        for value in (None, "", "54", True, 91, float("nan"), float("inf")):
            with self.subTest(value=value):
                # No persistence of nonfinite JSON/SQL fixture values is needed.
                with self.store.lock:
                    self.store.cases["ZF-3"]["home"]["lat"] = value
                    result = self.read()
                self.assertEqual(result["map"]["total"], 5)
                self.assertEqual(result["map"]["missing_geocode"], 2)

    def test_clusters_viewport_and_missing_population_reconcile(self) -> None:
        with patch.object(insights, "MAP_CAP", 1):
            result = self.read(bbox="54,-2,55,-1", zoom="8")
        self.assertEqual(result["map"]["mode"], "clusters")
        self.assertEqual(sum(r["count"] for r in result["map"]["items"]), 2)
        self.assertEqual(result["map"]["in_view"], 2)
        self.assertEqual(result["map"]["mapped"], 4)
        self.assertEqual(result["map"]["total"], 5)
        self.assertEqual(result["records"]["total"], 5)

    def test_heatmap_groups_and_cell_drill_are_exact(self) -> None:
        for by in ("area", "building", "archetype"):
            result = self.read(group_by=by)
            for cell in result["heatmap"]:
                drill = self.read(group_by=by, group=cell["group"], metric_stage=cell["stage"])
                self.assertEqual(drill["records"]["total"], cell["count"])
                self.assertEqual(drill["map"]["total"], cell["count"])
        self.assertIn(coordinator.UNKNOWN, self.read(group_by="building")["groups"])

    def test_filter_exclusions_and_paging_are_not_lifecycle_exclusions(self) -> None:
        result = self.read(area="Test", metric="filtered_out")
        self.assertEqual(result["cohort"]["selected_cases"], 4)
        self.assertEqual([x["id"] for x in result["records"]["items"]], ["ZF-5"])
        excluded = self.read(flag="support", metric="filtered_out")
        hazard = next(row for row in excluded["records"]["items"] if row["id"] == "ZF-4")
        self.assertTrue(hazard["stopped"])
        ids: list[str] = []
        for offset in range(0, 6, 2):
            page = self.read(limit="2", offset=str(offset))["records"]
            self.assertEqual(page["total"], 5)
            ids.extend(x["id"] for x in page["items"])
        self.assertEqual(ids, [f"ZF-{n}" for n in range(1, 6)])
        empty = self.read(area="Nowhere")
        self.assertEqual(empty["records"]["total"], 0)
        self.assertEqual(empty["map"]["items"], [])
        self.assertEqual(empty["cohort"]["excluded_by_filters"], 5)

    def test_stops_and_priority_do_not_grant_approval(self) -> None:
        stopped = self.read(metric="stopped")
        self.assertGreaterEqual(stopped["records"]["total"], 1)
        self.assertIn("ZF-4", [x["id"] for x in stopped["records"]["items"]])
        draft = self.read()["priority"]
        self.assertFalse(draft["approved"])
        self.assertIsNone(draft["count"])
        with self.assertRaises(ValueError):
            self.read(metric="priority")
        with patch.dict(ranking.CURRENT, status="Approved", owner="Synthetic human"):
            result = self.read(metric="priority")
            self.assertEqual(result["records"]["total"], 5)
            self.assertTrue(result["priority"]["approved"])

    def test_server_boundary_denies_spoofed_revoked_and_contractor_actors(self) -> None:
        for actor in (
            {},
            {"role": "Mystery"},
            {"role": "Contractor"},
            {**self.pam, "code": "FORGED"},
            {**self.pam, "email": "unknown@example.test"},
        ):
            with self.assertRaises(PermissionError):
                coordinator.read(self.store, actor, dict(as_of=AS_OF))
        with self.store.lock:
            self.store.staff[self.pam["email"]]["role"] = "Mystery"
            with self.assertRaises(PermissionError):
                coordinator.read(self.store, self.pam, dict(as_of=AS_OF))

    def test_invalid_parameters_and_closed_map_fields_refuse_explicitly(self) -> None:
        for query in (
            {"as_of": ""},
            {"unknown": "x"},
            {"view": "closed"},
            {"flag": "wat"},
            {"queue": "wat"},
            {"metric": "exclusions"},
            {"metric_stage": "wat"},
            {"group_by": "diagnosis"},
            {"limit": "0"},
            {"offset": "-1"},
            {"bbox": "nan,0,1,2"},
            {"bbox": "2,0,1,2"},
            {"q": "x" * 201},
            {"as_of": "2099-01-01T00:00Z"},
            {"start": "2099-01-01T00:00Z"},
        ):
            with self.subTest(query=query), self.assertRaises(ValueError):
                coordinator.read(self.store, self.pam, dict({"as_of": AS_OF}, **query))
        with self.store.lock:
            self.store.cases["ZF-1"]["resident"]["name"] = {"private": "malformed"}
            with self.assertRaises(ValueError):
                self.read()

    def test_untrusted_audit_and_private_fields_are_not_silent_success(self) -> None:
        with patch.object(self.store, "verify_ledger", side_effect=OSError("synthetic")):
            with self.assertLogs("zava_forward.core.coordinator", level="ERROR"):
                result = self.read()
        self.assertEqual(result["audit_integrity"], "Unknown")
        self.assertEqual(result["coverage"]["stage_history_unknown"], 5)
        self.assertIsNone(result["counts"]["entries"])
        raw = json.dumps(result)
        for private in ("PRIVATE", "Pat Test", "01000", "adjustment", "receiving_owner"):
            self.assertNotIn(private, raw)


class SqliteCoordinator(Coordinator):
    backend = "sqlite"


if __name__ == "__main__":
    unittest.main()
