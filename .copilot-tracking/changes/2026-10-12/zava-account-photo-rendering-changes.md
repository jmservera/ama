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
Publication pending. Guide/index updated; repaired the malformed added index
row from the earlier partial-context edit to retain the three-cell table.

## Remaining Work

Complete P01. Parent real-user acceptance remains separate and unavailable.
