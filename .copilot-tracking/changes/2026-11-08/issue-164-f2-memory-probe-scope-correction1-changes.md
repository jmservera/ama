---
title: Issue 164 F2 correction1 changes record
description: Implementation and focused validation record for correction1 of candidate b2f35d06
ms.date: 2026-11-08
---

Start `b2f35d066a3923c084acdc4c00f44d050d7539b2`, branch `fix/chat-eval-traceability-164`. Written after the correction1 research, plan, details and critique existed. Original records are untouched.

## Changes

* `chat_eval.py`: `SERVING_DECLARED_FALSE` ("declared not exercised: receipts declare memory_used false for every turn ... not independently observed panel consumption"); unknown text; `run_scenario` returns `turns_asked` and `execution_complete`; `memory_scope` is unknown unless every scenario ran to the end and left one receipt per turn asked and every receipt has a boolean `memory_used` (unknown takes precedence, with a declared-true count appended; `deviation` only for complete evidence); new `incomplete_scenarios`; field renamed `serving_declared_memory_used_turns`; `gate_results` falls back to unknown for an older scope lacking `incomplete_scenarios`; static open item reworded to "what receipts declare". The `bindings` policy salt is unchanged.
* `test_chat_eval.py`: the original golden, hand-built and CLI memory assertions updated to the new wording and fields; added actual cases: mixed good, constructor-failed and late-partial (probe then an unknown `before` op) scenarios; expected assertion failure stays complete; declared true with incomplete evidence is unknown; stale scope gate fallback; static text never claims observed non-consumption.
* `src/agents/README.md`: memory paragraph rewritten as receipt-declared with the unknown and deviation conditions.

## Additional cases versus the original critique

The original critique claimed constructor and partial-execution coverage; the b2f diff had only constructor-failure and no-probe cases. That claim stays as history. The actual added cases are listed above, including the first late partial-probe case.

## Validation (focused, CI-first; actual exit codes captured separately)

* Environment: `/tmp/f2-164-venv` resolves `chat_eval` to this worktree; Python 3.12.3, ruff 0.17.3, mypy 2.4.1; no package install. `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPYCACHEPREFIX=/tmp/f2c1-pyc`, ruff and mypy caches in `/tmp`. Seven pre-existing ignored directories were not touched.
* `ruff format` exit 0 (39 files unchanged after final formatting); `ruff format --check` exit 0; `ruff check` exit 0; `mypy` exit 0 (45 source files).
* `PYTHONPATH=../core/tests python -m unittest tests.test_chat_eval tests.test_chat_heldout`: exit 0, 56 tests, no skips (b2f was 53).
* The new and updated cases run against the b2f `chat_eval.py` blob: exit 1, 6 failures or errors (4 errors on missing new fields, 2 assertion failures). Source restored afterward; identities below.
* Outcome preservation: `chat_eval --json` at b2f versus now, after removing the descriptive memory fields and completion markers, compared equal; both CLI exits 0, enablement `insufficient`, task `disabled`.
* Origin/main re-read at `3c57a02d4d2ef61f6922436025b245c8a97e2694`; no rebase.
* Blob ids after the change: `chat_eval.py` fc363456, `test_chat_eval.py` 62b6ab26.
* Not run: other suites, SQL, browser, scanner, images, FULL gate, hosted CI.
