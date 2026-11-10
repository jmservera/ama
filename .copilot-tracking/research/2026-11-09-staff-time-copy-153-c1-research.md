---
title: Issue 153 C1 project mypy failure research
ms.date: 2026-11-09
task_id: 153-c1-project-mypy-1109
---

## Scope and disposition

Correction cycle C1 of 5 for #153 on the same branch, head cc77ea457. Research executed 2026-11-09T23:35Z. Planning Readiness: Ready.

## Evidence

* Hosted failure: run 42719465214 (job src-api, step Type check, 2026-11-09T23:29Z), `cd src/api && mypy`: six `no-untyped-call` errors at `tests/test_timecapture_copy.py` lines 192, 194, 195, 197, 198, 252; 204 source files; Python 3.12. Excerpt: `/tmp/zf-153-1109/logs/c1-hosted-failed-excerpt.log`.
* Local reproduction with the exact project command from `src/api` in the worktree venv `/tmp/zf-153-1109/venv` (Python 3.12.3, mypy 2.4.0 as pinned by the `pyproject.toml` dev extra): identical six errors, exit 1 (`logs/c1-mypy-red.log`).
* Cause of the earlier miss: the first check was `mypy tests/test_timecapture_copy.py`, a single-file run that does not use the project `files` and override context. No proxy equivalence is claimed.
* Project config (`src/api/pyproject.toml`): `strict = true`; `follow_imports = "skip"` plus `ignore_errors` for a named module list that includes `zava_forward.api.timecapture`, `zava_forward.api.server` and `test_mvp`. Their untyped constructors and methods (`TimeCapture.__init__`, `request_enable`, `activate`, `acknowledge`, `mine`, `App.__init__`) are untyped callables and trip `disallow_untyped_calls` in a typed test.
* Existing repository pattern for typed tests calling untyped legacy classes: a line-scoped `# type: ignore[no-untyped-call]` (for example `tests/test_case_journey.py:559`, `tests/test_employee_live_responses.py:34`, `tests/scale_load.py:102`). A module-level override exists only for two continuity test modules.

## Options

* Line-scoped specific-code ignore at the six calls: matches the existing pattern, no config or legacy-module change, and strict `warn_unused_ignores` keeps each ignore honest.
* Annotate the legacy `TimeCapture` and `App` methods: widens type scope into backend modules outside ownership that are currently excluded.
* Config override for the test module: loosens mypy configuration; excluded by owner direction.
* `cast(Any, ...)` or rewriting setup through HTTP only: excluded, or a large unrelated rewrite.

## Recommendation

Line-scoped `# type: ignore[no-untyped-call]` on exactly the six reported lines, behaviour unchanged. No JS change, so no fresh web review is required beyond the existing guidelines review (fetch sha256 d246b026, 2026-11-09T22:54Z).
