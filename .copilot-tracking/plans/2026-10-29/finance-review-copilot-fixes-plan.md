<!-- markdownlint-disable-file -->
# RPI Plan: Finance review Copilot fixes

## Task Metadata

* Task ID: finance-review-copilot-fixes-510
* Task slug: finance-review-copilot-fixes
* Plan date: 2026-10-29
* Planning status: Ready; independent critique Complete / Pass, no findings.
* Phase details: .copilot-tracking/details/2026-10-29/finance-review-copilot-fixes-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-29/finance-review-copilot-fixes-plan-critique.md

## Executive Summary

Preserve blank corrections as recorded human actions, but exclude blank string
inputs from confirmed values. Return an explicit opaque Unavailable entry for
each draft whose retained evidence is unavailable, leaving other drafts readable.
No financial authority changes. Commit locally; never push or use Azure.

### What You May Not Know

Existing single-draft tests deliberately expect read exceptions/HTTP 403.
Update those intentional contract assertions without weakening write denial,
history/snapshot privacy, real storage errors or actor authorization.
The requested tools were missing; a session-owned external venv now has the
existing core dev dependencies and editable core/agents/api distributions.

## User Decisions and Requirements

* Run the full dated Research/Plan/Implement/Review loop and git pull --rebase first.
* Fix exactly the two supplied PR #510 findings on docs/finance-96.
* Preserve corrections/history; required blanks remain missing; zero/false valid.
* Keep unaffected drafts readable without leaking unavailable draft content.
* Add regression tests outside the installed package and run the four specified checks.
* Commit locally; do not push, edit rubric scores manually or use Azure.

## Goals

* Restore truthful missing-required diagnostics and case read availability.
* Preserve source visibility, history integrity and existing held authority.

## Scope and Non-Goals

* In scope: form_review.py, existing core and HTTP external tests, component
  contract READMEs and dated RPI artifacts.
* Non-goals: new routes, UI, cloud, approval, data migration, unrelated findings,
  issue closure, generated rubric-score changes or publication.

## Functional Requirements

* Whitespace-only strings do not enter confirmed inputs; type validation and
  recorded corrections remain unchanged.
* Required blank fields produce Unknown missing-input diagnostics for required
  and required_when fields, immediately and in persisted diagnose snapshots.
* Blank controlling input leaves conditional requirements unknown.
* Numeric zero/boolean false remain confirmed and can activate typed conditions.
* Authorized list reads catch only DocumentUnavailable per draft. An unavailable
  entry has exactly draft_id, status "Unavailable", and a fixed recovery notice.
* No fields, history, attachments, snapshots, schema or exception detail leaks.
* Writes still deny unavailable evidence, and storage-service failures propagate.

## Non-Functional Requirements

* No mutation, scanning or source writes during view.
* Preserve per-report cache lifetime, typed equality and auth checks.
* JSON and SQLite reopen tests demonstrate persistence; no private data.

## Acceptance Criteria

* Public correct/diagnose/reopen regressions cover empty and whitespace strings
  under unconditional and active conditional requirements; history unchanged.
* Zero/false do not yield missing-input diagnostics and activate conditions.
* Two drafts with distinct retained sources: missing bytes, deleted metadata and
  quarantine yield an exact opaque affected entry and unchanged readable sibling.
* Existing historical/snapshot tests assert exact opaque read entries while
  maintaining action denials, nonmutation, outage propagation and recovery.
* HTTP GET returns 200 with opaque unavailable entry; unauthorized reads stay 403.
* Requested unittest discovery, ruff check, format check and mypy pass.
* One independent critique and one independent post-implementation Review recorded.

## Sources

* .copilot-tracking/research/2026-10-29/finance-review-copilot-fixes-research.md:
  Ready, executed; C1-C7 identify existing behavior and contract surfaces.
* PR #510 comments 4418481231 and 4418481281: exact owner-requested findings.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct and verify required-input diagnostics

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add blank/typed regression coverage and confirmed filter

* Evidence: C1/C2/C6/C7; detailed scope in phase details.
* Expected result: missing-required issues persist without losing corrections.

<!-- rpi:phase id=P02 -->
### [x] P02: Isolate unavailable drafts and reconcile contract

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add opaque read entries and two-draft regressions

* Evidence: C3/C4/C5. Preserve action denials and storage errors.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Update directly related HTTP tests and component documentation

* HTTP contract reflects explicit per-entry status; no frontend implementation.

<!-- rpi:phase id=P03 -->
### [x] P03: Validate and preserve local candidate

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Run requested checks and independent Review

* Record actual commands/outcomes, reconcile plan/details/changes before Review.
* Review findings route later, with no second Review in this task.

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Commit locally and attempt required external local gate

* Commit implementation and original evidence; no push.
* Fetch main, use tools/rpi-checks.py --all with --lock-timeout 0 and a new
  external directory. Missing prerequisites or busy ownership block only gate;
  no Azure fallback. Receipt remains external. Do not edit committed evidence
  afterward merely to copy the receipt.

## Locked Change and Validation Budget

* Test ownership: src/core/tests/test_form_review.py; HTTP tests belong to
  src/api/tests/test_form_staging_api.py. No tests inside package.
* Exact removals: none. Replace only intentional old read-denial assertions.
* Maximum additions: four new test methods (three core plus one HTTP).
* Canonical targets: one core module, two external test files, two READMEs.
* Generated targets: none; latest.json is excluded.
* Semantic coverage: typed conditional evaluation, blank/false distinction,
  opaque response and sibling availability, no mutation and write denial.
* Regression coverage: both caller findings via public actions and reads.
* Validation: caller's four src/core commands; targeted staging and API tests;
  full local gate attempted after committed candidate and independent Review.

## Dependencies

* P02 and P01 are independent; P03 requires both.
* Existing public synthetic fixtures and installed src distributions.
* Full-gate prerequisites remain a possible environment blocker.

## Critique Disposition

* Single final-candidate critique executed: Complete / Pass, all severities zero.
* Findings: none; no dispositions or divergent user decisions required.
* Original artifact: .copilot-tracking/reviews/plans/2026-10-29/finance-review-copilot-fixes-plan-critique.md

## Follow-Up Items

* RV-001 (Low), rank 1: authorized clean-candidate/gate-readiness work before
  any future publication; owner/candidate maintainer. Original Review identifies
  no code defect. Preserve ignored scratch, obtain a valid full-gate receipt,
  and retain separate human/hosted approvals. Outside the local-only fix scope.

## Handoff

* Changes: .copilot-tracking/changes/2026-10-29/finance-review-copilot-fixes-changes.md
* First task: P01-T01, after critique dispositions are resolved.
* User's explicit full-loop direction owns continuation, not indefinite auto mode.
* All bounded plan tasks complete. Required core checks passed; adjacent
  staging/API checks passed. Independent Review executed Complete / Residual
  work, no code defects, one Low gate-readiness residual.
* Local implementation/evidence commit: cdbbd4606160eaf285dcbc9d4d5e391125fc9367.
  Complete gate attempted afterward against fetched origin/main
  719e76e50b9f54b71514ee7b90833005f9bb4be8; exit 1, ignored-input refusal.
  No receipt exists. This completes the planned attempt, not gate acceptance.
* Gate eligibility: current checkout has ignored cache/bytecode/egg-info inputs;
  no blanket cleanup is authorized. Preserve them; report actual gate refusal
  after local commit rather than fabricating a full receipt.
