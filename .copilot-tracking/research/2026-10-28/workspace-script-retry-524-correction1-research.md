<!-- markdownlint-disable-file -->
---
title: Workspace script retry correction research
description: New correction cycle for issue 524, preserving original adverse review
ms.date: 2026-10-28
---

# Task Research: workspace-script-retry-524-correction1

## Research Brief

Research RV-001 session invalidation and RV-002 browser proof from the original
2026-10-28 Review. Intended use: the owner's explicitly requested full correction
loop through publication. Scope: loader/session routing, focused unit/browser
checks and API documentation. Non-goals: live cause diagnosis, deployment, Azure,
secrets, .env, private datasets or rewriting earlier evidence.
Output mode: convergence. Status: In progress.

## Research Parameters

Focused posture, selected for named defects with supplied reproduction evidence.
Evidence root: .copilot-tracking/. Source edits prohibited during Research.
Heavy admission: nonblocking flock every 60 seconds, maximum 40 minutes, as
explicitly authorized by the owner; never interrupt another holder.
Python additions must respect Ruff line length 100.

## Extension Registry and Provenance

* Repository instructions: selected for branch, synthetic data and evidence gates.
* RPI Research: selected; wider, deeper, contrarian inline investigation.
* Web Interface Guidelines: selected for the changed browser code.
* Research specialist: skipped; this is one tightly coupled source trace.

## User Participation and Research Decisions

The user explicitly requests research, plan, implement, review, heavy validation,
commit, push and PR in this continuing worktree. No routine phase prompts are
needed. This is a bounded authorized correction cycle, not authorization for
unselected follow-up work or live verification.

## Direction Controls

Preserve earlier artifacts; use the correction1 suffix throughout new evidence.
Reuse clean branch fix/workspace-script-retry-524; no associated PR exists.
Read-only GitHub issue inspection confirms live verification remains owner work.

## Research Questions

| ID | Question | Status |
| --- | --- | --- |
| Q1 | What guard prevents stale-session status and view dispatch? | Open |
| Q2 | What deterministic browser evidence proves first-load retry and late settlement? | Open |
| Q3 | Which required local checks and publication gates apply? | Open |

## Prior Knowledge Gate

Original Review: .copilot-tracking/reviews/logs/2026-10-28/workspace-script-retry-524-review.md.
Original RV-001/RV-002/RV-003 remain historical adverse outcomes. Verify them
against source; do not assume earlier unexecuted browser coverage passes.

## Research Cycle Log

Opening state persisted before substantive source investigation.

### Cycle 1: Wider

Inline source trace confirmed API 401 sets me=null and calls login without
aborting routeController. Loader recovery is shared and may finish later.
Original tests inject an artificial abort; browser sign-out leaves the document.
Reflection: reproduce same-document invalidation, not merely navigation.

### Cycle 1: Deeper

route restores routeStatus before dispatching recovered roleScreensView; the
post-await guard checks only AbortSignal. Capture the session object at route
entry and check identity after await and in catch. Identity, rather than only
truthiness, also rejects a replaced signed-in session.
Browser recovery already intercepts real initial requests but does not assert
the readiness global is absent before login/retry. Delayed companion sleeps
300ms after release and only excludes one status substring.
Reflection: observe real request failure, pending retry, actual global and view;
use real-script load/error settlement plus Chromium precise coverage for
evaluation counts without replacing the companion bytes.

### Cycle 1: Contrarian

Removing a timed-out script is not a cancellation guarantee. Do not retry after
timeout or load-without-global. Accept either late real evaluation exactly once
or explicit browser cancellation with zero evaluation; assert current view/status
unchanged in either case. A null-only guard misses replaced sessions; an abort-only
fix leaves the same unsafe assumption in the regression.
Reflection: retain the loader budget and semantics; fix route session identity
and strengthen observable browser contracts rather than redesigning recovery.

## Evidence Log

| ID | Finding | Source |
| --- | --- | --- |
| C1 | 401 clears session without route abort | src/api/src/zava_forward/api/web/app.js:28-36 |
| C2 | Post-await restoration and dispatch lack session guard | src/api/src/zava_forward/api/web/app.js:205-248 |
| C3 | Node signed-out fixture artificially aborts | src/api/tests/test_workspace_scripts.py:151-156 |
| C4 | Late browser check sleeps and omits exact status/evaluation | src/api/checks/workspace_scripts_browser_check.py:169-185 |
| C5 | Existing browser lifecycle owns synthetic loopback data/server | src/api/checks/design_system_browser_check.py:222-283 |
| C6 | Complete gate and external exact-head receipt required by repository instruction | .github/copilot-instructions.md:1; src/README.md:69-182 |
| W1 | Native controls, polite async status, state handling rules | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (retrieved 2026-10-28) |

## Findings Mapped to Questions and Evidence

Q1 answered by C1-C3: guard entry, post-await success and failure with session
identity, test null/replaced sessions without abort, exercise actual API 401/login.
Q2 answered by C4-C5: decisive initial failure and pending retry, unchanged real
bytes, deterministic load/error settlement, coverage evaluation count, exact
status and route comparison before revisit.
Q3 answered by C5-C6 and the owner's instructions: run unit/browser ourselves
after bounded nonblocking admission, static checks, one independent critique
and Review, commit, full external receipt, fresh-main verification before push.

## Alternatives and Decision State

Accepted identity guard (C1-C3), rejected abort-only or null-only fixes.
Accepted precise coverage plus direct script load/error events (C4); rejected
fixed sleeps, response-only readiness and modifying the real script body.
Preserve bounded loader behavior and owner-pending live cause.

## Planning Readiness

Research disposition: executed. Status: Complete. Planning Readiness: Ready.
No further complete cycle needed: named defect contracts are covered; remaining
runtime uncertainty is explicitly assigned to implementation validation.
No source edits during Research; all source evidence read directly, no worker
delegation warranted for this single trace. Self-check: questions, provenance,
three ordered waves, alternatives, constraints and readiness recorded.
Next action: parent transitions to Plan for this authorized correction loop.
