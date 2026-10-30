<!-- markdownlint-disable-file -->
# RPI Changes: employee-chat-closes-on-send

## Metadata

* Task ID: employee-chat-closes-on-send-2026-10-30
* Date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/employee-chat-closes-on-send-plan.md
* Details: .copilot-tracking/details/2026-10-30/employee-chat-closes-on-send-phase-details.md

## Execution Status

Full ordered loop executed, candidate Partial / Not accepted. P01-T01 and P02-T02 complete. P01-T02 marker reopened after original Review RV-001; P02-T01 full-unit evidence blocked (RV-002). One critique and one independent Review preserved; no repeat or source correction after Review.

## Execution Summary

Reproduce-before-fix, then surgical employee lifecycle correction and focused/full requested validation. Approved boundary: app.js, relevant widget/host only if needed, existing checks/tests plus at most one focused browser module, API README and dated evidence. No remote writes or Azure/deployment.

## Completed Work

Research baseline: actual loopback API and Chromium; 12 combinations show isolated sends pass, route refresh hides, equivalent session refresh hides and loses answer. External original baseline JSON/script/screenshot retained in session files. Research artifact records summarized original outcomes.

### Failing-before regression (P01-T01)

Added src/api/checks/chat_submit_browser_check.py outside runtime package. Before source edits it exited 1: `AssertionError: False/Enter/route: refresh dismissed submitted chat`. Original log: external session files/submit-red.log. This is the actual local app, health-checked loopback and real Chromium, not a DOM stub.

### Lifecycle correction (P01-T02)

app.js show() no longer steals focus owned by a visible shared chat. start() preserves reference identity only for equal complete user/account snapshots, updates other snapshot fields, disposes chat on changed auth and rejects success after me changed during re-check. Shared busy, external-focus and Escape semantics unchanged. Existing refresh expectation and related API guide updated. Resident host has no analogous workspace rerender path; runtime unchanged pending browser proof.

## Implementation-Time Plan and Detail Updates

PC-001 requires real start() auth equivalence/change/race tests; PC-002 exact focus and delayed-dismissal tests. Both preserve approved intent; no new user decision.

## Validation Record

* New browser regression: green, all 12 matrix cases plus actual start() setup/thread/ask auth variants/race and resident actual Enter/Send rules answers (external submit-green-2.log). Initial green-1 failed due to browser test expression returning api function; fixed test expression, no runtime correction needed.
* Existing comprehensive shared browser + pinned axe 4.10.3: passed, including 48 focus/denial combinations, 12 obsolete-result cases, all access status cases, resident consent/session and layout/following checks (shared-green-1.log).
* Targeted units: 68 tests, OK, 1 opt-in SQL skip; expected fixture diagnostics.
* ruff check ., ruff format --check ., mypy: passed; 59 formatted files, 114 source files. node --check app.js passed.
* Full API units: both attempts not started because nonblocking shared heavy lock was busy (final flock exit 75); no waiting, bypass or cloud fallback. Required full-unit validation remains blocked.
* New employee regression is also invoked by existing comprehensive shared browser owner, not only a standalone command.
* Final integrated shared browser rerun passed including new matrix/auth checks and all prior employee/resident/axe checks (shared-green-final.log, Chromium 156.0.8078.4). Standalone focused resident actual-rules send checks passed (submit-green-2.log); resident check code unchanged afterward.
* Final ruff check ., ruff format --check ., mypy, node --check app.js and git diff --check passed after integration; compileall new check passed.

Commands from src/api use `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests`, `/tmp/mv/bin/python`, `/tmp/mv/bin/ruff`, `/tmp/mv/bin/mypy`. Browser command: `python -m checks.chat_widget_browser_check --axe <external>/axe-4.10.3.min.js --out <new-external>/shared-green-final`; focused: `python -m checks.chat_submit_browser_check --out <new-external>/submit-green-2`. All raw logs/screenshots/JSON remain under external session files; no credentials recorded.

## Changed-Web Guidelines Review

Fresh source retrieved 2026-10-30 before direct changed-web inspection; assessed changed app.js focus/session block against all applicable fetched rules. Unchanged broad page aesthetics/content excluded from this bug scope.

### src/api/src/zava_forward/api/web/app.js

Pass for changed lines: native controls/ARIA/live updates unchanged; dialog-owned focus retained; no new animation, styling, navigation element or data presentation. No new changed-line guideline finding. This is not whole-app WCAG or human assistive-technology acceptance.

Original independent Review supersedes that direct focus assessment for the delayed-dismissal boundary: RV-001 establishes that app.js:95 and the contrary new test expectation still redirect deliberate outside/launcher focus after pending render. The earlier assessment is retained, not rewritten into a claimed success.

## Independent Review and Local Delivery (P02-T02)

Exactly one independent Review executed Complete; outcome Not accepted, two Medium findings. Canonical record: .copilot-tracking/reviews/logs/2026-10-30/employee-chat-closes-on-send-review.md. RV-001 is a remaining delayed-dismissal focus defect; RV-002 is missing required full-unit evidence. Both routed to later work. No implementation/review loop, issue closure, publication approval or remote operation inferred.

Original critique, all dated phase evidence and source candidate are included in the local delivery commit. Authenticated account resolved with gh api user; repository-local privacy-safe author/committer address used, required Copilot trailer and Refs-only issue reference. Commit identity is externally verifiable with git log; this record intentionally contains no self-referential commit hash.

## Pre-Review Reconciliation

* Pre-Review handoff recorded P01 complete; original Review later found RV-001 and parent reopened P01-T02/P01 markers, preserving that adverse result.
* P02-T01 partial/blocked only for required full API suite; targeted/static/browser results current.
* P02-T02 one independent Review and local commit delivered. RV-001 source/focus-regression work remains routed; original critique preserved, no repeat critique.
* Ready for independent assessment of the implemented boundary with explicit validation blocker, not for a conformant/publication claim.

## Blockers

Full API units cannot run while /tmp/ama-rpi-heavy.lock is held by another task. Owner/coordinator must run the documented full suite when available. No publication authorized; complete exact-head gate and hosted/human approval not claimed.

RV-001 remains open: preserve deliberately chosen connected focus after delayed rendering. Headline submitted-chat visibility/answer correction passes, but the full accessibility acceptance boundary is not met.

## Remaining Work

P01-T02 delayed-dismissal focus (RV-001, later rpi-implement); P02-T01 full-unit evidence (RV-002, later bounded validation).

## Follow-Up Items

Owner/coordinator live-site verification after separately authorized redeployment. Local evidence does not establish deployed behavior or human accessibility acceptance.

Rank 1: RV-001 bounded focus correction. Rank 2: RV-002 full API evidence when shared lock admits. Rank 3: coordinator live-site verification, separate deployment authorization required.

## Return-to-Caller State

Ordered Research/Plan/Implement/Review executed once. Candidate Partial / Not accepted; headline correction browser-proven, two routed Medium findings open. Local source/evidence commit only; no push, deploy or issue closure.
