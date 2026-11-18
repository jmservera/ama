---
title: Issue 142 plan details
ms.date: 2026-11-17
---

## Phase 1

Add a loop over listed names absent from the inventory; emit `(name, "uninventoried", "secret has no inventory entry, owner, rotation interval or expiry alert")`. Output is sorted for determinism. Names only; values never read.

## Phase 2

Test: a listing with an extra secret yields exactly one `uninventoried` finding and `main` exits 1; a clean listing yields none.

## Phase 3

One sentence in the README describing the new finding. No claim that C1 to C3 are proven.
