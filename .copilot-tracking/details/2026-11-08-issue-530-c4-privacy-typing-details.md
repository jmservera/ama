---
title: Issue 530 C4 chat privacy test helper typing details
ms.date: 2026-11-08
---

## Phase 2 edit contract (`src/core/tests/test_chat_privacy.py` only)

* Add `from collections.abc import Callable` and `from typing import TYPE_CHECKING, Any` and the finance-controls base pattern (`_TestCase = unittest.TestCase` under `TYPE_CHECKING`, else `object`); `class ChatPrivacyBehaviour(_TestCase)`. Runtime base stays `object`, so discovery, MRO and collection do not change.
* Declare `store: Any` and `make_store: Callable[[str], Any]` as annotation-only class attributes (no value, so no new runtime attribute and subclasses keep overriding with methods).
* Add `-> None` to every test and `setUp`, `tmp: str` on the two `make_store` overrides with `-> Any`, and `**env: str` on the `cp` helper with `-> ChatPrivacy`. Rename nothing. Module-level `cp` (the chat_privacy module alias) and the helper method `cp` stay as is; if the shadowing blocks typing the minimum is a local annotation, never a rename of public names.
* If an error needs a behaviour or assertion change, stop and report instead.
* Only if mypy still reports untyped calls from Core fixtures typed `ignore_errors`, annotate call sites; do not add overrides.

## Phase 3 checks (external caches: PYTHONPYCACHEPREFIX, RUFF_CACHE_DIR, MYPY_CACHE_DIR under `/tmp/rpi-530-c4`, `python -B`)

* Candidate venv `/tmp/rpi-530-c4/venv-cand`, editable installs of this worktree core, agents and api with the api `dev` extra; prove `zava_forward.core` and `zava_forward.api` origins under this worktree.
* `python -m mypy` in `src/api` (exit 0 required) and `python -m mypy` in `src/core`; `ruff check` in `src/core` and `src/api`.
* Unit: `python -m unittest -v test_chat_privacy` from `src/core/tests` with Core test PYTHONPATH, compared with the same run on the Main snapshot (identical verbose test ids, counts and results). Also load (not run) `test_mssqlstore.MssqlChatPrivacy` from `src/api/tests` with `ZF_TEST_MSSQL` unset and compare its collected test ids to the pre-edit candidate list (21 chat methods overall are checked later at admission); no SQL executes.
* AST proof: stripped of annotations and the typing base, the module AST equals the Main file AST; test ids and assertions identical.
* `git diff --check`, diff stat limited to this file plus original RPI records.
* Not run: API suite, SQL, browser, gate, images.

## Review route

* One authored Review, commit with repository-local noreply identity, Copilot trailer and `Refs #530`, no amend or push.
