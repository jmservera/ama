<!-- markdownlint-disable-file -->
# Release Changes: priority order 1292, correction cycle C4

**Related Plan**: [.copilot-tracking/plans/2026-11-08-priority-order-1292-c4-plan.md](../plans/2026-11-08-priority-order-1292-c4-plan.md)
**Base**: C3 head `dd8c71ca04e793b3c953c32d13e6ebbd5e90fc6d` (tree `ec90d255fd3e351d6645680f82cb397363a53522`)
**Research and plan commit**: `b90f49c16` (written before any source or test edit)

## Summary

Fourth and final authorized correction after the independent C3 review (4 High, 9 Medium; all 13 verified true in source).
Prior research, plans, reviews, C1 to C3 logs and earlier SQL results are unchanged and are historical for the new source.
Light SQLite, fake-adapter and static evidence only. No SQL Server, Docker, browser, heavy lock, full gate, push, PR or board write.
Disclosure: the three C4 research, plan and details files were written through a shell heredoc rather than the create tool; several C4 test and source edits were applied with small Python scripts.

## Changes by finding

| Finding | Change | Files |
| --- | --- | --- |
| F1 orphan events and tied sequences | `_proven_later` no longer uses the wall clock. A pair is proven only when both rows are unedited, both have an audit position and the audit order and the distinct insertion `seq` agree. | `sqlstore.py` |
| F2 C1 history | `_suspect_ranges` also reads and validates `rec_order_backfills`; any malformed entry makes every ordinal suspect. Ordinals are never changed. | `sqlstore.py` |
| F3, F7 projection and UI | `_export_record` applies the unresolved projection (`order_confirmed`, `actionable`, `relied_on`, `order_note`) and the limited summary keeps `order_confirmed`. The panel shows the note for every status and after a reload. Rejection and manual paths are untouched. | `continuity.py`, `app.js` |
| F4 partial BEGIN | `_Conn` rolls back a partly opened transaction or discards the connection, keeping the original error. SQLite is untouched. | `mssqlstore.py` |
| F5 singleton rollback | `_ambiguous_latest` confirms a batch only when the batch is mutually proven and the employee's previous newest record is not unresolved. Save and reload repair before publishing, so every row with an ordinal committed earlier. | `sqlstore.py` |
| F6 committed reload | `CommittedReloadError` after COMMIT when the reload does not settle; the priority and resolve endpoints return 409 with `outcome` `committed`. | `sqlstore.py`, `server.py` |
| F8 fixture admission | Literal loopback only, the published `HostIp` must equal the connecting address and port, and a remote `DOCKER_HOST`, TLS endpoint or non-default context is refused before inspection. | `sqlguard.py` |
| F9 quarantine | A rolled-back or never-started save drops pending `ai_record` and `ai_run_end` events naming a dropped record; unrelated entries are kept. | `sqlstore.py` |
| F10 repeated repair reads | New index `ix_recs_user_ord`; a small indexed page per touched employee replaces whole-history reads. | `sqlstore.py`, `mssqlstore.py` |
| F11 review cost | All batch rows are read in one query, coalesced, and swept once. | `sqlstore.py` |
| F12, F13 digests | The cache fingerprint is a content hash with an unreadable marker. Digests must be objects with an integer `count` of at least 1, a non-empty `head` and `sha256`; otherwise the evidence is unusable. | `sqlstore.py` |
| Docs | README section updated. #1288 also edits this file. | `src/core/README.md` |

## Test changes

* New `SqliteC4Corrections` and `MssqlBeginRecovery` (fake driver) classes in `src/core/tests/test_priority_order.py`; the SQLite class is deliberately not mirrored on SQL Server.
* The earlier `test_admitted_loopback_endpoint_is_accepted` was replaced by stricter tests: `localhost` and mismatched published addresses are now refused, which is an intentional policy change.
* All C3 tests pass unchanged against the C4 source.

## Evidence (retained in `.copilot-tracking/changes/logs/1292-2026-11-08-c4/`)

| Log | Exit | Result |
| --- | --- | --- |
| `red-c3-source` (new tests on a C3 source copy) | 1 | 28 tests: 26 failures, 9 errors (genuine red) |
| `green-priority-order`, `final-priority-order` | 0, 0 | 93 tests, 19 skipped (opt-in SQL Server, not run) |
| `green-test_resident_decisions` | 0 | 256 tests, 93 skipped (opt-in SQL Server) |
| `final-original-selector-resident` (`-k priority`) | 0 | OK, 3 skipped |
| `green-test_sqlstore`, `_sqlqueues`, `_sqlreads`, `_taskqueues` | 0 | 18, 14, 15 and 21 tests |
| `lint-ruff-3`, `format-check-3`, `typecheck-mypy-3` | 0, 0, 0 | ruff, ruff format on the two test files, mypy |
| `node-check`, `final-diff-check` | 0, 0 | `app.js` syntax, `git diff --check` |
| `green-original-selectors` | 5 | no tests matched: wrong module list; superseded by `final-original-selector-resident`; kept as is |
| `lint-ruff`, `format-check`, `typecheck-mypy`, `lint-ruff-2`, `format-check-2` | 1 | line-length, format and typing findings in the new tests, fixed; kept |
| `api-priority`, `api-priority-2` | 1, 1 | api discovery with `-k priority`: import errors for unrelated modules; not claimed as passing |

## Not proven

* The two native SQL selectors of #1292, `MssqlPriorityOrder`, SQL Server lock timeout, `@@TRANCOUNT` and cross-connection write, SQL scale, the ledger-enabled migration and real Docker provisioning.
* The FULL local gate and receipt, independent exact-head review, hosted CI and current-base integration with #184 and #1288 (overlap in `src/core/README.md` and the priority panel).
* No HTTP-level test of the 409 committed outcome; the server wiring is checked statically.

## Open decisions (not taken here)

* The named data owner must resolve flagged legacy records; no mechanism exists and no order is invented.
* The rolling-release boundary for mixed-version writers.
