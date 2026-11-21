---
title: Issue 2188 live, gate speed-up criteria (2026-11-21)
description: Per-criterion evidence for the local full gate speed-up at head 62496349e, covering layer cache, parallel images, API shards, the unimplemented test-class retry and tamper rejection
ms.date: 2026-11-21
---

Scope: synthetic demo, desktop only, FOCUSED tier, documentation only. No `src/` or `tools/` edit, no live Azure, no `rpi-checks.py --all`. Head 62496349e on branch `test/code-live-20261121T212247Z`.

Issue 2188 asks for four changes (cache keyed on Dockerfile and inputs, four concurrent image builds, API test shards, one retry of a failed test class) and three criteria: wall time measured before and after on the same tree, the receipt records retries, and verify still rejects tampered evidence.

## What the tree implements

| Requested change | State at head | Evidence |
| --- | --- | --- |
| Drop `--no-cache` | Implemented as a mode. `image_cache` is `layer` by default; `--fresh-images` adds `--no-cache`. Full-scope receipts require `fresh`, so the full tier keeps its fresh builds by design | `tools/rpi-checks.py` (`IMAGE_CACHE_MODES`, `require_fresh_images`), tests `test_scanned_image_builds_skip_layer_cache`, `test_layer_cache_mode_omits_no_cache_for_every_scanned_image`, `test_verify_rejects_full_scope_receipt_built_with_layer_cache` |
| Concurrent image builds | Implemented through `--jobs N` and a `ThreadPoolExecutor` over groups | `tools/rpi-checks.py` group executor |
| API shards | Implemented: `SHARDED_PROJECTS = {"api": 3}`, fail-closed partition, receipt fields `test_shards` and `shard_helpers` | tests `test_shard_partition_*`, `test_sharding_fails_closed_before_running_when_a_test_would_be_dropped` |
| Retry a failed test class once | Not implemented. `retry=True` on `command()` only tolerates expected probe failures (`expected_probe_failure`); no test-class retry and no retry count in the receipt | grep for `retried`, `retries` finds nothing in `tools/rpi-checks.py` |

## Criterion 1: wall time before and after on the same tree

Full-gate pair on one tree: unproven. A full gate is 40 to 90 minutes and `rpi-checks.py --all` is outside this run's remit. The ten retained full receipts (see [issue 1830 r5](issue-1830-live-r5-2026-11-21.md)) differ in head, base and host load, and `tools/rpi-gate-timing.py compare` refuses them as non-comparable. The jobs 1 runs held 2870 to 2930 s; the single jobs 4 run (g2061/run12) took 2402 s. That is a descriptive pointer, not a measured speed-up.

Bounded same-tree measurement that was possible: the API image build, same tree, same host, host load average about 4.3 for both (2026-11-21, UTC 21:25 to 21:28):

```text
docker build -q --no-cache -f src/api/Dockerfile -t ama2188-probe:fresh src   real 1m20.741s
docker build -q            -f src/api/Dockerfile -t ama2188-probe:layer src   real 0m1.286s  (second run 0m3.297s)
```

Layer cache cut one image build from 80.7 s to 1.3 s. The cached build ran after the fresh build had populated the layers, so this is a warm-cache best case for an unchanged tree, not a gate-level figure. Both throwaway tags were removed afterwards. Verdict: the image-cache part is measured; the whole-gate before and after is unproven.

## Criterion 2: receipt records retries

Unproven and not satisfiable: no retry is implemented, so the receipt records none. Implementing one would change gate semantics (a failing test class passing on re-run weakens the fail-closed contract, and a flaky test would be hidden unless the receipt exposes it). Under the repository's tiering that is a full-tier change needing an owner decision on whether retry is wanted at all, and this run may not run the full gate. It is recorded as an owner decision, not built.

## Criterion 3: verify still rejects tampered evidence

Proven for the current tree. Command, run 2026-11-21 from the worktree root:

```text
python3 -m unittest tools.test_rpi_checks -k tamper -k shard -k fresh -k layer_cache -k full_scope -k rejects
Ran 25 tests in 16.969s   OK
```

The selection includes `test_tampered_or_failed_receipt_refuses_without_executing_content`, `test_sensor_mssql_receipt_rejects_tampered_or_incomplete_evidence`, `test_relaxed_receipt_passes_selection_and_identity_but_not_tampering`, the shard-policy rejection tests and `test_verify_rejects_full_scope_receipt_built_with_layer_cache`. The receipt validator also rejects invalid `image_cache` and `test_shards` values (`tools/rpi-checks.py`, receipt policy check). A sharded or layer-cached receipt therefore cannot satisfy the full tier.

## Defect check

No real defect found in the cache, parallel or shard paths. No source change, so no full tier.

## Verdict

| Criterion | Status | Reason |
| --- | --- | --- |
| Wall time before and after on the same tree | Partly proven | Image build 80.7 s to 1.3 s measured; full-gate pair needs two full gates on one tree and is not run |
| Receipt records retries | Unproven | Retry not implemented; owner decision needed |
| Verify rejects tampered evidence | Proven | 25 targeted tests pass |
