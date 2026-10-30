---
title: Capacity delayed sibling 401 changes
description: Original implementation and validation evidence for issue 523
ms.date: 2026-10-28
---

Task 523-delayed-401 / capacity-page-523-delayed-401. Full plan declared:
.copilot-tracking/plans/2026-10-28/capacity-page-523-delayed-401-plan.md.
Details and original critique share the dated slug. Prior evidence untouched.

## Execution Status

P01 and P02-T01 complete; P02-T02 publication pending in this pre-commit
snapshot. Original Review Complete, scoped Conformant / full task Residual work.
Strict
regression was proved red before the production guard. One final-candidate
critique Complete / Revise, dispositions recorded;
PC-001/003 applied, PC-002 rejected against actual parent instructions and
explicit owner-required shared lock.

## Changes and Validation

Initial state (superseded by actual red/green results below): pending execution.
Original branch head 2d207b6284930d926324cdfea9282d3e78ce6203 includes rubric bot.

### P01-T01: Regression construction and admission

Added one two-endpoint scenario block in the existing browser harness.
Each scenario holds both refresh reads after a real mutation; fails one;
starts and holds retry reads; sends old sibling 401; observes sign-in; releases
real successful payloads; waits for the retained detached retry button's
finally transition before strict assertions. Checks one successful POST and one
persisted configuration. Both red orderings will run before production guard.

External launcher:
/home/azureuser/.copilot/session-state/30941a6a-b0c2-4550-8386-a144af07efac/files/capacity_401_validation.py.
It retries only the harness's exact lock-busy result every 60s, maximum 40m,
and does not retry actual test failures. Harness itself acquires the required
LOCK_EX | LOCK_NB before any generated data, SQL or browser. Initial admission
busy; observed shared-lock PID metadata only. No foreign output/resources read.

### Focused units and static checks

* Initial unit launcher failed import discovery (3 module import errors) because
  PYTHONPATH initialized before changing cwd. No tests actually ran there.
  Corrected to documented command from src/api with sanitized environment.
* `python -m unittest test_procurement_api test_auth test_ui_support -q`:
  PASS, 82 tests in 41.996s. Expected law-store diagnostic from fixture retained
  in external focused-units.log, not suppressed as a success-shaped fallback.
* `node --check` ops.js and app.js: PASS (final guard still pending).
* API `ruff check .`: PASS.
* Strict isolated Ruff E/F/I/B/UP and format at 100 on harness: PASS.
  Initial isolated import classification warning and new-block formatting
  corrected with the existing formatter; no semantic change.
* API `mypy` with external cache: PASS, 91 source files.
* `git diff --check`: PASS.

External logs and launcher live under the session files directory above.
At this historical checkpoint browser outcomes were pending; actual outcomes
are recorded below. Full-gate and live validation remain unavailable.

### P01-T01: First genuine red proof

red-packages-csp-safe-attempt-1.log: owned SQL Server and Chromium admitted on
first nonblocking attempt. Existing manager/draft scenarios passed. The new
packages-fails / older-workorders-401 ordering reached "retry continuation
settled", then failed the strict Sign in assertion with actual heading
"Capacity and work orders" at harness line 631. Exit 1. This is the requested
production race, not a fixture/timing failure. Production ops.js remains
identical to original HEAD, without the post-read guard.

At the next checkpoint the second red run was in progress; the external
in-memory launcher reverses only
the new test iteration to exercise workorders-fails first. No production/source
behavior is modified by that launcher; original logs remain separate.

Second genuine red completed: red-workorders-attempt-1.log, admitted immediately.
The workorders-fails / older-packages-401 ordering also reached "retry
continuation settled", then failed the strict Sign in assertion with actual
"Capacity and work orders", exit 1. Both required red outcomes now proved.
Owned containers cleaned by harness finally in both runs.

### P01-T02: Production guard

Added exactly `signal.throwIfAborted(); if (!me) return;` immediately after
the capacity Promise.all, before any form/content construction. No global
authentication, retry or draft behavior changed. Updated directly related
API README to describe the lifecycle guarantee and deterministic regression.
At this checkpoint green/static validation was pending; results follow below.

### P01-T02: Complete green and final static results

PASS, exit 0: green-attempt-1.log, admitted immediately with required heavy lock.
Owned SQL Server ama-capacity523-fb4c9313a3f5, loopback port 33259; generated
980 cases (443 open), 10 fictional staff; 1 package and all 601 work-order
identities matched browser responses. All 11 actual manager destinations passed.
Both delayed-sibling-401 endpoint permutations logged retry continuation
settled, retained Sign in heading/email/alert/focus, no capacity or retry
controls, exactly one real successful POST and one persisted configuration.
All previous seeded/empty, failed reads/retries, transport/403, editable-draft
recovery, cancellation and mutation-refresh expiry checks also passed.
Expected server BrokenPipe diagnostics from deliberately cancelled requests
remain in the log; browser unexpected HTTP/transport/page/console collectors
were empty. No error collector was disabled.

Final Node syntax (ops.js/app.js), API Ruff, strict harness E/F/I/B/UP and format
at 100, API mypy (91 source files) and whitespace checks all PASS.
Focused units: 82 PASS as recorded above; no backend source changed afterward.
No skip or historical full-gate receipt substitutes for this actual browser run.

## Pre-Review Reconciliation

P01-T01/P01-T02 checked with actual evidence; details, test ownership and
PC-001/003 dispositions reconciled. PC-002 remains rejected, not silently
represented as applied. Production delta is two guard lines; harness adds one
parameterized block and one typed local capture callback, no test removals.
No remaining implementation defect or design choice identified. P02-T01
original Review and P02-T02 publication still pending. Full gate remains blocked
by explicit az prohibition; live acceptance pending owner.

## Amendments and Divergences

No material divergence. Retained retry-button finally barrier is ordinary
test implementation detail from critique. Both red orderings required.

First admitted SQL/browser attempt (red-packages-attempt-16.log) failed in
test orchestration before the race assertion: request events can arrive before
both route interception callbacks finish. Not counted as red proof. Added one
typed local route callback with browser-side capture counter and explicit
wait_for_function barrier for both held reads, rather than a fixed sleep.
This immediately relevant test-only refinement preserves scope and was reflected
in the plan's maximum additions. Original failure log preserved.
Second admitted attempt (red-packages-capture-barrier-attempt-28.log) reached
the capture wait but rejected an expression-string wait under the application's
existing CSP. Corrected both waits to function expressions, matching existing
harness wait_for_function prior art. No CSP bypass or runtime policy change.
This fixture failure is also not red proof; its original log is preserved.

## Blockers and Remaining Work

Complete gate blocked: az barred; do not invoke it. P01 validation,
and original Review are now complete; only P02-T02 operational publication
remains in this committed pre-publication snapshot. Owner explicitly requested
scoped publication with this limitation; no full-gate or live acceptance claim.

## Original Review and Current Handoff

Exactly one original independent Review completed at
.copilot-tracking/reviews/logs/2026-10-28/capacity-page-523-delayed-401-review.md.
Execution Complete; scoped correction Conformant; full task Residual work.
No implementation defect found; one Low RV-001 noted stale pending prose.
Parent clarified current summary and marked earlier checkpoints historical as
the routed nonblocking handoff bookkeeping; no source correction, second
Review, closure-verification pass or regrading occurred. Original Review and
critique outcomes remain preserved.

Current results: P01 fully complete, P02-T01 complete. P02-T02 is explicitly
post-commit operational work and remains unchecked in this candidate snapshot.
Final push/thread evidence will be recorded externally at session
files/capacity-401-publication.json, avoiding a self-referential SHA commit.
Full gate blocked, live acceptance pending owner; hosted/human approval separate.

Tested source SHA-256:

* ops.js: e350f01c28a1e8acbcfbb6c6a8296d44035238e8866d10f4b3b95ee7686519bc
* harness: ac8151a004d48b0b8b79193c5a9afd866568313894f749caf5493f194072fcdf

All five exact task-created SQL container names from the failed fixture,
genuine red and green runs were checked afterward; none remained.
No foreign container or lock-owner output was read or altered.

## Follow-Up Items

Owner live verification; historical RV-004/005/006 outside this repair.
