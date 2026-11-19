# Changes: issue #126 live run 2

Refs #126. Tier FOCUSED; no src, SQL, web or infra file changed (artifacts only). mypy, ruff and web checks not applicable.

## Validation

* `cd src/core; PYTHONPATH=src:tests python3 -m unittest test_governance`: Ran 88, OK (skipped=18, opt-in SQL).
* `cd src/api; PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest test_governance_evidence_api`: Ran 10, OK.
* No Azure resource created; nothing to delete.

## Per-criterion table

| Criterion | State | Reason |
| --- | --- | --- |
| Protocol, DPIA, lawful basis approved before capture | Unproven | Needs named human approval; capture stays closed |
| Track 22 findings with dispositions | Engineering proven, live dispositions unproven | Register code and tests pass; no qualified person has recorded claims |
| Fresh current-source assessment | Unproven | Assessment run, not code; prior table at `.copilot-tracking/changes/2026-11-17/issue-126-residual-source-assessment-table.md` |
| Qualified owner acceptance | Unproven | Human decision |
| Real AI, SQL, Azure contract | Unproven | 18 SQL tests skipped; throwaway SQL would be FULL tier |
| Phase/tranche decisions, breach pause, BG-011 MDE (ticked) | Proven again | Tests above |

Unmet criteria needing new code: none.
