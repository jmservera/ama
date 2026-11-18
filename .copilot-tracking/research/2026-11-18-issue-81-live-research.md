---
title: Issue 81 live research (epic safety, consent, lifecycle)
ms.date: 2026-11-18
---

Refs #81. Demo scope, FOCUSED tier, docs-only unless a source defect needs a minimal fix.

## Findings so far

* Issue #81 has two unticked criteria: the #440 stabilization checkpoint, and "all child features closed or deferred".
* Children 82 to 88 and 131 are CLOSED. Child #130 is OPEN. The #440 triage gives #81 verdict Fix, gated by #1837 (nomination form submissions return HTTP 400).
* #1837 is OPEN. Its native fix is a local, unpublished candidate (FULL tier, concurrency finding pending), so it is not in main.
* Prior #130 live notes did not retest form-encoded browser submissions. This run retests that read-mostly.
* Research disposition: executed and reused. Planning readiness: Ready.

## Live result

Form-encoded POSTs for nomination_acknowledge, nomination_correct and challenge_open each returned HTTP 400 "Could not read that." on revision 0000031 (digest 5368f4e4). Nothing was written. Evidence: evidence/2026-11-18/issue-81-live/. Published note: docs/reference/research/issue-81-epic-audit-live-2026-11-18.md.
