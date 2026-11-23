# Research: issue 203 live proof, sixth run (2026-11-23)

Refs #203. Synthetic demo, desktop only, resource group `ama`, no Azure change. Base `5d486b6789` (equals `origin/main`). Research disposition: executed (opened before the search).

## Question

Which of the unticked criteria (1 reference search, 5 deployed app and CI green from `src/`) can be proven now, and does the fifth run (2026-11-22) still hold?

## Evidence plan

* Run `tools/check-legacy-references.py` and `tools.test_check_legacy_references`.
* `az containerapp show` for both apps, `/healthz` on both.
* `gh run list` for `src-ci.yml` and `src-deploy.yml`.

## Findings

* Criterion 1 regressed. `tools/check-legacy-references.py` exits 1 at `5d486b6789`: `.github/rubric/scripts/test_prepare.py:335` names `mvp/` and `prototype/` without the archive tag. The line was added on 2026-11-23 by `00428478c5` (#2329) as a regression guard that the rubric registry holds no retired globs. `tools.test_check_legacy_references.test_repository_has_no_violations` fails with the same line (7 of 8 tests pass). The checker treats regression guards through `GUARD_FILES`; the new guard is not listed, unlike the sibling `test_safe_output_runtime.py`.
* Criterion 5 unchanged: apps `Succeeded`, one active `Healthy` revision each (`ca-cutover-test-demo-api--0000058`, `ca-resident-demo--0000028`), `/healthz` 200 on both. `src-ci.yml` on `main`: last success is workflow_dispatch `42497999337` (2026-11-08); `src-deploy.yml` has 0 runs. Image provenance from `src/` stays unproven, and a deploy is out of demo scope.
* Raw output: `docs/reference/research/issue-203-live-20261123-evidence/`.

Planning Readiness: Ready.
