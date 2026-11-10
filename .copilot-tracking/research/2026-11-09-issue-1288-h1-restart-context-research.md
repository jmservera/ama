<!-- markdownlint-disable-file -->
# Research: issue 1288 H1 restart-context diagnostic

Phase read-back `date -u` 2026-11-09T23:36Z, before any observation. Bounded verification H1 on frozen `e847e2cac` (tree `91567b86e`), base `a8593a7a8` (Quality `1b7a1719b` plus rubric only). E11 succeeded; E12 and E13 unused and not consumed. No source, schema, test or model change. The six H0 records and the failed H0 result (33 selected, 31 ok, 1 skip, 1 FAIL, exit 1) are immutable and are NOT retroactively passed. Refs #1288 only; later main `b613` resident fix is outside this assessment; 891 unmerged excluded.

## What H0 did

* `harness_sql_contract.py` `MssqlRestartHarness.test_h0...` snapshotted the first service (`self.service`), then built `Assistants(self.open_store(), ta.config())` and compared `after == before`. It failed on `flag_status` (`not-current` after, `review-suggested` before); cited IDs differ truncated in the retained diff.

## Context the first service had (read from source)

* `qs.Http.mock` sets `self.store.ai = CapturingProvider(...)` then `release_support.install(self.store)`, which sets model versions, `ai.release = store.release_context`, creates `assistant_releases` if absent and inserts synthetic `fx-*` active release rows bound to `runtime_binding(cap, ai)`.
* `MssqlFixture.open_store()` returns a NEW `MssqlStore` whose `ai` is the default unconfigured `Ai`, with none of the above wired.
* `Assistants.detail` (assistants.py about 978-998): `held = continuity.active(..., constructed=not isinstance(store.ai, Ai))`; `epoch_current`; `release_denial = self.admission(...)` or "activation release changed" when `body["release"] != release_reference(...)` (which uses `runtime_binding(capability, store.ai)` and `live=isinstance(store.ai, Ai)`); `actionable` requires `epoch_current`, not stale, no hold, state ready/accepted, no `release_denial`. `review_flag` yields `not-current` when `not actionable` and state is `ready`.
* Hypothesis (from source, unobserved): the H0 second service had a default `Ai` and no release install, so the release reference and live/constructed mode differ and `actionable` is false. The flag IDs persisted; the projection guard, not the stored data, changed the status.

## Discriminating observation (one case, no campaign)

On one fresh disposable SQL Server, after the first service creates the task and flag: record guard fields (`state`, `stale`, `epoch_current`, `release_denial`, `actionable`, `display_state`, flag status) and the ID sets for (A) the H0-style restarted service with the default Ai, then (B) a restarted service whose store gets the SAME fixture-supported synthetic provider and `release_support.install` as the first. Compare persisted rows through a fresh raw connection (task body output citations, `sensor_consumer_control` sensor IDs, count of `assistant_releases`) before and after. B installs only synthetic `fx-*` rows exactly as the fixture does; the real release is never activated and no guard is disabled.

## Limits

Synthetic provider is a local mock, not a model. Fixture install re-inserts the same synthetic release rows, so a before/after row comparison of `assistant_releases` is recorded, not asserted identical in id timestamps. Whether the actual production restart path builds this context is a separate production question this fixture proof does not answer.
