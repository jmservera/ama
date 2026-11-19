# Plan: issue 1830 live r2 (2026-11-18)

* [x] Restore `tools/rpi-preflight.py`, `tools/rpi-gate-timing.py`, their two unit test files and `docs/reference/method/rpi-gate-preflight.md` from `a2c27fda6` unchanged.
* [x] Add the index line and a new log entry (append only).
* [x] Run focused tests, mypy-equivalent n/a (tools are not a `src/<project>`), `ruff check` and `ruff format --isolated --line-length 100 --check` on the new Python files.
* [x] Run the timing analyzer read-only on retained receipts; record the per-criterion proven/unproven table in the changes record and a research note under `docs/reference/research/`.
* [x] Tier FOCUSED; no `rpi-checks.py --all`; no gate file edit; no live Azure (not needed by any criterion).
