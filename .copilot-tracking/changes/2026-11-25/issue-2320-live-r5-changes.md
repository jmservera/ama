---
title: Issue 2320 live r5 changes
ms.date: 2026-11-25
---

Planned (implement-start): edit `src/core/src/zava_forward/core/store.py` (`Store.briefing` recording-busy fallback) and `src/api/tests/test_assistant_release.py` (one test); add research note `docs/reference/research/issue-2320-live-r5-2026-11-25.md` with probe script and JSON. Tier FULL (src change) but `rpi-checks.py --all` is not run here; the coordinator runs gates.

Done:

* `src/core/src/zava_forward/core/store.py`: `Store.briefing` returns a stale or read-only template answer (`recorded: false`, named reason) when recording hits a busy SQL write lock; other errors raise.
* `src/api/tests/test_assistant_release.py`: new busy-lock test.
* `docs/reference/research/issue-2320-live-r5-2026-11-25.md` plus probe script, JSON and screenshot.

Validation: `tests.test_assistant_release` 76 tests OK (12 skipped); `ruff check` clean in src/core; `mypy` in src/core reports 3 errors identical with and without the change (missing opentelemetry stubs, one unused ignore). Full gate not run (coordinator owns it); FULL tier is still required for the src change.

| Criterion | Status |
| --- | --- |
| 1 Profile briefing time | Proven (already ticked) |
| 2 Within 5 s, never 503 on a quiet system | Unproven live: 503s still logged on 0000069; fix not deployed |
| 3 Test proves read path does not take the write lock | Unproven in full: new test covers the busy-lock failure only; cache miss still writes |
| 4 Live re-check with elapsed times | Proven (already ticked) |
