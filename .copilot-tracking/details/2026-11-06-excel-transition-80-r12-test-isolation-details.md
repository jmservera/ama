---
title: Issue 80 r12 details, harness test isolation and current preservation proof
description: Phase details for the test-only isolation, README correction and external proof
ms.date: 2026-11-06
---

* Plan: [plan](../plans/2026-11-06-excel-transition-80-r12-test-isolation-plan.md). Research: [research](../research/2026-11-06-excel-transition-80-r12-test-isolation-research.md).

## Phase 1: test isolation

* File: `src/api/tests/test_browser_harness_scratch.py`, test `test_default_scratch_parent_is_unchanged`.
* Wrap the call in `tempfile.TemporaryDirectory()` and `patch.object(harness, "ROOT", Path(tmp))` alongside `patch.dict(os.environ, {}, clear=True)`. Assert `scratch_parent() == Path(tmp) / ".venv"`.
* Verify before the edit that the actual checkout `.venv` is the pre-existing empty directory (not created by this test); after the edit, run with a pre-removed condition is NOT possible (no deletion), so verify isolation by asserting the real `ROOT` directory listing and `.venv` stat (mtime, inode) are unchanged across a test run.

## Phase 2: README

* File: `src/api/README.md` paragraph at the shared browser harness note. State: default scratch under the repository `.venv`; absolute `ZF_BROWSER_SCRATCH` outside the checkout overrides it; `PYTHONDONTWRITEBYTECODE` and `PYTHONPYCACHEPREFIX` are passed to the server child when set.

## Phase 3: focused checks

* From `src/api`, `PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=<external>` with `python -m unittest tests.test_browser_harness_scratch`, plus Ruff check, Ruff format check and mypy on the test, caches external, direct exits with pipefail.
* Byte identity: `git diff --stat 5fa44964 -- src/*/src src/api/checks` must be empty for all five packages' src trees, the harness and the schema check.

## Phase 4 and 5

* Changes and state JSON validated (json.load, links, `git diff --check`) before the final Review. Review commit is separate and later.
* After the last commit, build the external proof described in the research under a new `/mnt/ama-gates/e80-r12-r65-1106` with refuse-overwrite; handoff external; pending manifest finite and bound to HEAD, tree and archive hashes.
