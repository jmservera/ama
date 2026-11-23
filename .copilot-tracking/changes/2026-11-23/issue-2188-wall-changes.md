# Issue 2188 wall-time changes (2026-11-23)

Status: complete. Tier: focused (additive receipt field). No divergence from plan.

## Files

* `tools/rpi-checks.py`: `wall_seconds` helper and receipt field.
* `tools/test_rpi_checks.py`: `test_wall_seconds_spans_earliest_start_to_latest_finish_with_retries`.
* `docs/reference/research/issue-2188-live-wall-time-2026-11-23.md`, `docs/reference/README.md`, `docs/reference/log.md`.

## Validation

`python3 -m unittest tools.test_rpi_checks` 130 OK; mypy clean; ruff format clean.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Drop `--no-cache` | Proven (unit level; 70.5 s to 7.2 s on one image, 2026-11-22) |
| Four concurrent image builds | Proven at scheduler level only |
| Shard API tests | Proven (unit level) |
| Retry failed class once, recorded | Proven (unit level); no live receipt with a real retry |
| Wall time before and after, same tree | Unproven (receipt now records `wall_seconds`; needs two full gates, `--all` forbidden) |
| Receipt records retries | Proven (unit level) |
| Verify rejects tampered evidence | Proven (unit level) |
