# Changes: issue 233 stage map drift check

* `src/core/src/zava_forward/core/atlas_screen_trace.py`: `stage_map_drift`, wired into `check` when the role screens source is supplied.
* `src/core/tests/test_atlas_screen_trace.py`: published map matches; drift, rename and missing map reported.
* `docs/reference/research/ux/atlas-screen-trace.md`, `docs/reference/log.md`: note and entry.
* Validation run: core atlas tests (17 OK), checker CLI complete, ruff check and format, mypy strict (/tmp/mypy-233). Not run: gate, full suites, benchmarks, rendered or assistive-technology checks.
