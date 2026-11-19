---
title: Issue 107 release-invariant classifier correction plan
description: Plan for the single remaining High classifier finding at 0b90a5d
ms.date: 2026-11-17
---

## Objective

After a completed supported mismatch execute/reinvoke, the judge must require non-active affected release rows in every post-worker snapshot regardless of `prompt_version`; unreadable required state is INSUFFICIENT.

## Phases

* [x] Phase 1 Failing-first regressions in `src/api/tests/test_old_image_sql_probe.py`: active MUTATED row after the mismatch worker; each affected approval restored only in `after_remaining` or only in `after_larger`; lost release row is INSUFFICIENT. Run them in an external venv and retain the failing log.
* [x] Phase 2 Judge change in `src/api/checks/old_image_sql_probe.py`: bind release IDs from `after_provision`, one release-state helper, replace the exemption, audit later snapshots.
* [x] Phase 3 Directly coupled README sentence, then focused test batch, Ruff, format, strict mypy, labelled SQLite self-test.
* [x] Phase 4 Review once, commit locally.

## Non-goals

No application, store, policy, network, lifecycle, budget, schema, dependency or gate change; no new abstraction beyond one small helper function.

## Evidence boundary

Fakes and SQLite only. No actual Docker, SQL or old-image execution. FULL tier retained.
