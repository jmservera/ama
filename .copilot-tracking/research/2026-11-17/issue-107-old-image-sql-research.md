---
title: Issue 107 old-image SQL material-mismatch research
description: Original dated research for the bounded old-image actual-execution SQL test increment
ms.date: 2026-11-17
---

## Status

Opening artifact written before substantive source search (research-open witnessed at seq 2). Findings below were added after that boundary.

## Scope

* Child candidate for the parent topic `feat/assistant-107-integration` (pinned 1c9ac230be1dad9a4ecc21975f9ffe0845309fc4); branch `test/assistant-old-image-sql-107`.
* Surviving criterion: an actual older application image/restart against the disposable SQL contract must not restore a revoked approval or replenish a finite allowance after independent material mutation or revocation.
* Test-only or diagnostic increment; no application, schema or policy change.

## Known inputs

* Retained older image `zava-forward-api:rpi-41446a0c013d3ba3617610b6`, ID sha256:ad99bbb99df321f8d874b0df52ead4b3e24f4fb02c21a2245b278ea1a1e2cf78, created 2026-11-08T01:30:13Z. Git source provenance is UNKNOWN (no OCI revision label).
* Container has no Docker socket and no SQL service; the image was not run here.
* Out of scope: successful partially-used restarted-claim clamp (merged #1271), authority-token rotation (#1608).

## Findings

### Existing evidence and its scope (not duplicated)

* `src/api/tests/test_assistant_restart_non_replenishment.py` (#1599) uses a fresh `SqlStore` plus `Assistants` over one SQLite file. Its `old_image` names (`old-image` owner, `LARGER` config, `change_release` after revocation) are current-source objects; no older package executes. Evidence scope: current code, SQLite, restart semantics.
* `src/api/tests/assistant_process_worker.py` (#1268) runs an OS process from current source against SQLite or MSSQL. Its `vary()` constructs rule, purpose and role differences inside a current process and says so ("not an old image").
* `src/core/tests/release_support.py` builds fixture releases from the current `assistants.runtime_binding`, so a current fixture release is bound to current versions only. This matters: an older image computes a different binding, so a release recorded by current source is itself a material mismatch for it, and a positive control needs a release recorded by the older runtime.
* #1271 (restarted-claim clamp for partially used claims) and #1608 (authority-token rotation) are out of scope.

### Contracts the probe must observe

* `assistant_release.py`: release rows are SQL-owned (`assistant_releases`: id, capability, status, body JSON, revision); `BOUND` lists the versions that must match; `invalidate_changed` revokes an active record whose bound versions differ; revoked and suspended are terminal; `change()` only moves active/suspended rows.
* `assistants.py`: `Assistants(store, env, provider, transport)`; `Limits(env)` reads `ZF_ASSIST_*`; durable pool is table `assistant_allowance` (calls, tokens, used_calls, reserved_tokens), read by the existing tests with `SELECT calls,tokens,used_calls,reserved_tokens FROM assistant_allowance`; `invoke`, `claim`, `execute`, `stop`, `runtime_binding(capability, ai)` are the surface.
* `test_assistants.MssqlFixture` and `src/core/tests/sqlguard.py` define the disposable SQL rules: literal loopback, password auth, task manifest, live container labelled `zf.task=1292-sql-disposable`, loopback-only publish, age under 24 hours. `src/api/checks/sensor_sql_check.py` shows the owned-container lifecycle; `src/api/checks/resident_demo_image_check.py` shows the reviewed `docker run` hardening (read-only root, capabilities dropped, no-new-privileges, tmpfs, owner label).
* The image `CMD` is `python -m zava_forward.api` (HTTP, Entra or demo auth, real provider route). Driving that route would need auth and a real or stubbed AI endpoint and would not give a call counter. An in-image fixed script that imports the packaged `zava_forward.core` under `--entrypoint python` executes the packaged application code against SQL with a local provider stub, keeps the counter, and needs no application change.

### Old image facts

* Only the image ID and creation time are in evidence (`available-old-image.txt`). No revision label was captured, so Git provenance is unknown and must stay unknown. The ID is the only immutable binding; the tag is a content key and is not used for provenance.
* Whether the packaged code has release admission, `runtime_binding`, an `assistant_allowance` pool or an `MssqlStore` compatible with the current schema is unknown. The probe must observe it (file hashes, versions, API surface) before any claim.

### Surviving gap and decision

No existing test runs an older packaged application against disposable SQL while a separate current-source connection revokes or mutates release state and a fresh older process restarts. The smallest increment is:

* a fixed in-image worker (`checks/old_image_worker.py`), stdlib plus packaged modules only, with actions `identify`, `provision` and `execute`;
* a host check (`checks/old_image_sql_probe.py`) that creates its own labelled SQL container, admits it with `sqlguard`, runs the older image by immutable ID with fixed argv, mutates and reads state through its own separate current-source connection, and classifies each named case;
* light deterministic tests of argv, guards, classification and the worker protocol (the worker run against current source on SQLite is a labelled self-test, never old-image evidence).

Named cases: C0 positive control (old runtime records its own release, executes, exactly one stub call, pool consumed); C1 revocation by the host connection then fresh older process (zero calls, status stays revoked, no new active row); C2 material mismatch of a bound field then fresh older process (zero calls, no active release); C3 finite allowance of one call then restart (second task zero calls, pool `used_calls` not reduced).

Outcomes: ACCEPTED only when C0 passes and C1 to C3 hold; VIOLATED when an older process dispatched, restored an approval or replenished (adverse output kept); INSUFFICIENT for unsupported protocol, schema refusal, setup/docker error, timeout or failed positive control; REFUSED for non-disposable targets or an unpinned image.

### Constraints and risks

* No Docker or SQL in this container: the actual continuation is for the coordinator. Light tests keep lower fidelity and are labelled.
* tmpfs `/state` means a restart loses worker-local state; SQL state persists. Recorded as a limit.
* `--network=host` follows the existing reviewed image check because the admitted SQL port is loopback-only.
* An application fix, changed permission meaning or an exhausted grant found by the probe is reported as a bounded follow-up, not implemented here.

### Planning Readiness

Ready. Research disposition: executed.
