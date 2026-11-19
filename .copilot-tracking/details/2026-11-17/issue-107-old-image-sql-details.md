---
title: Issue 107 old-image SQL probe details
description: Phase details for the bounded old-image SQL probe
ms.date: 2026-11-17
---

## Phase 1 worker (runs inside the older image)

Invoked `python /probe/old_image_worker.py /probe/<spec>.json` with `--entrypoint python`. Uses only stdlib and packaged `zava_forward.*`. Prints exactly one JSON line `{"status": "ok|unsupported|error", ...}`; any exception becomes `error` with the type and message (adverse output preserved, no secrets).

* `identify`: no database. Reports python, package versions via `importlib.metadata`, SHA-256 of packaged `assistants.py`, `assistant_release.py`, `mssqlstore.py`, `ai_registry.py`, `rai_release.py`, and the list of missing protocol members. Any missing member makes `status=unsupported`.
* `provision` (spec: capabilities, config env, case, principal): opens `MssqlStore(seed, env, state_dir)` (or `SqlStore` in self-test), sets the local stub provider with a call counter, creates the schema, records a fixture release for each capability bound to the packaged `runtime_binding`, invokes each capability for the case as the fixture programme manager, optionally executes one named task, and reports task ids, execute results, provider call count.
* `execute` (spec: task ids, optional re-invoke): fresh store and service (a restart), executes each task, attempts `invoke` for the named capability, reports results, provider calls and states. No release is recorded in this action, so any approval it sees was written elsewhere.

The stub provider returns the same constructed proposal as `test_assistants.Provider`, never reaches a network, and counts calls in process; the count is printed per action.

## Phase 2 host check

* Constants: pinned image ID `sha256:ad99bbb99df321f8d874b0df52ead4b3e24f4fb02c21a2245b278ea1a1e2cf78`; owner label `ama.rpi.owner=issue-107-old-image-sql`; every container name `ama-107-old-<12 hex>`.
* Guards before any container: image ID must equal the pin through `docker image inspect --format {{.Id}}` (fixed argv); refuse `DOCKER_HOST` non-local via the existing `sqlguard` rules; SQL admitted through `sqlguard.require_task_owned_loopback` after the probe's own labelled container and manifest are created.
* SQL container: label `zf.task=1292-sql-disposable`, loopback publish, memory and cpu limits, SA password generated per run, removed by exact name in `finally`.
* Old image runs: `docker run --rm --name N --label OWNER --network=host --read-only --cap-drop=ALL --security-opt=no-new-privileges --tmpfs /tmp --tmpfs /state:uid=10001,gid=10001 --memory 1g --cpus 1 --pids-limit 256 --user 10001:10001 --entrypoint python -v <probe-dir>:/probe:ro -e KEY... IMAGE_ID /probe/old_image_worker.py /probe/<spec>`; secrets pass by `-e KEY` from the process environment, never in argv. Finite `timeout`; on expiry `docker rm --force` of that exact name.
* Host separate connection: a current-source `_Conn` to the same database, never shared with the container; used only for narrow parameterised SQL: set a release `status` to revoked, rewrite one bound field in a release body, read `assistant_releases` and `assistant_allowance`.
* Cases C0 to C3 as in research; each case resets only the probe database (own database name `zf_old_image_107`, created and dropped by exact name).
* Classification: pure function from observations to `ACCEPTED|VIOLATED|INSUFFICIENT`; exit 0, 2, 3; refusal exit 4. A structured JSON report is written to a caller-supplied new directory outside the repository with raw worker output preserved.

## Phase 3 tests

* argv builder has exact fixed shape, no shell, no secret in argv, rejects other image identifiers and bad names.
* Guard refusals: wrong image ID, non-loopback server, missing manifest.
* Classification table: positive-control failure, unsupported, dispatch after revoke, replenishment, restored active row, all-good.
* Worker self-test on current source with SQLite: C0 to C3 observations produced through the same worker and the same classifier, with `fidelity: current-source-self-test` forced and never `ACCEPTED-OLD-IMAGE`.

## Phase 4 README

Short section in `src/api/README.md` under the existing assistant release guidance: exact command, prerequisites, outcomes, limits.

## Amendments from the single critique (applied directly)

* Preconditions and readback: each negative case first verifies by SQL that the capability has an active release recorded by the older runtime and that the task to be tested is pending and distinct from any consumed task; after mutating, the host rereads the row (status or bound field) and requires the change. A missing precondition or readback is INSUFFICIENT.
* Combined allowance: order is consume one call (C0), then mutate or revoke (C1/C2), then restart and try a distinct task. Pool `calls`, `tokens` ceiling and `used_calls` are read before and after; replenishment is `used_calls` lower or the ceiling higher together with an extra dispatch. A restart with a larger `ZF_ASSIST_CALL_ALLOWANCE` is included in C3; the expectation is no extra stub call beyond the original ceiling.
* Intended denial: the worker returns the invoke state and execute result; for revoked and mismatch cases the host requires the release row to be non-active and `invoke` state `disabled`, not merely zero calls.
* Import identity: worker mounted alone in `/probe` (read-only) with `python -I -B`, no `PYTHONPATH`; every action reports `__file__` and SHA-256 of loaded packaged modules; host requires site-packages paths and equal hashes across actions.
* Local engine: fixed `docker context show` must equal `default` and the context endpoint must start `unix://` before any run; `DOCKER_HOST` unset or unix.
* Ownership: created container IDs are captured; removal is by captured ID only after the run label is verified; a name collision aborts before creation. Database and container names embed a per-run random suffix.
* Redaction: generated passwords are removed from all printed and persisted text.
