# Issue 126 changes

Refs #126. Tier: FOCUSED (documentation and evidence only; no src change). Basis: no SQL, security, infrastructure or deployment edit; SQL-backed register tests were skipped and the SQL criterion is recorded as unproven.

## Files

* `docs/reference/research/issue-126-live-2026-11-19.md` and `issue-126-live-2026-11-19/` (probe script, probe shape, raw test output)
* `docs/reference/README.md` index row; `docs/reference/log.md` entry

## Validation

* `src/core` `tests.test_governance`: 88 OK, 18 skipped (opt-in SQL).
* `src/api` `tests.test_governance_evidence_api`: 10 OK.
* Live read-only probe of the demo API: 200, capture closed, 22 findings, 0 claims. No Azure resource created; nothing to delete.
* mypy, ruff and web checks not applicable (no source or web file changed).

## Per-criterion table

| Criterion | State |
| --- | --- |
| Protocol, DPIA, lawful basis approved before capture | UNPROVEN (named human approval) |
| Release decision per phase and tranche | Proven (tests) |
| Guardrail breach pauses scope | Proven (tests) |
| BG-011 definitions and MDE | Proven (tests) |
| Track 22 RAI findings with dispositions | Engineering proven; live dispositions UNPROVEN (none recorded) |
| Fresh current-source assessment | UNPROVEN (assessment run) |
| Qualified owner acceptance | UNPROVEN (human) |
| Real AI/SQL/Azure contract | UNPROVEN (SQL tests skipped) |

Unmet criteria needing new code: none.
