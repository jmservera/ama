---
title: Issue 82 missing or unknown funding authority readiness trace research
ms.date: 2026-11-12
task_id: server-gate-readiness-82-1112
---

## Scope and disposition

Research disposition: `executed`. Planning Readiness: `Ready` for one initial increment. Pinned base: `origin/main` `cd81888e4a81cf4c712d50b357ca900fd5c8c06b` (fetched 2026-11-12), branch `research/server-gate-readiness-82-1112`, clean worktree at start. Refs #82 only. Model: explicit Claude Sonnet 5.5.

Question: for ONE current-source trace, does server-controlled readiness or transition denial on missing or unknown funding/finance authority work, including its response reason, and is there a distinct concrete engineering gap (not an absent professional approval)?

## Authority and spent history

* Issue #82 is open, labelled partially delivered. Acceptance criteria 1, 2 and 4 are unticked; only the safety-release criterion is ticked and is not touched here.
* The 2026-11-12 coordinator comment (6836250525) admits only a "distinct existing requirement gap with actual scope" for this trace and forbids capacity-80 campaign renewal, a new rule or approval, historical branch resurrection and a generic gate audit. No closure or tick is permitted. That comment is the scope authority.
* Spent histories preserved and not repeated: closure audit 2026-11-05 (6652549123, booking/unknown tests passed, subset only); owner-approved audited replacement for corrupted in-progress checklists (6665756520); #1226 and #1228 quality/corrupt-metadata and provenance corrections; #1229 capacity gate (exhausted, finite campaign); #1230 documentation checkpoint (6676325877). No correction allowance is created or renewed by this task.
* Ancestry reconciliation: the lifecycle parent was integrated into main by `3a9767d5c` (#1240), an ancestor of the pinned main (`git merge-base --is-ancestor` exit 0). The parent-only prose about #1226/#1228/#1229/#1230 therefore describes delivered code now on main (`quality_gate`, `capacity_gate`, `CapacityGateError`, `quality_evidence_gate` are all in current `gates.py`/`store.py`), not a missing feature. Booking funding gates came from `c8f6dee19` (#1035) and the structured evidence gate from `803787ed0` (#1097), both on main.

## Current-source trace

PRD FR-008 requires deterministic evidence, eligibility, authority, safety, resident, funding, capacity, quality and finance gates before a controlled transition. BRD RULE-001 and RULE-002 require source, effective date, owner/reviewer on controlled rules; the rule records in `gates.py` carry the explicit "Unreviewed exercise rule: named reviewer required before live use" reviewer and are fixtures, not approval.

Trace for "Ready to book" to "Install booked" (`Store.advance`, `src/core/src/zava_forward/core/store.py`):

1. `advance` first computes `why = self.gate_reasons(c)`; `gate_reasons` tests funding as `if not c["funding_ok"]`.
2. Later, `require_booking_gates` calls `gates.booking_gates`, whose funding gate passes only for exactly `True`; absent, `None` or non-boolean is `unknown` with the reason "Funding confirmed: no evidence recorded, so this cannot pass."
3. `server.py` maps `GateError` to HTTP 409 `{"error": "Not ready yet.", "reasons": [...]}` and a bare `KeyError` to HTTP 404 `{"error": "Case not found."}`.
4. `Store.detail` and `status_line` also call `gate_reasons` for `gate` and the "Ready" status.

Executed probe ([probe-before.py](../../evidence/2026-11-12/server-gate-readiness-82-1112/probe-before.py), output [repro-before.out](../../evidence/2026-11-12/server-gate-readiness-82-1112/repro-before.out)) against ZF-3 with the shared test dataset (synthetic) in a temporary store:

| `funding_ok` | `advance` result | `gate_reasons` |
| --- | --- | --- |
| `False` | `GateError`, funding not confirmed reason | funding reason |
| `None` | `GateError`, funding not confirmed reason | funding reason |
| `"yes"` (non-boolean) | `GateError` (booking gate unknown) | `[]` (reads as ready) |
| key absent | bare `KeyError('funding_ok')` | `KeyError` |

## Gap confirmation

Existing tests (`core/tests/test_gates.py::test_booking_gates_fail_and_unknown`) prove `gates.booking_gates({}, None)` yields unknown and not allowed. No test drives the store-level `gate_reasons`/`advance`/`detail` path with an absent or non-boolean `funding_ok`. The pre-check does not use the same fail-closed definition, so:

* Missing funding evidence is still denied (no transition occurs), but the response reason is a misleading HTTP 404 "Case not found." instead of the 409 funding reason with owner and next action; `Store.detail` for the same case raises `KeyError`, which hides the case entirely.
* A non-boolean funding value is counted as met by `gate_reasons`/`status_line`/`detail["gate"]`, so the readiness view can read "Ready" while the transition gate says unknown. This contradicts "unknown never passes" at the readiness surface.

This is a distinct concrete engineering gap against FR-008 and criterion 2, in an existing delivered path. It needs no new rule, policy, reviewer or approval: the definition (explicit `True` only) already exists in `gates.check`/`booking_gates`.

## Out of scope and not claimed

* The `finance` gate kind is listed in `GATE_KINDS` but has no booking gate implementation. Adding a finance gate would be a new rule family needing a named authority; it is recorded as unassessed and not implemented. Funding is the only authority trace resolved here.
* `taskqueues.py` line 295 uses `not case.get("funding_ok")`; it already tolerates absent values and treats a truthy non-boolean as confirmed in a queue block. Changing queue semantics is a separate caller and is not part of this increment; recorded as a follow-up observation.
* No SQL Server run, no full gate, no hosted CI, no live state transition. The SQL store inherits `gate_reasons` from `Store`; the SQL-backed suite is not executed here (declared limit).
* Criteria 1, 2 and 4 remain unticked; named professional rule review remains an unproven, separate human gate.

## Constraints carried into the plan

* Smallest change: one condition in `Store.gate_reasons` (`c.get("funding_ok") is not True`), keeping existing reason text.
* Failing-first regression at the store and HTTP level; no weakening of fail/unknown, consent, safety or independent-review boundaries.
* Focused tier: impacted unit tests, ruff and mypy on touched files; no complete gate by default.
