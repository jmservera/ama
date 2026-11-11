---
title: Staff intake 132 C5 plan
ms.date: 2026-11-09
---

Corrective cycle C5 of five (final default). Task `staff-intake-132-c5`. Details: `.copilot-tracking/details/2026-11-09/staff-intake-132-c5-details.md`.

## Phases

* [ ] P0 Implement transition (`date -u`, state before and after), then ordinary merge of `feat/demo-quality-workflows-89-1109` (`a8593a7a`) into the own branch. No rebase, force or reset. Resolve only understood conflicts.
* [ ] P1 Red regressions on the combined tree: worker staff code, two-store interleave.
* [ ] P2 Source: `_worker` rejects any registered staff identifier; commit-time procurement read dependency adapter.
* [ ] P3 Green: focused intake tests, impacted suites on the combined tree, ruff and strict mypy.
* [ ] P4 Actual SQLite interleave, then MSSQL contract test under nonqueued owned lock. Browser only if UI changed (it is not).
* [ ] P5 One Review, changes record, docs, commit with trailer, handoff.

## Contract

* Worker identity: reject name, email, code or oid equal to ANY registered staff identity read through `store._quality_staff()`, plus the keying-in user and any value containing `@`. A staff NAME as worker stays allowed only where the existing participant resolution binds the full identity (unchanged).
* Read dependency: capture takes `store._proc_snap["procurement"]` first under `store.lock`; around `submit_quality` it installs the existing `procurement_validation` token with that snapshot and the caller's actor, refuses if a token is present, and restores the prior value in `finally`. A changed procurement row gives the existing `ConflictError`, mapped to HTTP 409 with no receipt.
* No permission, QA, consent, escalation or schema change; no edit outside 132-owned files.
