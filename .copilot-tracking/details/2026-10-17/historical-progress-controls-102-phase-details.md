---
title: Historical progress controls 102 phase details
description: Task-level evidence and completion boundaries
ms.date: 2026-10-17
---

Task 102 / historical-progress-controls-102. Initial direction: research C1-C11,
read-only bounded reporting, no unrecorded clocks or new lifecycle writers.

<!-- rpi:phase id=P01 -->
## P01: Report baseline

<!-- rpi:task id=P01-T01 -->
### P01-T01

Add src/core/src/zava_forward/core/progress.py with typed pure functions for
UTC input validation, exact existing return/reopen and handoff normalization,
independent interval derivation, report metadata and scenario queue simulation.
Read histories without mutation. Do not parse `history` narrative or audit
prose. Missing source/version/actor or unsupported records produce exceptions.
Conservative coverage state must prevent claiming complete historical totals.
Only source-authorized exact stages and handoff states map; no fuzzy synonyms.
Durations are seconds, calendar elapsed, no invented business-day/pause rules.
Period clipping must be explicit; open intervals are censored, not completed.
Source locators may be shown; raw source references and personal free text
must not leak. Preserve role-specific projections using need checks.

PC-102-002 normalization matrix: `returns` records must have aware `at`,
positive sequential version and exact STAGE_ORDER from/to labels (Completed
permitted as source-proven reopen origin). Boolean `reopened` distinguishes
return/reopen, never a narrative synonym. Only Contact paused and Resident
paused works classify paused intervals. Exact handoff states: Offered,
Received, Escalated, Accepted, Declined, Withdrawn, Completed. Offered starts
offer wait; Accepted/Declined/Withdrawn terminate it. Completed is retained
separately after acceptance, never a second acceptance. Missing predecessor,
invalid/duplicate/out-of-order version, unsupported state, ambiguous same-time
stage transitions or broken chain creates an explicit exception and null clock.

Scenario uses selected cohort size as an explicit hypothetical ready count
only when requested; default forecast unavailable without declared ready count.
Validate count <= selected denominator. No current stage implies installation
readiness, handover acceptance or capacity. Two sequential stages and independent
pools with positive integer weekly capacities and duration. Show four-week
central and one/three capacity plus two-week stage-duration sensitivities.
Source data limits distinguish declared scenario from validated committed
resources. Forecast never adds predicted events to observed timelines.

<!-- rpi:task id=P01-T02 -->
### P01-T02

Add Store.progress_report adapter using `_filtered` under existing lock.
Validate allowed views and filters rather than unknown-view scope expansion.
Default deny report roles even on direct calls. Add `report=progress` to
GET /api/stats and GET /api/cases.csv. Parse same options for both. Preserve
all default endpoints. CSV two columns `section`/`value`, with JSON cells so
every metadata/list field round-trips without formula-leading user content.

PC-102-001: staff roles in projection.STAFF_ROLES only, direct Store and HTTP,
before cohort selection. Contractor/unknown roles denied. Manager-only closed
view preserved. PC-102-003: schema progress/v1, fixed report top-level section
order, ascending case IDs and UTC/version-ordered events; compact sorted-key
JSON cells, UTF-8 CSV with LF newline. CSV rows reconstruct the exact semantic
report and identical requests produce byte-identical exports.

<!-- rpi:phase id=P02 -->
## P02: Evidence and validation

<!-- rpi:task id=P02-T01 -->
### P02-T01

Own fictional event fixtures in new test files; do not edit dataset.py or other
issue tests. Test UTC offsets, inclusive as-of, malformed and naive times,
out-of-order/version/gaps, inconsistent/same-time stages, missing offer,
receipt not acceptance, censored interval, pause/resume inferred only from
explicit stages, repeated reopening, zero events and empty denominator.
Assert identity/source/notes sentinels withheld. Compare entire CSV round-trip
to visible JSON report, not only row counts.

<!-- rpi:task id=P02-T02 -->
### P02-T02

Install editable packages in worktree .venv with pip. Run focused new suites
plus existing handoff/workflow/role/ledger tests. Run project configured ruff
and mypy. Use a unique issue-102 SQL Server container published only on
127.0.0.1 and a dedicated test database. Never inspect unrelated containers'
environment or credentials. Reopen store, external writer refresh and audit
invariance must be checked on SQLite and actual MSSQL. Build source API image,
run as UID 10001 and probe loopback health/report behavior if feasible.
Log environment failures honestly; clean up only own named resources if
authorized (caller prohibits resource deletion, so retain stopped own container).

<!-- rpi:task id=P02-T03 -->
### P02-T03

Update core/API README contracts, existing programme journey synthesis and
KB index/log without rewriting upstream history/routing. No private datasets,
staff roster, legal-currentness or company validation claims.

<!-- rpi:phase id=P03 -->
## P03: Review and publication

<!-- rpi:task id=P03-T01 -->
### P03-T01

Activate rpi-review once against completed implementation and original acceptance,
plan/research/changes. Preserve exact original review artifact and outcome.

<!-- rpi:task id=P03-T02 -->
### P03-T02

If concrete defects are found, record correction ONE/TWO in changes/state,
fix and run targeted checks. Do not relabel the original Review as passed,
run another full Review or claim independent coordinator closure.

<!-- rpi:task id=P03-T03 -->
### P03-T03

Resolve gh api user fresh, local privacy-safe email for author and committer;
Conventional Commit with required Copilot trailer. Stage only owned paths.
Normal topic push; main PR Refs #102, no closing keywords without full proof.
Record exact head, PR, validation limitations and session resume ID.
No merge/rebase/force push or other checkout changes.
