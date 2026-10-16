"""Local source observations only; no network or activation authority."""

from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
from unittest.mock import patch

from source_monitor_fixture import DAY, RAW, SOURCE, MonitorFixture

from zava_forward.orchestrator.source_monitor import main, run


class SourceMonitorJobTests(MonitorFixture):
    def test_job_obeys_cadence_and_records_missing_observation_failure(self) -> None:
        self.configure(cadence_days=366)
        report = run(self.monitor, {}, today=DAY)
        self.assertEqual(len(report["failures"]), 1)
        self.assertEqual(report["checked"], [SOURCE])
        retry = run(self.monitor, {}, today="2026-10-17")
        self.assertEqual(retry["checked"], [SOURCE])
        self.assertEqual(retry["skipped"], [])
        self.assertEqual(len(retry["failures"]), 1)
        self.assertEqual(self.monitor.changes()[0]["categories"], ["retrieval_failure"])

    def test_due_failure_retries_next_day_then_resumes_success_cadence(self) -> None:
        self.configure(cadence_days=30)
        observations = {
            SOURCE: dict(content=RAW.decode(), metadata={}, provenance="Synthetic local fixture")
        }
        self.assertEqual(run(self.monitor, observations, today=DAY)["checked"], [SOURCE])
        failure = run(
            self.monitor,
            {SOURCE: dict(error="Synthetic retrieval failure", provenance="Synthetic outage")},
            today="2026-11-15",
        )
        self.assertEqual(failure["checked"], [SOURCE])
        self.assertEqual(len(failure["failures"]), 1)
        retry = run(self.monitor, observations, today="2026-11-16")
        self.assertEqual(retry["checked"], [SOURCE])
        self.assertEqual(retry["skipped"], [])
        self.assertEqual(retry["failures"], [])
        self.assertEqual(run(self.monitor, {}, today="2026-11-17")["skipped"], [SOURCE])
        self.assertEqual(run(self.monitor, observations, today="2026-12-16")["checked"], [SOURCE])

    def test_local_metadata_observation_and_bounded_page(self) -> None:
        self.add_source("zzz-second-source")
        self.monitor.configure(
            "zzz-second-source",
            cadence_days=1,
            likelihood="Low",
            rationale="SYNTHETIC daily fixture",
            impact={"requirements": [], "journeys": [], "tests": [], "communications": []},
            actor="Juan Manuel Servera",
            role="rule_owner",
        )
        observations = {
            SOURCE: dict(
                content=(RAW + b"Local discovery").decode(),
                metadata={},
                provenance="SYNTHETIC local publication fixture",
            )
        }
        report = run(self.monitor, observations, today=DAY, limit=1)
        self.assertEqual(len(report["changes"]), 1)
        self.assertEqual(report["failures"], [])
        self.assertEqual(report["next_after"], SOURCE)
        second = run(self.monitor, {}, today=DAY, after=SOURCE)
        self.assertEqual(second["checked"], ["zzz-second-source"])
        self.assertIsNone(second["next_after"])
        for limit in (0, 101, True):
            with self.assertRaises(ValueError):
                run(self.monitor, {}, today=DAY, limit=limit)

    def test_cli_missing_observation_returns_nonzero_and_persists_failure(self) -> None:
        fixture = Path(self.tmp.name) / "observations.json"
        fixture.write_text(json.dumps({}))
        with (
            patch.dict(
                os.environ,
                {
                    "ZF_LAW_DB": str(self.path),
                    "ZF_LAW_BLOBS": str(self.blobs),
                    "ZF_LAW_STORE": "sqlite",
                },
            ),
            contextlib.redirect_stdout(io.StringIO()) as output,
        ):
            self.assertEqual(main([str(fixture), "--today", DAY]), 1)
        self.assertTrue(json.loads(output.getvalue())["failures"])
        self.assertEqual(len(self.monitor.changes()), 1)

    def test_job_has_no_approval_or_activation_path(self) -> None:
        observations = {
            SOURCE: dict(
                content=RAW.decode(),
                provenance="Local fixture",
                metadata={},
                actor="agent",
                action="activate",
            )
        }
        with self.assertRaisesRegex(ValueError, "unknown observation"):
            run(self.monitor, observations, today=DAY)
        self.assertEqual(self.monitor.changes(), [])
