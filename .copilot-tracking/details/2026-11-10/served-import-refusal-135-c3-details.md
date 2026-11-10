---
title: Issue 135 C3 served import refusal details
description: Phase details, contracts and tests for the served import refusal projection
ms.date: 2026-11-10
---

## Phase 1 contracts

* `import_refusals.normalise` keeps only `source_name` (1 to 400), `source_sha256` (empty or 64 lowercase hex), `reason` (1 to 400), `at` (1 to 32). Anything else raises `ValueError`; unknown keys are dropped.
* `ref_of` equals the feed ref `file:<digest or source_name>`.
* `record_import_refusals(refusals)`: validates the whole batch first, then under the store lock appends refusals whose ref is not kept; first copy wins; at most 500 kept else `ValueError` and nothing recorded. When something was added: one audit entry (`recorded_import_refusals`, count only) and `save()`. When nothing was added there is no save and no audit. Returns `added`, `already_present`, `total`.
* Persistence: JSON `Store` writes `data["import_exceptions"]`; `SqlStore.DOCS` gains `import_exceptions` so it is a meta document.
* Register: `import_refusals.load(self.data)`; a damaged document is listed as unrouted and the source line stays NOT_CONNECTED. With a configured steward the refusals go through `feed_failed_imports(queue, [], steward, refusals)`, ordered by time then ref, with the refusal time appended to the reason because the existing screen does not show `at`. Without a steward the count is listed as unrouted. Source line is the connected text only when a projection exists.

## Phase 2 contracts

* `exceptions.transfer(ledger, target)` sends `_feed_refusals(ledger)` (the same shape `feed_inputs` already produced, so hashless identity stays in the name) to `target.record_import_refusals`.
* CLI `transfer DB`: opens the ledger read-only, opens the store with `factory.open_store(os.environ)`, prints counts, exit 0; exit 2 for a missing or damaged ledger or a refused store write, nothing claimed. No path comes from a request.
* README: states the transfer, the JSON-store restart caveat (stop the server first; SQLite store picks it up live), and the limits.

## Phase 3 tests

* Core: `record_import_refusals` idempotent, validation, first-copy-wins, cap, SQLite restart readback, JSON restart readback.
* Register: steward sees the item with ref, digest, time in reason, Unknown eligibility, configured owner; operator does not; manager with no names sees none; reads change no document; no transfer keeps NOT_CONNECTED; damaged document is unrouted; no steward reports the count.
* Importer: transfer of a real ledger refusal into a real Core `Store`; repeat adds none; hashless refusal stays distinct; CLI exit codes.
* Tests must fail without the connection (verified by running them against the unmodified register).

## Phase 4 commands

* Importer: `python -m unittest discover -s tests -q` in `src/importer`.
* Core: the feed, queue and new register tests; API: `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest` for `test_exception_register*`.
* `ruff check`, `ruff format --check`, `mypy` for importer; ruff for touched Core and API files per their existing config.
* Served story: local `zava_forward.api` with synthetic data, `ZF_EXCEPTION_STAFF` naming a synthetic steward, real login path used by the existing tests.
