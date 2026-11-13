---
title: Issue 358 close-out plan
ms.date: 2026-11-13
---

## Plan

* [x] Phase 1: Verify expiry guard test and mutation (replacing the `endDateTime` clause with `False and` fails 58 tests; adding `or True` to the `> now` comparison fails the expiry tests; ad hoc runs, restored).
* [x] Phase 2: Verify Key Vault preservation tests and read-only live inspect (secrets null, names and flags only).
* [x] Phase 3: Verify delegating `main()` and run targeted tests, mypy.
* [x] Phase 4: Commit evidence only; no push, no issue edits.

Details: `.copilot-tracking/details/2026-11-13/358-close-entra-kv-1554-details.md`
