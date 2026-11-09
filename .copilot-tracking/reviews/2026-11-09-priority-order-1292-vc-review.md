<!-- markdownlint-disable-file -->
# Review: issue 1292 validation correction (2026-11-09)

**Executed**: once, after implementation, by an independent read-only `code-review` agent on the diff plus the implementing agent's evidence assessment. The coordinator's independent exact-head review and hosted CI remain mandatory. Boundary: whole candidate against `origin/main` `76db469b1` (named fresh main `9814cf6b2`), owner-selected demo-targeted tier. Evidence: [changes](../changes/2026-11-09-priority-order-1292-vc-changes.md). The original independent C2 (5 High, 4 Medium) and C4 (1 High, 11 Medium) "Revise" outcomes and the recovery review are preserved and are not cleared by this review.

## This cycle

| Item | Outcome |
| --- | --- |
| MSSQL `test_challenge_edited_in_case_outside_generation_candidates` | Root cause confirmed and reproduced on `9814cf6` and the frozen start (`4 != 40`); a fixture defect (seeded SQL database ignores a rewritten seed). Corrected with a backend-neutral `reseed` helper and a fresh test-owned database; 10/10 and the whole resident MSSQL class (91, 1 JSON-only skip) green; no assertion changed. Resolved |
| API broad suite 7 import errors | Missing `playwright` (API dev extra not installed). Restored from `src/api/pyproject.toml` pins; 2031 run, OK, 0 errors, 363 opt-in skips. Resolved |
| Pinned type check | `mypy` whole package found one in-scope type error in this issue's test file; fixed. Resolved |
| Review agent | No significant issues. Unverified by it: state-dir interaction; covered empirically by the real SQL runs |

## Original Review-to-regression matrix

| Original finding (C2 / C4) | Regression | Where it runs | Status |
| --- | --- | --- | --- |
| C2 F1 zero-ordinal fence between reload statements; F2 rollback publishes cache; F3 clock step; F4 unresolved as latest | `SqliteLegacyEdges`, `SqlitePriorityOrder` | SQLite; the inherited `SqlitePriorityOrder` methods also pass on SQL Server (93 run, 0 skips) | Addressed on SQLite; SQL Server proves the inherited reload, edit, tie and interleave cases only |
| C4 F1 orphan events and tied sequences; F2 `rec_order_backfills`; F3 continuity exports; F5 singleton rollback; F6 committed reload; F7 note; F9 `ai_task` quarantine; F10 and F11 bounded cost; F12 and F13 digests | `SqliteC3Corrections`, `SqliteC4Corrections` | SQLite only | Addressed on SQLite only, not on SQL Server; not claimed |
| C4 F4 partial BEGIN | `MssqlBeginRecovery` | Real `_Conn` with a fake driver, SQL Server run | Fake adapter, so real SQL Server BEGIN timeout behaviour stays unproven |
| C4 F8 fixture admission | `LoopbackGuard` plus this run | Admission succeeded through a real labelled container, manifest and `docker inspect`; negative cases by unit tests | Real provisioning path now exercised once (positive); remote-engine and spoof negatives remain unit-level |
| Resident decisions controls | `MssqlResidentControls` | SQL Server, corrected | Green; the former failure is a fixture defect, not a production defect |

## Open and not claimed

SQL Server scale, the ledger-enabled migration, the named data-owner resolution mechanism for flagged legacy order, the rolling-release (old writer) fence, the C2-C4 edge classes on SQL Server, the MSSQL-opt-in API classes (44 skips in `test_continuity_epoch_export` and `test_coordinator_api`), the full local gate (not selected), hosted CI, independent exact-head review, and every live or human acceptance step. Correction budget for #1292: 5 of 5 default cycles used; no further correction without an explicit issue-specific authorization. Use `Refs #1292`; #81 may proceed only after the coordinator accepts this source.

Outcome: conformant for the demo-targeted tier with the open items above; routed work is for later user-selected tasks, with no further Review in this task.
