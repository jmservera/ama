---
title: Issue 135 C3 served import refusal plan
description: Plan to project one refused import record into the existing scoped exception register
ms.date: 2026-11-10
---

* Continuation C3 of five (two remain afterwards). Plan recorded 2026-11-10T03:46Z. Details: `.copilot-tracking/details/2026-11-10/served-import-refusal-135-c3-details.md`.

## Phases

* [x] Phase 1: Core projection and register connection (`import_refusals.py`, `exception_register.py`, `store.py`, `sqlstore.py` DOCS).
* [x] Phase 2: Importer adapter and `transfer` command; README.
* [x] Phase 3: Focused regressions (Core persistence for JSON and SQLite, register scope, idempotency, importer transfer, CLI) that fail without the connection.
* [x] Phase 4: Targeted validation: importer suite, Core feed/queue/register tests, API register and screen tests, ruff, format, mypy; actual local served refusal, detail, restart and idempotent readback story with SQLite and JSON stores.
* [x] Phase 5: Single critique, single Review, changes record, handoff, frozen local commit.

## Success criteria

* One synthetic refused file in the importer ledger appears in `/api/exceptions` for the configured synthetic steward after a store restart, with stable ref, digest where known, reason, time, Unknown eligibility and configured-not-appointed owner.
* A second transfer adds nothing and changes no stored document; reads add only access audits.
* Operator-only, unnamed manager, unnamed and unauthenticated callers remain denied or empty as before.
* Unconfigured or damaged projection stays NOT_CONNECTED or reported unrouted.
* No API import of the importer, no new route, permission, role, model, replay or recovery action; the ledger and source file are unchanged.

## Dependencies and stops

* No dependency on quality, procurement, aftercare or concern code. Stop and report if one appears.
* SQL Server is not available for claim; persistence is claimed only for the stores actually run.
