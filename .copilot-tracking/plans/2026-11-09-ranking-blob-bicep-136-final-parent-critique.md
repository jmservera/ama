# Critique: final-parent integration plan (executed once, 2026-11-09)

Reviewer: read-only rubber-duck agent, one pass over the committed-to-be research, plan and details. Verdict: Revise. No Blocking findings. Not repeated for this task.

| Finding | Severity | Disposition |
| --- | --- | --- |
| Infra cwd ambiguity: CI globs are repo-root relative; unit selectors should be explicit and include `test_edge_module` (storage private endpoints, Container Apps networking) | Significant | Applied directly: plan amendment below |
| API priority coverage: add the resolution-route `CommittedReloadError` 409 `committed` check and `test_ranking_scale` | Significant | Applied: `test_case_journey` (parent-owned 409 `committed` assertion at parent `test_case_journey.py` line 593, verified by `git show`) was already selected; `test_ranking_scale` and `test_ranking_policy` added. No new synthetic probe invented |
| Conflicting pass criteria: inherited API wiring-test ruff failure expected yet "all exit 0" | Significant | Applied: classified as a retained ADVERSE DIAGNOSTIC, separate from mandatory selected checks |
| `ruff format` must not take `--select` or `--target-version` | Minor | Applied |

## Plan amendment (binding)

* Infra, cwd `infra/`: `az bicep build --file X` and `lint --file X` for each of `*.bicep modules/*.bicep` (relative to `infra/`), plus the four `build-params`.
* Infra unit tests, cwd `infra/`: `PYTHONPATH=tests REQUIRE_AZ_BICEP=1 python -m unittest test_bicep_policy test_identity_rbac test_secret_lifecycle test_api_ingress_transport test_governance test_edge_module`.
* API, cwd `src/api`: `PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest test_ranking_publication_wiring test_case_journey test_ranking_scale test_ranking_policy`.
* Mandatory selected checks: all of the above plus core selectors and isolated ruff check/format on the three-file infra CI form and the changed infra test file. Ruff check form: `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 <files>`. Ruff format form: `ruff format --isolated --line-length 100 --check <files>`.
* ADVERSE DIAGNOSTIC (not a selected pass criterion): the same isolated ruff check on `src/api/tests/test_ranking_publication_wiring.py`, expected exit 1 with 10 errors inherited from the parent; recorded as measured, never fixed here.
