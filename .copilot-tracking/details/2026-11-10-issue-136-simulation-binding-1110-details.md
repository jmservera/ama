---
title: Issue 136 public simulation lane deployment binding details
description: Phase details for the default-off public simulation lane startup binding
ms.date: 2026-11-10
---

See the [plan](../plans/2026-11-10-issue-136-simulation-binding-1110-plan.md) and the [research](../research/2026-11-10-issue-136-simulation-binding-1110-research.md).

## Phase 1 Bicep composition

* `main.bicep`: new parameter after `enableRankingArchiveBlob`; forward it as `enablePublicSimulationLane` in the `containerapps` module arguments; add five guard arguments of the form `!enablePublicSimulationLane || <condition> ? 'ok' : ''`.
* `guard.bicep`: five new params and `checked` entries.
* `containerapps.bicep`: parameter, `var publicSimulationStore` and `publicSimulationKey` literals under `/state/public-simulation/`, the fixed recipe var, conditional env array appended to the existing `concat`, `command: enablePublicSimulationLane ? [...] : null`, `maxReplicas: enablePublicSimulationLane ? 1 : 4`.
* Recipe behaviour: when neither file exists, create the directory with mode 0700 and call `provision`; open and close the lane to validate; on any exception print the error code only; then `os.execv` the ordinary API module. Existing files are never rewritten, partial or corrupt state is never touched.

## Phase 2 Compiled-template tests

* Render helper evaluates the compiled API container with a context for `tenant`, `environment`, `json`, `string` and attribute-accessing parameter objects. Newlines inside compiled string literals are escaped before evaluation so the multi-line recipe survives.
* Cases: default off at every level, forwarding, OFF identity with the base contract, enabled demo render, six refusals, replica clamp and mutation rejection.

## Phase 3 Executed recipe

* The startup test takes the rendered recipe string and runs it, unchanged, in the image. It reads results through `docker exec` or a second run on the same disposable named volume and removes every owned container and volume at the end.

## Phase 4 README and records

* One section in `infra/README.md`; changes record; review record after observation; state and handoff.

Stop conditions: any edit outside the listed files, any relaxation of runtime controls, any private data, cloud or model dependency.
