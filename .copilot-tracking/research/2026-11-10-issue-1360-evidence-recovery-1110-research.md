---
title: Issue 1360 evidence recovery research
ms.date: 2026-11-10
task_id: 1360-evidence-recovery-1110
---

## Scope

Evidence recovery only, at frozen head `c7d570c8b89adab76a6402bd29c0cee215ab0233`. Not a new extension, not E2, no source change. Planning Readiness: Ready.

## Root clarification (independent42ad, functional approve, publication blocked)

* Retained `ruff-check.log` shows E501 at `tests/test_import_exceptions.py:643`; the final source differs (the docstring was shortened afterwards). No final green rerun is retained.
* No retained core mypy log, no raw red-run output, and no baseline-versus-current core formatter output.
* The original handoff claims stay as historical author claims and are not rewritten.

## Approach

Fresh exact-head runs with commands, exit codes, module origins, head and base recorded in an external evidence directory: importer ruff check, ruff format check, mypy and tests; core mypy; core ruff check and format check of the changed files. For the core formatter claim compare current `sqlstore.py` against the base version using scoped temporary copies outside the worktree. The original red cannot be reconstructed as original; a new labelled diagnostic may run the two committed-case tests against a temporary copy with the old one-line tuple. Unprovable claims are retracted. A required source correction stops to Root, with no automatic E2.
