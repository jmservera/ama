---
title: Issue 80 capacity C4 details
description: Phase details for the C3-R1 fix
ms.date: 2026-11-10
---

## Phase 1 detail

* File: `src/api/checks/capacity_browser_check.py`, inside `hold_capacity_read` (about line 735). Before: `route.fulfill(status=503, body="Unavailable")` then `return`. After: `inject(route)` then `return`.
* `inject(route, *, status=503)` (line 228) calls `expected_failures.add(route.request)` and then `route.fulfill(status=503, body="Unavailable")`. The response and requestfailed listeners and the console filter consult `expected_failures`, so the served retry 503s are no longer reported at the `assert not failures` after the stage.
* Registration happens only inside the flag-guarded, exact-endpoint branch, so no other request is allowed.

## Evidence to record

`impl.diff`, direct exits for Ruff check and format, Node syntax, API 11, static 60 in `phase80-capacity-c4-evidence-1110/`.

## Proof limits

Focused checks do not run the browser scenario. The correction is unexercised at runtime; the delayed-401 iterations and the empty-capacity assertion remain unobserved after C2.
