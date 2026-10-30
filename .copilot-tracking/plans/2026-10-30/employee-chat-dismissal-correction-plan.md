<!-- markdownlint-disable-file -->
# RPI Plan: employee-chat-dismissal-correction

## Task Metadata

* Task ID: employee-chat-dismissal-correction-2026-10-30
* Task slug: employee-chat-dismissal-correction
* Plan date: 2026-10-30
* Planning status: Ready; independent critique Complete / Pass, no findings
* Phase details: .copilot-tracking/details/2026-10-30/employee-chat-dismissal-correction-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-30/employee-chat-dismissal-correction-plan-critique.md

## Executive Summary

Correct only delayed rendering's focus decision: within the same rendered authenticated workspace, leave a deliberately selected connected external control or chat launcher focused. Do not reopen chat. Preserve ordinary workspace landing for actual destination/session changes and removed controls, and keep the original submitted-chat visibility fix.

Implementation result: RV-001 corrected with red/green browser proof; RV-002 full API evidence obtained, 1361 tests / OK / 318 skips under required lock. Static and focused/shared/employee browsers pass. Additional unchanged resident-assistant browser failure is separately baseline-proven and retained, so broader AC4 acceptance remains partial.

### User Decisions and Requirements Highlights

* Existing branch, local Refs-only commit, no push, Azure or live warming.
* Red-before-green browser proof, all 12 original send combinations and complete requested API/static/browser evidence.

### What You May Not Know

The original passing browser check asserted the wrong focus target. Correcting that assertion is mandatory. Blindly skipping all autofocus would break ordinary navigation, so counterexamples are part of acceptance.

### Unresolved Decisions or Blockers

No owner decision. Full API passed under requested lock. Additional standalone resident-assistant browser fails on unchanged legacy `documents help` expectation, reproduced from archived 366ca4a2; broad AC4 is not claimed complete. Focused/shared/employee browser and static checks pass.

## Sources

* .copilot-tracking/research/2026-10-30/employee-chat-dismissal-correction-research.md: C1-C8/W1, executed / Ready.
* .copilot-tracking/reviews/logs/2026-10-30/employee-chat-closes-on-send-review.md: original RV-001/RV-002, preserved unchanged.
* Owner request 2026-10-30: exact branch, stages, lock timeout and validation.

## User Decisions and Requirements

* Run a new correction Research/Plan/Implement/Review cycle for RV-001 and RV-002 on fix/employee-chat-closes-on-send from 366ca4a2.
* A user who deliberately closed chat must retain chosen focus after delayed rendering, with no reopening.
* Add a failing-before regression in src/api/checks and keep every Enter/Send x case/no-case x none/route/session combination passing.
* Run full src/api discovery with the specified PYTHONPATH and python3, holding /tmp/ama-rpi-heavy.lock using flock -w 600, plus ruff check, ruff format --check, mypy and browser checks.
* Commit dated evidence locally, Refs-only; no push, live warming, Azure or credential output.

## Goals

* Resolve the demonstrated focus defect and missing package evidence without changing widget, resident or auth authority.
* Preserve original adverse evidence and independently assess this distinct correction candidate.

## Scope and Non-Goals

In scope: app.js show focus ownership, existing focused browser module and directly coupled shared-browser expectation, API README, dated correction artifacts. No source removals, generated runtime output, dependency changes or new check modules. Maximum runtime change: show plus one last-rendered-context variable. Test owner: checks/chat_submit_browser_check.py, already integrated by checks/chat_widget_browser_check.py. Maximum additions: extend render_focus and add one navigation/counterexample helper in that module; update the shared check's closed-refresh focus assertion to launcher. Canonical code is src/api/src/zava_forward/api/web/app.js; no generated counterpart.

Out of scope: shared-widget/resident redesign, unrelated unit fixes, new tools, remote or issue changes, live/human/WCAG acceptance, publication gate claims.

## Functional Requirements

* FR1: Same rendered session/path refresh preserves exact connected external/launcher focus after deliberate Escape, Close or external-focus dismissal; panel hidden and launcher aria-expanded=false.
* FR2: Composer, log and Sources focus retained; pending submitted answer and draft/skill semantics unchanged.
* FR3: Genuine destination/session changes and removal of the focused app/external node retain normal #app focus fallback. No global autofocus suppression.

## Non-Functional Requirements

* NFR1: No timer, global dismissal flag, widget callback or dependency added.
* NFR2: Synthetic loopback fixtures, existing tools, sanitized environment; no default private data, live inference, Azure or credentials.
* NFR3: Full unit command runs once admitted under authorized waiting lock; actual exits/counts/skips recorded externally and in dated Changes. No lock bypass or fabricated pass.

## Acceptance Criteria

* AC1: New exact focus assertion fails on original app.js, then passes after correction for delayed Escape, Close and external dismissal; hidden/no-reopening and draft retained.
* AC2: All 12 original sends pass and existing auth/session stale-result and resident boundaries remain passing.
* AC3: Browser counterexamples prove actual navigation/session or removed targets still land in #app; no-chat rendering remains usable.
* AC4: Full API suite, ruff check ., ruff format --check ., mypy, focused/shared/browser checks pass or explicit failures block acceptance. Required command: from src/api, PATH=/tmp/mv/bin:$PATH and PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -q, within flock -w 600 /tmp/ama-rpi-heavy.lock.
* AC5: One independent critique, one independent post-implementation Review, original evidence unchanged, privacy-safe local Refs #550 commit with required trailer and no push.

## Implementation Context Record

Research and state share task slug/date. Implementation owns .copilot-tracking/changes/2026-10-30/employee-chat-dismissal-correction-changes.md. Independent Review owns .copilot-tracking/reviews/logs/2026-10-30/employee-chat-dismissal-correction-review.md. Parent continues automatically after gates; no publication is authorized.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct focus ownership with measured regression

Dependencies: finalized critique dispositions.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Red-before-green browser correction and documentation

Extend exact delayed-dismissal assertions first, preserve failing original-source log, then minimally correct show and document same-context scope. Verify navigation counterexamples and original matrix.

<!-- rpi:phase id=P02 -->
### [x] P02: Complete local evidence and independent assessment

Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Locked full API suite and static/browser checks

Use fresh external session evidence paths, flock -w 600, existing pinned axe 4.10.3, focused and shared checks plus employee/resident assistant checks where existing coverage warrants. Record actual commands, exits, skips, interpreter/browser versions. No publication gate substitution.

Execution complete, not all-success acceptance: full API passed, static/focused/shared/employee passed, additional resident browser failed both candidate and original baseline. Changes preserves every adverse attempt and routes unrelated resident reconciliation.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Independent Review and local commit

Reconcile artifacts, dispatch one read-only fresh Review, record outcome separately from execution. Route new findings rather than repeating Review. Resolve GitHub identity privately, local privacy-safe author/committer, Refs #550 only, required trailer. Do not push.

Completion evidence: one independent Review Complete / Not accepted on broad AC4, original RV-001/RV-002 resolved; local source/evidence commit 2b12ce3f. This marker records execution/delivery, not broad acceptance. No source changes after Review and no push.

## Dependencies

* Existing /tmp/mv Python 3.12 and development tools/browser.
* Shared lock admission, authorized timeout 600 seconds.
* Pinned axe file; hash enforced by existing browser checks.

## Critique Disposition

Exactly one final-candidate independent critique executed Complete / Pass with no findings. No revisions or owner decisions required; original critique preserved in its distinct task.

## Follow-Up Items

* Reconcile unchanged standalone resident-assistant legacy topic prompts with current finite grammar; outside employee focus correction. Owner/coordinator; evidence resident-green.log, `documents help` refuses instead of old Survey expectation. No silent unrelated fix.
* Coordinator-owned deployed-site verification after separate deployment authorization; local synthetic checks do not establish live/human acceptance.

## Handoff

All P01/P02 execution/delivery markers complete; source/evidence committed locally as 2b12ce3f. One independent Review Complete / Not accepted on broad AC4; original RV-001/RV-002 resolved, RV-003 separate resident residual. Automatic session remains at Follow-up with no child authorized. No source correction, repeat Review or push.
