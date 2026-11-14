# Plan: #132 named-owner variation and escalation routing (2026-11-14)

Critique: one pass, executed; compatible findings applied directly (no write endpoint, no contractor access, keep env-configured owner).

* [x] Phase 1: `job_pack.named_owner` rejects blank, placeholder ("unknown", "tbc", "unassigned", ...) names and non-manager/safety roles; `escalation()` uses it.
* [x] Phase 2: `job_pack.assert_advisory` refuses any record whose `contract_instruction` is not exactly False; `escalation()` self-checks.
* [x] Phase 3: `staff_intake.escalation_destination` adds `owner_assigned`, `owner_status`, `advisory_only`; new `route_escalation` refuses when no named owner is configured. `view().boundaries.advisory_only` added.
* [x] Phase 4: staff-intake screen shows Owner status and "Contract instruction: No".
* [x] Phase 5: focused core and API unit tests; ruff, format, mypy.

## Cycle 1 correction plan (1 of 5)

Critique: one pass, executed; compatible with the confirmed decisions (advisory only, staff only, no contractor access, no work-order mutation).

* [x] C1: `staff_intake.escalate` added to `ACTIONS` as `POST /api/workorders/{id}/field-escalate`; appends an immutable record to `case["escalations"]` (named_owner, owner_role, escalation_kind, summary, routed_by, routed_at, contract_instruction False) and a `field_escalation_routed` audit entry via the quality operation scope; `view()` returns `escalations`.
* [x] C2: `job_pack.named_owner` now requires person-name characters and rejects placeholder words in any position, role-only titles, and slash, underscore, digit and email forms; configured contact is validated and placeholder config reports no owner.
* [x] C3: HTTP tests for fail-closed (400, no state or audit change), staff-only (403), persistence across restart and configured routing; core name tests.
* [x] C4: counts and evidence corrected in the changes and review artifacts.

## Cycle 2 correction (2 of 5)

Fixed independent cycle 1 findings: escalation summary held for roles without a recorded need (advisory note kept), staff-intake.js escalation form, readback and computed contract-instruction text, non-string and dotted-initial owner rejection, README and AC5 numbering. Focused core/api tests, ruff and mypy pass. Browser, SQL Server, human AT and hosted CI not run. Refs #132.
