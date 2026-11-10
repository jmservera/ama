---
title: Issue 135 failed-import producer plan
description: Prospective plan for the importer failed-import producer, durable ledger and adapter to the existing exception queue
ms.date: 2026-11-09
---

* Task: `import-exception-135`; research `.copilot-tracking/research/2026-11-09/import-exception-135-research.md`; details `.copilot-tracking/details/2026-11-09/import-exception-135-details.md`.
* Plan written 2026-11-09T22:29Z (actual), before any source change. Divergences are recorded in the changes file.

## Objective

One local synthetic failed-import path (refused file, blocking mapping preview, rejected batch) leaves a durable record that the existing core feed and queue turn into a steward-owned `failed_import` item with the original source identity, reason and `Unknown` eligibility. Component evidence only; served detail waits for the shared hook.

## Scope

* Owned: `src/importer/src/zava_forward/importer/exceptions.py` (new), `__main__.py` (`stage`, `exceptions` subcommands), `src/importer/tests/test_import_exceptions.py` (new), `src/importer/README.md`.
* Reused unchanged: `exception_feeds.feed_failed_imports`, `ExceptionQueue`, `exception_register.staff_from_env`, the served exception screen.
* Excluded: `server.py`, `role-screens.js`, `store.py`, sqlstore, `exception_register.py`, endpoint inventory, schema, other worktrees. No replay, recovery, model call, role grant, approval fiction or private data.

## Phases

* [x] Phase 1: durable refusal ledger and `submit_file` producer (refuse, record, keep the source untouched).
* [x] Phase 2: adapter `route` (batches plus refusals into the core feed; unassigned path reported, not raised) and `exceptions` read-only CLI.
* [x] Phase 3: dedicated tests (idempotency, restart, source unchanged, role scope, no row values, no writes on view, unassigned owner).
* [x] Phase 4: importer README, shared-hook contract, targeted checks, changes, one Review.

## Validation (targeted, no blanket FULL)

* Importer unit suite (existing 39 plus new) in a fresh issue-qualified venv with `pip install -e` of core and importer.
* Core exception tests only if core is touched (it is not planned to be).
* Real local run: CLI `stage` of a synthetic bad workbook to a scratch SQLite file, a second process for `exceptions`, source hash before and after.
* No SQL Server and no browser or served-API run: the connected served path is not claimed, so the shared-heavy-resource admission is not needed and none is taken.
* Lint and type: `ruff` and `mypy` if configured in `pyproject.toml`.

## Risks

* Refusal reasons could carry row values; mitigation: sanitise duplicate-key conflict text and test it.
* Queue item ids depend on insertion order; the stable identity is the `ref` (`batch:<id>`, `file:<sha>`). Recorded as a limit.

## Shared-hook contract (pause, coordinator to serialise)

See the details file, section Contract.
