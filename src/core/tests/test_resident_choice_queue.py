"""Cross-home resident choice queue: role-gated, projected, read-only (synthetic data only)."""

import copy
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

import dataset
from zava_forward.core.store import Store


class ResidentChoiceQueue(unittest.TestCase):
    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        data = copy.deepcopy(dataset.DATA)
        extra = (
            ("rc1", "Retrofit Coordinator"),
            ("qi", "Quality Inspector"),
            ("bs", "Building Safety Liaison"),
        )
        for code, role in extra:
            data["staff"].append(
                dict(code=code, name=f"Synthetic {code}", email=f"{code}@example.test", role=role)
            )
        path = Path(tmp.name) / "synthetic.json"
        path.write_text(json.dumps(data))
        self.store: Any = Store(str(path))  # type: ignore[no-untyped-call]
        self.users = {p["email"].split("@")[0]: p for p in data["staff"]}

    def test_allowed_roles_see_open_homes_with_choice_and_commitment_fields(self) -> None:
        for code in ("sam", "pam", "rc1"):
            page = self.store.resident_choice_queue(self.users[code])
            self.assertEqual(page["total"], len(page["items"]))
            self.assertGreater(page["total"], 0)
            for item in page["items"]:
                self.assertEqual(
                    set(item),
                    {"id", "address", "town", "measure_decisions", "resident_update"},
                )
                self.assertIsInstance(item["measure_decisions"], list)

    def test_other_roles_are_refused(self) -> None:
        for code in ("qi", "bs"):
            with self.assertRaises(PermissionError):
                self.store.resident_choice_queue(self.users[code])
        with self.assertRaises(PermissionError):
            self.store.resident_choice_queue({"role": "Contractor", "code": "x"})

    def test_closed_homes_are_left_out_and_paging_reports_total(self) -> None:
        self.store.cases["ZF-1"]["closed"] = True
        everyone = self.store.resident_choice_queue(self.users["sam"])
        self.assertNotIn("ZF-1", [i["id"] for i in everyone["items"]])
        first = self.store.resident_choice_queue(self.users["sam"], limit=1, offset=0)
        self.assertEqual(len(first["items"]), 1)
        self.assertEqual(first["total"], everyone["total"])
        self.assertEqual(first["items"][0]["id"], everyone["items"][0]["id"])

    def test_queue_does_not_change_the_store(self) -> None:
        before = json.dumps(self.store.cases, sort_keys=True, default=str)
        self.store.resident_choice_queue(self.users["pam"])
        self.assertEqual(json.dumps(self.store.cases, sort_keys=True, default=str), before)


if __name__ == "__main__":
    unittest.main()
