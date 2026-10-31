<!-- markdownlint-disable-file -->
# Implementation Plan: gate-chat-test-572-validation-correction

Task ID: 572. Date: 2026-10-31. Parent: gate-chat-test-572.

## Executive Summary

Validation/evidence-only correction: requested main merge is already satisfied.
Obtain missing real API/Chromium evidence, preserve original adverse records,
then commit dated correction evidence and run the complete gate with a 30-minute
admission wait and one admission retry. Publication requires a fresh passing
receipt, current-main verification and independent exact-head assessment.
No source, test, workflow or dependency changes are presently justified.

## User Decisions and Requirements

* Continue on chore/gate-chat-test-572; merge latest main without rewriting.
* If conflicted, take main's score snapshot, preserve both knowledge-log entries.
* Update workflow hashes only for an actual workflow edit.
* Wait 1800 seconds for heavy admission and retry once; light checks need no lock.
* Run API unit tests, Ruff check/format and full local gate; pip only, no secrets
  or Azure changes. Commit with supplied Copilot trailer, push without force,
  and create a PR to main containing original and correction RPI artifacts.
* Use Closes #572 only if all four criteria are proven; otherwise Refs #572
  with explicitly unmet criteria.

## Goals

Collect the parent's missing execution and exact-head publication evidence.

## Scope and Non-Goals

Only dated correction tracking evidence; preserve original history. No runtime,
UI, workflow, score or dependency edit. Any discovered source defect becomes
explicit correction work rather than an unreported validation workaround.

## Functional Requirements

Retain exact owned browser selector and fail-closed runtime/receipt rules.
Run real opted-in Chromium on synthetic loopback fixtures and full browser/MSSQL
groups. API discovery uses documented shared core/agents test paths.

## Non-Functional Requirements

Use the same shared heavy lock; never interrupt its owner. Focused Chromium uses
outer `flock -w 1800`; self-locking full gate uses `--lock-timeout 1800`, avoiding
documented double-lock deadlock. Retry admission once, never silently retry a
failed assertion as if it passed. New external logs/output for every attempt.
All source/base/tool changes invalidate final gate evidence.

## Acceptance Criteria

AC1-AC4 are exactly issue 572's current criteria. Required evidence is named
Chromium success/zero skips, preserved negative-skip regressions, owned command
inventory, and a freshly verified full exact-head receipt including real MSSQL.
Hosted checks and owner merge approval remain separate.

## Test Ownership Contract

Canonical owners: tools/test_rpi_checks.py and src/api/tests/test_chat_panel.py.
Removals: none. Maximum additions: zero for this validation-only correction.
Generated targets: external logs/receipt only, not copies inside git.
Synthetic parser/receipt regression is not actual browser evidence.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01: Actual validation evidence

* [x] P01-T01: Run API discovery, API/tooling Ruff and tooling tests.
* [x] P01-T02: Run exact real Chromium with locked admission and one timeout retry.

<!-- rpi:phase id=P02 -->
### P02: Original correction Review and candidate

* [x] P02-T01: Reconcile evidence and obtain one independent correction Review.
* [ ] P02-T02: Commit dated original correction evidence with privacy-safe identity.

<!-- rpi:phase id=P03 -->
### P03: Final gate and publication

* [ ] P03-T01: Fetch/reconcile main; full committed gate with 1800-second admission.
* [ ] P03-T02: Verify against freshly fetched main and independent exact-head
  assessment; push and PR only with passing evidence. No later candidate commit
  may reuse this receipt.

## Critique Disposition

Single critique Complete / Revise; original verdict preserved.
PC-001: executor-specific temporary-file restriction does not apply to the
parent's Bash tools. Parent executes the unchanged shared lock; no alternate
executor, lock, bypass or source change is needed. Real admission logs are the
resolving evidence, not an assumed pass.
PC-002: applied directly. Later main drift requires relevant source/test/tool
comparison with the reviewed boundary. Evidence-only ancestry may proceed with
documented equivalence; relevant changes require scoped independent exact-head
assessment before publication. Earlier focused results are historical after
relevant input changes; the current full gate must execute those inputs.
PC-003: applied directly. No unresolved blocking Review source/acceptance finding
may publish. Only the deliberately later final-gate evidence proceeds to P03;
nonblocking residuals need explicit disposition and never relax AC1-AC4.

## Follow-Up Items

None invented. Original RV-001/RV-002 remain historical outcomes.

## Handoff

P01 and original correction Review complete. Review Complete / Residual work:
no blocking source defect; AC4's full exact-head execution/publication evidence
remains deliberately pending in P03. Candidate commit follows this reconciliation.
Final P02-T02/P03 status is recorded externally and in the PR to avoid a
post-gate candidate/evidence commit invalidating the authoritative receipt.
Research is Ready. Details use the same IDs. Changes record is
.copilot-tracking/changes/2026-10-31/gate-chat-test-572-validation-correction-changes.md.
Do not claim a final receipt before the final candidate commit.
