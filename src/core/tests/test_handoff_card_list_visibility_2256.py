import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

import dataset as _dataset
from zava_forward.core import change_provenance
from zava_forward.core.store import Store as _Store
from zava_forward.core.workflows import HANDOFF_PENDING, handoff_view

Store: Any = _Store
AS_OF = "2026-10-14T09:00+00:00"
EXTRA_STAFF = (
    ("RC-01", "Rex Coordinator", "rex@example.test", "Retrofit Coordinator"),
    ("PS-01", "Pia Support", "pia@example.test", "Programme Support Officer"),
    ("QI-01", "Quin Inspector", "quin@example.test", "Quality Inspector"),
)


class OfferedHandoffVisibility(unittest.TestCase):
    """A case card that says a handoff is open must also appear in every queue the role can open."""

    def _store(self, tmp: str) -> tuple[Any, dict[str, Any], str]:
        path = Path(tmp) / "visibility.json"
        data: dict[str, Any] = copy.deepcopy(_dataset.DATA)
        for code, name, email, role in EXTRA_STAFF:
            data["staff"].append({"code": code, "name": name, "email": email, "role": role})
        path.write_text(json.dumps(data), encoding="utf-8")
        store: Any = Store(str(path))
        staff = {r["email"].split("@")[0]: r for r in store.data["staff"]}
        cid = data["cases"][0]["id"]
        store.offer_handoff(
            staff["sam"],
            cid,
            "rex@example.test",
            "note",
            metadata=_dataset.change_metadata(store, cid),
        )
        return store, staff, cid

    def test_managers_see_every_pending_state_while_unrelated_staff_do_not(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store, staff, cid = self._store(tmp)
            for state in HANDOFF_PENDING:
                with change_provenance.controlled(store, staff["sam"], cid) as (c, actor):
                    c["handoff"]["state"] = state
                    store._save_workflow(actor, "test_set_state", cid, state)
                card = handoff_view(store.cases[cid], as_of=AS_OF)  # type: ignore[no-untyped-call]
                self.assertEqual(card["state"], state)
                for who in ("pam", "pia"):
                    user = staff[who]
                    for queue in (store.unaccepted_handoffs, store.unowned_handoffs):
                        if queue is store.unowned_handoffs and state != "Offered":
                            continue
                        rows = queue(user, as_of=AS_OF)
                        with self.subTest(role=user["role"], queue=queue.__name__, state=state):
                            self.assertEqual([r["case_id"] for r in rows], [cid])
                            self.assertEqual(
                                (rows[0]["status"], rows[0]["proposed_receiver"]),
                                (card["status"], card["proposed_receiver"]),
                            )
                            self.assertEqual(rows[0]["chase_owner"], card["chase_owner"])
                with self.subTest(role="Quality Inspector", state=state):
                    self.assertEqual(store.unaccepted_handoffs(staff["quin"], as_of=AS_OF), [])

    def test_case_card_judges_an_old_offer_on_the_same_clock_as_the_waiting_list(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            store, staff, cid = self._store(tmp)
            with change_provenance.controlled(store, staff["sam"], cid) as (c, actor):
                c["handoff"]["offered_at"] = "2020-01-01T09:00+00:00"
                c["handoff"]["due_at"] = "2020-01-04T09:00+00:00"
                store._save_workflow(actor, "test_old_offer", cid, "old offer")
            store.as_of = "2020-01-02"
            card = store.detail(cid, staff["pam"])["handoff"]
            row = store.unaccepted_handoffs(staff["pam"])[0]
            self.assertTrue(card["overdue"])
            self.assertTrue(card["needs_escalation"])
            self.assertTrue(row["needs_escalation"])
            self.assertGreater(card["elapsed_hours"], 24 * 365)


if __name__ == "__main__":
    unittest.main()
