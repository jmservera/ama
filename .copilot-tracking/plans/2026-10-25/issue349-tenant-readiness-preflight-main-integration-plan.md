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
* [x] Phase 3: Merge origin/main without rewriting; resolve conflicts keeping both log entries; add changes note.
* [x] Phase 4 (review done; gate below): Focused tests, independent review, then one full gate only if the heavy lock is free.

Constraints: draft PR stays draft, Refs #349 only, no push or self-merge, no
criteria ticked, original Conformant review and 2026-10-24 evidence untouched.

## Amendment A1 (made after the merge exposed a concrete contract discrepancy)

Focused test test_contract_matches_runtime_role_maps fails on the merged tree:
main added ApplicationAdmin to the manifest (13 roles) and the runtime exposes it
as the ADMIN_ROLE constant in src/api auth.py, outside DEFAULT_ROLE_MAP and
RULE_ROLE_MAP. Planned minimal change: the test also reads ADMIN_ROLE and expects
13 roles. Test-only; checker unchanged. Not a repeat critique: within the
critiqued scope (align tests only on a concrete current contract discrepancy).

Research note: the research expected no test change; A1 supersedes that expectation. The research text is preserved as written.
