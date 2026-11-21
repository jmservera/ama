---
title: Epic 104 criteria re-check at head 981aa6aaf (2026-11-21)
description: Per-criterion proven and unproven table for epic 104 with fresh issue states, a read-only Azure check of AI deployments and quota, and 59 offline tests; no source change
ms.date: 2026-11-21
ms.topic: reference
---

Refs #104. Scope is the synthetic demo, desktop only, head `981aa6aaf`. Owner decisions of 2026-11-18 apply. No source file changed, no Azure resource was created (nothing to delete) and nothing is ticked in any issue. This adds to the [2026-11-18 audit](./issue-104-epic-audit-live-2026-11-18.md) and the [2026-11-19 re-check](./issue-104-criteria-recheck-live-2026-11-19.md), which stay as dated snapshots.

## What changed since 2026-11-19

* #164 and #216 are now CLOSED, so the child gaps listed on 2026-11-19 reduce to #108.
* The Azure revision moved from 0000033 to `ca-cutover-test-demo-api--0000038` (digest prefix `sha256:bc5cb9ae`).
* No open issue carries the `bug` label.

## Evidence (folder `.copilot-tracking/evidence/2026-11-21/issue-104-live-20261121T081349Z/`)

* `issue_states.txt`: REST reads of #104, #105 to #108, #164, #216, #432, #435 and #440 with their unticked criteria. #108 has one (model names, versions and quotas in the chosen region); #435 has three owner decisions; #440 has two.
* `az_revision.json`, `ai_accounts.json`, `ai_deployments_quota.json`: read-only Azure reads. Account `aif-cutover-test-rzsrg` (uksouth, S0) has deployment `standard` (gpt-4.1-nano 2025-04-14, GlobalStandard, capacity 10) and `resident-mini` (gpt-4.1-mini 2025-04-14, Standard, capacity 1), both Succeeded. The quota usages API returned an empty list through both the CLI and REST.
* `offline-agents-tests.txt`: from `src/agents`, with a throwaway venv holding `opentelemetry-api` and `opentelemetry-sdk` 1.45.2 (deleted afterwards), `python -m unittest test_epic104_bounded_ai_invariants test_candidate_comparison test_heldout_freeze`: 59 tests OK.
* No browser proof: no UI or API behaviour changed, and sign-in pages show account names.

## Per-criterion table

| Criterion | Result | Basis | Why |
| --- | --- | --- | --- |
| C1 Stabilization checkpoint #440 | Unproven | #440 OPEN, two unticked criteria | The criterion excludes merged children as proof. Owner approval of pivots and deferrals, a non-worker review and a published PR are needed; a worker that may not push cannot supply them. |
| C2 All child features closed or deferred | Unproven | #105, #106, #164, #216, #432 CLOSED; #107 OPEN with no unticked criteria; #108 OPEN with one | #108 is neither closed nor recorded as deferred. Quota headroom is empty in the API and the production region is undecided. |
| C3 AI never approves, executes, ranks or mutates controlled records (ticked) | Proven again | 59 tests OK including the 27-test invariant suite | No contradiction. |
| T1 #432 complete or gap recorded (ticked) | Proven | #432 CLOSED 2026-11-18; cost Unknown with inputs named | Unchanged. |
| T2 No capability enabled beyond the exercise without finite limits and alert (ticked) | Proven | Limit-breach tests stop dispatch with the workflow-only path; deployments have finite capacity | No new enablement was made. |

## Sub-gap of C2: #108 region confirmation

Model names, versions, SKUs and capacities in uksouth are now confirmed for the demo deployments (above). Subscription quota headroom is not: the usages API returns empty, as it did in #2014. This stays unproven and needs the Azure subscription owner or a later route.

## Why C1 and C2 cannot close

What an engineer can prove is proven above. C1 needs owner continue, pivot or defer records and a reviewed PR. C2 needs #108 closed, or a recorded owner deferral of its quota criterion. Ticking and closing are owner actions and were not taken.

## Limits

* Azure and issue facts are as read on 2026-11-21 and may change.
* SQL Server variants of the tests are opt-in and not claimed.
* Independent exact-head review and hosted CI are outstanding.
