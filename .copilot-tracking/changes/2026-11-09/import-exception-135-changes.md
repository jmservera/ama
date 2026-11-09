---
title: Issue 135 failed-import producer changes
description: Implementation record, divergences and validation for the importer failed-import producer
ms.date: 2026-11-09
---

* Implementation started 2026-11-09T22:30Z after the single critique (22:30Z); recorded 22:33Z (actual times).
* Base `a04668ae94b5c2f38e6c55ed789db245e8c71d16`.

## Changes

| File | Change |
| --- | --- |
| `src/importer/src/zava_forward/importer/exceptions.py` | New: `RefusalLedger` (`import_refusals`), `submit_file`, `feed_inputs`, `route`, allowlisted reason builders |
| `src/importer/src/zava_forward/importer/__main__.py` | `stage` and read-only `exceptions` subcommands |
| `src/importer/tests/test_import_exceptions.py` | 20 new tests |
| `src/importer/README.md` | Capability, limits and boundary, `ms.date` |

## Divergences and amendments

* Critique amendments applied as recorded: hash-keyed ledger ref, reason allowlist, local diagnostic CLI, race handling, bounded fallback hash.
* Divergence from plan: the scanner refuses a non-workbook as a content-scan mismatch before the xlsx reader, so the CLI path reports that reason; the structural reader refusal is covered by the generic phrase only.
* Not changed: `exception_feeds.py`, `exception_queue.py`, `exception_register.py`, api, store, schema, screen, other worktrees.

## Validation actually run (venv `/tmp/issue135-import-1109-venv`, `pip install -e src/core src/importer`, ruff 0.17.1, mypy 2.4.0)

* Baseline importer unit suite before change: 39 tests OK.
* After change: 59 tests OK (39 existing plus 20 new), including the dependency-rule test.
* `ruff check`, `ruff format --check`, `mypy` (strict): pass after one correction cycle (E501 and optional narrowing). Cycles used: 1 of 5.
* Real local run: CLI `stage` of a synthetic bad file twice in two processes (exit 1, one ledger row), `exceptions` in a third process shows one `EX-001 failed_import` with eligibility `Unknown`, source name and hash; database and source file hashes identical before and after viewing. Without `ZF_EXCEPTION_STAFF` the item is reported as unrouted and the owner as Unassigned (Unknown).
* Not run, with reasons: core and api suites (no core or api file changed); SQL Server and browser or served API (served path not claimed, no shared-heavy-resource admission taken); blanket FULL gate (not applicable to this tier).

## Limits

* Component-only and partial. The register, served screen and `GET /api/exceptions` do not show these items; the register still says failed imports are NOT_CONNECTED.
* Queue item ids (`EX-nnn`) depend on read order; the stable identity is the item `ref`.
* The feed drops `structure`, `data_label` and `version` for refusals; they live in the ledger and `Routing` only.
* `src/core/README.md` still says the importer producer is not built; it is a core-owned doc and was not edited.
