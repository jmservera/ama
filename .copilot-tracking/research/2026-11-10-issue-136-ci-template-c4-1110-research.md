---
title: Research for issue-136-ci-template-c4-1110
description: Why the resident-demo template test fails on the published PR 1380 head
ms.date: 2026-11-10
---

## Failure

PR 1380 head `6759867552cdebf789544eb9865ad217d394dff8`, run 42811294452, job 129813174121 (log `ROOT/ci-1380-namespace-actual-1207.txt`): `test_resident_demo_deploy.TemplateTests.test_main_stack_remains_separate_from_resident_demo` fails at `assertIn("maxReplicas: 4", main)`; 540 tests, one failure, four skips. Reproduced locally before any edit (exit 1, `proof/red.*`).

## Findings

* The test reads `infra/modules/containerapps.bicep` as raw text. Frozen-binding line 239 is now `maxReplicas: enablePublicSimulationLane ? 1 : 4`, so the literal `maxReplicas: 4` no longer occurs.
* The template is correct, not regressed: the compiled API container app scale is `[if(parameters('enablePublicSimulationLane'), 1, 4)]`. Default OFF renders 4, enabled renders 1 (existing `test_bicep_policy` asserts both, lines 766 and 768, 2268-2281). The agents job cap of 5 is unchanged.
* The failing test's real intent: the main stack's scale contract stays independent of the resident-only demo. Its other assertions (`param apiMinReplicas int = 0`, `minReplicas: apiMinReplicas`, no "resident" in `main.bicep` or `deploy.py`) still pass.
* The test module already has a `compiled()` helper that runs `az bicep build --stdout` for `resident-demo.bicep`; it can be parameterised by file.
* `main` `901fea60` differs from this branch in `infra/` only by the six feature files, so no adoption is needed to fix this.

## Decision

Keep the template unchanged. Replace the brittle literal with a compiled-template assertion of the API scale contract (min parameter reference, max conditional 1-or-4) and keep the resident separation checks, extending them to the compiled containerapps text.

## Planning Readiness

Ready. Not covered: any change to replicas, budgets, permissions or the resident stack.
