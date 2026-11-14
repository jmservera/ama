# Plan: #132 named-owner variation and escalation routing (2026-11-14)

Critique: one pass, executed; compatible findings applied directly (no write endpoint, no contractor access, keep env-configured owner).

* [x] Phase 1: `job_pack.named_owner` rejects blank, placeholder ("unknown", "tbc", "unassigned", ...) names and non-manager/safety roles; `escalation()` uses it.
* [x] Phase 2: `job_pack.assert_advisory` refuses any record whose `contract_instruction` is not exactly False; `escalation()` self-checks.
* [x] Phase 3: `staff_intake.escalation_destination` adds `owner_assigned`, `owner_status`, `advisory_only`; new `route_escalation` refuses when no named owner is configured. `view().boundaries.advisory_only` added.
* [x] Phase 4: staff-intake screen shows Owner status and "Contract instruction: No".
* [x] Phase 5: focused core and API unit tests; ruff, format, mypy.
