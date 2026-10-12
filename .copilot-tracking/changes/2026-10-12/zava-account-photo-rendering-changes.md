---
title: Account Photo Rendering Repair Evidence
description: Scoped necessary child implementation and validation
ms.date: 2026-10-12
---

## Scope and State

Full P01, task zava-account-photo-rendering-2026-10-12, automatic.
Research reused from parent live failure; single critique PC-001 disposed
directly. Two test additions, no removals; one existing assertion updated.
Implementation active, no decision blocker.

## P01-T01

Image-only Blob CSP implemented; two success/boundary tests added and the
existing auth CSP assertion retained/updated. Full-suite execution revealed
a second equivalent tile CSP assertion in test_ui_support.py; it is also
retained and updated as a tightly coupled current-state correction, not a
new test or semantic relaxation. The first full run had that one expected
assertion mismatch; rerun passes 286 tests with 26 existing skips.

## P01-T02

ACR db4 succeeded after 36 seconds; welcome-20261012-02 deployed.
Revision 0000004 is latest/ready, existing client and enabled token store
unchanged. Actual HTTPS Blob image check now loads the public logo at width
644 under image-only blob CSP; the same test failed in parent Review.
Public welcome 200. Browser-user-agent API request redirects to authentication;
non-browser API 401 is checked separately. No real personal photo/token used.
Published in 25b5f0f through existing #65. Guide/index updated; repaired the malformed added index
row from the earlier partial-context edit to retain the three-cell table.

## Remaining Work

P01 complete; child ready for its one Review. Exact-head 25b5f0f MVP CI
(test/image/security/SQL), MVP validation and prototype validation succeeded.
Rubric re-scoring is still running, not capstone acceptance. Parent real-user
acceptance remains separate and unavailable. Parent Review is not repeated.
ACR db4 image digest
sha256:f9651f66bcf98fbd10e5e2e84848606d88b74b8eca3c824d808a750449656a89.
Actual non-browser root/health 200 and own-photo/me APIs 401 after repair.
All local links retained: eight baseline missing targets, no new/changed
fragment defects. Preserved d72faa1 rubric bot record, score 45/100 and
unmet capstone floors remain outside this repair's acceptance.
