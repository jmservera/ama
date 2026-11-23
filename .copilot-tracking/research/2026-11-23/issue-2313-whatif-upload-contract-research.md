# Research: issue 2313 what-if upload contract (Refs #2313)

Disposition: executed (reuses `docs/reference/research/issue-2313-what-if-live-2026-11-23.md`).
Planning Readiness: Ready.

## Findings

* Earlier workers added `infra-image-build.yml`, its contract test, the gate-matrix entry and a path-filter execution test.
* `infra/tests/test_pipeline.py` checks `infra-plan.yml` structure, `workflow_run` trigger and checkout order, but no test asserts that the what-if job uploads its result, fails when the file is missing, is read-only (no apply or deploy), or that `id-token` is limited to the what-if job.
* Criterion 1 ("uploads the result") therefore rests on inspection only. A regression test closes that gap. Live proof stays blocked: `INFRA_PLAN_ENABLED` unset, OIDC owner action (#138).
