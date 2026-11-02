# Research: gate blockers from #572 (PR #756)

Disposition: executed. Planning Readiness: Ready.

* Blocker 1: `src/core/tests/test_chat_case_answers.py:64` passed `dict[str, Sequence[...]]` to a `dict[str, object]` parameter (mypy arg-type, invariance). Reproduced with `mypy tests/test_chat_case_answers.py` in `src/core`. Introduced by #752.
* Blocker 2: `case_journey_browser_check.py` snapshots `all_text_contents()` of tabs, then clicks each with `exact=True`. The AI tab label changes (`AI assistance (loading)` to a settled count) between snapshot and click, so the exact name is stale. The check passed three times on a warm local run, confirming a race rather than a deterministic failure. Three loops affected (axe scan, reflow, 200% zoom).
* Tracked `tools/__pycache__/*.pyc` already matched by `.gitignore` (`__pycache__/`, `*.pyc`) but were committed; untracking is safe.
