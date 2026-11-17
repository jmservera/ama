---
title: Research - controlled rule source/date/version/reviewer (#82)
ms.date: 2026-11-14
---

## Findings

* Issue #82 has 3/4 ACs ticked; open AC: each controlled rule identifies its source, effective date, version and reviewer. Comments say named professional review stays open and no approval may be invented.
* `src/core/src/zava_forward/core/gates.py` already defines frozen `GateRule(gate, source, effective_date, version, reviewer)` with validation (non-blank strings, ISO date) and `as_record()`; `GateResult.as_record()` exposes `rule`.
* `CONTROLLED_RULES` registers safety release, four booking rules, quality, capacity, eligibility, authority and finance; all nine `GATE_KINDS` covered. Reviewer is the explicit marker `Unreviewed exercise rule`, reported by `unreviewed_rules()`.
* `src/api` defines no rules of its own; it consumes core gate results.
* Gap: no test proves every emitted gate result exposes a registered rule or that no rule exists outside the registry.

Research disposition: executed. Planning Readiness: Ready.
