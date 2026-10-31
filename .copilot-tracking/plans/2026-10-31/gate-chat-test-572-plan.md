<!-- markdownlint-disable-file -->
# RPI Plan: Exact chat-panel execution evidence

## Task Metadata

* Task ID: 572
* Task slug: gate-chat-test-572
* Plan date: 2026-10-31
* Planning status: Ready; single critique Complete / Revise, PC-001 resolved directly
* Phase details: .copilot-tracking/details/2026-10-31/gate-chat-test-572-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-31/gate-chat-test-572-plan-critique.md

## Executive Summary

Reuse the chat-panel wiring already merged by #575/#595. Close the remaining
exact-case evidence weakness: aggregate "Ran 1 test / OK" for an unrelated case
currently satisfies the dedicated receipt. Bind that command to one exact
verbose successful case in both live execution and verification, then exercise
real Chromium and the complete committed gate.

No runtime, workflow, skip-allowlist or dependency-pin change is intended.
The full gate is a post-Review publication prerequisite, not a claim made by
mocked receipt tests. Missing prerequisites or inherited failures block push.
Initial API discovery exposed missing dependencies, restored with pip; focused
validation is now waiting for shared-lock admission. Current main has advanced,
requiring a non-rewriting local topic merge before the final gate.

## User Decisions and Requirements

* Read #572 first and complete Research, Plan, Implement, Review in order.
* Meet all four issue criteria, preserving fail-closed integration/dependency skips.
* Run requested API discovery, Ruff check/format and tools/test_rpi_checks.py.
* Exercise local Playwright; pip only; no secrets/credential files, mvp code, main or other worktree changes.
* Commit dated evidence with the Copilot trailer; push chore/gate-chat-test-572 and open a main PR using Refs #572 only when publication gates pass.

## Goals

* Prove the dedicated Chromium command executes the exact required chat case.
* Retain current owned local execution and command/workflow coverage.
* Produce fresh real-browser and full exact-head acceptance evidence.

## Scope and Non-Goals

In scope: tools/rpi-checks.py, tools/test_rpi_checks.py, src/README.md and this
task's dated evidence. No generated source targets. No UI/runtime changes,
additional browser harness, broad skip changes, CI edits, cloud or paid inference.

## Functional Requirements

* Existing parser gains optional exact test-ID enforcement, used only for the
  dedicated chat selector; existing suites retain current behavior.
* Execution and receipt verification share enforcement: exactly one test, zero
  skips, one exact verbose "... ok" result and no other result lines.
* Preserve exact API-discovery exception and strict required integration skips.

## Non-Functional Requirements

* No new dependencies, unsafe casts or broad catches; strict tooling types pass.
* Receipt mutation regressions update hashes/counts so failures prove semantics.
* Original critique/Review remain immutable; final receipt stays external and
  is invalidated by any later commit/base/tool/input change.

## Acceptance Criteria

* AC1: Existing exact selector/flag/path/coverage retained; actual local Chromium executes one named test, zero skips.
* AC2: Unexpected integration/dependency skips still fail, including chat skips in the dedicated stage.
* AC3: Regression tests reject wrong/missing/duplicate success IDs, incorrect totals and skipped required execution; existing dispatch and discovery regressions pass.
* AC4: After original Review and candidate commit, fresh --all gate passes all groups, including browser/MSSQL, and verifies against fetched current main immediately before publication.

## Sources

* .copilot-tracking/research/2026-10-31/gate-chat-test-572-research.md: C1-C8 and W1-W2.
* tools/rpi-checks.py and tools/test_rpi_checks.py: canonical gate/parser/receipt owners.
* src/README.md: complete local gate and shared locking.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Enforce exact chat execution

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Update shared parser and both call sites

Optional expected-test identity in check_skips; selected only by the dedicated
chat command at Runner.command and verify_commands. Reuse discovery tuple's
verbose ID. Reject mismatched result identity/counts explicitly with GateError.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add regressions and guide clarification

Owner: GateTests in tools/test_rpi_checks.py. Exact removals: none. Maximum
additions: two test methods, plus cases in existing receipt mutation method.
Update both passing receipt fixtures to name the actual required selector.
Semantic browser coverage remains unchanged in test_chat_panel.py; no test there
is added/removed. Document exact successful-ID proof in src/README.md.

<!-- rpi:phase id=P02 -->
### [ ] P02: Validate and independently review

Depends on P01.

<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: Run requested local validation and real browser

API command exactly as requested; API Ruff check/format; tooling unittest,
Ruff check/format and strict mypy. Run opted-in exact browser case under the
existing shared heavy lock, retaining external logs. Missing tools permit only
pip/pinned trusted prerequisite restoration, not skip tokens or cloud fallback.

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Perform one independent original Review

Activate rpi-review once. Preserve outcome and route residual findings to later
work, without a current-task implementation/review loop.
Blocking current-task source/acceptance findings stop publication. Missing final
committed gate evidence is intentionally obtained in P03. Nonblocking residuals
require explicit disposition without relaxing acceptance.

<!-- rpi:phase id=P03 -->
### [ ] P03: Exact-head publication gate

Depends on P02.

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Commit, full gate, verify and publish

Resolve gh account/privacy-safe local email. Commit implementation and original
dated evidence/trailer. Fetch main; run --all in a new external directory using
the runner's own shared lock. Verify fresh receipt against current main directly
before independent exact-head assessment and push. No later evidence commit may
reuse it. Publish with Refs #572 and factual evidence only if requirements pass.
Require no unresolved blocking original Review findings and an eligible
independent exact-head assessment. Review completion alone is not approval.
An intermediate implementation checkpoint may precede the original Review to
enable a clean non-rewriting current-main merge. The final evidence candidate
includes the original Review and is committed before the complete gate.

## Dependencies

* Local Chromium, Docker/MSSQL, pinned scanner and shared lock admission.
* Independent critique and original Review before publication.
* Current main/base and clean committed inputs for final receipt.

## Critique Disposition

Single critique: Complete / Revise, preserved unchanged in the critique artifact.
PC-001 resolved directly: P02-T02/P03-T01 and phase details now distinguish blocking
source/acceptance findings, planned later full-gate evidence and explicitly
disposed nonblocking residuals. No second critique or user decision needed.

## Follow-Up Items

* None.

## Handoff

Implementation changes record:
.copilot-tracking/changes/2026-10-31/gate-chat-test-572-changes.md.
No unresolved design choices. P03 remains a real execution obligation.
