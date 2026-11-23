# Issue 2188 timing-retries changes (2026-11-23)

Status: complete. Tier: focused (read-only analyzer; no src, gate semantics, permission, image or package change). No divergence from plan.

## Files

* `tools/rpi-gate-timing.py`: `retries`, `retried_groups` in report; per-arm `retries` and Retries markdown column in compare.
* `tools/test_rpi_gate_timing.py`: new test; markdown assertions updated.
* `docs/reference/research/issue-2188-live-timing-retries-2026-11-23.md`, `docs/reference/README.md`, `docs/reference/log.md`.

## Validation

`python3 -m unittest tools.test_rpi_gate_timing` 19 OK (new test fails on the old tool); ruff check and isolated format clean; mypy clean. `rpi-checks.py --all` not run; hosted CI not observed (nothing pushed).

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Drop `--no-cache` | Proven (unit level; 70.5 s to 7.2 s one image, 2026-11-22) |
| Four concurrent image builds | Proven at scheduler level only |
| Shard API tests | Proven (unit level) |
| Retry failed class once, recorded | Proven at shard level (unit); no live receipt with a real retry |
| Receipt records retries | Proven (unit level); now visible in timing compare |
| Verify rejects tampered evidence | Proven (unit level) |
| Wall time before and after, same tree | Unproven (needs two full gates; `--all` forbidden) |
