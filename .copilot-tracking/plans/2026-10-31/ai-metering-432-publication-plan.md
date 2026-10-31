<!-- markdownlint-disable-file -->
# RPI Plan: AI metering publication remainder

## Task Metadata

* Task ID: 432-publication; slug ai-metering-432-publication.
* Parent: 432-review-findings; date 2026-10-31.
* Planning status: Ready; one critique Complete / Revise, findings directly disposed.
* Details: .copilot-tracking/details/2026-10-31/ai-metering-432-publication-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-publication-plan-critique.md

## Executive Summary

Publish the completed source-only metering work with honest full-gate and
independent assessment evidence. Add a minimal explicit inherited-lock mode
so the user-required outer flock and existing self-locking runner can compose
without deadlock or an unlock gap. Preserve normal runner/receipt contracts.

### What You May Not Know

The old failed lock attempt ran no integration groups. Current main a75bbdff
has no observed baseline-fix PR. Operational economics and whole-issue
acceptance remain unproven; this PR uses Refs #432. Original parent adverse
Review and subsequent correction evidence remain immutable.

## User Decisions and Requirements

* Continue this clean feat/ai-metering-432 worktree through the remaining full
  RPI loop and publish; merge origin/main, taking main rubric score on conflict.
* Queue with flock -w 1800 on /tmp/ama-rpi-heavy.lock; do not stop because busy.
* If full gate exposes known main B023 or test_chat_panel failures, refetch and
  merge main if fix/gate-baseline-b023 landed; otherwise record and proceed.
* Push git push -u origin HEAD without force and open main PR with evidence.
* Pip only; no secrets, Azure, paid inference or fabricated acceptance.
* Preserve privacy-safe identity and required Copilot commit trailer.

## Goals

* Safely acquire continuous shared-resource exclusion before the full gate.
* Deliver a reviewed, traceable PR while distinguishing source observations,
  integration evidence, allowed baseline exceptions and operational gaps.

## Scope and Non-Goals

* In scope: tools/rpi-checks.py, tools/test_rpi_checks.py, the existing
  src/core/tests/test_sensor_privacy.py transport fixture, src/README.md and dated
  child evidence; authorised ancestry merge and publication.
* Out of scope: metering redesign, unrelated baseline fixes, generated pitch,
  raw telemetry content, private data, spend or human/hosted acceptance.

## Functional Requirements

* Add optional --heavy-lock-fd. Validate descriptor/path regular-file
  inode/device, reject symlink/nonmatching/invalid FD; duplicate the descriptor
  and assert nonblocking exclusive flock without unlocking caller ownership.
* Standalone heavy_lock(timeout) remains unchanged; no environment bypass,
  receipt trust change, unlock/reacquire handoff or foreign process mutation.
* Keep lock across Runner.run and automatic verification; caller owns outer FD.

## Non-Functional Requirements

* Wrong/closed/contended descriptors fail explicitly. Only runner-owned duplicate
  is closed. Child subprocesses must not gain uncontrolled lock ownership.
* All existing runner tests plus focused Ruff/format/mypy pass.
* Full --all gate uses clean committed exact HEAD and fresh external output,
  pip-isolated dependencies, actual SQL/browser/images/scanner groups.
* No passing gate claim for the explicitly allowed known baseline failures.

## Acceptance Criteria

* Actual util-linux outer-flock subprocess runs heavy_lock successfully without
  self-deadlock; a separate open cannot acquire until caller releases its lock.
* Wrong file, closed/negative FD, symlink and existing other-owner contention
  fail closed; caller FD survives normal and exceptional context exits.
* Original metering test cap and test modules remain unchanged. New child
  coverage owns tools/test_rpi_checks.py only, maximum five new test methods,
  removals none; semantically assert ownership/invalidity, retain regressions.
* Source/evidence commits exist; full gate attempted after commit; passing
  receipt verified at current base, or exact known baseline exception documented.
* One child independent critique and one child independent Review preserved.
* Branch pushed normally and main PR open with Refs #432 and explicit gaps.

## Sources

* Child research: .copilot-tracking/research/2026-10-31/ai-metering-432-publication-research.md; C1-C5/W1.
* Caller-named correction changes and original Review; complete gate src/README.md.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Compose lock safely and prepare candidate

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement validated inherited lock and ownership tests

* Dependency: one final-candidate critique and dispositions.
* Targets: runner/test file and directly related gate README.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Reconcile main, original evidence and committed candidate

* Dependency: P01-T01 targeted validation.
* Fetch/merge main; preserve original parent files and record exact identities.
  Commit implementation and original child evidence with privacy-safe identity.
* First full gate revealed a coupled existing privacy test needs an explicit
  mocked financial admission fixture. Correct that existing method, retain all
  privacy assertions, and rerun a fresh committed candidate; no new method/module
  or production admission exception. P01-T02 is reopened for this in-scope
  validation correction before the sole child Review.

<!-- rpi:phase id=P02 -->
### [ ] P02: Complete queued integration validation

<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: Run complete gate and reconcile known baseline exceptions

* Dependency: P01-T02 clean committed candidate.
* Command: flock -w 1800 /tmp/ama-rpi-heavy.lock python3 tools/rpi-checks.py
  --all --jobs 3 --heavy-lock-fd 3 --base CURRENT_MAIN --out NEW_EXTERNAL_DIR.
* Preserve failed output; if known B023/chat baseline failure, fetch main and
  merge landed fix, otherwise record the caller-authorised exception.
* Freeze all in-tree evidence before final gate and the sole child exact-head
  Review. Final result/state evidence stays in an external dated tracking mirror
  and the PR body, without dirtying or changing assessed HEAD.
* Verify passing receipt immediately before exact-head assessment and push.
  A changed source/base/identity after Review blocks that assessed boundary and
  routes a later task; do not silently claim assessment of future commits.

## Dependencies

* Real local gate prerequisites; no skip/cloud fallback or protection change.
* Independent Review is a child lifecycle phase after implementation/gate.
  Publication follows it, with no second Review; material findings route later.

## Critique Disposition

| Finding | Disposition | Resolving contract |
| --- | --- | --- |
| PC-001 High | Directly applied | Freeze all in-tree evidence before sole exact-head child Review; final review/state in external dated tracking mirror and durable PR body |
| PC-002 High | Directly applied | Per-command/group status/root-cause matrix; known failures and causal blocked descendants explicitly disclosed, all independent failures block |
| PC-003 Medium | Directly applied | Five-method ownership/invalidity/subprocess/main-lifetime allocation in phase details |

Original critique Complete / Revise is preserved; no second critique.

## Follow-Up Items

* Owner/Finance: OD-51, numerical applicable prices, attributable billing,
  measured held-out batch and time released. Outside source-only publication.
* Accounting/presentation owners: resident/historical joins and actual
  manifest-owned pitch/Q&A delivery. Preserve RV-006.
* Owner/reviewers: hosted checks and human approval remain required after PR.

## Handoff

* Changes: .copilot-tracking/changes/2026-10-31/ai-metering-432-publication-changes.md
* Automatic parent continues P01 after critique; no routine question needed.
