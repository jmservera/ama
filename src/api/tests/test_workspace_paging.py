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
        for query in (
            "limit=0",
            "limit=101",
            "limit=x",
            "limit=5&offset=-1",
            "limit=5&offset=y",
            "limit=",
            "limit=5&offset=",
            "offset=",
        ):
            code, error = self.call(f"/api/workorders?{query}")
            self.assertEqual(code, 400, query)
            self.assertIn("error", error)

    def test_blank_paging_values_are_rejected_for_packages(self) -> None:
        for query in ("limit=", "limit=5&offset=", "offset="):
            self.assertEqual(self.call(f"/api/packages?{query}")[0], 400, query)


class OpsPagerSourceTests(unittest.TestCase):
    """Source guards for the capacity pager; the browser check covers behaviour."""

    js: str

    @classmethod
    def setUpClass(cls) -> None:
        from pathlib import Path

        cls.js = (Path(__file__).parents[1] / "src/zava_forward/api/web/ops.js").read_text()

    def test_page_change_confirms_unsaved_drafts(self) -> None:
        self.assertIn("appointmentDrafts().length && !window.confirm(", self.js)

    def test_superseded_loads_are_rejected_before_render(self) -> None:
        self.assertIn("if (loadSeq !== capacityLoadSeq) return;", self.js)
        guard = self.js.index("loadSeq !== capacityLoadSeq")
        self.assertLess(guard, self.js.index("const pkgs = pkgPage.items"))

    def test_paging_is_serialized_while_a_refresh_is_running(self) -> None:
        step = self.js.index("const step = (delta)")
        guard = self.js.index("if (busy()) return;", step)
        self.assertLess(guard, self.js.index("live.offset =", step))
        self.assertIn("() => saving || Boolean(capacityHistoryBarrier)", self.js)

    def test_out_of_range_retry_checks_guards_before_changing_offsets(self) -> None:
        loop = self.js.index('for (const [kind, result] of [["packages", pkgPage]')
        end = self.js.index("CAPACITY_PAGE[kind].offset =", loop)
        window = self.js[loop:end]
        self.assertIn("signal.throwIfAborted();", window)
        self.assertIn("capacityHistoryGeneration !== recoveryGeneration", window)

    def test_browser_check_reads_paged_envelopes(self) -> None:
        from pathlib import Path

        check = (Path(__file__).parents[1] / "checks/capacity_browser_check.py").read_text()
        self.assertNotIn('"/api/workorders").json()[0]', check)
        self.assertIn("/api/workorders?limit=1&offset=0", check)


if __name__ == "__main__":
    unittest.main()
