---
title: Regulatory evaluation gates plan
description: Issue 216 synthetic implementation and evidence boundary
ms.date: 2026-10-16
---

Task: issue-216 / regulatory-eval-gates. Full plan scope.

## Executive Summary

Extend the existing extractive development evaluation with independent expected
fragments, adversarial cases, critical hazard misses and a generated 60,000-home
baseline. Label source cadence on rule-card reads without changing approved
rules or suppressing alerts. Missing comparative staff evidence selects cards
alone for shipping; explicit synthetic development lookup remains available.

## User Decisions and Requirements

* Implement #216 on the merged #328/#331/#348 work; PR uses Refs #216 only.
* ADR 0005 is accepted for synthetic development, not operational reliance.
* Juan Manuel Servera is the exercise Legal, Compliance and DPO owner.
* Thresholds are provisional and reported per check, never as one overall pass.
* New executable work only in src/ and infra/; no private datasets or Azure needed.
* Update READMEs, reference log, RPI artifacts, commit and push this clean topic branch.
* User requests all four RPI phases in this invocation; no mode switch is inferred.

## Goals

Make local safety measurements reproducible, non-vacuous and honest.

## Scope and Non-Goals

Pure agents graders; offline runner and fixtures outside packages; core cadence
read model; API card responses and existing chat display. No model, approval,
real staff data, SQL platform acceptance or operational enablement.

## Functional Requirements

Separate citation, refusal, hazard, recall, stale-source and comparison checks;
show numerators, denominators, failed case IDs, thresholds and evidence limits.
Hazard misses are critical regardless of recall; recall threshold remains unset
until baseline owner review. Comparison records same-source cards/provision links
and structural results, but no benefit without human evidence.

## Non-Functional Requirements

Deterministic outputs; no secret/private inputs; read-only freshness labels;
portable parameterized SQL; empty coverage is not a pass; test negative controls.

## Acceptance Criteria

Local: exact-fragment and metadata validity; expected refusal and false-refusal
measurements; critical seeded hazard miss; baseline before recall threshold;
cards-only ship recommendation without comparison; cadence labels; no aggregate
pass. Unmet: owner-agreed thresholds, held-out legal grading, continuing-stock
pipeline evidence and staff comparison/precision/acknowledgement/comprehension.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01 Evaluation contracts

* [x] P01 complete
<!-- rpi:task id=P01-T01 -->
* [x] P01-T01 Implement independent extractive graders and per-check report.
<!-- rpi:task id=P01-T02 -->
* [x] P01-T02 Add frozen adversarial retrieval cases and 60,000-home seeded baseline runner.

<!-- rpi:phase id=P02 -->
### P02 Source cadence visibility

* [x] P02 complete; depends on P01
<!-- rpi:task id=P02-T01 -->
* [x] P02-T01 Read configured source-monitor cadence and label cards/API/chat without mutations.

<!-- rpi:phase id=P03 -->
### P03 Evidence and delivery

* [x] P03 complete; depends on P02
<!-- rpi:task id=P03-T01 -->
* [x] P03-T01 Run tests, ruff, mypy and loopback app; record report and acceptance audit.
<!-- rpi:task id=P03-T02 -->
* [x] P03-T02 Perform one post-implementation review, commit, push and open PR.

Delivery: PR #355, main base, Refs #216 only. Review snapshot was Not accepted;
RV-001 to RV-003 were corrected and regression-tested as recorded in changes,
without a second review or independent closure claim. Full bounded local plan
is delivered; issue-level owner/human/continuing-stock criteria remain unmet.

## Test Ownership and Targets

No test removals. Add at most 45 methods across agents grader/runner, core freshness
and API regression tests. Existing regulatory tests remain owners of retrieval,
state, permission and handoff behavior. Canonical new semantic report under
src/agents/evals/; generated report recorded there. Existing historical report
loses aggregate `passed`; its other evidence remains. Use installed editable
packages, absolute test PYTHONPATH, per-project ruff and mypy.

## Critique Disposition

One final-candidate critique executed, verdict Revise; all five planner-owned
findings accepted and resolved in phase details before implementation:
PC-001 independent frozen oracle/full envelope; PC-002 pinned profile units;
PC-003 freshness reduction/clock/storage truth table; PC-004 fix or disclose
blocking defects without repeating review; PC-005 coordinated legacy migration.
No divergent user decision, no second critique. Implementation ready.

## Follow-Up Items

## Owner-Requested PR 355 Corrections

The 2026-10-16 user explicitly advances this follow-up to implementation on the
same task/branch. Preserve the historical one-pass critique/review; this is
implementation of supplied independent review findings, not a repeated review.
Source boundary remains src/ only, with documentation and RPI evidence updates.
No legal approval or issue checkbox change is authorized.

<!-- rpi:phase id=P04 -->
### P04 Integrated regression correction and delivery

* [x] P04 complete
<!-- rpi:task id=P04-T01 -->
* [x] P04-T01 Merge origin/main first, retaining both append-only log histories.
<!-- rpi:task id=P04-T02 -->
* [x] P04-T02 Reproduce full API failures, correct retained-history assertions and resolve unavailable-store behavior honestly.
<!-- rpi:task id=P04-T03 -->
* [x] P04-T03 Run all three complete suites with absolute fixture paths, Ruff/format/mypy and local HTTP; reconcile README/PR counts and acceptance audit.
<!-- rpi:task id=P04-T04 -->
* [x] P04-T04 Record supplied review disposition, commit with trailer, push normally and update existing PR 355.

P04 delivered as main merge c311752 and correction 4d4525f, pushed normally.
Existing PR #355 updated with the complete 529/93/559 run counts and distinct
528/93/449 passes, 1/0/110 skips. No active implementation markers remain.
Historical independent verdicts remain historical; CI and owner review remain
separate from local verification and issue-level acceptance.

## Remaining Acceptance Work

Owner ratification and independent grading; actual staff paired trial and net
effort/cost; continuing-stock integration and authorized platform verification.
