---
title: Loading and HAX briefing phase details
description: Evidence-based task contracts for issue 531
ms.date: 2026-10-28
---

## Authorized rebased continuation (2026-10-29)

The coordinator authorized rebase, independent review and correction of the
result, without push. Parent is `27d11262`. The rebased independent assessment
confirmed RV-001/002/003 remain open; the original Review is preserved.
P02 captures rules fragments/references before generation, protects unsaved
briefing review values with explicit discard confirmation, and blocks refresh
and mode replacement during pending or history-blocked reviews. P01 places
form and briefing announcers outside busy subtrees without replacing existing
pending/disabled ownership. P03 adds targeted regressions, runs source-local
API discovery and locked journey/assistants/briefing browser checks with axe.
Continuation complete: source-local API discovery passed 1215 tests with 316
environment-dependent skips. Loading/briefing, journey and assistants checks
passed with 4/42/40 zero-violation axe scopes; employee briefing and workspace
script recovery passed. Corrections and regression evidence are in the changes
record; original Review outcome is unchanged. No push or publication receipt.

<!-- rpi:phase id=P01 -->
## P01: Loading and action feedback

<!-- rpi:task id=P01-T01 -->
### P01-T01: Static shell and shared async lifecycle

C1/C2: render fallback before all blocking scripts. Early shell watchdog must
not depend on app.js or the new helper and must expose retry without inline
script handlers. Mark ready only after session/login is usable. Preserve
existing bounded script recovery. Shared helper observes returned promises,
deduplicates controls/forms, announces immediate text and adds spinner after
200ms. Finally clears timers, restores owned state only and surfaces uncaught
errors. Existing action-specific catches retain their specific messages.
Wire direct account/import/filter listeners and await fire-and-forget redraws.
Initial routes and independent panels must not have empty containers while
waiting. Abort paths may be silent only when the obsolete region is gone.

Integration inventory (PC-001): h click/submit/change handlers across app,
panels, ops, assistants, chat, timecapture and role screens; direct account,
CSV import, queue filter/search/sort listeners; ops appointment submit must
return its mutation promise. Standalone law.html loads the shared helper and
law.js wraps each direct click/form action. Leaflet refresh is non-control
work: existing map loading/status plus busy/spinner, without disabling links.
Review direct callbacks for dropped promises, not merely async declarations.

Implementation complete: helper timing/state ownership and real delayed
draft/appointment/law/map paths passed; existing script recovery passed.
Completed startup placeholder is removed, leaving one document h1.

<!-- rpi:phase id=P02 -->
## P02: Briefing and review interaction

<!-- rpi:task id=P02-T01 -->
### P02-T01: Statement metadata and HAX interface

C3: preserve raw model statement-to-citation association before analyse strips
markers. Never fabricate associations from the flattened citations list.
Rules template statements can be derived directly from the actual three input
cases. Add timestamp at generation, not every cache read. No review mutation
authority change. Three outcome choices accept as draft, edit draft, reject
draft; accept has no text field, edit shows larger draft and required reason,
reject shows larger reason only, cancel retains local fields. Server still
checks reason, source freshness and one-time review. Local dismissal/show is
the only undo. Render source case links only from server-provided scoped IDs;
unresolved references remain text, not navigation authority.

PC-002 invariant: metadata describes only final shown text. Preserve filtered
bullet semantics and publish fence. Template/quarantine output gets actual
template attribution or explicit attribution unavailable, never abandoned AI
references. Generation timestamp has UTC offset and remains stable on cache
reads. Deterministic tests cover valid/unresolved marks, dropped bullets,
fallback, zero/fewer-than-three cases, quarantine and cache stability.

Implementation complete: focused JSON/SQLite task tests and actual browser
source/type/time/conditional-review checks passed. Published source case IDs
bound case links, including single-case labels without an explicit case prefix.
Whole-bullet validation runs before statement splitting.

<!-- rpi:phase id=P03 -->
## P03: Validation and handoff

<!-- rpi:task id=P03-T01 -->
### P03-T01: Unit/browser/axe evidence and documentation

Use an owned venv with installed src distributions and constructed loopback
fixtures. Focused API/core unit checks, existing briefing/script/journey checks,
new delayed shell/action/review/browser regression, pinned axe 4.10.3 and
reduced-motion/reflow. Lock heavy checks via repeated `flock -n` admission,
stop after 40 minutes rather than bypass. Ruff line length 100 for new Python.
Preserve failures and actual command exits. Run original independent RPI
Review once, route findings, commit original evidence before final full gate.
No az invocation even if installed. If full gate requires az, leave commits
local for coordinator; do not publish with partial evidence. PR draft uses
`Refs #531`, parent base and dependency explicitly.

PC-001/003 checks: extend the one new browser check to actual appointment and
law actions with delayed/error/duplicate controls, plus map region feedback.
Migrate case_journey_browser_check.py document review to choose edit, fill and
submit separately while preserving delayed dispatch and later-edit recovery.
Test cancel/reopen and external getText-backed resident draft payload equality.

Current validation: required briefing, workspace scripts and case-journey
checks passed; final shell/loading check has four zero-violation axe scopes,
assistants has 58 passing browser checks plus axe, and design/workbench role
checks passed. Full API discovery passed 1178 tests with 316 environment-dependent
skips. Existing workbench mode/
retry and case-journey Node assertions were migrated without removing checks.
Full publication gate, parent reconciliation, SQL Server and human/deployed
acceptance remain outside these local passes.

P03 implementation/validation handoff is complete. Original independent Review
completed once, execution Complete and outcome Not accepted. RV-001/002/003
are routed to later implementation, not marked closed by these completed
execution markers. RV-004 remains separately owned residual acceptance.
