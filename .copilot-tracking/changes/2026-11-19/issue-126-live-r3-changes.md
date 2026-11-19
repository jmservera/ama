# Changes: issue #126 live run 3

Refs #126. Tier FOCUSED; no src, SQL, web or infra file changed. mypy, ruff and web checks not applicable.

## Validation

* `cd src/core; PYTHONPATH=src:tests python3 -m unittest test_governance`: Ran 88, OK (skipped=18, opt-in SQL).
* `cd src/api; PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest test_governance_evidence_api`: Ran 10, OK.
* Live probe via Playwright on `ca-cutover-test-demo-api` revision 0000033: 200, 22 findings, live use BLOCKED.
* No Azure resource created; nothing to delete.

## Per-criterion table

| Criterion | State | Reason |
| --- | --- | --- |
| Protocol, DPIA, lawful basis approved before capture | Unproven | Needs named human approval; capture stays closed |
| Track 22 findings with dispositions | Code proven, live dispositions unproven | No qualified person has recorded claims |
| Fresh current-source assessment | Unproven | Assessment run, not code |
| Qualified owner acceptance | Unproven | Human decision |
| Real AI, SQL, Azure contract | Unproven | 18 SQL tests skipped; throwaway SQL is FULL tier |
| Phase/tranche decisions, breach pause, BG-011 MDE, registers (ticked) | Proven again | Tests and live probe above |

Unmet criteria needing new code: none. Evidence: `docs/reference/research/issue-126-live-r3-2026-11-19.md`.
