---
title: Issue 82 round 1 research
ms.date: 2026-11-03
---

Disposition: executed. Planning Readiness: Ready.

## Prior delivery

* No merged PR delivers #82 (searched "Refs #82" and gate titles; hits are unrelated: #702, #439, #528, #324, #594).
* Existing server checks raise exceptions (`require_safety_clear`, `require_resident_clear`, `require_building_clear`, capacity and finance checks in `procurement.py`, `quality.py`, `finance.py`). None returns pass/fail/unknown, none carries rule source, effective date, version or reviewer.
* `release_hazard` (`src/core/src/zava_forward/core/workflows.py`) allowed any safety role or manager; the hold records `accountable_role` but release did not enforce it. Independence of the releaser from raiser and repairer exists in `hazard.require_independent`.

## Acceptance criteria status before this slice

* Gate returns pass, fail or unknown with reason: unmet (exceptions only).
* Unknown never passes: partly met in individual checks, not as a shared contract.
* Safety hold release by named accountable role, different person: partly met (independence only).
* Rule source, effective date, version, reviewer: unmet for gates (rule cards exist for law rules only).

## Slice choice

Slice 1 (this PR): shared deterministic gate result contract with rule metadata, plus the safety-release gate enforced in `release_hazard`. Later slices: convert resident, funding, capacity, quality, finance and evidence checks to GateResult and surface unmet gate, owner and correction route in the API and UI (AC-011); link rule metadata to approved rule cards.
