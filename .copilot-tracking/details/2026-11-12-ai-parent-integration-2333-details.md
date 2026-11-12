---
title: Details for #104 AI parent integration
ms.date: 2026-11-12
---

## P02

* `git merge --no-ff origin/main` then `git merge --no-ff e4aac8b72802f583f19eabf88e14742f68f4f653` in this worktree only. Privacy-safe repository-local identity and Copilot trailer. Verify the candidate source delta equals its own commit and no other ancestry enters (`git rev-list` of the second parent excluding main).

## P03

* Venv outside the repository, pip only: `pip install --require-hashes -r src/api/requirements.txt` if available, then `pip install --no-deps` non-editable of core, agents, api from a `git archive` of the frozen tree. `PYTHONPATH` only the test-helper directories (`tests:../core/tests:../agents/tests`).
* Tests from `src/api`: `test_assistant_release` (60 tests, expect 7 MSSQL skips), its 3 changed-material tests, `test_assistants.ApiTests.test_active_chat_memory_is_never_evidence_for_a_chat_proposal`, `test_regulatory_chat_api` (216, 12 tests).
* Static: ruff check and format check on the three touched test files; `py_compile` of the worker.

## P04

* New section appended to the existing evidence pack: candidate and parent identities separate from merged main, commands, results, adverse outcomes, caveats, limits.

## P05

* One independent read-only review of the frozen local head; findings route to later work.

## Critique dispositions (applied directly)

* C1 applied: `ZF_TEST_MSSQL` is explicitly unset (`env -u`) and the release run must show exactly 7 skips.
* C2 applied: tests and non-editable installs both come from one `git archive` of the assembled commit; record the commit, import `__file__` origins and exit codes.
* C3 applied: assert `origin/main` equals `8e6e554570f4075ff41ea130e29511455f57df2d` and HEAD equals `4459dadb4c751fcb4e1cc93d369ff844f2cbc9b7` before merging; stop on mismatch.
* C4 applied: a failed validation or material review finding blocks a successful checkpoint; adverse results are recorded without claiming validation.
* C5 applied: Python 3.12, ruff from `tools` pins if present (else the installed version is recorded and no hosted-parity claim is made); any excluded file is named.
