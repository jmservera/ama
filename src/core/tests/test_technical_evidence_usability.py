import unittest

from zava_forward.core.doc_controls import (
    is_available_case_document,
    is_clean_document,
    is_clean_upload,
    is_rescan_pending,
    scan_status,
)
from zava_forward.core.signoffs import missing_items
from zava_forward.core.store import Store


def case(*docs: dict[str, object]) -> dict[str, object]:
    return dict(technical=dict(signoffs={}), documents=list(docs), stock_reconciliation=[])


def doc(kind: str, **extra: object) -> dict[str, object]:
    return dict(kind=kind, generated=False, **extra)


class TechnicalEvidenceUsability(unittest.TestCase):
    def evidence(self, c: dict[str, object]) -> set[str]:
        items = missing_items(c, usable_only=True)
        return {m["item"] for m in items if m["item"].startswith("Evidence:")}

    def test_pending_scan_does_not_satisfy_evidence(self) -> None:
        c = case(*(doc(k, scan=dict(status="pending")) for k in Store.EVIDENCE))
        self.assertEqual(self.evidence(c), {f"Evidence: {k}" for k in Store.EVIDENCE})

    def test_missing_scan_does_not_satisfy_evidence(self) -> None:
        c = case(*(doc(k) for k in Store.EVIDENCE))
        self.assertEqual(len(self.evidence(c)), len(Store.EVIDENCE))

    def test_clean_and_generated_documents_satisfy_evidence(self) -> None:
        kinds = list(Store.EVIDENCE)
        docs = [doc(kinds[0], scan=dict(status="clean"))]
        docs += [dict(kind=k, generated=True) for k in kinds[1:]]
        self.assertEqual(self.evidence(case(*docs)), set())

    def test_failed_infected_malformed_and_conflicting_statuses_fail_closed(self) -> None:
        quarantined = (
            doc("EPC"),
            doc("EPC", scan=dict(status="pending")),
            doc("EPC", scan=dict(status="infected")),
            doc("EPC", scan=dict(status="failed")),
            doc("EPC", scan=dict(status="mismatch")),
            doc("EPC", scan=None),
            doc("EPC", scan={}),
            doc("EPC", scan="clean"),
            doc("EPC", scan=dict(status=None)),
            doc("EPC", scan=dict(status="unknown")),
            doc("EPC", scan_status="pending"),
            doc("EPC", scan_status="infected"),
            doc("EPC", scan_status="failed"),
            doc("EPC", scan_status=None),
            doc("EPC", scan_status=""),
            doc("EPC", scan=dict(status="clean"), scan_status="infected"),
            doc("EPC", scan=dict(status="clean"), scan_status="pending"),
            doc("EPC", scan=dict(status="failed"), scan_status="clean"),
        )
        for item in quarantined:
            with self.subTest(doc=item):
                self.assertNotEqual(scan_status(item), "clean")
                self.assertFalse(is_clean_document(item))
                self.assertFalse(is_clean_upload(item))
                self.assertFalse(is_available_case_document(item))
                c = case(item)
                epc_row = next(r for r in Store.checklist(c) if r["kind"] == "EPC")
                self.assertFalse(epc_row["present"])
                self.assertIn("Evidence: EPC", self.evidence(c))
                default_items = {m["item"] for m in missing_items(c)}
                self.assertIn("Evidence: EPC", default_items)

        self.assertTrue(is_clean_upload(doc("EPC", scan_status="clean")))
        self.assertTrue(is_rescan_pending(doc("EPC")))
        self.assertTrue(is_rescan_pending(doc("EPC", scan=dict(status="pending"))))
        self.assertTrue(is_rescan_pending(doc("EPC", scan_status="pending")))
        self.assertTrue(
            is_rescan_pending(doc("EPC", scan=dict(status="clean"), scan_status="pending"))
        )
        for non_pending in (
            doc("EPC", scan=dict(status="failed")),
            doc("EPC", scan=dict(status="infected")),
            doc("EPC", scan=dict(status="mismatch")),
            doc("EPC", scan=dict(status="clean")),
            doc("EPC", scan=None),
            doc("EPC", scan_status=None),
            dict(kind="EPC", generated=True),
        ):
            self.assertFalse(is_rescan_pending(non_pending))

        with self.assertRaises(TypeError):
            Store.checklist({"documents": [None]})
        with self.assertRaises(KeyError):
            Store.checklist({"documents": [{}]})


if __name__ == "__main__":
    unittest.main()
