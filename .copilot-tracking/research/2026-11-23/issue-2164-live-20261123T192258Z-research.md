---
title: Research for issue 2164 live r9
ms.date: 2026-11-23
---

## Scope

Issue #2164: roster-bound Entra staff must inherit roster scope in `assistants.authorize`; tests for `view_only` and scope bypass. Research disposition: reused (r1 to r8 notes: fix 6a03928ccb on HEAD, deployed in the live replica).

## New angle

Existing test `test_bound_entra_staff_inherit_roster_scope_and_revocation` covers scope, role/disabled/active/oid change and row deletion. Uncovered branches of the bound path in `assistants.authorize` (src/core/src/zava_forward/core/assistants.py):

* bound principal carrying `view_only` (check precedes the roster re-read);
* roster row tenant mismatch (denied) versus empty tenant (legacy, allowed);
* malformed roster scope on the re-read row (denied);
* token whose `bound.email` differs from its `email` (forged, `identity.verified` rejects);
* area-scoped row that includes the case area (allowed).

Planning Readiness: Ready. Owner-only items (live roster edit) skipped; no src change expected.
