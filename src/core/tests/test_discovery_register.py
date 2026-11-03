import unittest
from datetime import date

from zava_forward.core import discovery_register as d

ON = date(2026, 11, 3)


def definitions(validated: bool = False) -> list[d.EventDefinition]:
    out = [
        d.EventDefinition(e, f"Synthetic {e}", "Retrofit Programme Manager")
        for e in d.REQUIRED_EVENTS
    ]
    if validated:
        out = [d.validate_event(x, "Synthetic PM", "Retrofit Programme Manager", ON) for x in out]
    return out


class OwnerTests(unittest.TestCase):
    def test_status_steps(self) -> None:
        self.assertEqual(d.DiscoveryOwner().status(), "NOT_NOMINATED")
        self.assertEqual(d.DiscoveryOwner("Sponsor", "Owner").status(), "ENDPOINT_NOT_AGREED")
        self.assertEqual(
            d.DiscoveryOwner("Sponsor", "Owner", "practical completion", "PM").status(),
            "ENDPOINT_NOT_AGREED",
        )
        self.assertEqual(
            d.DiscoveryOwner("Sponsor", "Owner", "Accepted handover", "").status(),
            "ENDPOINT_NOT_AGREED",
        )
        self.assertEqual(
            d.DiscoveryOwner("Sponsor", "Owner", "Accepted handover", "PM").status(),
            "ENDPOINT_AGREED",
        )


class DictionaryTests(unittest.TestCase):
    def test_empty_and_unvalidated_have_gaps(self) -> None:
        self.assertEqual(len(d.dictionary_gaps([])), len(d.REQUIRED_EVENTS))
        gaps = d.dictionary_gaps(definitions())
        self.assertEqual(len(gaps), len(d.REQUIRED_EVENTS))
        self.assertIn("has not validated", gaps[0])

    def test_validated_dictionary_has_no_gaps(self) -> None:
        self.assertEqual(d.dictionary_gaps(definitions(True)), [])

    def test_events_stay_separate(self) -> None:
        merged = [x for x in definitions(True) if x.event != "invoice"]
        self.assertEqual(
            d.dictionary_gaps(merged), ["Define the invoice event as a separate event"]
        )

    def test_only_owner_role_validates(self) -> None:
        with self.assertRaises(ValueError):
            d.validate_event(definitions()[0], "Analyst", "Retrofit Flow and Data Analyst", ON)
        with self.assertRaises(ValueError):
            d.validate_event(definitions()[0], " ", "Retrofit Programme Manager", ON)


class ConstraintTests(unittest.TestCase):
    def setUp(self) -> None:
        self.c = d.Constraint(
            "CAP", "Capacity", ("Procurement and Contracts",), proposed_by="Analyst"
        )
        self.sup = d.Evidence("Synthetic wait", "extract-1", d.SUPPORTS)
        self.con = d.Evidence("Synthetic short queue", "extract-2", d.CONTRADICTS)

    def test_seed_candidates_are_not_findings(self) -> None:
        rows = d.register_rows(list(d.CANDIDATE_CONSTRAINTS))
        self.assertEqual([r["rank"] for r in rows], [1, 2, 3, 4, 5])
        self.assertTrue(
            all(r["notice"] == d.NOT_FINDING and r["status"] == d.PROPOSED for r in rows)
        )

    def test_evidence_validation(self) -> None:
        for bad in (
            d.Evidence("x", "s", "neutral"),
            d.Evidence("", "s", d.SUPPORTS),
            d.Evidence("x", " ", d.SUPPORTS),
        ):
            with self.assertRaises(ValueError):
                d.add_evidence(self.c, bad)

    def test_accept_needs_both_sides_of_evidence(self) -> None:
        with self.assertRaises(ValueError):
            d.decide(self.c, "Owner", "Procurement and Contracts", True, "ok")
        c = d.add_evidence(self.c, self.sup)
        self.assertEqual(
            d.evidence_gaps(c),
            ["Record contradicting evidence, or note what was searched and not found"],
        )
        with self.assertRaises(ValueError):
            d.decide(c, "Owner", "Procurement and Contracts", True, "ok")
        done = d.decide(
            d.add_evidence(c, self.con), "Owner", "Procurement and Contracts", True, "ok"
        )
        self.assertTrue(done.is_company_finding)
        self.assertEqual(d.register_rows([done])[0]["notice"], "")

    def test_searched_note_counts_as_contradiction_record(self) -> None:
        c = d.add_evidence(self.c, self.sup)
        c = d.Constraint(
            **{**c.__dict__, "no_contradiction_note": "Searched 12 months of capacity logs; none"}
        )
        self.assertEqual(d.evidence_gaps(c), [])

    def test_decision_rights(self) -> None:
        c = d.add_evidence(d.add_evidence(self.c, self.sup), self.con)
        with self.assertRaises(ValueError):
            d.decide(c, "Owner", "Retrofit Flow and Data Analyst", True, "ok")
        with self.assertRaises(ValueError):
            d.decide(c, "Analyst", "Procurement and Contracts", True, "ok")
        with self.assertRaises(ValueError):
            d.decide(c, "Owner", "Procurement and Contracts", True, " ")

    def test_dispute_stays_visible_and_is_not_a_finding(self) -> None:
        disputed = d.decide(self.c, "Owner", "Procurement and Contracts", False, "Data disputed")
        self.assertEqual(disputed.status, d.DISPUTED)
        self.assertFalse(disputed.is_company_finding)
        self.assertEqual(d.register_rows([disputed])[0]["notice"], d.NOT_FINDING)

    def test_decided_constraint_is_closed_to_new_evidence(self) -> None:
        disputed = d.decide(self.c, "Owner", "Procurement and Contracts", False, "Data disputed")
        with self.assertRaises(ValueError):
            d.add_evidence(disputed, self.sup)


if __name__ == "__main__":
    unittest.main()
