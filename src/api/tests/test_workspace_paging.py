"""Paged package and work order reads for the capacity workspace (#616)."""

import unittest

from test_procurement_api import ProcurementApiFixture


class WorkspacePaging(ProcurementApiFixture):
    def issue_two(self) -> None:
        for contractor, cid in (("Test Ltd", "ZF-1"), ("Other Ltd", "ZF-2")):
            self.assertEqual(
                self.call(f"/api/packages/{self.pid}/capacity", self.capacity(contractor))[0], 200
            )
            self.assertEqual(self.call("/api/workorders", self.issue(cid))[0], 200)

    def test_unpaged_reads_keep_the_list_shape(self) -> None:
        self.issue_two()
        code, rows = self.call("/api/workorders")
        self.assertEqual((code, len(rows)), (200, 2))
        code, packages = self.call("/api/packages")
        self.assertEqual((code, len(packages)), (200, 1))

    def test_work_orders_are_paged_with_totals(self) -> None:
        self.issue_two()
        code, first = self.call("/api/workorders?limit=1&offset=0")
        self.assertEqual(code, 200)
        self.assertEqual((first["total"], first["limit"], first["offset"]), (2, 1, 0))
        self.assertEqual([w["case_id"] for w in first["items"]], ["ZF-1"])
        code, second = self.call("/api/workorders?limit=1&offset=1")
        self.assertEqual([w["case_id"] for w in second["items"]], ["ZF-2"])
        code, past = self.call("/api/workorders?limit=1&offset=5")
        self.assertEqual((code, past["items"], past["total"]), (200, [], 2))

    def test_packages_are_paged(self) -> None:
        code, page = self.call("/api/packages?limit=5")
        self.assertEqual(code, 200)
        self.assertEqual((page["total"], len(page["items"]), page["offset"]), (1, 1, 0))
        self.assertEqual(self.call("/api/packages?limit=5&offset=1")[1]["items"], [])

    def test_contractor_totals_exclude_hidden_orders(self) -> None:
        self.issue_two()
        code, page = self.call("/api/workorders?limit=10", actor="kim")
        self.assertEqual(code, 200)
        self.assertEqual(page["total"], 1)
        self.assertEqual([w["case_id"] for w in page["items"]], ["ZF-1"])
        self.assertEqual(self.call("/api/packages?limit=5", actor="kim")[0], 403)

    def test_bad_paging_values_are_rejected(self) -> None:
        for query in ("limit=0", "limit=101", "limit=x", "limit=5&offset=-1", "limit=5&offset=y"):
            code, error = self.call(f"/api/workorders?{query}")
            self.assertEqual(code, 400, query)
            self.assertIn("error", error)


if __name__ == "__main__":
    unittest.main()
