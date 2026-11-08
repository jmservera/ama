---
title: Issue 1231 r28 details, root stage-cleanup propagation
description: Phase details and acceptance for the root propagation
ms.date: 2026-11-07
---

* Phase 2 acceptance: `ranking_publication.py` keeps one `os.unlink(` call and `_remove`; `DurabilityUnconfirmedError` stays an OSError with errno and carries `stage_retained`; the Store handler order is unchanged; the README states `stage_retained` once and keeps the retry re-sync wording.
* Adopted root tests must fault the child's real stage name (leading `.`, suffix `.tmp`), and keep every existing assertion.
* Preservation: incoming non-tracking delta matches the root's delta for non-conflicting paths; `docs/reference/log.md` has zero deleted lines and keeps the root append; no existing `.copilot-tracking` path changes.
* Checks are listed in the plan; Docker, browser, MSSQL, scanners and `--all`/`--changed` are not run.
