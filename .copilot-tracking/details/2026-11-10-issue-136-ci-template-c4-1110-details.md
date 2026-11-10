---
title: Details for issue-136-ci-template-c4-1110
description: Exact test change
ms.date: 2026-11-10
---

## Phase 1 edit

1. `compiled(bicep: str = "resident-demo.bicep")` builds the named file.
2. In `test_main_stack_remains_separate_from_resident_demo`, keep the `apiMinReplicas` text checks and the "resident" absence checks, remove the `maxReplicas: 4` literal, then compile `modules/containerapps.bicep`, take the `Microsoft.App/containerApps` resource scale, and assert:
   * `minReplicas == "[parameters('apiMinReplicas')]"`
   * `maxReplicas == "[if(parameters('enablePublicSimulationLane'), 1, 4)]"` (default branch 4, enabled branch 1, not inverted)
   * `enablePublicSimulationLane` default is `False`
   * no "resident" in the compiled containerapps template JSON text.

## Mutation validation

On a temporary copy outside the repository, mutate the template (invert branches, replace cap 4 with 3, add a resident string) and confirm the assertions fail each time. Retain the output.

## Validation

The actual test, `test_resident_demo_deploy.py` whole module, `test_bicep_policy.py`, ruff check and format, mypy comparison, `az bicep build` and `lint` for main, guard, containerapps and resident-demo.
