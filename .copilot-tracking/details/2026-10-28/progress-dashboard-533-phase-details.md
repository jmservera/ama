---
title: Progress dashboard phase details
ms.date: 2026-10-28
---

Task #533, progress-dashboard-533.

## P01: Server read models

P01-T01: under store.lock, read refreshed cases/recommendations. Dashboard
admission is case-local, not a global metadata flag (SQL does not retain every
seed metadata key). Reconstruct labelled Identified/Accepted handover/
Withdrawn/Excluded simulation actions plus human_home_case_closed and
controlled reopen events. Deduplicate same-state repeats; do not infer
opening from stage_since. Expose missing coverage. Duration uses known open
to closure per episode and nearest-rank p90, no sample => null.
Current journey uses the six step groups in case-workspace.js; unknown stages
remain Unknown. Group by owner_role with Unknown fallback.
Current overdue uses existing store.work_context, not new statutory clocks.
Imported Reopened - aftercare is an open transition. Opened counts initial
plus reopened episodes; report reopened separately for clarity. Duration
resets at each reopen. Archive uses latest observed closing transition;
unknown/contradictory dates never derive from stage_since. Undated rows are
included in unbounded archive, excluded with bounded dates, counted visibly.
Archive status is explicitly Recorded case status (stage).
AI records require is_synthetic=true plus nonempty all-admitted case_ids;
task=briefing and source=ai, review resolved_at in selected UTC day range.
Accepted/Edited/Rejected are review outcomes (Edited displayed Changed), not
approval. Unknown dates and unreviewed are explicit. Real-activity-shaped
unmarked records referencing synthetic cases remain excluded.

P01-T02: server maps endpoints to existing cases/stats permission kinds, with
manager check again in archive read. Preserve legacy /api/cases untouched.
Reject unsupported query keys/duplicates and invalid bounds. Construct fixtures
in public test code; JSON and SQLite read paths prove refreshed-lock semantics.

## P02: Native employee surfaces

P02-T01: small router/script recovery seams only. /progress.js owns progress
and closed renderers. URL query names start/end for dates, status/team/q/page
for archive. Accessible labelled controls use submit rather than per-keystroke
fetch. Cancel obsolete responses through existing route signal and recheck
before rendering. Tables have caption, scoped headings, named focusable scroll
regions. Bars show counts as text, no colour-only series. Loading, empty and
explicit error/retry states must differ.

P02-T02: browser harness owns temporary synthetic Store/server; isolate
environment from inherited model/data settings, use loopback only. Axe 4.10.3
matches existing pinned SHA256. Check URL reload/history, all chart/table
parity, paging/filter reset, status safety marker, denied roles and stale route
response. No private generator input or cloud service.

## P03: Validation and review

P03-T01: use /tmp/ama-533-venv (created after default Python lacked installed
namespace); existing pip dev dependencies installed. Heavy admission uses an
owned flock descriptor and nonblocking retry <=2400 seconds, no foreign process
interruption. Run new tests first, related regressions then API discovery,
Ruff (100-column new Python), mypy and node --check.

P03-T02: activate rpi-review once; independent fresh worker reads bounded diff
and evidence, writes review only. Preserve original critique and Review even
if adverse. Commit with authenticated noreply email and Conventional Commit
trailer. Full local gate and hosted/human approval remain separate; no push/
PR when full gate requires prohibited az. Provide prepared stacked PR text
in changes artifact.

## Execution Reconciliation

P01/P02 and P03 executed; local commit preserves original critique and one
Review. New browser harness covers manager paths; denied-role coverage is in
HTTP tests and all-role inventory, not claimed as browser coverage.
Review Complete / Defects found: RV-001 Medium date-field association/focus
and RV-002 Low aria-busy remain later rpi-implement work. No source corrections
or repeated Review were performed after that assessment. Full gate, parent
reconciliation and human acceptance remain distinct publication boundaries.
