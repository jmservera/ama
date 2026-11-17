# Issue 1818 c2 research

Disposition: executed. Planning Readiness: Ready.

PR #1826 `src-api` mypy fails on `src/api/tests/test_map_sensors.py`: override of `Seed.put` drops `consent`, `home`, `offset` positionals (line 18); `ApiTests.request` is untyped (lines 22, 34); returning Any (line 25).
Base `Seed.put(count, consent, home, offset, **kw)` in `test_quality_sensors.py`.
