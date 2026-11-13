# Plan: Live SQL 2028-01-01 cutoff apply and verify (Refs #521 criterion 4)

Research: [research](../../research/2026-11-13/521-live-sql-2028-verify-1554-research.md). Details: [details](../../details/2026-11-13/521-live-sql-2028-verify-1554-details.md). Tier: Focused (live SQL change, owner decision recorded; no source change).

## Phases

* [x] 1. Probe: render check, DNS, TCP 1433, token-authenticated connect, read current `ck_allowed_case_window` definition (read-only). Token in memory only.
* [x] 2. Apply (only if reachable and the database is identified): run the idempotent constraint transaction only, then read back `sys.check_constraints`.
* [x] 3. Record redacted evidence in the changes file; if blocked, record the exact probe result and leave criterion 4 unticked.
* [x] 4. Run `test_cutover_audit`, secret scrub (0 hits), remove only `/tmp/venv-*` directories created by this task (none).
* [x] 5. Independent `code-review-security`, then local commit with trailer; `commit-complete` witness. No push, no issue edits.

## Gates and constraints

* No firewall, RBAC or private endpoint change. No row window updates. No view or grant batch (needs resident client id).
* Never print, log or commit a token, server secret or subscription id.
* A dry-run render check precedes the apply; the apply aborts if the rendered constraint lacks `2028-01-01T00:00:00`.

## Critique (rubber-duck, executed once): approve with changes; all applied

| Id | Disposition |
| --- | --- |
| PC-001 | Applied: single non-master database must be unambiguous from `az sql db list`; verify `DB_NAME()` and server on connect; stop if more than one candidate. |
| PC-002 | Applied: record `git merge-base --is-ancestor` evidence that the 2028 `AUTHORITY_END` source is on `origin/main` before applying. |
| PC-003 | Applied: read back object, enabled and trusted flags and full predicate; after any error or disconnect reconnect and re-read; unreachable is recorded as unknown. |
| PC-004 | Applied: count rows with `valid_to` beyond the cap (count only) before applying; on failure re-read the original constraint; never modify rows. |
| PC-005 | Applied: record sanitised error categories only, no raw CLI output, connection strings or exceptions. |
| PC-006 | Applied: remove only `/tmp/venv-*` directories created by this task. |
