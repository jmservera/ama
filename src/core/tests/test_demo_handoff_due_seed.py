import copy
import json
import tempfile
import threading
import unittest
from copy import deepcopy
from pathlib import Path
from typing import Any

import dataset as _dataset
from zava_forward.core import change_provenance
from zava_forward.core import demo_handoff_due_seed as seed
from zava_forward.core.store import Store as _Store
from zava_forward.core.workflows import handoff_view

Store: Any = _Store


class FakeStore:
    def __init__(self, cases: dict[str, Any]) -> None:
        self.cases, self.lock = cases, threading.RLock()
        self.audits: list[tuple[str, str, str, str]] = []
        self.saves = 0

    def _case(self, case_id: str) -> Any:
        return self.cases[case_id]

    def audit(self, who: str, action: str, case_id: str, detail: str) -> None:
        self.audits.append((who, action, case_id, detail))

    def save(self) -> None:
        self.saves += 1


def case(case_id: str, **handoff: Any) -> dict[str, Any]:
    base: dict[str, Any] = dict(
        state="Offered",
        from_name="Ann",
        from_code="AN",
        to_name="Miguel",
        offered_at="2026-10-13T09:00",
        due_at=None,
    )
    return dict(id=case_id, owner="Ann", owner_code="AN", handoff={**base, **handoff})


class DemoHandoffDueSeed(unittest.TestCase):
    def store(self) -> FakeStore:
        return FakeStore(
            {
                "C1": case("C1"),
                "C2": case("C2", offered_at="2026-12-01T09:00+00:00"),
                "C3": case("C3", state="Accepted"),
                "C4": case("C4", offered_at="2026-11-20T10:00", due_at="2026-11-25T10:00+00:00"),
                "C5": dict(id="C5"),
            }
        )

    def test_inspect_writes_nothing(self) -> None:
        store = self.store()
        before = deepcopy(store.cases)
        report = seed.run(store, apply=False)
        self.assertEqual((report["handoffs_to_write"], report["due_at_to_write"]), (2, 1))
        self.assertEqual(store.cases, before)
        self.assertEqual((store.saves, store.audits), (0, []))

    def test_apply_writes_aware_times_with_london_offset_and_marks_them(self) -> None:
        store = self.store()
        report = seed.run(store, apply=True)
        self.assertTrue(report["applied"])
        c1 = store.cases["C1"]["handoff"]
        self.assertEqual(c1["offered_at"], "2026-10-13T09:00+01:00")
        self.assertEqual(c1["due_at"], "2026-10-16T08:00+00:00")
        self.assertEqual(c1[seed.MARK]["offered_at_was"], "2026-10-13T09:00")
        c4 = store.cases["C4"]["handoff"]
        self.assertEqual(c4["offered_at"], "2026-11-20T10:00+00:00")
        self.assertEqual(c4["due_at"], "2026-11-25T10:00+00:00")
        self.assertEqual(store.cases["C2"]["handoff"]["offered_at"], "2026-12-01T09:00+00:00")
        self.assertNotIn(seed.MARK, store.cases["C3"]["handoff"])
        self.assertEqual((store.saves, len(store.audits)), (1, 1))

    def test_apply_twice_changes_nothing_more(self) -> None:
        store = self.store()
        seed.run(store, apply=True)
        again = seed.run(store, apply=True)
        self.assertEqual((again["handoffs_to_write"], again["applied"]), (0, False))
        self.assertEqual(store.saves, 1)

    def test_revert_restores_original_handoffs(self) -> None:
        store = self.store()
        before = deepcopy(store.cases)
        seed.run(store, apply=True)
        self.assertEqual(seed.revert(store)["handoffs_reverted"], 2)
        self.assertEqual(store.cases, before)

    def test_view_shows_due_time_only_after_seed(self) -> None:
        store = self.store()
        self.assertIsNone(
            handoff_view(  # type: ignore[no-untyped-call]
                store.cases["C1"], as_of="2026-10-14T09:00+00:00"
            )["due_at"]
        )
        seed.run(store, apply=True)
        shown = handoff_view(  # type: ignore[no-untyped-call]
            store.cases["C1"], as_of="2026-10-14T09:00+00:00"
        )
        self.assertEqual(shown["due_at"], "2026-10-16T08:00+00:00")
        self.assertEqual(shown["elapsed_hours"], 25.0)


class RealStoreSeed(unittest.TestCase):
    def test_waiting_list_shows_seeded_due_time_through_the_store(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "seed.json"
            data: dict[str, Any] = copy.deepcopy(_dataset.DATA)
            data["staff"].append(
                dict(
                    code="RC-01",
                    name="Rex Coordinator",
                    email="rex@example.test",
                    role="Retrofit Coordinator",
                )
            )
            path.write_text(json.dumps(data), encoding="utf-8")
            store: Any = Store(str(path))
            sam = next(r for r in data["staff"] if r["email"].startswith("sam@"))
            rex = next(r for r in data["staff"] if r["email"].startswith("rex@"))
            cid = data["cases"][0]["id"]
            store.offer_handoff(
                sam, cid, rex["email"], "note", metadata=_dataset.change_metadata(store, cid)
            )
            with change_provenance.controlled(store, sam, cid) as (c, actor):
                c["handoff"]["offered_at"] = "2026-10-13T09:00"
                c["handoff"]["due_at"] = None
                store._save_workflow(actor, "test_age_handoff", cid, "x")
            as_of = "2026-10-14T09:00+00:00"
            before = store.unaccepted_handoffs(rex, as_of=as_of)
            self.assertEqual([r["due_at"] for r in before], [None])
            self.assertIsNone(before[0]["age_hours"])
            seed.run(store, apply=True)
            after = store.unaccepted_handoffs(rex, as_of=as_of)
            self.assertEqual([r["due_at"] for r in after], ["2026-10-16T08:00+00:00"])
            self.assertEqual(after[0]["age_hours"], 25.0)
            self.assertEqual(
                Store(str(path)).cases[cid]["handoff"]["due_at"], "2026-10-16T08:00+00:00"
            )


if __name__ == "__main__":
    unittest.main()
