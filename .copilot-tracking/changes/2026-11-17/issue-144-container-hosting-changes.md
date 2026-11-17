---
title: Issue 144 assessment changes
ms.date: 2026-11-17
---

## Changes

* `infra/README.md`: added "Assessment against main (issue 144, 2026-11-17)" with test results and the PR 1641 drift note.
* `infra/tests/test_container_hosting_completeness.py`: added `test_recorded_reports_disclaim_declared_scale_and_production_claims`.

## Validation (FOCUSED tier; no SQL, Bicep, deployment or security change, so FULL tier not triggered)

* `python3 -m unittest infra.tests.test_container_hosting_completeness`: 17 OK
* `infra.tests.test_container_contract`, `test_bicep_containerapp_demo_wiring`: 28 OK
* `src/api` (discover -p) `test_scale_fixture_load_and_restart.py` 4, `test_restart_audit.py` 1, `test_scale_load.py` 7: OK
* `src/agents` `test_worker.py`: 19 OK
* `ruff format --isolated --line-length 100 --check` on the test file: clean
* mypy: not applicable (no `src/<project>` change). `rpi-checks.py --all`: not run (heavy lock, FOCUSED tier).
* Adverse note: the new test also passes without the README edit; it pins existing report fields, so it guards future drift rather than reproducing a failure.
