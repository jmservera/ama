---
title: Issue 79 plan, r24 directory-sync audit correction
ms.date: 2026-11-07
---

Planning readiness: ready. Critique: one author-only prospective critique (not independent), below, before any test or source edit.

## Plan

* Phase 1: commit research, plan, details.
* Phase 2 RED: add a core test (directory fsync fails after link) and a Store/API test; run them and keep the failing output.
* Phase 3: `DurabilityUnconfirmedError(OSError)` raised by `publish` when only `_fsync_dir` fails; Store audits `ranking_snapshot_publication_unconfirmed` under the actor with policy, signed state, as-of and hash, then raises; API maps it to 409.
* Phase 4: GREEN, Ruff, mypy, Changes, Review, log entry, commit.

## Acceptance

* The final file stays, owner-only mode and no-replacement behaviour are unchanged, the stage temp file is removed.
* Audit contains exactly one unconfirmed entry (not `published`, not `already_published`) and the chain verifies; the API response is 409 with no filesystem path or error text.
* If the audit write also fails, the failure is logged and surfaces (no success-shaped fallback).
* Existing 53 core and 15 API tests still pass.

## Critique

* Subclassing `OSError` keeps the runner path unchanged but could be caught by an `except OSError` that treats it as a plain failure; the Store catches the subclass first. Catching only the subclass avoids a broad catch.
* Do not claim confirmation: the event name and message say unconfirmed. Not rolling back is deliberate.
* Retry durability confirmation stays a residual. No change to policy, quotas, SQL, dependencies or workflows.
