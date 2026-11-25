import json
import tempfile
import unittest
from pathlib import Path

from zava_forward.api import eval_report_cache


class EvalReportCacheTests(unittest.TestCase):
    def setUp(self) -> None:
        eval_report_cache.clear()
        self.addCleanup(eval_report_cache.clear)
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.golden = Path(tmp.name) / "golden.json"
        self.golden.write_text("{}")
        self.calls = 0

    def func(self) -> dict[str, object]:
        self.calls += 1
        return {"n": self.calls, "rows": [1]}

    def test_second_read_does_not_recompute_and_returns_a_copy(self) -> None:
        first = eval_report_cache.cached(self.func, self.golden)
        first["rows"].append(2)
        second = eval_report_cache.cached(self.func, self.golden)
        self.assertEqual(self.calls, 1)
        self.assertEqual(second, {"n": 1, "rows": [1]})

    def test_changed_golden_recomputes(self) -> None:
        eval_report_cache.cached(self.func, self.golden)
        self.golden.write_text(json.dumps({"changed": True}))
        self.assertEqual(eval_report_cache.cached(self.func, self.golden)["n"], 2)

    def test_state_is_bounded(self) -> None:
        for i in range(eval_report_cache.MAX_ENTRIES + 3):
            self.golden.write_text(str(i))
            eval_report_cache.cached(self.func, self.golden)
        self.assertLessEqual(len(eval_report_cache._entries), eval_report_cache.MAX_ENTRIES)

    def test_missing_golden_still_raises(self) -> None:
        with self.assertRaises(FileNotFoundError):
            eval_report_cache.cached(self.func, self.golden.with_name("absent.json"))


if __name__ == "__main__":
    unittest.main()
