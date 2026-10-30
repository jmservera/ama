<!-- markdownlint-disable-file -->
# RPI Phase Details: employee-chat-dismissal-correction

## Metadata

* Task ID: employee-chat-dismissal-correction-2026-10-30
* Date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/employee-chat-dismissal-correction-plan.md
* Research: .copilot-tracking/research/2026-10-30/employee-chat-dismissal-correction-research.md

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Focus correction | Complete, red/green browser proven | P01-T01 |
| P02 | Validation and local delivery | Complete execution/delivery, broad AC4 unmet | P02-T01/P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Focus correction

Context: show only preserves visible chat descendants; original delayed-dismissal check asserts the wrong #app target (C2/C3). Native hide semantics already correct (C6).

Intent/boundaries: change employee show only plus last-rendered context, focused checks and related README. No shared-widget/auth/resident changes. No removals or generated targets; at most one added helper.

Immediately relevant implementation reconciliation: the first integrated shared browser run failed at employee_refresh's closed-chat branch because it also expected #app focus after deliberate launcher dismissal. Update only that existing assertion to launcher, consistent with FR1/RV-001; no behavior requirement changes, no new helper or repeated critique. Raw adverse shared-green.log preserved. Distinguish the body counterexample by explicitly blurring rather than duplicating external-node removal.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Red-before-green browser correction and documentation

Dependencies: one critique disposition. Capture exact focus after real dismissal while real case render is held, release read, assert activeElement equality, hidden panel and false expanded state. Include Escape, Close and outside navigation control. Retain draft on explicit reopen. Keep internal composer/log/Sources assertions. Extend actual browser counterexamples for cross-path navigation and lost focus: removed app input, disconnected external control, body/no-chat, changed session.

Implementation candidate: record session/path of last show; preserve outside-app focus only within that rendered context, excluding body/root and requiring isConnected after replacement. Existing visible chat ownership remains independent. Destination/session transitions still focus app. Do not restore an old node after user focus changes or add dismissal flags.

Completion evidence: unchanged-source browser failure, corrected-source browser pass, 12 original combinations, README scoped claim. No source edits before red assertion run.

Actual result: submit-red.log exited 1 on exact Escape retained-focus assertion before runtime edits; submit-green.log exited 0 after show correction, all three dismissals, internal focus, ordinary navigation/session/lost-focus counterexamples, 12 sends, auth lifecycle and resident actual Enter/Send passed.

<!-- rpi:phase id=P02 -->
## P02: Validation and local delivery

Context: original RV-002 is missing full discovery, not a failed suite. Owner explicitly allows queued lock wait this time.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Locked full API suite and static/browser checks

Dependencies: P01 runtime finalized. From src/api with existing /tmp/mv/bin first on PATH:

```bash
flock -w 600 /tmp/ama-rpi-heavy.lock env \
  PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests \
  python3 -m unittest discover -s tests -q
ruff check .
ruff format --check .
mypy
```

Use sanitized env for units (allow only tool/home/lang/runtime paths, no inherited model/storage credentials); do not change selectors or skip policy. Full discovery's expected opt-in skips must be enumerated from actual output. Existing browser fixture health-checks owned constructed-data loopback. Run focused submit (actual resident Enter/Send), shared-widget with pinned axe (integrates new employee assertions), employee chat and resident assistant checks. Record all results in Changes; unrelated failures stay failures, not silently repaired.

Environment refinement from actual failure: retain existing PATH after prepending /tmp/mv/bin when using env -i; otherwise Node's existing nvm path is lost. First full discovery's 45 missing-node errors remain adverse evidence; fresh complete locked rerun is mandatory and was admitted. No packages installed.

Completion evidence: actual counts/exits/skips, external raw logs/JSON, browser/version and exact command provenance. Lock timeout or missing prerequisites block AC4; no cloud fallback.

Actual result: complete locked rerun exited 0, 1361 tests in 474.769s, OK / 318 skips. 317 skip declarations inventoried by ID/reason; one JSON COMMIT non-applicability (JsonProgressApi.test_committed_handoff_failure_returns_existing_explicit_outcome_contract). Static/focused/shared/employee browser pass. Additional resident browser fails `documents help` expected Survey: Missing on candidate and archived original 366ca4a2, retained as separate follow-up; broader AC4 is partial, not silently waived. One Review may assess this explicit result before local commit.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Independent Review and local commit

Dependencies: P02-T01 evidence reconciled. Fresh reviewer may write only new Review artifact. Preserve original critique and adverse Review. One Review execution, distinct outcome and follow-up routing. Parent records current phase/checklist/state before and after transition, then privacy-safe local commit after gh api user lookup without printing credentials. Refs #550 only, required Copilot coauthor. No push or live warmup.

Completion evidence: independent Review artifact and local Git commit; full publication gate, hosted checks and human approvals unclaimed. No blockers known at candidate drafting.

Actual result: exactly one Review Complete / Not accepted on broad AC4; original RV-001/RV-002 resolved, RV-003 baseline resident residual. Source and original dated correction evidence committed locally as 2b12ce3f with authenticated privacy-safe author/committer, Refs #550 and required coauthor. No push, no source changes after Review. Closeout artifact reconciliation is documentation/state only; no repeated Review.
