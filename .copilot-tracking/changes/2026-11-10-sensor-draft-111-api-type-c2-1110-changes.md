---
title: Issue 111 API typing C2 changes
ms.date: 2026-11-10
task_id: 111-api-type-c2-1110
---

## Prospective (registered before implement-start)

* One test-only typing edit in `src/api/tests/test_sensor_review_draft_api.py`: exact-call `# type: ignore[no-untyped-call]` on the legacy `App` constructor call. Plus these dated RPI records. No production, config, UI, schema or dependency change. This spends the one Root-selected remaining inherited batch (minimum 0 afterwards).

## Actual

* `src/api/tests/test_sensor_review_draft_api.py`: `App(self.store, PASSWORD)` extracted to a local `app` with an exact-call `# type: ignore[no-untyped-call]` and a justification comment; `make_handler(app)` unchanged in behaviour. `git diff --stat`: 1 file, 3 insertions, 1 deletion. No `pyproject.toml`, production, UI, schema or dependency change.
* Raw results in `ROOT/checks-111-api-type-c2-1110/`.

## Validation

* Before (unchanged `2b050647b`): API `mypy` (configured, pinned 2.4.0, venv `/tmp/zf-111-1110/venv`) exit 1, the identical single error at line 63, 220 files. Local run omitted CI `PYTHONPATH`; same error.
* After: API `mypy` exit 0, no issues in 220 files; 6 API draft cases OK (0 skips); `ruff check` and `ruff format --check` on the touched file exit 0; `node --check` unchanged `ops.js` exit 0.
* Browser: `checks.quality_sensors_browser_check` under own `flock -n /tmp/ama-rpi-heavy.lock` admission (no holder shown, flock exit 0) FAILED to launch, exit 1: Chrome aborted with `Socket path too long` because the check hard-codes its fixture/profile root at `Path.cwd()/.qXXXXXX`, and this worktree path exceeds the Unix socket limit. This is an environment path-length failure before any page loaded, NOT a UI assertion result, and it is NOT a pass. Per the grant it stops for Root: no retry, no source edit, no proxy. Smallest decision: allow a short-path synthetic copy run, or run the check from a shorter checkout path.
* MSSQL 22 carry-forward: only the one test-typing line differs from `2b050647b`, no runtime, dependency or SQL test input changed, so the earlier 22/0 skips/exit 0 evidence is carried forward, not rerun. Whole-suite results other than the above not rerun.
* Budget: Root-selected batch spent; conservative minimum 0; no further automatic correction.

