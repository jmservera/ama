# Issue 2188 live changes (2026-11-23)

Status: complete. Tier: focused (scheduling-only gate-tool change; no src, permission, image, package or receipt-semantics change). No divergence from plan.

## Files

* `tools/rpi-checks.py`: `IMAGE_CONCURRENCY`, `docker_slots`/`docker_gate`/`trivy_lock`, `docker_capacity`; dispatch no longer holds one lock; Trivy scans serialised.
* `tools/test_rpi_checks.py`: serial test replaced by `test_images_build_concurrently_and_mssql_runs_alone`.
* `docs/reference/research/issue-2188-live-image-concurrency-2026-11-23.md`, `docs/reference/README.md`, `docs/reference/log.md`.

## Validation

`python3 -m unittest tools.test_rpi_checks` 129 OK; mypy clean; ruff format clean; ruff check 12 pre-existing errors unchanged.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Drop `--no-cache` | Proven (unit level; 70.5 s to 7.2 s on one image, 2026-11-22) |
| Four concurrent image builds | Proven at scheduler level (barrier test); no real timed four-image build |
| Shard API tests | Proven (unit level) |
| Retry failed test class once, recorded | Proven (unit level); already implemented at head; no live receipt |
| Wall time before and after, same tree | Unproven (needs two full gates; `--all` forbidden) |
| Receipt records retries | Proven (unit level) |
| Verify rejects tampered evidence | Proven (unit level) |
