---
title: Issue 136 public simulation lane deployment binding plan
description: Prospective plan for one initial default-off demo-only startup binding of the public simulation lane in the API container app
ms.date: 2026-11-10
---

## Provenance

Written after the [research](../research/2026-11-10-issue-136-simulation-binding-1110-research.md) and before any source edit, in the same session. Phase details are in the [details](../details/2026-11-10-issue-136-simulation-binding-1110-details.md). The single final-candidate critique is in the [critique](critiques/2026-11-10-issue-136-simulation-binding-1110-plan-critique.md) and is author-inline: no nested agent runs, so it is not independent. The coordinator's exact-head independent review is the independent control and is not repeated here.

## Scope

Refs #136 and #1288 only. One initial scope. Product hunks: `infra/main.bicep`, `infra/modules/guard.bicep`, `infra/modules/containerapps.bicep`, the existing `infra/tests/test_bicep_policy.py`, one new focused startup test file under `infra/tests/` and the existing `infra/README.md`. No `ai.py`, `simulation_lane.py`, API, UI, #133 adapter, device, generator, Dockerfile or workflow change. No parameter set is switched on. No push, PR, GitHub edit, deployment or model call.

## Plan

* P1 `main.bicep`: add `param enablePublicSimulationLane bool = false` with a description that states demo-only, default off, volatile, single replica and no deployment, durability, live-ingestion or model approval. Pass it to `containerapps` and compute the named guard values.
* P2 `guard.bicep`: add named `minLength(1)` guard inputs, each with an "Empty means" description and a `checked` entry: `publicSimulationRequiresDirectDemo` (demoDirectIngress and development profile), `publicSimulationRequiresBrowserAuthentication` (`entraClientId` set, not bearer-only), `publicSimulationRequiresApplications` (`deployApplications`), `publicSimulationRequiresRealApiImage` (`apiImage` is not the `k8se/quickstart` placeholder), `publicSimulationRequiresSingleReplica` (`apiMinReplicas <= 1`). Each passes when the flag is off.
* P3 `containerapps.bicep`: add `param enablePublicSimulationLane bool = false`. Enabled only: two env entries, `command: ['python','-c', recipe]` and `maxReplicas: 1`. Off: no command (`null`), no env entry, `maxReplicas: 4`, every other property unchanged. The recipe is a fixed multi-line literal with double quotes only, no interpolation and no key material.
* P4 Tests in `test_bicep_policy.py`: a render helper that evaluates the compiled API container (env, command, scale) with an ARM-function context; default-off and propagation checks; OFF rendering equals the pre-change contract (no command, no `ZF_SIM_STORE`/`ZF_SIM_KEY_FILE`, `maxReplicas` 4, same env names and values as the base template); enabled valid demo rendering (two env values equal the recipe literals, separated from `/state/mssql`, `ZF_STORE=mssql` and every `AI_*` value identical to the OFF render for the same `enableApiAi`, no key, secret or credential); each refusal combination named through the compiled guard (production, non-demo, unauthenticated or bearer-only, placeholder image, applications off, `apiMinReplicas` 2 and 4); a mutation check that removing the replica clamp or a guard fails the assertion.
* P5 New `infra/tests/test_public_simulation_startup.py`: skipped unless Docker and a pre-built API image tag are supplied through `ZF_API_IMAGE`. It renders the recipe from the compiled enabled template and runs that exact string with `docker run image python -c <recipe>` (no `--entrypoint`), `--user 10001:10001`, `--read-only`, `--cap-drop=ALL`, `--security-opt=no-new-privileges`, a tmpfs `/tmp` and an owned disposable named volume at `/state`. Scenarios: fresh start (modes, separation, `Lane.open`, observe, readback, API `/healthz`), second valid start (same store id and readings), partial state (key only), corrupt store, each unchanged byte for byte and the API still serving with the lane unavailable.
* P6 `infra/README.md`: a short section stating the opt-in, volatile lifetime, startup recipe, manual or unavailable behaviour, no real or live acceptance and the actual runtime and source pins. Tick no criterion.
* P7 Validation tier: owner demo targeted tier, not the complete or `--changed` gate. Run: `az bicep build` of the three templates and the existing entry points, `infra/tests` targeted modules (`test_bicep_policy`, `test_container_contract`, the new startup test with the real image), the existing API simulation and App tests, scoped ruff and type checks for the touched Python files. A fresh API image is built only if no current image carries the frozen source, under the shared non-queued heavy lock.
* P8 Commit locally, in two commits: this tracking set before implementation, then the implementation and its changes and review records. Repository-local privacy-safe identity and the Copilot trailer.

## Success

All checks in P7 pass or the exact skip or failure is recorded. OFF output is proven unchanged. The recipe executed from the rendered template starts the API at UID 10001 under the retained runtime controls. All five #136 criteria stay unticked.

## Stop conditions

A needed change in `ai.py`, `simulation_lane.py`, the Dockerfile, the API or any non-listed file; a baseline fault outside the scope (report the owning issue); a requirement to relax read-only root, capabilities or UID; an inability to retain the durable accounting guarantee.
