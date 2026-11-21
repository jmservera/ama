---
title: Issue 1258 live changes (2026-11-21)
description: Changes and per-criterion table for the 2026-11-21 pass
ms.date: 2026-11-21
---

Tier FOCUSED. No src change, so no full tier; `rpi-checks.py` not run. Refs #1258.

## Changes

* Added `docs/reference/research/issue-1258-live-r6-2026-11-21.md`, one README index line and one log entry.

## Validation

* 146 tests in four ranking modules, OK. Mutation check: removing the parent sync failed ten `AncestorDurabilityTests`; src restored, no diff.
* Not run: full suites, `rpi-checks.py`, hosted CI (no push).

## Criteria

| Criterion | Status |
| --- | --- |
| 1 Sync ancestors before confirming | Proven (code, unit) |
| 2 Post-link failure is `committed_unconfirmed` | Proven (unit) |
| 3 Syscall-order regression failing before the fix | Proven (unit, mutation) |
| 4 Existing behavior intact | Proven (unit, 146 tests) |
| 5 FULL receipt, independent review, hosted checks | Unproven: needs forbidden `--all` gate, a pushed head and hosted CI; mocks do not prove real crash durability |
