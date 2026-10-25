<!-- markdownlint-disable-file -->
---
title: Issue 349 current-main integration plan
description: Plan for a non-rewriting merge and historical-claim alignment
ms.date: 2026-10-25
---

Research: ../../research/2026-10-25/issue349-tenant-readiness-preflight-main-integration-research.md
Details: ../../details/2026-10-25/issue349-tenant-readiness-preflight-main-integration-phase-details.md

* [x] Phase 1: Research (read-only).
* [x] Phase 2: Critique executed once before merge (rubber-duck): Revise. Applied: pre-merge SHA equality check (abort on mismatch); conflict inventory of log.md and rubric score files with the branch score recorded in the changes artifact rather than dropped; claims labelled owner-reported, not independently verified; timestamps and authorship preserved. No repeat critique.
* [ ] Phase 3: Merge origin/main without rewriting; resolve conflicts keeping both log entries; add changes note.
* [ ] Phase 4: Focused tests, independent review, then one full gate only if the heavy lock is free.

Constraints: draft PR stays draft, Refs #349 only, no push or self-merge, no
criteria ticked, original Conformant review and 2026-10-24 evidence untouched.
