# Issue 1837 live changes

Order note: test and check edits were drafted before this record and the plan existed; the witness `implement-start` boundary therefore follows the edits. Recorded honestly.

## Files

* `src/api/tests/test_nomination_api_routes.py`: extended browser test; added native-encoding refusal and script/CSRF-header tests.
* `src/api/checks/nomination_route_forms_browser_check.py`: new axe browser check.
* `docs/reference/research/issue-1837-live-demo-evidence-2026-11-18.md` and `issue-1837-live-2026-11-18/`: evidence, probes, results.
* `docs/reference/README.md`, `docs/reference/log.md`: index and log.

## Per-criterion proven/unproven

| Criterion | Status |
| --- | --- |
| Failing-first regression for three forms | Proven at 9da3fcd (fails), passes on main |
| Valid submissions retain records; JSON compatible | Proven locally; unproven live (deployed image lacks script; redeploy not authorised) |
| Negative boundaries | Proven locally and live without writes |
| Browser journeys with axe, no skips | Partly: zero violations except open target-size finding |
| RPI evidence, independent review, hosted CI | RPI proven; independent review and hosted CI not done |
| Full tier receipt | Unproven by instruction (FULL classified, no full gate) |

## Validation

* unittest tests.test_nomination_api_routes: 8 OK, no skips
* mypy (src/api): no issues in 348 files; ruff check and format check clean
* No web UI files changed, so accessibility baseline and content standard tests are not applicable; no workbench check changed, so the scenario manifest hash is unchanged.
* Azure: no resource created; nothing to delete.
