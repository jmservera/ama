"""live_report shares one withheld-value scan per case set (Issue #2303)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

from dataset import DATA
from zava_forward.core import projection
from zava_forward.core.store import Store

StoreAny: Any = Store


class LiveReportWithheldScanTests(unittest.TestCase):
    def test_one_scan_per_distinct_case_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "zavaforward.json"
            path.write_text(json.dumps(DATA))
            store: Any = StoreAny(str(path))
            manager = next(
                m for m in store.data["staff"] if m.get("role") == "Retrofit Programme Manager"
            )
            case_ids = [c["id"] for c in store.data["cases"]][:2]
            store.data["recommendations"] = [
                dict(
                    id=f"R{i}",
                    kind="ai_task",
                    task="briefing",
                    source="ai",
                    status="Rejected",
                    reason="Not suitable",
                    case_ids=list(ids),
                )
                for i, ids in enumerate([case_ids, case_ids, case_ids[:1], case_ids])
            ]
            real = projection.withheld_scope_values
            with mock.patch.object(projection, "withheld_scope_values", side_effect=real) as spy:
                report = store.ai_live_report(manager)
        self.assertEqual(spy.call_count, 2)
        self.assertEqual(len(report["reviewer_reasons"]), 4)


if __name__ == "__main__":
    unittest.main()
