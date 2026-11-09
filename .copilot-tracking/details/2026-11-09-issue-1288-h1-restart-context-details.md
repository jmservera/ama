<!-- markdownlint-disable-file -->
# Details: issue 1288 H1 restart-context diagnostic

Plan: `.copilot-tracking/plans/2026-11-09-issue-1288-h1-restart-context-plan.md`. Readback `date -u` 2026-11-09T23:37Z.

## Harness (external, `harness_h1_restart_context.py`)

* Class `MssqlRestartContext(Fresh-like helper, ta.MssqlFixture, qs.Http)`; one test selected by explicit id.
* Setup as H0: `self.ready()`, `tid, _ = self.proactive()`.
* `observe(service)` returns: detail fields `state`, `stale`, `epoch_current`, `release_denial` (missing list or None), `actionable`, `display_state`, flag `status`, sorted `sensor_cited_ids`, sorted reading and sensor ID pairs, `snapshot.citations` sensor keys, and per-role `service.sensors` ID sets (refused roles recorded).
* Raw fresh-connection reads: `assistant_tasks` body output citations and state for `tid`, `sensor_consumer_control` sensor IDs, `COUNT(*)` of `assistant_releases`.
* Sequence: raw snapshot; observe first service; A = `Assistants(self.open_store(), ta.config())` observe (recorded, not asserted); raw; B = `store2 = self.open_store()` with an independent `CapturingProvider()`, `model_version` and `model_version_strong` = `test-model`, `ai.release = store2.release_context`, no database writes (amended after the critique); observe; raw; assert B equals the first service on every observed field and the raw snapshots are identical across all three points; A's differences are recorded with their guard fields.
* Outputs `h1.json`; all services stopped in cleanups; wrapper `sql-run-h1.sh` is the E5-style one-shot admission with a fresh `mktemp` scratch and venv, container removed on exit.
