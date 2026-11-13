---
title: Issue 82 deterministic gates closure research
ms.date: 2026-11-13
---

## Disposition

Research disposition: executed. Planning Readiness: Ready.

## Evidence

* Issue #82 criteria: 1/4 ticked. Open: (1) each gate deterministic pass/fail/unknown with reason, (2) unknown never passes, (4) each controlled rule names source, effective date, version, reviewer.
* `src/core/src/zava_forward/core/gates.py`: `GATE_KINDS` lists evidence, eligibility, authority, safety, resident, funding, capacity, quality, finance. `GateRule` validates source/effective_date/version/reviewer; `check` returns unknown for non-boolean evidence or a not-yet-effective rule; `transition_allowed` needs every result to be pass.
* Rules and gates present: safety release, booking (funding, safety, resident), evidence, quality, capacity. Absent: eligibility, authority, finance rules and gates, and no registry that proves every kind has a rule.
* Call sites: `store.py` booking (`booking_gates` + `evidence_gate`), `quality.py`, `procurement.py`/`appointments.py` (`CapacityGateError`), `workflows.py` safety release. Finance `_fin_commit_raise` (`finance.py`) and `grants.require_authority` use ad hoc ValueError/PermissionError with no gate result or rule record.
* All existing rules carry the reviewer text "Unreviewed exercise rule: named reviewer required before live use". No named human reviewer exists; none may be invented.
* Tests: `src/core/tests/test_gates.py` covers metadata validation, outcomes, booking, evidence, quality.

## Gap and scope

* Add eligibility, authority and finance rules and gate functions with the same unknown-never-passes semantics.
* Add `CONTROLLED_RULES` registry keyed by every `GATE_KINDS` entry, test that each has all four metadata fields and that an unreviewed marker is explicit.
* Wire finance (commitment against approved budget) and authority (financial designation) denials to gate results, keeping existing error types and text.
* Eligibility has no recorded evidence field in the data model; inventing one is out of scope. The gate function exists and returns unknown without evidence; no call site is wired.
* Named reviewer for each rule cannot be established in software; criterion 4 is only provable as "field present with explicit unreviewed marker". Closure of #82 is therefore not claimed (`Refs #82`).
* Tier: Focused (non-gate tooling, core unit tests, ruff, mypy).
