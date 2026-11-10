---
title: Issue 73 served parent integration - phase details
ms.date: 2026-11-10
---

## Conventions

* Scratch: /tmp/issue73-1110-scratch (logs/ subfolder). Venvs: FULL=/tmp/issue73-1110-venv-full, NOSQL=/tmp/issue73-1110-venv-nosql, both editable from this worktree.
* Every command's exit code and skip count is recorded in the changes record. Fixtures are synthetic; ZF_DATA is always an explicit temporary file.

## P2 merge

* `git merge --no-ff origin/main` (pinned 4244e84e) with a message naming the pin. Expected: automatic merge with no conflict. If a conflict appears, resolve only the conflicting hunks preserving both intents and append-only logs.

## P3 commands

* V1 (cwd src/core, FULL): `python -m unittest discover -s tests -q` is the whole Core suite and is the primary run; focused subset first: `python -m unittest test_discovery_assistant_demo test_import_refusals test_exception_feeds test_exception_queue test_sqlstore test_governance -q`.
* V2 (cwd src/importer): `python -m unittest discover -s tests -q` in FULL and in NOSQL.
* V3 (cwd src/api, FULL): `PYTHONPATH=../core/tests:../agents/tests python -m unittest test_exception_register test_exception_register_screen test_role_screens test_role_screens_conformance test_workspace_scripts test_workbench -q` (module names resolved from tests/), then the whole API discover if time permits.
* V4: `python -m zava_forward.core`; `... discovery-demo`; `... discovery-demo extra`; `python -m zava_forward.importer --help` and the stage/transfer subcommands against a temporary SQLite and synthetic workbook created by the tests' own builders.
* V5: copy of the child's run-mssql approach adapted to this worktree and FULL venv: flock -n heavy lock, one container labelled zf.task=73-served-parent-1110, manifest via core/tests/sqlguard, `ZF_IMPORT135_MSSQL=1 python -m unittest test_import_refusals -v`; remove only that container; image kept.
* V6: Playwright against a local server on a free loopback port with temporary ZF_DATA (SQLite and JSON), synthetic sign-in; steward register shows the failed import with Unknown eligibility, operator does not, restart persistence, repeat transfer idempotent. Remove .playwright-mcp or browser artefacts.
* V7/V8: `ruff check . && ruff format --check . && mypy` in each of src/core, src/importer, src/api (FULL); src/core and src/importer in NOSQL; `python -c "import mssql_python"` must fail in NOSQL.
* V9: `python -m unittest test_dependency_rule -q` in each project; witness `verify` at the end.

## Evidence

* Changes record lists merge parent hashes, tree hash, each command with exit and counts, skips with reasons, container id and image digest, and runtime identities.
