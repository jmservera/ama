---
title: Issue 80 round 6 research
description: Missing administrator, unknown-role and finance-intersection denial coverage for the form-schema CSV
ms.date: 2026-11-05
---

Research disposition: executed (gap check against current tests and source) plus reuse of rounds 1 to 5. Planning readiness: Ready. Written before any test edit in this round.

## Chronology note

The r5 records were written after the r5 implementation; they do not show an independent prior plan step. This is stated, not regraded, and the r5 records are unchanged. Round 6 writes research, plan and details first.

## Intake (verified 2026-11-05)

* Head `60a18c124ce911a82d55a17c27d265c9915acb00`, tree `57637fdbe8fb4d2963095536e1622a0b6ee78429`, status clean including ignored files (0 entries).
* Main `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`; parent `feat/case-workbench-integration-73` at `ead177ef90d24666557708ea344848a1be43bdf8`, not moved. Declaration comment 6660883728 authorizes the combined candidate.

## Gap

* r5 review recorded that administrator and unknown-role denials were not tested directly. The brief asked for both, plus a Finance actor lacking a resident or reason-view right.
* Existing form-staging tests cover signed-out, contractor and `sam` (Resident Liaison, not Finance), a reason-view environment change and SQL role revocation to Programme Support Officer (which loses reason-view). No test uses the Application Administrator role, an unregistered role, or a Finance role lacking resident-record rights.

## Source facts

* `projection.allowed` gives the Application Administrator only the `me` kind, so the export is refused by the route kind check before the store call. An unknown role is not in `STAFF_ROLES`, so it is refused the same way.
* `forms._actor` independently requires `FINANCE_VIEW`, `RESIDENT_VIEW_ROLES`, `can_see_reason` and document read. `Grants and Evidence Officer` is in `FINANCE_VIEW` and passes the route kind check but is not in `RESIDENT_VIEW_ROLES`, so it reaches `list_schemas` and must be denied there.

## Scope

Tests only, using real HTTP, real login and the real role helpers; staff for the extra roles are registered in the synthetic store the way existing fixtures do. No production, core, UI or dependency change unless a test reproduces a real bug, in which case the failing evidence is kept and only a minimal guard fix is allowed. No heavy gate, browser or SQL server (#96 holds the lock).
