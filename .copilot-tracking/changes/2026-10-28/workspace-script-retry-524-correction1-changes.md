<!-- markdownlint-disable-file -->
---
title: Workspace script retry correction implementation evidence
description: New implementation and validation evidence for issue 524
ms.date: 2026-10-28
---

# RPI Changes: workspace-script-retry-524-correction1

## Metadata

Task ID: 524-correction1. Date: 2026-10-28. Full plan scope.
Plan: .copilot-tracking/plans/2026-10-28/workspace-script-retry-524-correction1-plan.md.
Details: .copilot-tracking/details/2026-10-28/workspace-script-retry-524-correction1-phase-details.md.

## Execution Status

Complete implementation, full plan. P01/P01-T01/P01-T02 and
P02/P02-T01/P02-T02 complete for implementation and pre-Review handoff.
Approved write boundary: app.js, existing workspace unit/browser owners, API
README and new correction1 tracking artifacts. Earlier artifacts immutable.
One critique executed, original Revise with PC-001/PC-002 directly applied.

## Validation Intent

Focused units, syntax, Ruff/mypy and <=100-character changed Python lines;
full API discovery and actual Chromium under bounded shared-lock admission,
then independent Review and committed exact-head complete gate before publication.
No Azure, secrets, .env, private datasets or live acceptance.

## Completed Work

### P01-T01: Session identity boundary

app.js now captures the current me object, ignores no-session route entry,
rejects changed identity after awaited recovery and suppresses stale-session
errors. The existing Node owner covers ended and replaced sessions across map
and specialist destinations, ready/error/timeout/load outcomes, without abort.
The new regression failed against original source with stale role status,
then passed after the guard. Node syntax also passed.

### P01-T02 and P02-T01: Initial real-browser execution

External log: /tmp/ama-524-correction1-heavy-20261028.log. Shared nonblocking
admission succeeded immediately at 17:24:11Z. Full API discovery passed:
1149 tests in 427.344s, 314 existing opt-in/integration skips (not full integration
acceptance). The first three browser scenarios passed actual failed-initial-load
recovery (Leaflet one/two failures and real lexical companion).
The previously unexecuted native-focus assertion then failed: programmatic focus
after a mouse navigation does not establish keyboard :focus-visible modality.
The check now tabs from the main region to the actual Reload workspace button;
this is an in-scope fixture correction, not a production styling change.
Original failing output preserved; browser-only re-execution required.
Static checks passed: 32 focused units, package Ruff/format, mypy 92 files,
explicit changed Python <=100-character limit.

Browser attempt 2 preserved at /tmp/ama-524-correction1-browser-attempt2-20261028.log:
native keyboard reload now passes both exhaustion variants. Exact independent
status assertion caught an incorrect test expectation: the existing synthetic
sam fixture is Resident Liaison Officer, not Retrofit Programme Manager.
Corrected only that expected role; no production change.

Browser attempt 3 preserved at /tmp/ama-524-correction1-browser-attempt3-20261028.log:
the independent list legitimately updates status after its heading appears.
The test now waits for its completed perspective/scope/count announcement before
capturing the exact baseline, then compares it after script settlement. This
avoids mistaking the independent route's own normal asynchronous update for a
stale recovery write; no fixed sleep and no weakened post-settlement comparison.

## Validation Record

Final browser log: /tmp/ama-524-correction1-browser-attempt4-20261028.log.
At 17:32:31Z nonblocking acquisition found contention; the authorized 60-second
retry acquired at 17:33:31Z. Actual Chromium suite passed: Leaflet recovery after
one/two failed requests; real lexical companion recovery; terminal exhaustion
and missing-global native keyboard reload; navigation, timeout late delivery,
sign-out, actual same-document API 401/login; local Leaflet HTTP 200, 147552 bytes,
MIME/content length/no-store. Late responses in navigation, timeout and session
expiry each settled load/ready with exactly one real top-level evaluation.
Exact settled independent status/hash/view stayed unchanged, no stale dispatch,
no document refresh or pageerror. Cancellation was not observed; its safe
zero-evaluation/failure branch is asserted rather than assumed.

Final lightweight rerun after fixture corrections: 32 focused tests passed in
0.212s; package Ruff and 47-file format check passed; mypy 92 source files passed;
both changed Python files <=100 characters; Node syntax and git diff --check
passed. Full API discovery's 314 preexisting opt-in/integration skips are not
claimed as SQL/browser integration acceptance; the complete publication gate
supplies those separate required selectors.

## Implementation-Time Plan and Detail Updates

Only local regression-fixture corrections described above; approved intent,
scope, test ownership and retry policy unchanged. No significant divergence,
no new user decision or repeated critique.

## Pre-Review Reconciliation

Plan markers, details, completed-work summary, validation, follow-up and handoff
are current. Full implementation complete; one independent Review is ready.
Remaining publication gates are intentionally separate, not falsely checked
implementation acceptance.

## Blockers

None for Review. Complete committed-candidate gate and exact-head assessment
remain prerequisites for publication.

## Remaining Work

One independent correction Review; preservation-backed generated-cache cleanup;
privacy-safe commit; full external exact-head gate, fresh-main verification and
independent exact-head assessment; nonforce topic push and PR.

## Follow-Up Items

Owner live diagnosis and post-deployment verification remain pending (RV-004).
