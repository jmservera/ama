---
title: Epic 93 criteria re-check at head 9c3fe9dcb (2026-11-21)
description: Per-criterion proven and unproven table for epic 93 with a fresh offline run, a signed-in read-only finance probe and issue states, and no source change
ms.date: 2026-11-21
ms.topic: reference
---

Refs #93. Scope is the synthetic demo, desktop only, head `9c3fe9dcb` (equal to origin/main). Owner decisions of 2026-11-18 apply. No source file changed, no Azure resource was created (nothing to delete), no demo record was written and nothing is ticked in any issue. This note adds to the [2026-11-18 audit](./issue-93-epic-audit-live-2026-11-18.md), the [2026-11-19 re-check](./issue-93-first-unmet-criterion-live-2026-11-19.md) and the [2026-11-20 child closure re-check](./issue-93-child-closure-live-2026-11-20.md), which stay as dated snapshots.

## Evidence (folder `.copilot-tracking/evidence/2026-11-21/issue-93-live-20261121T075635Z/`)

* Issue states, read by REST on 2026-11-21 (GraphQL was rate limited): #94, #95, #99 and #96 CLOSED; #2140 (the #96 remainder) OPEN with label `delivery:deferred`; #440 OPEN with two unticked criteria (finding triage with owner approval, delivered review artifacts and Major HVE behavior validation); no open issue carries the `bug` label; #1837 is open.
* Offline, from `src/core`, `PYTHONPATH=src:tests:../agents/src:../agents/tests python3 -m unittest` over `test_finance_no_automated_path_93`, `test_finance_match_controls`, `test_finance_signoffs`, `test_grant_lifecycle_controls`, `test_exposure_limits`, `test_funding_automation_boundary`, `test_form_staging`, `test_form_review`, `test_form_review_pack`, `test_form_dependencies`, `test_form_export`, `test_form_criteria_5_6`: 270 tests in 79.9 s, OK, 45 skipped (opt-in SQL Server variants, not claimed as passed). Log `offline-core-tests.txt`.
* Azure, read-only: `az containerapp show -g ama -n ca-cutover-test-demo-api` reports revision `ca-cutover-test-demo-api--0000038` (0000033 on 2026-11-20), image digest prefix `sha256:bc5cb9ae`. File `az_revision.json`.
* Live, Playwright Chromium 1366 by 900, employee demo account signed in through Entra with credentials read at run time and never printed or saved. Five GET calls, all HTTP 200, no write, no screenshot because pages show the account name. Files `live_probe.py`, `live_probe.json`, `live_probe_summary.txt`; a scan for `@` found none.
  * Finance: 13 invoice rows, 7 `Received` and 6 `Exceptions`, 6 on hold; none paid or approved.
  * Exposure: status `Held`, `automatic_cut` false, `decision_owner` null, reason "No person-approved investment limit or tolerances are recorded."
  * Funding: 167 cases (1 `Draft ready`, 25 `To prepare`, 141 `Not started`); grants column "No grant record" for 163 and "Not recorded" for 4; no award, claim or cash state.
  * Form schemas: `{"schemas": []}`.

## Per-criterion table

| Issue | Criterion | Result | Evidence | Why |
| --- | --- | --- | --- | --- |
| #93 C1 | Stabilization checkpoint #440 | Unproven | #440 OPEN, two unticked criteria | The criterion says merged children alone do not satisfy it. Owner approval of pivots and deferrals, a non-worker review and a published PR are needed; none is possible for a worker that may not push. |
| #93 C1a | BRD, PRD and ADR reconciliation | Proven for the finance rows | 2026-11-19 note: the issue body cites BRD FR-018 and FR-019, which are not the finance rows (FR-023, FR-024 are) | Correcting the issue body is an owner action |
| #93 C1b | Local-first regression checks | Proven | 270 tests OK, 45 skipped | SQL Server variants not claimed |
| #93 C1c | Bugs dispositioned | Proven for #93 | No finance defect found; no open `bug` issue; #1837 stays the one gating finding on other epics | Unchanged since 2026-11-18 |
| #93 C1d | Azure-only residuals and owner pivot or defer decision | Unproven | Live probe above; residual is the #96 schema approval moved to #2140 | The owner decision is a human act |
| #93 C2 | All child features closed or deferred | Proven | Four children CLOSED; remainder deferred to #2140 | The deferred part stays unverified, not passed |
| #93 C3 | No automated path submits a bid, approves match funding, certifies a claim or records cash | Proven again (already ticked) | `test_finance_no_automated_path_93` and the funding boundary tests pass; live views show no paid, awarded, claimed or cash state | No contradiction |

## Why C1 cannot close

Everything an engineer can prove for C1 is proven above. What remains is an owner continue or defer record for #93 and #2140, the review and artifacts bar of #440, and correction of the BRD identifiers in the issue body. Ticking C2 and closing the epic are owner actions and were not taken.

## Limits

* Azure and issue facts are as read on 2026-11-21 and may change.
* The live probe is read-only; write paths (invoice intake, grant states, form packs) were not exercised live.
* Independent exact-head review and hosted CI are outstanding.

The raw live_probe.json (about 42 KB of funding and roster data) is not committed; the figures above come from the retained logs in the evidence folder.
