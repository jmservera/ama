"""Generated-stock, write-cold and repeat-page measurements for issue 327."""

import json
import statistics
import tempfile
import time
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from test_sqlreads import STAFF, dataset, queue_cases
from zava_forward.core import taskqueues
from zava_forward.core.sqlstore import SqlStore


class QueueWriteScale(unittest.TestCase):
    def test_queue_pages_after_writes_at_60000(self) -> None:
        data = dataset(queue_cases(60000))
        data["as_of"] = "2026-10-16"
        with tempfile.TemporaryDirectory() as tmp:
            seed = Path(tmp) / "synthetic.json"
            seed.write_text(json.dumps(data))
            started = time.perf_counter()
            store = SqlStore(str(seed), str(seed.with_suffix(".sqlite")))
            self.addCleanup(store.db.close)
            print(f"[queue327] initialization_s={time.perf_counter() - started:.3f}", flush=True)
            observed_counts = []
            original = store.work_context
            for queue, _, _ in taskqueues.DEFINITIONS:
                writes, cold, repeat, evaluations = [], [], [], []
                for iteration in range(3):
                    started = time.perf_counter()
                    with store.lock:
                        case = store._case("ZF-00000")
                        case["benchmark_revision"] = f"{queue}-{iteration}"
                        store.save()
                    writes.append((time.perf_counter() - started) * 1000)
                    calls = 0

                    def counted(*args: Any, **kwargs: Any) -> Any:
                        nonlocal calls
                        calls += 1
                        return original(*args, **kwargs)

                    with patch.object(store, "work_context", new=counted):
                        started = time.perf_counter()
                        page = store.page_cases(STAFF[1], "all", filters={"queue": queue}, limit=50)
                        cold.append((time.perf_counter() - started) * 1000)
                        evaluations.append(calls)
                        started = time.perf_counter()
                        again = store.page_cases(
                            STAFF[1], "all", filters={"queue": queue}, limit=50
                        )
                        repeat.append((time.perf_counter() - started) * 1000)
                    self.assertEqual(page, again)
                print(
                    f"[queue327] queue={queue} matches={page['total']} "
                    f"write_ms={[round(x, 1) for x in writes]} "
                    f"cold_ms={[round(x, 1) for x in cold]} "
                    f"repeat_ms={[round(x, 1) for x in repeat]} "
                    f"cold_contexts={evaluations} "
                    f"medians_ms={statistics.median(writes):.1f}/"
                    f"{statistics.median(cold):.1f}/{statistics.median(repeat):.1f}",
                    flush=True,
                )
                # Timings are observations; the structural assertion avoids noisy CPU gates.
                observed_counts.append((queue, evaluations, len(page["items"])))
            for queue, evaluations, size in observed_counts:
                with self.subTest(queue=queue):
                    self.assertEqual(evaluations, [size] * 3)


if __name__ == "__main__":
    unittest.main()
