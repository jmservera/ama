<!-- markdownlint-disable-file -->
# Changes: issue 1288 merged-main SQL contract verification

Written 2026-11-09T23:28Z (read back with `date -u`). Refs #1288 only. Verification, not a correction cycle: E11 succeeded; E12 and E13 are unused and unchanged.

## Source change

None. No source, test, schema, workflow or shared-doc edit. The only repository changes are the dated records under `.copilot-tracking/`.

## Identities

* Checkout: `a8593a7a8` (equals origin/main), tree of the observed source `5113adcb2...`. The diff to Quality merge `1b7a1719b` is `.github/rubric/scores/latest.json` only; `src`, `infra`, `tools` and workflows are unchanged. Executable provenance is `1b7a1719b`.
* Records head before this commit: `815e384cf` (tree `d5b952dd...`, clean).
* Unmerged 891 Core/AI changes are excluded.
* Disposable SQL Server 2022 RTM-CU27-GDR 16.0.4305.5, image `sha256:cf8f0ab2ebe6...`, container `70b1e984829f...` on 127.0.0.1 only, removed on exit (0 left). Admission: one `flock -n /tmp/ama-rpi-heavy.lock`, exit 0, no holder present, no queue or retry.
* Owned env: `/tmp/ama-1288-sqlproof-*/venv` (hash-locked `src/api/requirements.txt`, then editable core/agents/api from this worktree). `/tmp/e8venv` not used.
* External harness `harness_sql_contract.py` sha256 `166e9406f723...` (not shipped, not a test edit). Raw logs (external, not committed): `logs-merged-sql-proof-1109/sql-run/`; `api.stderr.txt` sha256 `ba1995df09bc...`, `observations.json` sha256 `0f8358d4dce0...`.

## Observation (one SQL run, exit 1)

33 explicitly selected tests: 31 ok, 1 skip, 1 FAIL, 0 errors. Run time 97.4 s.

* Existing exact-source refresh (30 tests, ok except the skip): `test_quality_sensors.MssqlHttp` six selected tests, `MssqlReadModel.test_latest_is_in_the_captured_source_and_citations`, `test_quality_sensors_e1.MssqlDirectControlWrites` (6) and `MssqlManualAndProactive` restart test, `test_quality_sensors_e2.MssqlBoundary` (10 ok plus the 1 SQLite-only skip "the cross-process SQLite withdrawal is SQLite-only", not waived) and `MssqlCursor` long-history restart test.
* H2a (direct `fence_send` after the SQL-clock expiry): ok. Admission succeeded; after expiry `DispatchWithdrawn` with "Operator authority/allowance has expired."; exactly one `send-refused` event visible on a fresh raw connection; attempt still `reserved`; settle set `active_until=0` with the debit kept (1 call, 12600 tokens); a second `begin_call` declined with the same reason without a new attempt or debit; peer accepts 0, bytes 0.
* H2b (real `Ai.evidence` path with the existing lane, counting meter, local TLS peer, valid synthetic reply): ok. Result `not-sent` / `suspended-before-dispatch`; meter reserved/checked 1/1, token 1 (these fire before the transport fence by design); peer accepts 0, bytes 0; one committed `send-refused` event visible on a fresh connection; attempt settled `suspended-before-dispatch`, `active_until=0`, one debit.
* H0 (IDs and role projection across a restart): FAIL at the comparison `after == before`. The restarted service's flag status was `not-current` against `review-suggested` before. Cause not established from the retained output, which truncated the diff.

## Limits

The H0 harness built the restarted `Assistants` from a plain second store, which may lack the release/epoch context the fixture installs on `self.store`; `actionable` in `assistants.detail` depends on that context (`release_denial`, `epoch_current`). That is a hypothesis, not a finding. One SQL exercise was authorised and no retry was made, so H0 stays inconclusive; it is not a defect claim and not a pass. The in-process slot checks are not database readbacks. Provider simulation is code-OFF; the TLS peer is a counted synthetic stub, not a model or release approval. No hosted CI covers the Quality MSSQL classes.
