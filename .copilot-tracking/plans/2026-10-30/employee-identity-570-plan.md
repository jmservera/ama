---
title: Employee acceptance identity plan
description: Bounded offline runner contract repair
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

Task: employee-identity-570-2026-10-30. Refs #570.

## Executive Summary

Replace the next-run display-email identity expectation with independently
verified expected tenant/object IDs. Leave application auth unchanged: no
mapping bug is demonstrated. Preserve immutable historical evidence and state
that its actual failed display claim cannot be reconstructed. One critique
Complete / Revise; compatible findings applied below. Implementation and one
Review complete; outcome Residual work, no offline implementation defect found.
Local commit/post-commit gate handoff recorded in changes; live work excluded.

## User Decisions and Requirements

* Run Research, Plan, Implement and Review in order with dated artifacts.
* Commit locally using Refs #570 only; no push or issue mutation.
* No live sign-in, private test-user file, Azure change or deployment.
* Require failing-before regression outside the installed package, API units
  under flock -w 600 /tmp/ama-rpi-heavy.lock, Ruff and mypy.
* Provide next-live instructions; only the owner authorizes attempts.

## Sources

Research: .copilot-tracking/research/2026-10-30/employee-identity-570-research.md,
C1-C8. Details:
.copilot-tracking/details/2026-10-30/employee-identity-570-phase-details.md.

## Goals

Explain the faulty runner contract without inventing a raw historical claim.
Provide an importable browser predicate for future acceptance, not a new
sign-in runner that could silently consume a third attempt.

## Scope and Non-Goals

Add src/api/checks/employee_identity_check.py and
src/api/tests/test_employee_identity_check.py; update src/api/README.md.
No application auth/me/core/infra changes. Original 1030c files unchanged.
No live features, cleanup hardening, visibility repair or historical acceptance.
Exactly two Python additions, zero removals, one existing guide change plus
dated phase/state evidence; no generated source or dependency changes.

## Functional Requirements

The browser predicate fetches same-origin /api/me and accepts only a valid
trusted-proxy Entra projection with exact canonical expected tenant/object
identity, ProgrammeManager role and false view_only.
Expected IDs must be independently verified before any attempt, never learned
from the response. Wrong account with matching display email must fail.
Display-email comparison and optional roster binding are boolean diagnostics
only. Absent/multiple/aliased display claims must not block correct identity.
Malformed expected or observed IDs, schema, provider, role, HTTP and view-only
values fail closed. No payload/claim/ID/string diagnostics leave the predicate.

## Non-Functional Requirements

Use existing Python/Node/unittest patterns, constructed local HTTP fixtures,
no credential access, browser launch or dependencies added.
New tests stay outside zava_forward/api. No raw live responses retained.
Keep original failure and original critique/Review immutable.

## Acceptance Criteria

* A regression against original BINDING fails before repair for a legitimate
  rosterless /me with absent display email; corrected predicate passes.
* Synthetic real auth -> /me payloads with missing, multiple and aliased
  display claims pass only for independently expected IDs.
* Same-display-email wrong object/tenant, malformed expectations, and each
  HTTP/schema/provider/role/view-only guard reject; all results boolean-only.
* API suite, Ruff and mypy run; exact outcomes and limitations recorded.
* One independent critique and one post-implementation Review preserved.
* Local commit uses authenticated privacy-safe identity and Refs #570;
  final external complete local gate attempted without push or live activity.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01: Offline predicate and regression

* [x] P01-T01: Capture failing-before regression and implement reusable predicate.
* [x] P01-T02: Document diagnosis, integration boundary and next-live prerequisites.

<!-- rpi:phase id=P02 -->
### P02: Validation and persistence

* [x] P02-T01: API units with shared flock; Ruff, mypy and immutable hash checks.
* [ ] P02-T02: One independent Review, local commit and external gate attempt.

## Critique Disposition

Original: .copilot-tracking/plans/2026-10-30/employee-identity-570-critique.md.
Exactly one execution, Complete / Revise. No significant user decision needed.

* PC-001 applied: red invokes old predicate with its original string argument
  and real synthetic /me payload, checks all non-identity guards pass, then
  intentionally fails authentication assertion. Green uses new ID arguments.
  Exceptions/interface mismatch are not valid red evidence.
* PC-002 partially applied: explicit honest blocked closeout, direct full-gate
  invocation (no double lock), no fallback or bypass. Rejected its assertion
  that this parent's /tmp operations are prohibited: no such restriction
  applies here, and caller explicitly requires the shared /tmp lock. Reviewer
  environment restrictions do not transfer to parent. /tmp/mv tools were
  successfully checked; session files are explicitly available for external
  logs/gate output. No constraints bypass or waiver is involved.
* PC-003 applied: explicit transportFailed/jsonFailed booleans and no error
  strings; rejection/abort/parser-canary cases; exact request/timeout tests;
  malformed arrays and all schema shapes added to regression coverage.
* PC-004 applied: exact ten-path allowlist and reviewer output below.

## Exact Write and Commit Allowlist

Parent owns all paths except Review:

* src/api/checks/employee_identity_check.py
* src/api/tests/test_employee_identity_check.py
* src/api/README.md
* .copilot-tracking/research/2026-10-30/employee-identity-570-research.md
* .copilot-tracking/plans/2026-10-30/employee-identity-570-plan.md
* .copilot-tracking/details/2026-10-30/employee-identity-570-phase-details.md
* .copilot-tracking/changes/2026-10-30/employee-identity-570-changes.md
* .copilot-tracking/rpi-sessions/2026-10-30/employee-identity-570-state.json

Independent workers own their original assessment records:

* .copilot-tracking/plans/2026-10-30/employee-identity-570-critique.md
* .copilot-tracking/reviews/logs/2026-10-30/employee-identity-570-review.md

Exclude all seven original 1030c files and all external logs/receipts.
Record original hashes before/after and compare exact staged names.

## Follow-Up Items

1. Owner/identity administrator supplies independently verified expected
   tenant/object IDs; acceptance owner authorizes fresh attempt budget and
   integrates the predicate into a fresh guarded runner before employee
   chat/map/case acceptance. Outside scope: no live permission in this task.
2. Runner maintainer owns prior RV-002 visibility and RV-003 fault-path cleanup
   work. These are separate defects, not repaired by identity comparison.
3. Model and accessibility owners retain separately authorized enabled-model
   and human/AT acceptance. No inference from local browser predicate tests.

## Handoff

Implemented P01 and P02-T01. Full API units: 1368 tests, 318 skips, success;
Ruff check/format and mypy passed. General discovery skips are not SQL/browser
proof or a passing complete gate. P02-T02 Review/local commit/external gate
are recorded at the artifact-freeze boundary. Review Complete / Residual work,
no offline implementation defect found. Final commit and gate results stay
external as described in the changes record:
.copilot-tracking/changes/2026-10-30/employee-identity-570-changes.md.
