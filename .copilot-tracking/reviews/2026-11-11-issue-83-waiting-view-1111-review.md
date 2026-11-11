---
title: Issue 83 waiting-time screen original review
ms.date: 2026-11-11
task_id: issue-83-waiting-view-1111
---

## State

* Execution: Complete (single original Review, no second pass).
* Outcome: Residual work. No code defect found; whole #83 remains unaccepted.
* Reviewed head: 8196c6e53e5077344d5f14127bc414178d726e50 (base 7880b95b19525ff465cab27870ba9d55b57110a3).
* Boundary: src/api/src/zava_forward/api/web/app.js, src/api/tests/test_handoff_waiting_view.py, src/api/README.md.

## Artifacts compared

* .copilot-tracking/research/2026-11-11-issue-83-waiting-view-1111-research.md
* .copilot-tracking/plans/2026-11-11-issue-83-waiting-view-1111-plan.md (P01 to P03 ticked, P04 is this Review)
* .copilot-tracking/details/2026-11-11-issue-83-waiting-view-1111-phase-details.md
* .copilot-tracking/plans/2026-11-11-issue-83-waiting-view-1111-plan-critique.md (Revise; PC-001 to PC-006 applied directly, one critique only)
* .copilot-tracking/changes/2026-11-11-issue-83-waiting-view-1111-changes.md

## Process qualifications

* Review lens: one independent code-review subagent (read-only), plus root reconciliation. The subagent did not fetch the web rules; root fetched them.
* Web Interface Guidelines (vercel-labs, retrieved 2026-11-11): first fetch returned the first 3000 characters, a second returned the remainder; the changed-file check was done by root against both parts. Not a conformance or accessibility acceptance claim.
* Tests ran with PYTHONPATH pointing at the worktree because editable installs resolve to the coordinator's primary checkout. No install.
* The first Chromium run exposed a validator defect (negative age_hours) fixed inside the initial increment before freeze; this is original adverse evidence, not a post-review correction.
* Historical #83 correction balance: not recorded in any retrieved artifact (Unrecorded). No correction authority was inferred or used.

## Findings

* RV-001 Low, residual: web-rules pass notes the loading text uses three dots (existing repository style, app.js around line 827 onward matches the surrounding views), no skip link and no locale-formatted numbers beyond Intl for as-of. Pre-existing pattern; destination: distinct follow-up, no action required for this increment.
* RV-002 Info, evidence limit: "personal list empty but queue present" and escalated or merely-old rows are constructed responses, not real-backend states (same scope makes the first impossible with real data). Disclosed in the changes record and tests; destination: none.
* RV-003 Info: "Longest wait first" relies on the server sort order in unaccepted_handoffs, which is descending age_hours. Verified by the review lens; destination: none.
* RV-004 Residual, human: criterion C3 ("Unaccepted handoffs are visible and escalated within approved times (BG-010)") remains unmet. OD-09 approved times, routes and operational acceptance are absent; neither the fixture nor a company agent supplies them. Destination: owner/human acceptance follow-up; #83 must not be ticked or closed from this work.

## Checks against intent

* Read-only, no API/core/permission/threshold/escalation change: confirmed by diff scope (three files).
* Route guard ordering after contractor and no-case-access guards: confirmed.
* Failure handling: refused or malformed load shows a fixed alert, no table, no raw server text; 401/abort silent: confirmed by tests.
* Injection: case_id via encodeURIComponent, text nodes only: confirmed.
* Existing pending list and CSV download regressions: 59 tests OK in the changes record.
* ASCII only in changed files: confirmed by the review lens.

## Validation

* Review lens re-ran test_handoff_waiting_view with ZF_BROWSER_TESTS=1: 10 tests OK.
* Earlier results (changes record): regression 59 OK, node --check exit 0, ruff and mypy clean on the new test.
* Not run: full gate, SQL, image build, deployment, live cloud, hosted CI.

## Routing

* No defect for rpi-implement; no decision gap for rpi-plan; no research gap.
* Residual: RV-004 to owner acceptance; RV-001 optional later follow-up.
* Source correction needed: none, so no coordinator admission of correction authority is requested.
