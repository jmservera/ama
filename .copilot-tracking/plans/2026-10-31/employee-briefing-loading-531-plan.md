<!-- markdownlint-disable-file -->
# RPI Plan: Employee briefing loading assurance

## Task Metadata

* Task ID: 531
* Task slug: employee-briefing-loading-531
* Planning status: Ready plan; implementation Partial, mandatory validation blocked
* Plan date: 2026-10-31
* Phase details: .copilot-tracking/details/2026-10-31/employee-briefing-loading-531-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-31/employee-briefing-loading-531-plan-critique.md

## Executive Summary

Retain the merged loading and HAX UI. Add a focused real-server browser scenario
that records all three successful draft-review outcomes and verifies durable
history, unchanged cases and no repeated submission. Refresh the existing API
guide with this evidence and the UX-participation/live acceptance boundaries.
The implementation batch exists, but API/browser execution is now blocked:
first individual and second combined attempts timed out on the shared lock.
No fresh API/browser/axe pass or publication readiness is claimed.

### What You May Not Know

The issue's six local boxes are already checked after #538 and #581, but
live verification is not. The requested UX agent again returned questions,
not a note; the existing HAX mapping must not be called specialist validation.

## User Decisions and Requirements

* Run Research, Plan, Implement and Review in order with dated committed evidence.
* Read #531 first, reuse merged coverage and preserve Fluent 2, WCAG and plain-language standards.
* Load web-design-guidelines before web edits; use the UX agent for the design note.
* Run exact full API discovery, Ruff lint/format and local Playwright; pip only.
* No secrets, credential files, Azure changes, mvp code, main or other worktrees.
* Commit with specified Copilot trailer; push requested topic and open PR to main only after publication gates.
* Use Refs #531 and state unmet criteria unless reviewed evidence proves all criteria.

## Goals

* Improve observed successful review behavior without repeating delivered redesign.
* Preserve truthful draft-only authority and immutable review boundaries.

## Scope and Non-Goals

* In scope: existing loading_briefing_browser_check.py, API README and dated RPI evidence.
* Non-goals: runtime redesign, framework swap, deployed sign-in/verification, human or full WCAG/Fluent acceptance.

## Functional Requirements

* Use the real UI buttons and real local API for accept, edit and reject.
* Edits/rejections require reasons; success is a draft review, not works approval.
* Persist exact review values, prevent subsequent submission and leave permitted case projections unchanged.

## Non-Functional Requirements

* Constructed fixtures and loopback server only; external browser traffic blocked.
* Existing 320/390/1280 axe, static/held-script startup, retry and reduced-motion checks retained.
* Heavy checks serialized with flock -w 600 /tmp/ama-rpi-heavy.lock.

## Acceptance Criteria

* Three successful real review responses agree with same-ID records independently read through the existing continuity export by a separately authenticated synthetic Programme Manager, and with displayed authority disclaimers.
* Review reason/text are exact; accept has no editor/reason request.
* Case data before/after agrees; already-reviewed record cannot be reviewed again.
* Requested API tests, Ruff checks and pinned-axe browser suite run, with failures/skips retained honestly.
* Live AC7 and unavailable UX specialist output remain explicit; no unsupported closing keyword.

## Sources

* .copilot-tracking/research/2026-10-31/employee-briefing-loading-531-research.md: C1-C7/W1-W5 and three-wave synthesis.
* src/api/README.md: existing HAX design mapping and evidence boundaries.
* src/api/tests/test_ai_tasks.py: API/core review prior art.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [ ] P01: Strengthen local outcome evidence

* Dependencies: merged #529, #538 and #581; available pip/Chromium/axe prerequisites.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add successful review round trips and guide clarification

* Expected result: real durable accept/edit/reject records and case invariance; no production changes.
* Detail section: P01-T01 in phase-details artifact.

<!-- rpi:task id=P01-T02 -->
#### [ ] P01-T02: Validate and reconcile evidence

* Expected result: requested API and browser checks; dated changes and readiness for one independent Review.

## Locked Test Ownership

* Canonical target: src/api/checks/loading_briefing_browser_check.py.
* Owner: API browser runner; reuse briefing_data and main owned-server lifecycle.
* Removals: none. Maximum additions: one scenario function and one invocation.
* Semantic coverage: durable three-outcome review and invariant case data.
* Regression coverage: retain every existing loading, retry, timing, source, reason and axe check.
* Generated targets: fresh external session output directory only; no images/venv/logs added to Git.
* Validation: requested full discovery, ruff check, ruff format --check; browser suite with SHA-verified axe 4.10.3; focused mypy.

## Dependencies

* Missing installed src namespace caused initial import failure; isolated pip venv now installed from current worktree.
* Complete local --all gate after commit; offline tooling is permitted, Azure changes are not.

## Critique Disposition

Execution Complete; original verdict Revise. Original findings preserved.

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Rejected in part; scratch inventory applied | No parent instruction prohibits /tmp or task-owned temporary files; worker-local restriction cannot override explicit requested checks or repository lock. Retained outputs use external session files. Existing main creates synthetic.json/server.log in an owned TemporaryDirectory under repository .venv and removes it on exit. Do not change the shared lock or harness. Verify worktree cleanliness before gate. |
| PC-002 | Applied | Use full successful review response and manager-authorized /api/continuity/export ai_records keyed by id; aggregate /api/ai/report is not used. Exact status/reviewer_action/reviewer_reason/override_text/review_evidence; same-ID second refusal; permitted case detail equality only. |
| PC-003 | Applied | Original Review then commit, fetch/reconcile reviewed main base, self-locking --all --lock-timeout 600 gate, fetch/verify current-base receipt, separate independent exact-head assessment, verify again and push. Drift invalidates gate; no rebase or outer flock. |

No further critique is run. No substantive draft delegation was needed for this
single coupled phase.

## Follow-Up Items

* Live employee verification AC7: requires separately authorized identity/site run.
* UX-authored note: invocation returned only intake questions; no contribution claimed.
* Staff/assistive-technology and full Fluent adoption: separate existing workstreams, not local acceptance.

## Handoff

* Changes: .copilot-tracking/changes/2026-10-31/employee-briefing-loading-531-changes.md.
* Next: One independent assessment of the partially implemented candidate, qualified as blocked by mandatory validation; commit evidence locally and attempt full gate. No push/PR without full gate and independent exact-head assessment.
