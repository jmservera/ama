# Issue 229 Cycle 3 correction

* Browser check register-panel control counts now exclude `button[data-jump-target]`, matching the unit tests.
* `indicatorRows` no longer emits `State: Pass` for an empty, unreadable, unrouted or roles_not_named register; it reads `Needs review` or `Action needed`.
* Tests invoke the jump `onclick` handlers (focus then scrollIntoView start) and assert the state labels.
* Validation: targeted modules (94 tests), ruff check, ruff format, mypy. Browser check not run locally.
