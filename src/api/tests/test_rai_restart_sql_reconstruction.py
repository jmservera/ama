"""Issue #146 RAI criterion 5: every RAI metric is rebuilt from SQL audit records after a restart.

Two separate store and service lifecycles share one file-backed SQLite database. Nothing in memory
survives the restart, and replayed telemetry must not be counted twice.
"""

import json
import unittest
from datetime import UTC, datetime, timedelta

from zava_forward.core import rai_metrics
from zava_forward.core.sqlstore import SqlStore

from test_assistants import Assistants, Base, config

A, B = "stock-prioritisation", "quality-evidence"


def window():
    now = datetime.now(UTC)
    return (now - timedelta(hours=1)).isoformat(), (now + timedelta(hours=1)).isoformat()


class RestartReconstruction(Base):
    def restart(self):
        """Destroy every in-memory object and open a fresh store and service on the same file."""
        self.service.stop()
        self.store.db.close()
        self.store = SqlStore(str(self.seed), str(self.dbpath))
        self.store.ai = self.provider
        self.service = Assistants(self.store, config())

    def raw(self, kind, **body):
        with self.service.transaction() as db:
            self.service.event(db, "task-raw", kind=kind, **body)

    def lifecycle_one(self):
        first = self.run_ready(A)
        self.verify(first)
        second = self.run_ready(B)
        self.service.review(self.pm, second["id"], "reject", second["revision"], "Not usable.")
        self.provider.bad = "citation"
        bad = self.service.invoke(self.pm, A, "ZF-2")
        self.service.execute(bad["id"])
        self.provider.bad = None
        self.raw("send-refused", reason="lease ended")
        self.raw("permit-denied", reason="release changed")
        self.raw("disabled", reason="allowance exhausted")
        self.raw(
            "completed", state="quarantined", envelope={"outcome": "returned"}, actual_tokens=40
        )

    def replay_batch(self):
        """The same audit rows a collector would re-send, as opaque telemetry events."""
        with self.service.transaction() as db:
            rows = db.execute("SELECT id,at,body FROM assistant_events ORDER BY at,id").fetchall()
        return [
            dict(
                json.loads(body),
                event_id=eid,
                observed_at=datetime.fromtimestamp(at, UTC).isoformat(),
            )
            for eid, at, body in rows
        ]

    def test_metrics_rebuild_after_restart_with_no_double_count(self):
        start, end = window()
        self.lifecycle_one()
        before = self.service.rai_metrics(self.pm, start, end)
        self.assertEqual(before["status"], "counted")
        metrics = before["metrics"]
        self.assertEqual(metrics["invocation"], 3)
        self.assertEqual(metrics["human_review"], 2)
        self.assertEqual(metrics["override"], 1)
        self.assertEqual(metrics["refusal"], 2)
        self.assertEqual(metrics["fallback"], 1)
        self.assertEqual(metrics["withheld"], 1)
        self.assertEqual(metrics["validation_failure"], 1)
        self.assertEqual(metrics["consumption"], 4)
        self.assertEqual(metrics["tokens"], 130 * 3 + 40)
        self.assertEqual(metrics["latency_samples"], 3)
        batch = self.replay_batch()

        self.restart()
        again = self.service.rai_metrics(self.pm, start, end)
        self.assertEqual(again["metrics"], metrics)

        replayed = self.service.rai_metrics(self.pm, start, end, replay=batch)
        self.assertEqual(replayed["metrics"], metrics)
        self.assertEqual(replayed["replay"]["duplicates"], len(batch))
        self.assertEqual(replayed["replay"]["new"], 0)

        self.raw("send-refused", reason="after restart")
        new_only = dict(batch[0], event_id="telemetry-only-1", kind="send-refused")
        after = self.service.rai_metrics(self.pm, start, end, replay=batch + [new_only])
        self.assertEqual(after["metrics"]["refusal"], metrics["refusal"] + 2)
        self.assertEqual(after["replay"]["new"], 1)
        self.assertEqual(after["metrics"]["invocation"], metrics["invocation"])
        again = self.service.rai_metrics(self.pm, start, end)
        self.assertEqual(again["metrics"]["refusal"], metrics["refusal"] + 1)

    def test_replay_cannot_inflate_or_leak_and_bad_input_blocks(self):
        start, end = window()
        self.lifecycle_one()
        batch = self.replay_batch()
        self.restart()
        base = self.service.rai_metrics(self.pm, start, end)["metrics"]
        self.assertEqual(
            self.service.rai_metrics(self.pm, start, end, replay=batch * 3)["metrics"], base
        )
        bad = [dict(batch[0], event_id="has space!")]
        self.assertEqual(
            self.service.rai_metrics(self.pm, start, end, replay=bad)["status"], "blocked"
        )
        self.assertEqual(self.service.rai_metrics(self.pm, end, start)["status"], "blocked")
        outside = [dict(batch[0], event_id="old-1", observed_at="2001-01-01T00:00:00+00:00")]
        self.assertEqual(
            self.service.rai_metrics(self.pm, start, end, replay=outside)["metrics"], base
        )
        with self.assertRaises(PermissionError):
            self.service.rai_metrics(dict(role="Resident", email="x@example.test"), start, end)

    def test_reader_is_pure_over_rows(self):
        self.assertEqual(rai_metrics.classify(dict(kind="unknown-kind")), ())
        self.assertEqual(
            rai_metrics.classify(dict(kind="review", action="reject")), ("human_review", "override")
        )


if __name__ == "__main__":
    unittest.main()
