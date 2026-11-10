# Review: issue 111 inherited repair (2026-11-10)

Task `111-sensor-draft-inherited-repair-1110`. One Review, executed by the implementing agent (no new agents were permitted, so this is not independent). Root independent exact-head assessment is still required before publication.

## Execution and boundary

* Reviewed: uncommitted diff over frozen head `d5e7ac2ef560a09a7035ef55d038b40315313977` in `sensor_review_draft.py`, `test_sensor_review_draft.py` and `src/core/pyproject.toml`, plus the changes record and witness events 1 to 5.
* Evidence: `phase111-inherited-repair-evidence-1110/frozen-head-regressions.log` (4 new tests fail on the frozen head, 17 old pass), `lint-type.log`, `tests-working-tree.log`.

## Findings

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Info | JSON path: `save()` returning is the commit point, so memory is kept and `DraftAuditError` reports a saved draft with a missing audit record. Verified by tests for I/O and non-I/O audit failures, unrelated save and reload, and idempotent retry with original `created_at` and `created_by`. | Conformant |
| 2 | Info | SQL path control flow is unchanged in effect: audit, then save, rollback of list and pending audit when not committed, `CommittedReloadError` counts as committed. Covered on SQLite (failure before commit, conflict and retry). | Conformant; MSSQL not run |
| 3 | Low | A retry after an audit-after-commit failure returns the existing draft and does not write the missing audit entry. The existing Store contract has no way to replay one audit entry idempotently, so this is reported rather than hacked. | Open, later work (Follow-up) |
| 4 | Low | A non-`OSError` audit failure propagates unchanged (draft kept, message not draft-specific). Narrow catch avoids a broad `except`. | Accepted |
| 5 | Low | Live MSSQL was not run for the restructured SQL branch, by brief. | Open, later work if Root selects it |
| 6 | Info | Typing: no cast, `type: ignore`, `ignore_errors`, broad catch or success-shaped fallback. One override stanza (`disallow_untyped_calls = false`) follows existing precedent. `Any` appears only in the `Json` alias for schema-less payloads. | Conformant |
| 7 | Info | No change to approval, consent, gate, hold, hazard, ranking or task behaviour. No store, SQL, importer, server or UI file touched. | Conformant |

## Outcome

Execution: done once. Outcome: conformant for the two coupled defects at the stated tier, with findings 3 and 5 routed to later user-selected work. No further Review in this task.
