---
title: Issue 1248 saved-call History readiness repair changes
description: Final changes record for the test-only readiness repair, preserving the phase 1 proof and R4 adverse evidence
ms.date: 2026-11-07
ms.topic: reference
---

## Chronology

* Prospective research, plan, details, critique and issue record: commit 9e0c29cd. Unchanged.
* Phase 1 controlled proof: commit 82ce7f63 and [phase 1 record](issue-1248-phase1-proof-changes.md). Unchanged. Base run 407 PASS, held run 411 PASS.
* R4 adverse evidence (`/mnt/ama-gates/g86-r4-1107/0102-browser.log`, receipt sha256 7c96fb63...) untouched.

## Change

One file: `src/api/checks/case_journey_browser_check.py` (test-only). No application, role, dataset or transport change.

* Before Save, capture the old `[data-case-workspace]` handle and hold only the post-Save `**/api/cases/ZF-1` read (`page.route`, removed in `finally`, idiom of the existing held-read checks).
* Deterministic regression while held: the outcome is cleared and the old workspace is still attached, and History read once lacks the saved call. This demonstrates the old completion signal's failure.
* Release the read (`route.fulfill(response=route.fetch())` under `expect_response`), wait for the old workspace to detach (the #1184 idiom), then select History and `expect(#case-panel-history).to_contain_text("Unsaved synthetic call")`, the web-first exact outcome in the actual panel.
* Kept in order: the unrelated-draft check "successful call clears itself, not unrelated draft" on Resident, then "saved call reaches actual history" on History. The old one-shot `inner_text()` assertion is removed because the web-first expectation replaces it, not weakened.
* Phase 1 traffic list, request listener and DIAG print removed from the normal run; they remain in commit 82ce7f63.
* No sleep, retry, blanket timeout, skip or weaker matching.

## Evidence

* Dev run (pre-freeze, uncommitted diff): `/mnt/ama-gates/g1248-final-1107/dev.log`, EXIT 0, 409 PASS. Not the final check.
* Final checks run on the frozen head are recorded outside the repository under `/mnt/ama-gates/g1248-final-1107/`; their paths and exits are reported in the return and are not claimed here.
* A focused pass is not a full-gate pass or an accessibility conformance claim.

## Attribution Limits

* Proven only in the controlled synthetic scenario: the cleared outcome precedes the refreshed History data.
* Not proven: that this caused the original R4 failure (timing not captured; unchanged base passed), nor the universal absence of an application defect.
