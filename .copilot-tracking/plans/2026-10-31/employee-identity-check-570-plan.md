---
title: Employee identity runner implementation plan
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Task Metadata

Task ID: 570. Slug: employee-identity-check-570. Ready after direct critique disposition.
Post-implementation outcome: Not accepted. RV-001/RV-002 remain open;
planning readiness was not implementation acceptance or publication approval.
Details: .copilot-tracking/details/2026-10-31/employee-identity-check-570-phase-details.md.
Critique: .copilot-tracking/reviews/plans/2026-10-31/employee-identity-check-570-plan-critique.md.

## Executive Summary

Wire the existing immutable Entra predicate into maintained employee-only
authenticated-session checks. Preserve strict expected-account verification and
record capture-free chat, map and case results. No application mapping change.
After critique, do not add credential-handling or sign-in automation: these
are unnecessary to repair the admission caller and currently cannot run safely
without independent identity evidence. The helper consumes zero sign-in attempts.

### What You May Not Know

The base already contains the predicate and synthetic HTTP tests. Historical
automation is not a maintained caller and still has weaker identity guards.
Directory read access is denied, so independently verified Aadi object ID is
unavailable. Live acceptance remains blocked; no sign-in budget consumed.

## User Decisions and Requirements

* Run all four RPI phases in order; commit dated original evidence.
* Use fix/employee-identity-check-570 at 5666bd33; src source, external tests.
* Refs #570 only; privacy-safe local commit email and requested trailer.
* API discovery with the supplied PYTHONPATH, Ruff lint/format and actual local
  installed Chromium execution. Pip only.
* Authorized Aadi sign-in expires 2027-01-31; at most two attempts, warm app,
  password-only file read within automation, no secret capture, no Azure changes.
* Verify live employee chat, map filters, case; push without force and open main PR.

## Goals

Remove remaining caller ambiguity without weakening expected-account admission.

## Scope and Non-Goals

Maintained checks/employee_acceptance_check.py, owning API tests and README.
This is an authenticated-session entry point, not a credential/sign-in runner.
Historical evidence unchanged. No UI, authorization, roster or infrastructure edits.

## Functional Requirements

Mandatory independently supplied GUID expectations, validated before evaluation.
Only an exact well-formed all-boolean shared BINDING projection with authenticated
strictly true admits downstream observations. Exact supplied origin and fixed
authorized live origin (or explicitly local loopback test origin) checked before
and after probe and each stage. Reprobe before every stage, including after
navigation. Reject malformed projections and stop on session loss.
Explicit stage failures; aggregate booleans/counts only. No credential reads,
fills, browser authentication, session storage, or sign-in entry point.
Expected IDs and provenance remain caller-owned, never learned from /me.

## Non-Functional Requirements

Reject debug environment before evaluation. Never retain raw URLs, DOM text,
exception messages or response bodies. Fail nonzero on unproven checks in
the local browser CLI; session API returns explicit passed/failed/blocked stage
statuses. /me uses unchanged 120-second fetch timeout. Observation waits are
120 seconds maximum each, no retries or sign-in. Browser lifecycle and a
whole-process watchdog belong to the authorized caller, not this page adapter.

## Acceptance Criteria

* Cause identified with code/historical boolean evidence, preserving unknown raw claim.
* Maintained runner invokes immutable predicate, with positive rosterless and
  wrong-account regression through real installed Chromium and actual /me fixture.
* Invalid expectations and debug environment fail before page evaluation.
* Live chat/map/case criterion remains unproven unless independent expected IDs
  and actual successful live observations are available.

## Sources

.copilot-tracking/research/2026-10-31/employee-identity-check-570-research.md,
C1-C6 and W1-W3; src/api/README.md independent identity boundary.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [ ] P01: Implement and validate bounded runner

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Maintain the caller and regression

Add one maintained src/api/checks session runner, reuse BINDING, add at most one new
test module (six focused tests maximum), remove no existing tests. Semantic
coverage: actual constructed /me payloads; regression coverage: absent display
email admits expected immutable identity, same-email wrong identity denied.
Canonical code is src; generated reports external. Test ownership API.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Execute local and eligible live validation

Run from src/api the exact supplied API discovery with
PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests,
Ruff lint/format and mypy. Because checks are formatter-excluded, explicitly
format-check the runner using isolated Ruff configuration too.
Run `python -m checks.employee_acceptance_check` for actual Chromium regression.
Six new tests: malformed expectations, malformed projection, origin/debug guard,
downstream/session-loss gating, Chromium rosterless and Chromium wrong account.
Reuse existing HTTP fixture through composition, not test-class inheritance.
Attempt
independent directory lookup alternatives read-only; do not sign in if expected
IDs unavailable. Record sanitized blocked live statuses without claiming success.

Completion evidence: API discovery 1436 tests, 320 documented opt-in skips;
six new focused contracts pass, two actual Chromium regressions pass. Positive
Chromium also executes actual synthetic chat/map/case observers (workflow-only,
not actual AI). API Ruff lint/format, explicit runner format and mypy pass.
Read-only CLI user and direct Graph resolution both denied; live is blocked,
zero sign-in attempts. This checkbox proves local validation and prerequisite
evaluation only, not the issue's live criterion. P01 as a whole remains partial
against the original requested live outcome.

<!-- rpi:phase id=P02 -->
### [ ] P02: Review and publication

<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: One independent Review, commit and gate

Preserve original Review, record findings as follow-ups without repeating it.
Commit original evidence then run complete local gate and verify current-base
external receipt immediately before non-force push and exact-head assessment.
Missing prerequisites block publication; no fabricated receipts.

## Dependencies

Installed src distributions restored in external pip venv after missing import.
Independent expected IDs required for live acceptance; unavailable currently.
Local gate tool prerequisites required for publication.

## Critique Disposition

Original critique execution Complete, verdict Revise, eleven findings retained.
Direct scope correction avoids adding another sensitive login runner:
the maintained repair accepts an already authenticated Page only.

| Finding | Disposition |
| --- | --- |
| PC-001 | Resolved by scope: zero sign-in submissions or credential entry point; no new budget/reset possible. |
| PC-002 | Expected IDs stay independently caller-attested; absent evidence still blocks live. No automation asserts attestation. |
| PC-003, PC-004 | Sensitive browser/credential lifecycle not introduced; fixed result schema, fixed errors, no raw capture; synthetic local fixture only. |
| PC-005 | Strict projection, exact origin before/after, admission required before each callback and after navigation. |
| PC-006 | Unchanged fetch timeout and explicit finite operation waits; caller owns watchdog, adapter never signs in/retries. |
| PC-007 | Concrete stage predicates: current chat answer without alert; unselected map filter plus HTTP 200/data/state; offered case link and loaded case/no alert. Model label recorded separately. Any unproven required stage fails/blocks. |
| PC-008 | Exactly six new tests in one module, composed existing HTTP fixture, two actual Chromium executions. |
| PC-009 | Exact discovery, explicit runner format check and browser CLI; include two tracked browser selectors as full-gate extra tests. |
| PC-010 | Retain original environment concern; run repository-mandated gate only, with external output, no workaround or tool edits. Failure blocks publication. |
| PC-011 | P01-T01 owns README integration example, independent expectation, no-sign-in boundary and live blocker. |

No second critique. All source changes remain within the original caller's
runner-or-mapping repair request. Removing unnecessary new sign-in capability
does not claim live acceptance or alter the owner's authorized attempt policy.
Original independent Review later found PC-005 and PC-007 incompletely realized:
navigation inside observers is not freshly gated before next action, and map
acceptance can pass malformed rendered data. Preserve these adverse outcomes.

## Follow-Up Items

* Restore directory evidence and prove live acceptance if blocked; identity administrator.
* RV-002: gate navigation inside observers before further action; later implementation.
* RV-001: reject malformed map rendering/data and add negative regression; later implementation.

## Handoff

Changes: .copilot-tracking/changes/2026-10-31/employee-identity-check-570-changes.md.
Ready P01 after critique. Live prerequisite does not authorize weaker identity.
Current handoff: one Review Complete / Not accepted. No correction or repeated
Review in this task; preserve original evidence, commit bounded candidate and
perform prescribed publication gate without treating it as review approval.
Push/PR remains blocked while material Review defects are open.
