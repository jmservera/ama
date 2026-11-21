---
title: Issue 144 container hardening guard fix for Container Apps (2026-11-20)
description: Defect, fix, local evidence and per-criterion status for the container hardening guard that refused to start on Azure Container Apps
ms.date: 2026-11-20
ms.topic: reference
---

## Scope

Synthetic demo, desktop only. Refs #144. Base `df9831da7`. Local source change and local Docker evidence only; no Azure write was made and no credential is recorded. Classification: FULL tier (security control in `src/core`). The complete local gate, a verified external receipt and independent exact-head review are run by the coordinator and are not claimed here.

## Defect (owner-measured on a live replica as uid 10001)

* `CapInh` equals `CapBnd` (`0xa80425fb`) while `CapPrm`, `CapEff` and `CapAmb` are 0, so the guard check "Linux capability mask CapInh must be zero" fails. Container Apps cannot drop capabilities or set the user.
* `EmptyDir` mounts `/tmp` and `/state` are `root:root` mode `0777` without the sticky bit, so "Scratch directory is world-writable without sticky bit" fails.
* `src/check-container.py` runs Docker with `--cap-drop=ALL`, a sticky tmpfs `/tmp` and `/state` owned by 10001, so it hid both.

## Fix

* `_drop_inheritable_capabilities()` in `src/core/src/zava_forward/core/container_hardening.py` calls `capget` and `capset` (version 3 header `0x20080522`, two data structs) with the inheritable set cleared. It runs after `NoNewPrivs` and before `/proc/self/status` is read, and is injectable (`drop_inheritable_fn`) like `prctl_fn`. The zero-mask verification is unchanged, so a failed drop fails closed.
* `prepare_private_scratch()` creates `/tmp/zf` and, when `ZF_STATE` is configured, `/state/zf` (mode `0700`, owned by the current user, `exist_ok` because `EmptyDir` survives restarts) and repoints `TMPDIR` and `ZF_STATE`. It is a no-op unless `ZF_CONTAINER_HARDENING=enforced`. `ZF_STATE` is repointed only when already set because `resident-demo` forbids it by design. All twelve guard-bearing entrypoints call it before the guard.
* The sticky-bit rule and the zero-mask rule are not relaxed.
* `CapBnd` stays non-zero: lowering it needs `CAP_SETPCAP`. With `NoNewPrivs == 1` and empty permitted and ambient sets, `execve` cannot raise any capability, so the bounding set is inert. This is an engineering argument and is recorded for reviewer confirmation.

## Evidence

| Check | Result |
| --- | --- |
| `src/core/tests/test_container_hardening.py` (8 tests): CapInh non-zero then dropped passes; failed drop, drop that leaves the mask, and non-zero permitted all refuse; world-writable directory without sticky refused and private subdirectory accepted; helper idempotent and no-op when not enforced; real `capset` returns 0 unprivileged | Pass |
| `infra/tests/test_container_hosting_144.py` (19 tests, includes real kernel child-process guard run and entrypoint exit-code-2 refusal) | Pass |
| `src/orchestrator` (143), `src/importer` (125) unit suites; `src/api` live receiver, simulator, control and log-privacy tests (112, 2 skipped) | Pass |
| `ruff check` per project, ruff format check on the new and changed core files, `mypy` in orchestrator and importer | Pass. `mypy` in `src/core`, `src/api` and `src/agents` reports only existing `opentelemetry` import errors from the missing optional package on this host, none in changed files |
| `python3 src/check-container.py <project> <image>` for api, agents, orchestrator and importer built from this tree | Pass for all four |
| Container simulating the Container Apps state: root starts, sets `CapInh=0xa80425fb` with a real `capset`, drops to uid 10001 (`CapPrm`/`CapEff` 0), read-only root, `/tmp` and `/state` tmpfs mode `0777` without sticky, `ZF_CONTAINER_HARDENING=enforced` | Without the helper the guard refuses on the world-writable scratch directory; with `prepare_private_scratch()` it passes, and `CapInh` reads `0` afterwards. The api and agents images start past the guard in the same mounts |
| Read-only Azure check of `ca-cutover-test-demo-api` | Active revision `0000037`, Healthy, ScaledToZero, with `ZF_CONTAINER_HARDENING=off`: the deployed demo does not enforce hardening |

## Per-criterion status (unticked criteria of #144)

| Criterion | Status | Basis |
| --- | --- | --- |
| Worker and job images are real, versioned and deployed through the pipeline | Unproven | Not addressed by this change. No live pipeline deployment receipt was captured; a deployment is an Azure write outside this task |
| Container hardening is enforced in the deployed app, not only in CI | Unproven | The startup defect is fixed locally and reproduced with a faithful local simulation, but the deployed demo runs with `ZF_CONTAINER_HARDENING=off`. The live receipt (a Container Apps replica Running and Healthy under `enforced`) is not captured and needs an owner-authorised Azure write (a new image revision with the enforced setting) |

## Follow-up

* After the owner authorises a revision, deploy an image built from this change with `ZF_CONTAINER_HARDENING=enforced` and record replica state, `/proc/self/status` capability lines and the absence of a startup refusal.
