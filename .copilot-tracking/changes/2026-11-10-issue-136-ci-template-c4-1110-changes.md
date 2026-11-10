---
title: Changes for issue-136-ci-template-c4-1110
description: Change record for the resident-demo template test correction
ms.date: 2026-11-10
---

## Product change

`infra/tests/test_resident_demo_deploy.py` only (12 insertions, 3 deletions). `compiled()` takes an optional bicep file (default `resident-demo.bicep`). `test_main_stack_remains_separate_from_resident_demo` no longer asserts the raw text `maxReplicas: 4`; it compiles `modules/containerapps.bicep` and asserts the API `minReplicas` parameter reference, `maxReplicas == [if(parameters('enablePublicSimulationLane'), 1, 4)]`, the parameter default `False`, and no "resident" in the compiled template or `main.bicep`. The template is unchanged.

## Evidence (raw under `phase136-ci-template-c4-evidence-1110/proof/`)

* Red before edit: `red.*`, exit 1, same assertion as CI.
* Green: target test and whole module exit 0; `test_bicep_policy` and `test_container_contract` exit 0.
* Mutation check (`mutation.out`): unmutated passes; inverted branches, cap 3 and a resident name each fail; default ON fails.
* Offline Bicep build and lint for main, guard, containerapps and resident-demo: all exit 0.
* ruff check and format exit 1 on baseline only: the single E501 and format hunk at line 133 are identical at HEAD (`CHAT_RETENTION_DAYS` line, not touched). My own line 173 E501 and format hunk were fixed after the first run (two E501 seen; that first raw output was overwritten by the rerun, only the final one is retained).
* mypy exit 1: 20 baseline errors in this test file (base copy also 20) plus the 3 known `test_bicep_policy` errors; none introduced.
* Image `sha256:d6d6fe32...` reused: `src`, `infra/modules`, `infra/main.bicep` and the startup test are byte-identical to `6759867` (`image-reuse-identity.txt`); startup tests not rerun.

## Divergences

The edits were issued in the same batch as `implement-start`, so the witness recorded a dirty source at that event (qualification retained).
