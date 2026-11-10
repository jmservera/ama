---
title: Issue 136 public simulation lane deployment binding changes
description: Change record for the default-off public simulation startup binding
ms.date: 2026-11-10
---

Plan: [plan](../plans/2026-11-10-issue-136-simulation-binding-1110-plan.md). Base `d52f20a5198de7269f39daf794911545aee01ced`. Refs #136 and #1288 only; all five whole-issue criteria remain unticked.

## Source changes

* `infra/main.bicep`: `enablePublicSimulationLane` (bool, default false), forwarded to `containerapps`, five named guard values.
* `infra/modules/guard.bicep`: five `publicSimulationRequires...` guard params and `checked` entries.
* `infra/modules/containerapps.bicep`: param, fixed store/key literals and recipe var; enabled-only env (`ZF_SIM_STORE`, `ZF_SIM_KEY_FILE`), `command: ['python','-c',recipe]`, `maxReplicas: 1`; `command` is `null` and `maxReplicas` 4 when off.
* `infra/tests/test_bicep_policy.py`: `contains` added to the ARM evaluator subset; module-level `render_api_container`; new `test_public_simulation_lane_binding_is_default_off_guarded_and_keeps_accounting`; the existing replica test now asserts the conditional expression and the rendered OFF value 4.
* `infra/tests/test_public_simulation_startup.py` (new): runs the rendered recipe in the actual API image.
* `infra/README.md`: section "Public simulation lane startup binding".

## Divergences from the plan

* D1 Guard and render tests were added to the existing `BicepPolicyTests` (as planned); only the Docker test is a new file. No other divergence in scope.
* D2 The API simulation regression ran with `PYTHONPATH` pointing at this worktree `src/*/src` because the editable installs resolve to a different checkout (`/home/azureuser/source/ama/src/...`) that lacks `simulation_lane`. No global install or reinstall was done.

## Validation (targeted demo tier; no complete or `--changed` gate)

* `az bicep build` of `main.bicep` exit 0; `az bicep lint` of main, guard and containerapps: no output.
* Compiled-template diff versus a `git archive` of `d52f20a5` with the flag at its default: only the new parameter, five guards, `command: if(...null)`, `maxReplicas: if(...,1,4)`, the recipe and path variables and template hashes differ; env expression gains only the conditional ZF_SIM_ entries.
* `tests/test_bicep_policy.py`: 60 tests OK (also failed correctly under two mutations: clamp removed, single-replica guard weakened). `test_container_contract.py`: 7 OK. `test_iothub_module.py`: 23 OK.
* `src/api/tests/test_quality_simulation_lane.py`: 30 OK (see D2).
* Image `zava-forward-api:rpi-136sim-d52f20a` (`sha256:cc1ec99e86db...`) built once with `docker build -f src/api/Dockerfile src` under `flock -n /tmp/ama-rpi-heavy.lock`.
* `ZF_API_IMAGE=... tests/test_public_simulation_startup.py`: 2 OK (fresh start: key 0600, store 0600, dir 0700, uid 10001, 12 readings observed and viewed, empty stderr; second start: key hash identical and 0 new readings; key-only and corrupt-store states byte and mode identical with `/healthz` 200 and an unavailable-lane message).
* `src/check-container.py api <image>`: PASS.
* Ruff: new test file clean; `test_bicep_policy.py` has one pre-existing RUF100 finding at the unchanged `eval` line that is not part of this change.

## Resources

Owned: one image tag, disposable named volumes `zf-sim-test-*` and containers (all removed; none left). No private data, cloud call, global install or other holder disturbed.
