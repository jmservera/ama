import unittest

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


if __name__ == "__main__":
    unittest.main()
