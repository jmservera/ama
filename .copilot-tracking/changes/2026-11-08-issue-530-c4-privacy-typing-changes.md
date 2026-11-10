---
title: Issue 530 C4 chat privacy typing changes
ms.date: 2026-11-08
---

## Change

* `src/core/tests/test_chat_privacy.py` only (32 insertions, 21 deletions): `ChatPrivacyBehaviour` takes a `TYPE_CHECKING`-only TestCase base (runtime base remains `object`, matching `test_finance_match_controls.py`), annotation-only `store: Any` and `make_store: Callable[[str], Any]`, `-> None` on setUp and every test, `**env: str -> ChatPrivacy` on `cp`, `tmp: str -> Any` on both `make_store` overrides. No assertion, skip predicate, backend, public name or production code changed. No suppression, ignore or `Any` cast of a call.

## LIGHT evidence (external: `/tmp/rpi-530-c4`; caches external; `python -B` and `PYTHONDONTWRITEBYTECODE`)

* Origins (candidate venv, editable): `zava_forward.core`, `agents`, `api` resolve under this worktree `src/*/src`. An earlier non-editable api install (resolved to site-packages) was replaced by an editable install before any recorded check; its `build/` directory was relocated as below.
* API `python -m mypy` in `src/api` (the failed r1 command, candidate sources): exit 0, `Success: no issues found in 190 source files`. Main snapshot baseline same command: exit 0, 190 files.
* Core `python -m mypy`: exit 0 (268 files). Core and API `ruff check`: exit 0. Core `ruff format --check`: 215 files already formatted, exit 0.
* `python -m unittest -v test_chat_privacy` in `src/core/tests`: candidate 29 tests OK, Main snapshot 29 tests OK, sorted per-test result lines identical. `MssqlChatPrivacy` load-only (no SQL): 13 unique ids; the mixin base is `(object,)` at runtime with no `make_store` attribute.
* AST proof: after removing annotations, typing imports, the TYPE_CHECKING block and the `_TestCase` base, the module AST equals the Main file AST (`ast-equal True`).
* `git diff --check` clean.
* Relocated 4 ignored generated paths created by this task's pip installs (`src/{agents,core}/src/*.egg-info`, `src/api/src/zava_forward_api.egg-info`, `src/api/build`; 77 files) to `/tmp/rpi-530-c4/moved/` with SHA-256 multiset match (`journal-before.sha`). Worktree is ignored-clean.

## Not run

* API suite, SQL, browser, Docker, lock, gate, images. The failed r1 receipt (SHA-256 `15adeeff795d96375f186438b2f101759a8d6ecb8bf799383bdb6615dea104e8`) is unchanged and not a successful partial receipt. The 21 SQL methods and three Chromium/axe states remain unexecuted.
