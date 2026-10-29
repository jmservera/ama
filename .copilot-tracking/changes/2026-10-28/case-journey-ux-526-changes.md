---
title: Case journey UX 526 implementation evidence
description: Changes, validation, amendments and handoff for the employee workspace
ms.date: 2026-10-28
---

## Scope and state

Full plan P01-P03, task 526. P01/P02 implemented; P03 validation blocked.
Plan/details and original one-pass critique remain canonical.
All PC-001..005 dispositions apply without a second critique.

## P01 workspace structure

P01-T01/P01-T02 implemented. New optional case-workspace.js derives all stages
and creates summary/stepper/manual tabs. caseView constructs nine retained
headed panels; open safety is single/live above tabs. Same-case tab changes
do not abort requests or invoke the discard guard. Other query/route changes
keep the existing guard. Same-case refresh preserves dynamic resident draft
nodes/record handlers and dirty controls; successful actions clear only their
own section. Case/identity departure disposes case-local state.
Missing or failed optional enhancement keeps stacked sections with explicit
status/error. Existing required-file recovery remains.

## P02 AI presentation

P02-T01 implemented. Draft/proposal warnings, explicit missing confidence,
Sources, review fieldsets/reasons/linked errors and native acceptance
restrictions are consistent. Assistant listing follows all case cursors;
ready nonstale outputs count as reviewable, other states do not. Local draft
records are deduplicated and update summary/tab together. Assistance failure
reports unavailable count, not a fabricated zero. Reviewed/stale proposals
are grouped in a details disclosure. Chat retains the explicit advisory/
separate-proposal review boundary.

## P03 validation and documentation

Baseline unit probe: 69 discovered, 53 import errors, distributions absent.
Installed existing declared project/dev extras into .venv; no manifest change.
Chromium availability probe succeeded: 156.0.8078.4.
Targeted semantics/static tests: 23 passed (journey/content/design-system).
API Ruff, format and project-scoped mypy passed (92 source files).
Eight journey tests execute the
shipped JavaScript in Node, including all 25 stages and evidence/blocker rules.
Heavy browser validation queued under the shared lock with 60-second retries.
P03-T01 implemented: one new semantic unit file and one focused browser check,
with explicit tab navigation added to existing checks. Supplied design is
indexed, log appended and API reproduction guide updated. Existing assistant
label/stale assertions are intentionally adapted under PC-003; no scenarios
or authority/domain-invariance checks removed. Ruff line limit 100 enforced
on the new files, and project-scoped mypy passed for modified typed harnesses.

### Exploratory browser attempts (preserved)

External root: /tmp/ama-526-evidence.
The first lock acquisition waited ten 60-second intervals; all attempts used
the shared nonblocking lock and a 40-minute ceiling.

* journey-01: failed at draft rendering after structural/keyboard/draft-retention
  checks passed. journey-03 exposed the actual 404: the reused workbench fixture
  had a document without `name`, causing the existing AI task source lookup to
  raise KeyError. Complete only this focused fixture's name/mime; do not change
  server semantics or claim a live AI run.
* journey-02: immediate URL assertion raced native Space activation. Add
  URL-condition synchronization, not a sleep or removed keyboard assertion.
* journey-04: passed dynamic AI edit/reason/record retention, loading axe,
  >50-proposal pagination and all blocked-state tabs, then failed the empty
  fixture. Playwright supplies a request as a second handler argument; it
  replaced the default state argument. Use a single-argument route handler.
* A targeted module test invocation omitted the existing `tests` import path
  for test_ui_support; this was invocation setup, not an application failure.
  Correct the test-module path; the required discovery command remains unchanged.

No failed result is represented as passing. Original logs/directories remain
external; the final local publication gate is still required independently.

### Final admission result and exact remaining boundary

The queued aggregate command exhausted all 40 nonblocking attempts at 60-second
intervals and exited 1. Its first command, journey-05, never started. Actual
shared-lock ownership was confirmed read-only with lslocks (python3 PID
4142039); no foreign output, container or process was touched.

Final lightweight results: 23 targeted tests passed in 1.936s; API Ruff and
format passed (47 formatted files); mypy passed (92 source files); actionlint,
JavaScript syntax and git diff --check passed.
The existing partial local run exercised the real loopback application and
saved a constructed case call into actual history, plus draft review and
keyboard paths. It is not a complete final-candidate browser result.

The exact full API discovery command, complete existing browser/axe suites,
new focused check through all states, actual 200% zoom, and final screenshot
inspection remain unverified. No final results.json or successful zoom evidence
exists. Exploratory blocked-state/loading axe observations do not establish the
entire requested accessibility check or human acceptance.

Implement does not advance through an unmet validation gate. The one independent
post-implementation Review is Not executed (outcome unavailable), not a passing
review. The full committed-candidate RPI gate, final external receipt,
current-main verification, exact-head assessment, push and PR are Not performed.
Preserve this implementation and supplied specification in the first local
commit; no publication is implied.

Resume after coordinated free lock ownership: run journey-05 in a new external
output directory, then the required full API discovery and existing
design-system/workbench, employee, assistant, provenance, regulatory/axe and
challenge variants. Preserve every adverse result. Only after P03 reconciles,
enter the one Review, commit original evidence, and run the complete local gate.

## Amendments and divergences

Chat answers lack a recorded-review API; use explicit existing proposal route.
No new journey/confidence field or made-up confidence value.
Existing-field review-signal chips use "Funding not confirmed", not a fabricated
funding mismatch. Return history/stage supplies the rework signal.
Minor extension: execute the new focused journey check in the existing src-api
browser CI step and retain its evidence; no existing check is renamed.
Actionlint and git diff --check pass.

## Remaining work and blockers

G-LOCK: shared heavy-lock admission exhausted its 40-minute ceiling.
Remaining local browser/API results, independent Review and publication gate.
Screen-reader, real staff usability and post-deploy verification are pending
the owner and are not claimed by synthetic local checks.
