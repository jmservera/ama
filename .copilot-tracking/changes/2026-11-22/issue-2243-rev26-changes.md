---
title: Changes for issue 2243 revision 0000026 re-verification
ms.date: 2026-11-22
---

## Changes

* Added `docs/reference/research/issue-2243-rev26-2026-11-22.md` with probes, screenshots and JSON under `issue-2243-rev26-2026-11-22/`.
* Added an index paragraph in `docs/reference/README.md` and a log entry in `docs/reference/log.md`.
* No source, Azure or SQL change. Tier: focused (docs only); hosted CI is read after the coordinator pushes.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Derive EXPIRES from `ZF_DEMO_EXPIRES_AT` | Proven | Env `2028-01-01` on rev 0000026; label no longer "exercise has ended"; merged #2249 |
| Add a test | Proven | Tests recorded in the guard note (20 plus related suites) |
| Rebuild and roll the resident image | Proven (roll), unproven (commit behind digest) | Rev 0000026 Healthy at 100%; registry firewalled |
| Resident chat answers with the model within caps | Not met | Both probe questions `reason=usage_limit` at 23:34 UTC; owner ledger action needed |

## Owner gates

* Budget ledger expiry: apply current `resident-assistant.sql`, set `resident_ai.budget.expires_at`, confirm `reserved_cents` below 2000.
* SUS-1: decide on the leftover suspension; employee chat stays rules only (0 model calls on API 0000054) until then.
