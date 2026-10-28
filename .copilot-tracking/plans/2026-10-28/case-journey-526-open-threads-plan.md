---
title: Case journey 526 open threads plan
description: Five further corrections for PR 529
ms.date: 2026-10-28
---

## Task Metadata

Task ID: 526-pr529-open-threads-20261028.
Slug: case-journey-526-open-threads. Implementation-ready after one critique.
Details: .copilot-tracking/details/2026-10-28/case-journey-526-open-threads-phase-details.md.

## Executive Summary

Close the five verified review defects without changing stepper semantics,
approval authority or visual design. Reuse snapshot reconciliation, preserve
post-dispatch review edits against the reviewed record, and synchronize native
step links with challenge history URLs. Correct the 38-scan receipt contract.
The no-Azure constraint prevents the required full publication gate; retain a
local commit for coordinator publication rather than bypass it.

## User Decisions and Requirements

* Full research, plan, implement, review loop in the requested existing branch.
* Fix all five open Copilot threads, add regressions and inspect sibling patterns.
* Preserve pending edits, submitted text, record identity and retained tab behavior.
* Run API units including workspace scripts and journey; gate-tool units; journey axe.
* Nonblocking shared heavy lock, retries bounded to 40 minutes. No az/Azure or secrets.
* Ruff 100 columns; no workflow changes; normal push only if publication is eligible.
* Commit dated artifacts, Conventional Commit and supplied Copilot trailer.
* Keep `Refs #526`, with no closing keyword; reply/resolve only after safe publication.

## Goals

Prevent unsaved-edit loss and unnecessary full-route tab navigation. Restore exact
unit and receipt contracts and leave reproducible validation and independent review.

## Scope and Non-Goals

In scope: app.js, case-workspace.js, panels.js pagination hook, owning API tests,
journey browser harness, tools/rpi-checks.py and tools/test_rpi_checks.py, related API guide.
No workflow, server authority, CSS, schema, external provider or private-data changes.

## Functional Requirements

* Both navigation and unload use reconciled DOM/pending dirty state; tab-only exempt.
* Route VM supplies case globals and exercises pending-only, clean and tab paths.
* Dispatch values remain immutable; newer document text/reason remain labelled,
  copyable and dirty, without enabled actions for a completed review.
* Journey anchors preserve every non-tab query parameter after pagination.
* Receipt verification accepts exactly 38 scans and rejects wrong counts/violations.

## Non-Functional Requirements

Native anchors, accessible labels/status and existing keyboard/stepper behavior
remain. No new dependency or abstraction layer. Python additions <=100 columns.
All heavy checks acquire the named lock with `flock -n` and finite retry.

## Acceptance Criteria

Focused executable regressions cover each defect, API suite and tooling suite pass,
journey emits exactly 38 pinned axe scans without serious/critical violations or
page errors. Sibling inspection is recorded. Original adverse results are preserved.
Independent Review execution and outcome are distinct from hosted/human approval.
Unresolved in-scope findings or failed mandatory checks block acceptance and must
be named in the handoff even if a local checkpoint commit is created.

## Sources

.copilot-tracking/research/2026-10-28/case-journey-526-open-threads-research.md
owns C1-C7/W1-W2 and the five thread IDs.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct and regress the five threads

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Shared dirty check and route harness

Reuse rememberCaseFields and supply required VM globals with behavioral regressions.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Document review race and sibling inspection

Compare dispatch snapshots, preserve newer read-only recovery by record, retain
submitted replacement and disable completed review actions. Inspect related paths.

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Journey query and receipt contracts

Synchronize hrefs at selection/render and in-place pagination. Correct exact count
and add negative receipt coverage. Keep all step names, states and routing targets.

<!-- rpi:phase id=P02 -->
### [ ] P02: Validate and deliver evidence

Depends on P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run requested checks

API discovery, focused Node-backed tests, gate tooling, Ruff and JS parse; locked
journey/axe, with immutable external logs. No full gate if it invokes prohibited az.

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Independent Review and commit

One independent post-implementation Review, commit source and original dated
evidence. Publish/reply/resolve only if required full gate permits; otherwise
explicit coordinator local-only handoff.
Implementation and mandatory local validation are ready for Review; this marker
remains open only for Review execution and local commit/handoff bookkeeping.

## Locked Test Ownership and Targets

Canonical targets are existing shipped JS and owning tests, not generated bundles.
Removals: none. Maximum additions: eight unit test methods across existing test
files and bounded assertions inside the existing journey browser harness; no new
browser scans or suites. API owns semantic/navigation/review regressions, tooling
owns exact receipt output shape. Browser regressions execute actual DOM and delayed
responses, not source-string proxies. Existing journey semantic tests stay intact.

## Dependencies and Blockers

Existing .venv and pinned axe/Chromium. Full gate az dependency blocks publication,
not independent local testing or commits. Research Ready; no unresolved user choice.

## Critique Disposition

One independent critique executed, original verdict Revise retained at
.copilot-tracking/reviews/plans/2026-10-28/case-journey-526-open-threads-plan-critique.md.

* PC-001 rejected: the worker asserted an execution-specific /tmp prohibition
  that does not apply to the parent. User explicitly requires the actual shared
  /tmp/ama-rpi-heavy.lock; silently relocating it would violate that direction.
  Keep the approved nonblocking shared lock and bounded external scratch.
* PC-002 applied directly: unresolved in-scope findings block local acceptance,
  distinct from unrelated follow-ups and the existing publication blocker.
  Preserve the one original Review outcome; no repeated critique.

## Follow-Up Items

Coordinator publication after complete current-base exact-head gate remains a
conditional handoff, not a local success or authorization to use Azure.
