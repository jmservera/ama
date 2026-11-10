---
title: Issue 136 binding C1 changes
description: Changes record for the bounded C1 on the public simulation startup binding
ms.date: 2026-11-10
---

## Edits (base for this cycle `18040b68b`, frozen input `53fcf666c9e757a8bb33d6b557158fa963920ade`)

* `infra/modules/containerapps.bicep` (F1): the `simulation_lane` import moved inside the existing `try`; paths, `provision`, `Lane.open` validation, error-code report and the final `os.execv` are unchanged. No new fallback, no key echo, no state rewrite, no policy, model, budget, auth or scale change.
* `infra/tests/test_public_simulation_startup.py` (F2 and F1 proof): the readback probe uses one pinned slot-aligned clock (computed once, an instant just before the current slot because the consumer rejects stale or future readings) through `Lane.open(..., clock=)`; the rendered startup command is unchanged. It asserts retained `store_id`, readback digest and `added == 0` at the same instant. New slot-crossing negative control (added 1, same `store_id`, changed view) and a new import-failure case (harness `sitecustomize` makes only the recipe's own `python -c` import fail through a read-only bind mount and `PYTHONPATH`; the ordinary API then serves the real `/healthz`). Class attribute annotations and long lines fixed in this file.
* `infra/README.md`: placeholder guard limit, import inside the guard, pinned test clock and local-evidence limits.

## Evidence (raw files under `ROOT/phase136-binding-c1-evidence-1110/proof`)

* Red on the old recipe: `red-startup-old-recipe*` run 1 failed at the harness cwd (preserved adverse), run 2 failed three tests because a fixed 2023 instant is rejected as stale (`added` 0, preserved adverse, so the clock became a runtime slot-aligned instant), run 3 failed only the import-failure test with the real `ImportError` traceback (F1 red).
* Green: `green-startup-new-recipe` and `green-startup-final` 4 tests OK; policy 60 OK; container contract 7 OK; IoT Hub 23 OK; API simulation 30 OK; `check-container` exit 0; Bicep build and lint exit 0 for main, guard, containerapps.
* Owned venv `/tmp/c1venv136` with `ruff==0.17.1`, `mypy==2.4.0`, core, agents and api pip-installed; imports resolve under its `site-packages` (`venv-origins.txt`).
* Reused image `zava-forward-api:rpi-136sim-d52f20a` ID `sha256:cc1ec99e86db174ffc0bfac94512db423bfd81fe80c1a8e637f5e04dfe5aaea8`; `git diff d52f20a5 HEAD -- src` empty; no rebuild; `image-config.txt` shows no entrypoint and Cmd `python -m zava_forward.api`.
* Heavy-resource lock `flock -n /tmp/ama-rpi-heavy.lock` free for every container run; no holder seen; no leftover `zf-sim-test` container or volume.

## Adverse and residual results (not waived)

* `ruff check` on `infra/tests/test_bicep_policy.py` (workflow-pinned isolated command) reports 3 E501 and the format check fails; the base file passes both. These violations come from lines added by the frozen original candidate, not from C1, and C1 scope excludes that file, so they are reported and unrepaired (`ruff-*-policy`, `lint-baseline-classification.txt`).
* `mypy --check-untyped-defs` on `test_bicep_policy.py`: 3 base errors plus 2 at `2254` and `2256` introduced by the original candidate (`mypy-startup-final.out`, `mypy-baseline-d52f20a-policy.txt`); the startup test file itself has none. The first lint run with default non-isolated ruff produced RUF100 and is not the pinned configuration.
* Local container health uses the default JSON working store; it is not MSSQL, browser-auth or Azure evidence, and no model call was made. Accounting stays `ZF_STORE=mssql`.
* Original hooks override use remains disclosed. No stash, reset, discard or hooks override in this cycle.
