---
title: IoT first-run preflight plan for PR 557
description: Documentation-only quota and cost preflight correction
ms.date: 2026-10-29
---

<!-- markdownlint-disable-file -->

## Task Metadata

* Task ID: pr-557-comment-4418722664
* Task slug: iot-first-run-preflight-557
* Planning status: Ready; independent critique executed, Pass, no findings
* Phase details: .copilot-tracking/details/2026-10-29/iot-first-run-preflight-557-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-29/iot-first-run-preflight-557-plan-critique.md

## Executive Summary

Require fresh operator quota, remaining cost headroom and active-alert verification before the one approved bounded publisher run. Include the verified current daily usage explicitly in the existing `RunBudget` constructor. No runtime or Azure change is necessary.

### What You May Not Know

`RunBudget` trusts caller declarations and defaults consumed quota to zero. It can enforce the quota inequality only when supplied with real current usage; reference strings are not evidence of live quota, available money or an active alert. The USD60/month routed model is not extra authority for the bounded USD5 exercise.

### Unresolved Decisions or Blockers

None for implementation. Live prerequisites remain unknown/out of scope. Required independent Review and complete local gate must be reported honestly; no push is authorized regardless of results.

## User Decisions and Requirements

* Run research, plan, implement and review with dated artifacts.
* Run `git pull --rebase` first, then rebase onto `origin/main`; preserve both sides of any append-only index/log conflicts and take main's rubric copy without hand-editing it.
* Fix only PR #557 Copilot comment 4418722664, docs only unless code is clearly necessary.
* Require preflight quota verification and `daily_used_units`, remaining cost headroom and actual active-alert verification before the single approved run.
* Commit locally; do not push and do not use Azure.

## Goals

* Close the operator-guidance gap without changing runtime defaults or existing approval boundaries.

## Scope and Non-Goals

* Canonical target: `src/api/README.md`, bounded exercise instructions.
* Evidence targets: dated research, plan, details, critique, changes, Review and session JSON.
* No runtime/test/source-infrastructure changes, generated targets, cloud commands, private data, approval claims, remote writes or issue closure.
* Reference index/log need no new entries because no knowledge-base file changes; their existing entries were preserved by the rebase.

## Functional Requirements

* FR1: named owner verifies the reused hub's current B1 daily usage for the applicable UTC quota day immediately before the single run; other traffic and attempted/uncertain deliveries cannot be omitted or treated as zero.
* FR2: explicitly require `daily_used_units=verified_daily_used_units` alongside existing two-message, 1/s, 60s limits; retain at least 40000 units from the 400000-unit daily allowance after run and accounted traffic.
* FR3: verify actual subscription currency and remaining aggregate cost headroom within the approved bounded allowance/window, and the actual enabled alert and its scope/threshold/recipient. References are evidence pointers, not checks.
* FR4: missing, stale or insufficient evidence blocks the run; budget/activation declarations neither query Azure nor prove/enforce subscription-wide cost or alert state.

## Non-Functional Requirements

* Preserve one-call/no-retry/no-concurrency, cutoff, credential, service-key and separate activation boundaries verbatim outside the focused addition.
* Use concise ASCII Markdown, repository relative links, and no fabricated usage/cost/alert values.

## Acceptance Criteria

* AC1: the first-run constructor explicitly passes verified usage, not the zero default.
* AC2: operator steps explain current quota/reset period, conservative accounting and >=40000 units retained; no run with unknown headroom.
* AC3: actual cost/currency/active-alert checks precede the run and point to existing authoritative cost guidance.
* AC4: existing bounded scope and behavior remain unchanged; no executable file or rubric edit.
* AC5: independent critique, focused documentation checks, one independent post-implementation Review, local commit, and complete local gate attempt/evidence are recorded without claiming blocked checks passed.

## Sources

* .copilot-tracking/research/2026-10-29/iot-first-run-preflight-557-research.md: C1-C5/W1, Research executed, Planning Readiness Ready.
* docs/reference/research/iot-sensor-analytics-research-plan.md: cost/scale and outstanding live gates.
* src/core/src/zava_forward/core/synthetic/sensor_stream.py: existing quota calculation.
* infra/README.md: bounded existing-hub authorization.

## Validation Ownership and Locked Boundary

* Existing test owner: core `test_sensor_stream` owns budget behavior; API `test_iot_stream` owns publisher validation. Neither suite needs edits for a docs-only change.
* Exact test removals: none. Maximum additions: zero test files/cases.
* Canonical target: `src/api/README.md`; generated targets: none.
* Semantic coverage: compare wording and constructor to C1-C5; verify the exact quota inequality and conservative other-traffic/uncertainty handling, cost/alert evidence and stop conditions.
* Regression coverage: compare preservation of existing single-run/rate/time/cutoff constraints and perform Markdown/link/diff checks. No cloud preflight or executable tests are needed to validate prose.
* Original Review precedes committing implementation and all dated evidence. Then fetch main and attempt `python3 tools/rpi-checks.py --all --base <reviewed-main-sha> --out <new-external-directory> --lock-timeout 0`; verify a successful receipt separately. Missing prerequisites/shared lock block that gate, not the local documentation fix. No cloud fallback or protection change.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct and validate the first-run documentation

* Dependencies: completed research and resolved independent critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Require actual preflight evidence and explicit quota input

* Add the focused operator requirements and extend the inline constructor without changing existing run limits.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Validate prose and record implementation evidence

* Check exact quota semantics, cost/alert requirements, links, unchanged bounds and `git diff --check`; reconcile plan/details/changes for independent Review.

## Dependencies

* Existing budget contract, research cost section and approval are adequate; do not restart research.
* Full-gate prerequisites and independent/human/hosted approvals are not granted by this fix.

## Critique Disposition

One independent final-candidate critique executed at the metadata path: Pass, zero findings. No planner correction or significant user decision required; no repeat critique.

## Follow-Up Items

* None.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-10-29/iot-first-run-preflight-557-changes.md
* Implementation tasks P01-T01/P01-T02 and phase P01 complete; semantic/link/diff checks passed.
* Ready for one independent original Review, followed by local commit and external complete-gate attempt.
* No unanswered implementation decision; no live approval or publication. AC5's Review/commit/gate evidence is pending lifecycle closeout, not unchecked implementation.
