---
title: Issue 2188 live, concurrent image builds (2026-11-23)
description: Lifts the single docker lock so up to four image groups build concurrently, with per-criterion evidence for the gate speed-up issue
ms.date: 2026-11-23
---

Scope: synthetic demo, desktop only. Gate-tool change in `tools/rpi-checks.py` (scheduling only), no `src/` change, no Azure access, no `rpi-checks.py --all`. Tier: focused with targeted tests; classification basis is that no permission, pinned image, package, secret, deployment or security control changed and receipt semantics are unchanged. The coordinator owns any full gate.

Source finding: `/tmp/gate-review-findings.md` D3 (dispatch held `docker_lock` around every image build) and the claim that the retry was unimplemented. The retry half was already stale at head 342fad401d (see [the 2026-11-22 refresh](issue-2188-live-gate-speed-2026-11-22.md)).

## Change

* `Runner.dispatch` no longer serialises on one lock. A four-slot semaphore (`IMAGE_CONCURRENCY`) admits one slot per image group (`image-*`, `logo-0600`); `mssql` takes all four slots, so it still runs alone as before.
* Trivy scans (`image()`) hold `trivy_lock`, because concurrent scans share one `cache/trivy` directory and its database lock. The build and `src/check-container.py` probe (ephemeral ports, per-run tags) run concurrently.
* Effective concurrency is min(4, `--jobs`); `worker_limit` already budgets 2 CPUs and 4 GiB per job and each build is capped at 3 GiB and 2 CPUs.
* `test_sql_and_image_resources_are_serial` is replaced by `test_images_build_concurrently_and_mssql_runs_alone`: four image groups reach a four-party barrier (they cannot finish unless they overlap) and `mssql` never overlaps an image.

## Evidence

```text
python3 -m unittest tools.test_rpi_checks            Ran 129 tests in 35.4s  OK
python3 -m mypy tools/rpi-checks.py                  Success: no issues found
ruff format --isolated --line-length 100 --check     already formatted
ruff check tools/rpi-checks.py                       12 errors, identical before and after (pre-existing)
```

## Per-criterion table

| Criterion | Status | Reason |
| --- | --- | --- |
| Drop `--no-cache` (cache keyed on inputs) | Proven (unit level) | `layer` mode default; image build 70.5 s to 7.2 s measured on 2026-11-22 |
| Build four images concurrently | Proven at scheduler level, not at gate level | Barrier test shows four groups overlap and mssql is exclusive; no real four-image build was timed |
| Shard API tests | Proven (unit level) | existing shard tests pass |
| Retry a failed test class once, recorded | Proven (unit level) | `test_failed_shard_is_retried_once_and_recorded`, `test_validate_retries_rejects_tampered_or_forged_records`; no live receipt with a real retry |
| Wall time before and after on the same tree | Unproven | needs two full gates; `--all` not permitted here |
| Receipt records retries | Proven (unit level) | `receipt["retries"]` validated |
| Verify rejects tampered evidence | Proven (unit level) | tamper tests inside the 129 |

Residual risks: real concurrent Docker builds depend on host capacity (a 4-image run uses up to 12 GiB build memory; `--jobs` and `worker_limit` bound it); Trivy serialisation is a precaution not proven necessary.
