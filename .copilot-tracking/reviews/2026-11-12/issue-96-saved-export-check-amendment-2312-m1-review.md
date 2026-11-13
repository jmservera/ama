---
title: Issue 96 saved export check M1 correction 2 independent Review
description: Independent final Review of the M1 correction at the local frozen head, run in a separate agent context
ms.date: 2026-11-12
---

## Execution and outcome

Review executed once by a separate `code-review` agent context (not the author) at local frozen source head `626b7dbeacc0691c6b998f2e82f66eb0cfab2682`. The reviewer edited nothing and wrote nothing inside the repository. Outcome: Conformant with qualifications. No open material finding. Not repeated.

## Findings

* RV-1 (Low, records): the changes record said the failing-first run had "3 tests with 6 failures". Three tests were selected (two new plus the existing forged-copy control) and all 6 failures were in the two new tests. Disposition: wording corrected in the changes record; no code change.
* RV-2 (Informational, disclosed): a malformed copy answers `Invalid` before the case and draft lookup (previously `Unavailable` for a missing draft), and the frozen core still maps its own digest and row-parsing `TypeError` to `Invalid`. Matches critique CR-1 and CR-2 and the README. No action.

## Evidence reported by the reviewer

* The guard returns false for any `fields` list holding a non-object row or a non-text `field_id`; the core then answers its existing `Invalid`. Non-list `fields` fall to the core, which already catches the `TypeError`. No client-caused input was found that still produces a 503 or leaks a value.
* An internal `TypeError` reaches the shared `except Exception` handler, which logs only the exception type and returns the fixed 503 text; the test asserts 503, a logged error, no `Invalid` and no fault text, and unchanged state.
* Role, CSRF, the 404 switches and the 400 draft mismatch precede the guard. Core and UI are unchanged (`origin/main...HEAD` has no `src/core` or `src/ui` change).
* README makes no approval, eligibility or provenance claim; no stale marker or old comment remains.
* Executed: the full held download module on HEAD (16 OK) and the new tests against the old `server.py` from a `/tmp` copy with forced import path (6 failures, as claimed).

## Not verified

Hosted CI, human or accessibility approval, browser or UI behaviour, other test modules (run by the author, see the changes record), the failing-first log file contents, deployed logging.

## Routing

No further work in this task. Later user-selected work: route-specific CSRF, view-only, oversized-body and no-store assertions (assessment L1); UI remains unimplemented and waits.
