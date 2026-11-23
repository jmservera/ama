---
title: Epic 93 criteria re-check at head 3a18e32175 (2026-11-23)
description: Per-criterion proven and unproven table for epic 93 with a live read-only finance probe, a regression found and fixed in the provenance register, and issue states
ms.date: 2026-11-23
ms.topic: reference
---

Refs #93. Scope is the synthetic demo, desktop only, head `3a18e32175` (equal to origin/main). Owner decisions of 2026-11-18 apply. No Azure resource was created (nothing to delete), no demo record was written and nothing is ticked in any issue. This note adds to the [2026-11-21 re-check](./issue-93-criteria-recheck-live-2026-11-21.md), which stays a dated snapshot.

## Evidence (folder `.copilot-tracking/evidence/2026-11-23/issue-93-live-20261123T150451Z/`)

* Issue states by REST on 2026-11-23: #94, #95, #96 and #99 closed; #2140 open with `delivery:deferred`; #440 open with two unticked criteria; #2301 open and owns the nine-epic demo checkpoint record; no open `bug` issue; #1837 open.
* Azure, read-only: `az containerapp show -g ama -n ca-cutover-test-demo-api` reports revision `ca-cutover-test-demo-api--0000055` (0000038 on 2026-11-21).
* Live, Playwright Chromium 1366 by 900, employee demo account signed in with credentials read at run time and never printed or saved; five GET calls, all HTTP 200, no write, no screenshot because pages show the account name. Scrubbed summary in `live_probe_summary.txt`; a scan for `@` found none.
  * Finance: 13 invoices, 7 `Received` and 6 `Exceptions`, 6 on hold, none paid or approved.
  * Exposure: status `Held`, `pause_signal.automatic_cut` false, `decision_owner` null.
  * Funding: 167 cases (1 `Draft ready`, 25 `To prepare`, 141 `Not started`); grants 163 "No grant record" and 4 "Not recorded"; no award, claim or cash state.
  * Form schemas: empty list.
* Offline, from `src/core`: the 12 finance, grant and form modules of the 2026-11-21 run gave 270 tests with one failure (`offline-core-tests.txt`). The failure, `test_form_review_pack.test_public_payload_is_registered_and_passes_privacy_checks`, came from three payloads added by main commit #2316 (`src/agents/evals/eval-manifest.schema.json`, `synthetic-eval-manifest.json`, `synthetic-eval-predictions.json`) that `privacy.public_issues` reported as `unregistered_public_payload`.

## Defect found and fixed

The synthetic-data privacy gate requires every public payload under `src/*/evals/` to be listed in `docs/reference/research/retrofit-synthetic-data/provenance-register.json`. #2316 added the frozen evaluation harness files without register entries, which broke a finance form review pack test on main. The fix registers the two synthetic example files by glob (marker field `version`) and the schema (marker field `description`, added to the schema). The gate itself is unchanged. After the fix the same 12 modules plus `test_synthetic_provenance` pass: 284 tests, OK, 45 skipped (`offline-core-tests-after-fix.txt`). The existing registration test is the regression test: it failed before and passes after. This affects the repository gate, not any finance behaviour; no finance defect was found.

## Per-criterion table

| Issue | Criterion | Result | Evidence | Why |
| --- | --- | --- | --- | --- |
| #93 C1 | Stabilization checkpoint #440 | Unproven | #440 open; #2301 open | The criterion says merged children alone do not satisfy it. Owner approval of pivots and deferrals, a non-worker review and a published PR are required; a worker that may not push cannot supply them. |
| #93 C1a | BRD, PRD and ADR reconciliation | Proven for the finance rows | 2026-11-19 note | The issue body cites BRD FR-018 and FR-019, which are not the finance rows; correcting the body is an owner action. |
| #93 C1b | Local-first regression checks | Proven after one fix | 284 tests OK, 45 skipped | One regression found and fixed above; SQL Server variants are not claimed. |
| #93 C1c | Bugs dispositioned | Proven for #93 | Defect above fixed in this commit; no open `bug` issue | The fix needs a PR and review to reach main. |
| #93 C1d | Azure-only residuals and owner pivot or defer decision | Unproven | Live probe; residual is the #96 schema approval in #2140 | The decision is a human act. |
| #93 C2 | All child features closed or deferred | Proven | #94 #95 #96 #99 closed; remainder in #2140 | The deferred part stays unverified, not passed. |
| #93 C3 | No automated bid, match approval, claim certification or cash | Proven again (already ticked) | `test_finance_no_automated_path_93` and boundary tests pass; live views show no paid, awarded, claimed or cash state | No contradiction. |

## Limits

* Azure and issue facts are as read on 2026-11-23 and may change.
* The live probe is read-only; write paths were not exercised live.
* The fix is a local commit only. Independent exact-head review, hosted CI and the coordinator gate are outstanding.
