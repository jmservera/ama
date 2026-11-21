# Details: issue 2187

Phase 1: `tools/rpi-checks.py`, add `needs_heavy_lock` before `heavy_lock`; branch in `main()` at the `with heavy_lock(...)` site.
Phase 2: `tools/test_rpi_checks.py`, add tests next to the existing heavy-lock tests (`GateTests`).
Phase 3: check `src/README.md` for lock wording; adjust only if it claims an unconditional lock.
Validation: `python3 -m unittest tools.test_rpi_checks` selected cases, `python3 -m ruff check` and `ruff format --isolated --line-length 100 --check` on the tools files.
