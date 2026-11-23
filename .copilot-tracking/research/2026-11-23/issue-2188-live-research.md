# Issue 2188 live research (2026-11-23)

Research disposition: executed. Planning Readiness: Ready.

## Findings at head 342fad401d

* Criterion "four concurrent image builds" is unmet: `Runner.dispatch` wraps `mssql`, `image-*` and `logo-0600` in one `docker_lock` (`tools/rpi-checks.py` dispatch), and `test_sql_and_image_resources_are_serial` pins peak concurrency 1.
* Criterion "retry a failed test class once, recorded in the receipt" is already implemented at head (finding in /tmp/gate-review-findings.md predates it): `SHARD_ATTEMPTS`, `retryable_failure`, `record_retry`, `validate_retries`, receipt `retries`; tests `test_failed_shard_is_retried_once_and_recorded`, `test_validate_retries_rejects_tampered_or_forged_records`.
* `Runner.image` uses a per-run token tag per group, ephemeral container ports in `src/check-container.py`, and per-project output names, so builds and container probes do not collide. Trivy scans share one `cache/trivy` directory; concurrent runs on one cache can contend on its database lock, so scans stay serialised.
* `mssql` starts a SQL Server container needing memory; it stays exclusive of image groups.
* Memory/CPU: each build is capped at 3 GiB / 2 CPUs; scheduling is already bounded by `--jobs`, which `worker_limit` budgets at 2 CPUs and 4 GiB per job.

## Design decision

Image groups take one slot of a four-slot semaphore (build and container probe concurrent); `mssql` takes all four slots; Trivy scans hold a lock. Effective image concurrency is min(4, jobs).
