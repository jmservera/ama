---
title: Issue 82 remaining gate family readiness plan (2026-11-06)
ms.date: 2026-11-06
---

Selected increment: capacity gate at the booking transition, with the coupled contract-authority check, exposing deterministic pass/fail/unknown, reason and provenance while preserving existing semantics. Details: `../../details/2026-11-06/issue-82-family-readiness-details.md`. STOP here for coordinator scope and tier admission; no source or test edit has occurred.

* [ ] Phase 1: shared tests that fail first (see details).
* [ ] Phase 2: `gates.capacity_gate`/`CAPACITY_RULE` and wire `require_booked_capacity` so it builds a GateResult from the existing predicate outcome and raises as before.
* [ ] Phase 3: Changes, canonical Review, local commit.

## Critique (single pass, self-run)

* Risk of behavior drift: existing messages and exception types (ValueError, PermissionError) are asserted by current tests. Applied: keep raised types and texts; the GateResult only adds provenance and Unknown mapping. If the exception type must change, STOP and re-tier.
* Risk of a generic abstraction: Applied: one rule and one function modelled on `evidence_gate`.
* Unknown mapping: malformed or legacy capacity details (not a dict, hash mismatch from corruption) must be Unknown, not Pass; existing code already refuses, so Unknown refuses likewise.
* Invented policy: none. Rule reviewer stays "Unreviewed exercise rule"; source cites PRD FR-008 with the contract-capacity record (PRD FR-016); date, version are the implementation date and 1 and are not claimed approved.
* Out of scope: eligibility, finance, new roles, schema, persistence, UI.

## Validation

* Tier for implementation: FULL (server authority and capacity control over a SQL-backed store). No downgrade. Heavy lanes need coordinator admission (#185 holds it now).
* Light selectors now/later: `test_gates`, `test_consultation_controls`, `test_quality_procurement` (JsonFlows, SqlFlows), `test_procurement*`; SQL-backed `api/tests/test_mssqlstore.MssqlProcurement` only inside the maintained gate.
* This planning commit: Markdown and diff review only.
