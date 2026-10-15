---
title: Research - assistant test sandboxes committed in PR 287
---

* Evidence: `git ls-files 'mvp/.assistant-test-*'` returned 450 files (225 directories, each `cases.sqlite` and `seed.json`).
* Source: `Base.setUp` in `mvp/tests/test_assistants.py` created `Path.cwd() / ".assistant-test-<uuid>"`, inside the repository when run from `mvp/`. Cleanup lived in `tearDown`, which does not run when `setUp` fails or the run is interrupted. `release_support.py` does not create sandboxes.
* A full run on the tracked tree left `git status` clean, so the 225 directories were leftovers from failed or interrupted runs.
* Baseline on main: 719 tests, OK (skipped=92).
* Planning Readiness: Ready.
