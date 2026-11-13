# Research: tools/ unit test verification at 74a93a137a (Refs #470, #1204, #1297)

Research disposition: executed. Planning Readiness: Ready.

## Context read

* docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/reference/README.md and docs/reference/memory.md read or sized at start (memory is context, not evidence).
* HEAD is 74a93a137a983e0a87418e3321a6847ba9bcd278, worktree clean.

## Test modules under tools/

* test_ama_worker_watch.py, test_backlog_sync.py, test_check_demo_feedback.py, test_check_design_trace.py, test_ci_affected.py
* test_climate_paired_blocker.py, test_climate_paired_bounds.py, test_climate_station_bounds.py
* test_install_actionlint.py, test_rpi_checks.py, test_rpi_phase_witness.py, test_tracking_retention.py
* rename-zava-tests.py (Zava migration regressions)

## Side-effect screen (grep, no execution)

* No test references docker, playwright launch, or gh issue/project writes. test_backlog_sync.py patches mod.gh with a fake.
* test_rpi_checks.py mentions chromium/playwright only as command strings, mocked runner.install_chromium, patched gate.heavy_lock and patched urlopen; no real install or lock expected.
* test_install_actionlint.py uses a fake network object for urllib requests.
* test_check_demo_feedback.py references socket/http only in a forbidden-import assertion.

## Risks

* Tests may write caches or bytecode: mitigate with PYTHONDONTWRITEBYTECODE=1, then git status --short for untracked files.
* Some modules may need src/ packages: if import fails, record it as a result, do not edit.
* Run each module with python3 -m unittest, capture exit code directly.
