---
title: Issue 2188 live, gate speed-up criteria refresh (2026-11-22)
description: Per-criterion evidence for the local full gate speed-up at head 3219004e90, superseding the retry finding of the 2026-11-21 note
ms.date: 2026-11-22
---

Scope: synthetic demo, desktop only, FOCUSED tier, documentation only. No `src/` or `tools/` edit, no live Azure, no `rpi-checks.py --all`. Head 3219004e90, branch `test/gate-speed-live-20261122T231607Z`. This note supersedes the retry finding in [the 2026-11-21 note](issue-2188-live-gate-speed-2026-11-21.md), which was written before the shard retry landed in #2272.

## What the tree implements

| Requested change | State at head | Evidence |
| --- | --- | --- |
| Drop `--no-cache` | Implemented as a mode: `layer` by default, `--fresh-images` adds `--no-cache`. Full-scope receipts must be `fresh`, so the full tier keeps fresh builds by design | `image_build_argv`, `require_fresh_images`; tests `test_scanned_image_builds_skip_layer_cache`, `test_verify_rejects_full_scope_receipt_built_with_layer_cache` |
| Build four images concurrently | Not implemented. `dispatch` takes `docker_lock` for every `image-*`, `logo-0600` and `mssql` group, so images build one at a time; `--jobs` parallelises the other groups | `tools/rpi-checks.py`, `dispatch`; `test_sql_and_image_resources_are_serial` asserts the serial policy |
| Shard api tests | Implemented: `SHARDED_PROJECTS = {"api": 3}`; 268 api modules split 89, 90 and 89 across three shards; fail-closed if a test would be dropped | `shard_partition`, `plan_shards`; tests `test_shard_partition_*`, `test_sharding_fails_closed_before_running_when_a_test_would_be_dropped` |
| Retry a failed test class once | Implemented at shard granularity (not per class): one retry (`SHARD_ATTEMPTS = 2`) of a shard failing with a test exit code; timeouts, missing tools and interrupts are never retried; the failed row moves to `receipt["retries"]` and its log stays hashed in `files` | `retryable_failure`, `record_retry`, `validate_retries`; `test_failed_shard_is_retried_once_and_recorded`, `test_second_shard_failure_or_timeout_is_not_excused` |

The partition counts above are the number of test modules per shard (89 + 90 + 89 = 268).

## Criterion 1: wall time before and after on the same tree

Whole-gate pair: unproven. It needs two full gates (40 to 90 minutes each) on one tree and `rpi-checks.py --all` is outside this run's remit. Retained receipts differ in head, base and host load and `tools/rpi-gate-timing.py` refuses them as non-comparable.

Bounded same-tree measurement of the cache change, one image, same host, 2026-11-22 (load average 5 to 8 during the run):

```text
docker build -q --no-cache -f src/api/Dockerfile -t ama2188b:fresh src   real 1m10.546s
docker build -q            -f src/api/Dockerfile -t ama2188b:layer src   real 0m7.249s
```

The layer-cache build ran after the fresh build had populated layers, so this is a warm best case, not a gate figure. Both throwaway tags were removed. Verdict: image-cache part measured, gate-level pair unproven.

## Criterion 2: receipt records retries

Proven at unit level. `receipt["retries"]` is written by `record_retry` and validated by `validate_retries` (exact key set, monotonic log name, hash match against `files`, positive non-timeout exit code, no reuse by a command row). No full-gate receipt with a real retry exists; the retry has not been exercised outside tests.

## Criterion 3: verify rejects tampered evidence

Proven at unit level, run 2026-11-22 from the worktree root:

```text
python3 -m unittest tools.test_rpi_checks -k tamper -k shard -k retry -k retries -k fresh -k layer_cache -k full_scope
Ran 19 tests in 13.697s   OK
python3 -m unittest tools.test_rpi_checks tools.test_rpi_gate_timing
Ran 144 tests in 45.733s   OK
```

`test_tampered_or_failed_receipt_refuses_without_executing_content` and `test_validate_retries_rejects_tampered_or_forged_records` cover content and retry-record tampering. The FAILED lines in the output are expected negative-path fixtures.

## Verdict

| Criterion | Status | Reason |
| --- | --- | --- |
| Wall time before and after on the same tree | Partly proven | Image build 70.5 s to 7.2 s measured; gate-level pair not run |
| Receipt records retries | Proven (unit level) | Retry and receipt record implemented; no live full-gate receipt |
| Verify rejects tampered evidence | Proven (unit level) | 144 tests pass; no full-gate receipt verified here |
| Four images concurrent (issue text, not a criterion) | Unproven, not implemented | `docker_lock` serialises images for host resource safety; changing it is a gate-semantics change needing the full gate |

Remaining for the owner: run the gate before and after on one tree, and decide whether to lift `docker_lock` for images.
