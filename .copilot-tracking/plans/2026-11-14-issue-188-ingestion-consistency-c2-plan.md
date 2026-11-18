# Issue #188 Cycle 2 plan

* Type helpers with `Observation`; add `live_series()` returning `list[dict[str, str]]`.
* Replace `**kwargs` with a typed local `check(rows, humidity)` wrapper passing explicit `Tolerance` arguments.
* Keep the deliberate invalid-config (tuple) and invalid-batch cases with targeted `type: ignore`.
* Cast report metrics for indexing.
* Validate: mypy, ruff check, ruff format --check, unittest.
* Critique: executed once inline; no conflicts.
