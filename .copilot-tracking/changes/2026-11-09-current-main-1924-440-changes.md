<!-- markdownlint-disable-file -->
# Changes: current-main 1924 issue 440 checkpoint (2026-11-09)

Plan: [plan](../plans/2026-11-09-current-main-1924-440-plan.md). Details: [details](../details/2026-11-09-current-main-1924-440-details.md). Critique: [critique](../plans/2026-11-09-current-main-1924-440-critique.md) (Revise, PC-001 to PC-004 applied).

## Files changed

* `docs/architecture/cutover-evidence-pack.md`: appended dated section "Integrated current-main journey checkpoint (2026-11-09, Refs #440 #81 #123 #184 #136)".
* `docs/reference/README.md`: one index paragraph.
* `docs/reference/log.md`: one appended entry.
* No source, test, workflow, infrastructure, issue, PR or board change.

## Checks run (sanitized `env -i`, task-owned venv with this worktree's editable `src/core`, `src/agents`, `src/api`)

| Id | Scope | Exit | Result |
| --- | --- | --- | --- |
| A1 | `src/core` unittest discover | 0 | 628 ran, 111 skipped (108 need SQL) |
| A2 | `src/api` unittest discover | 1 | 36 errors: `node` missing from my sanitized PATH (self-inflicted fault, retained, not counted) |
| A2b | `src/api` rerun with `node` on PATH | 0 | 439 ran, OK, 59 skipped (58 assistants SQL, 1 opt-in Chromium) |
| A3 | `src/agents` queue and worker tests | 0 | 30 ran, OK |
| S1 | `MssqlResidentControls` on disposable SQL Server 2022 behind a nonqueued `flock -n` heavy-lock admission | 0 | 108 ran, OK, 1 by-design skip, 528 s; container removed, leftover query empty |

Totals of A1, A2b, A3, S1: 1205 ran, 0 failures, 171 skips.

## Limits

* No browser, assistive-technology, actual-model, Azure, live or private-data run. Playwright was not installed in the venv.
* A2b output contains 37 handled fail-closed tracebacks ("law store is not loaded"); no defect asserted.
* SQL beyond S1 is not rerun; #1326 evidence is reused by source identity only.
* No defect or refactoring need confirmed; no issue proposed.

## Qualification Q1 (appended 2026-11-09 after frozen head `3965fa489`; original text above unchanged)

Prospective records: [q1 plan](../plans/2026-11-09-current-main-1924-440-q1-plan.md) and [q1 details](../details/2026-11-09-current-main-1924-440-q1-details.md), committed as `1a7e994fe` before any edit.

* S1 deviation: the original plan and details selected only sanitized SQL-off A1 to A3. S1 was selected afterwards without a recorded prospective amendment and is not an ordered phase. Rationale is only what the brief allowed (one distinct necessary heavy check under nonqueued shared-lock admission); no other authority is inferred. S1 is broader than the #1326 two MSSQL methods plus four parity tests. The coordinator withdrew its overbroad no-coverage claim in issue 440 comment 6750088725, preserving 6749815210. The "no SQL rerun" wording elsewhere in the state record is historical and is superseded by this entry.
* Retention: the producer removed `/tmp/i440-1924-opq5ok`, so "logs retained in scratch" is superseded. A-series originals survive at the coordinator `observed-440-1945-logs` (readback OK). S1 raw retention is unverified; no copy located; nothing reconstructed. The S1 summary rests on the historical producer transcript.
* Count: four final processes A1, A2b, A3, S1 (including one SQL run), 1205 discovered, 171 skipped; A2 separate; the 108 S1 discoveries are not all SQL executions.
* The scratch cleanup listed above is historical; no cleanup, rerun or source change occurred in Q1.

Files changed in Q1: `docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md`, `docs/reference/log.md`, research (append), this record, state (append), Q1 plan, details and Q1 review record (the original review and critique files are untouched). Original review and critique files are untouched.
