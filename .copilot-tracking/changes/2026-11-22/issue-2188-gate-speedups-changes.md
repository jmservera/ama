---
title: Changes for issues 2188 and 2187
date: 2026-11-22
---

## Changes

* tools/rpi-checks.py: failed test shards (exit code above 0, not 124, 127 or 130, not interrupted) are retried once; the failed row moves to `receipt["retries"]` (group, log, sha256, exit_code, argv); the failed log stays in `files`, so verification hashes it. `validate_retries` rejects malformed, forged, reused-log or non-failing records. Log indices are monotonic so a retry never overwrites a concurrent shard log.
* tools/test_rpi_checks.py: three tests (retry recorded, second failure or timeout not excused, tampered or forged retries rejected).

## Validation

* `python3 -m unittest tools.test_rpi_checks`: 126 tests OK. `ruff format --check`: clean. `ruff check`: 20 findings, identical to baseline. `mypy tools/rpi-checks.py`: no issues.
* Tier: tooling edit that changes gate evidence semantics, so FULL applies; `rpi-checks.py --all` was forbidden for this task and was not run. The coordinator must run the full gate; the change is a gap until then. No src code changed. Live Azure and browser proofs are not applicable to a local gate tool.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| #2187 lock only when a heavy group is selected; test | Proven (pre-existing, re-run) | `needs_heavy_lock`, `main`; tests `test_heavy_lock_only_for_docker_sql_or_browser_groups` and `test_main_skips_lock_without_heavy_group_and_takes_it_with_one` pass in the 126-test run |
| #2188 drop --no-cache (cache keyed on inputs) | Proven in code (pre-existing) | `image_build_argv`; `require_fresh_images` keeps full tier fresh; builds tests pass |
| #2188 shard api tests | Proven in code (pre-existing) | `shard_partition`, `plan_shards` tests pass |
| #2188 retry a failed class once, recorded | Proven by this change at shard granularity | three new tests; test class granularity not attempted |
| #2188 receipt records retries | Proven | `receipt["retries"]`, `validate_retries` |
| #2188 verify still rejects tampered evidence | Proven for retries and file hashes (unit level) | `test_validate_retries_rejects_tampered_or_forged_records`; existing hash tests pass; no full-gate receipt run |
| #2188 build four images concurrently | Unproven, not implemented | serialised by `docker_lock` for host resource safety; changing it needs a full gate to validate |
| #2188 wall time measured before and after on same tree | Unproven | needs two full gates; `--all` forbidden here |
