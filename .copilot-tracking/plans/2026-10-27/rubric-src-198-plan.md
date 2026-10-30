---
title: Rubric src cut-over implementation plan
description: Scoped test repairs and truthful issue 198 evidence
ms.date: 2026-10-27
---

## Task Metadata

* Task ID: 198
* Task slug: rubric-src-198
* Planning status: Ready; single critique Complete / Revise, directly dispositioned
* Details: .copilot-tracking/details/2026-10-27/rubric-src-198-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-27/rubric-src-198-plan-critique.md

## Executive Summary

Verify the already-delivered src registry and repair migration-stale tests.
Publish a durable score/sequencing ledger and correct current rubric guidance.
Preserve production registry, gate, workflow/check names and rubric_version.
Use Refs #198: unavailable historical scorecards and the originally prescribed
dedicated registry sequencing cannot be fabricated or retroactively achieved.

### What You May Not Know

The legacy include globs were already removed by #295/#300/#302. All M1-M6
merge snapshots carry the same 47-point assessment, not fresh migration
scores. #499 has actual 77 vs 77 hosted evidence. The current suite has
18 failures, not the historical 19; one deck-selection mismatch is unrelated.

## User Decisions and Requirements

* Run Research, Plan, Implement and Review in order with dated artifacts.
* Keep src layout, human/resident boundaries, workflow names and rubric version.
* Local validation only; no full gate, no cloud or private datasets.
* Commit, push the existing topic branch and open one draft PR to main.
* Prove criteria before ticking; otherwise use Refs #198.

## Goals

* Make src and retired-path coverage executable and migration evidence truthful.
* Re-assess the old failures without concealing unrelated failure or skips.

## Scope and Non-Goals

In scope: existing rubric test modules, rubric README, cut-over evidence pack,
knowledge-base index/log and dated RPI artifacts. No application code is needed.
Non-goals: alter scoring, registry membership, model scores, historical PR bodies,
deployment, deck selection or incomplete acceptance.

## Functional Requirements

* Verify ADR-layout files count and excluded/retired files do not.
* Test current event contracts rather than assuming every YAML supports PR/push.
* Make gate regression fixtures independent of mutable recorded grades.
* Record baseline, available migration snapshots, real retirement comparison,
  sequence deviations and criteria/recovery ownership in the sign-off pack.

## Non-Functional Requirements

* No production behavior/score changes; version 2 remains unchanged.
* Preserve original evidence and earlier append-only log bytes.
* Local suite must have no new failures; explicitly retain unrelated failure
  and seven missing-runtime skips unless runtime prerequisites already exist.

## Acceptance Criteria

* Existing src coverage plus new retired-path and trusted-base transition
  regressions prove inclusion/exclusion and old-registry deletion behavior.
* All 17 seed/trigger-related failures are repaired; unrelated deck-selection
  failure is reported, not silently fixed or skipped.
* Documentation distinguishes carried snapshots, actual scores and causality.
* Workflow Markdown/lock unchanged together; no recompilation needed.
* PR uses Refs and itemizes remaining #198 acceptance gaps.

## Sources

* .copilot-tracking/research/2026-10-27/rubric-src-198-research.md: C1-C8/W1-W3.
* docs/adrs/0006-src-layout-and-cutover.md: layout and counting.
* Issue #198 body/comments and migration PRs: scope and historical limits.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Repair regression coverage

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Isolate test baselines and current workflow triggers

Use an explicit synthetic 66-point fixture in existing gate tests; make the
prepare deletion expectation relative to its baseline. Assert the exact
current direct-event matrix, source path and workflow_run chain.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Cover retired inputs and registry timing

Parameterize retired mvp/prototype paths and verify no counting. Add temporary
Git regression proving old base registry detects deleted evidence and a PR
registry edit activates only after merge.

<!-- rpi:phase id=P02 -->
### [x] P02: Reconcile evidence and validate

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Update rubric guidance and sign-off ledger

Correct historical/current language and add linked evidence, test reassessment,
recovery matrix and acceptance gaps; update KB index and append log.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Validate and preserve exact outcomes

Run rubric suite, targeted new regressions, diff/link checks. Record all
failures/skips. One independent post-implementation Review; no review loop.
Publication follows the single Review: commit artifacts with implementation,
then push and open draft PR. It is not a prerequisite for implementation
completion and does not change the original Review verdict.

## Test Ownership and Locked Boundary

* Owners: existing test_gate.py, test_prepare.py, test_safe_output_runtime.py.
* Exact removals: none; replace stale fixture/event assumptions in place.
* Maximum additions: two test functions, with parameterized retired cases.
* Semantic coverage: real prepare/gate calls and parsed real YAML, no mock scores
  presented as assessments.
* Regression coverage: legacy include refusal, deletion/base registry semantics.
* Canonical targets: test modules and listed docs; generated targets: none.
* Validation: complete local rubric suite (baseline 355 pass/18 fail/7 skip),
  targeted selectors, JSON/diff/link and workflow/version byte invariants.
* No heavy gate: bounded tests/docs repair, not a large change.

## Dependencies

All relevant registry removals are merged. No owner/legal decision blocks
independent delivery; missing historical assessment evidence blocks closure.

## Critique Disposition

| Finding | Disposition | Resolution |
| --- | --- | --- |
| PC-001 | Accepted, resolved in details | Synthetic prepare A2=5, proposed 3, recomputed metadata and exact valid/drop assertions |
| PC-002 | Accepted, resolved in details | Record pre-deletion solution-code fingerprint; assert bootstrap false and old-base removal |
| PC-003 | Accepted, resolved in details | Exact event matrix includes src CI workflow_dispatch |
| PC-004 | Rejected, unsupported premise | No caller/platform workspace-only scratch restriction exists; normal pytest temporary directories are permitted. User explicitly permits external gate output. No historical cleanup is authorized or performed |

Original critique remains Complete / Revise; no second critique. No human
decision required; implementation-ready after these compatible corrections.

## Follow-Up Items

* Recover historical migration scorecards if available; otherwise owner must
  disposition the acceptance gap, not accept an invented score.
* Separate deck registry/test mismatch; outside migration scope.

## Handoff

Implementation complete: 31 targeted checks pass; complete suite 374 pass /
one unchanged unrelated failure / seven missing-runtime skips. Diff/link,
production byte invariants and append-only log prefix pass. Continue to one
independent Review; historical acceptance and deck mismatch remain follow-up.
