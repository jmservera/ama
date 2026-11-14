import unittest
from typing import Any

from zava_forward.core import resident_access as ra


def authority(**kw: Any) -> dict[str, Any]:
    base = dict(
        status="Confirmed",
        tasks=["Communicate", "Attend"],
        measure="M1",
        authority_date="2026-01-01",
        review_date="2026-06-01",
    )
    return {**base, **kw}


class ResidentAccess(unittest.TestCase):
    def test_every_step_has_an_alternative_without_inferring_incapacity(self) -> None:
        for code in ("J1", "J2", "J3", "J4", "J5", "J6", "R1"):
            out = ra.step_alternative(code, ["Phone only", "Easy Read or plain language"])
            self.assertTrue(out["non_digital"])
            self.assertFalse(out["capacity_inferred"])
        with self.assertRaises(ValueError):
            ra.step_alternative("J9")
        with self.assertRaises(ValueError):
            ra.step_alternative("J1", ["Lacks capacity"])

    def test_view_is_task_limited_and_expires(self) -> None:
        view = ra.representative_view([authority()], "2026-05-31")
        self.assertEqual(view["tasks"], ["Attend", "Communicate"])
        self.assertNotIn("Works decision", view["tasks"])
        expired = ra.representative_view([authority()], "2026-06-01")
        self.assertFalse(expired["allowed"])
        self.assertEqual(expired["tasks"], [])
        self.assertNotIn("M1", str(expired))

    def test_latest_version_governs_and_unconfirmed_is_denied(self) -> None:
        for status in ("Revoked", "Disputed", "Unclear"):
            self.assertFalse(
                ra.representative_view([authority(), authority(status=status)], "2026-02-01")[
                    "allowed"
                ]
            )
        self.assertFalse(ra.representative_view(None, "2026-02-01")["allowed"])
        self.assertFalse(
            ra.representative_view([authority(authority_date="2026-03-01")], "2026-02-01")[
                "allowed"
            ]
        )


if __name__ == "__main__":
    unittest.main()
