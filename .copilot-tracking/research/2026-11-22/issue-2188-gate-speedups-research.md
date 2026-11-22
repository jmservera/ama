---
title: Research for issues 2188 and 2187 (gate speed-ups, lock scoping)
date: 2026-11-22
disposition: executed
planning_readiness: Ready
---

## Findings (read from tools/rpi-checks.py at HEAD 671a17fde3)

* R1 (#2188 drop `--no-cache`): already delivered. `image_build_argv` adds `--no-cache` only when `fresh`; default image cache is `layer`; `--fresh-images` is implied for full scope and `require_fresh_images` makes verify reject full receipts without `image_cache=fresh`.
* R2 (#2188 shard api tests): already delivered (`SHARDED_PROJECTS`, `shard_partition`, `plan_shards`, tests at test_rpi_checks.py).
* R3 (#2188 retry a failed test class once, recorded in the receipt): NOT delivered. Verification demands exactly one passing row per trusted-matrix check, so a retry needs a separate receipt field.
* R4 (#2188 build four images concurrently): NOT delivered. `dispatch` serialises mssql, images and logo-0600 behind `docker_lock` because the heavy lock covers one host resource and builds are capped at 3g/2 CPU each. Concurrency changes resource-safety assumptions and cannot be measured without a full gate (forbidden here).
* R5 (#2187): delivered by `needs_heavy_lock` plus `main` gating, with tests `test_heavy_lock_only_for_docker_sql_or_browser_groups` and `test_main_skips_lock_without_heavy_group_and_takes_it_with_one`.
* R6 (#2188 before/after wall time on the same tree): needs two full gates; `rpi-checks.py --all` is forbidden for this task. Unprovable here.
* R7 (verify rejects tampered evidence): `validate_receipt` hashes every file in `files`; a new retry log must sit inside that map so tampering is rejected. Will be tested.

## Decision

Implement R3 (shard-level retry once, recorded in `receipt["retries"]`, validated on verify). Leave R4 and R6 documented as unproven. Tier FULL applies to gate-tool semantics per the instructions; the task forbids `--all`, so focused tests only and a stated gap.
