---
title: Issue 145 live research (2026-11-24 10:26Z run)
ms.date: 2026-11-24
---

Refs #145. Task 145-live-20261124T102600Z. Research disposition: executed (opening note; findings appended below).

## Scope

Synthetic demo, desktop only, resource group `ama`. Read-only Azure SQL observation only; no restore drill, no Key Vault change.

## Prior evidence reused

* [Audit 8](../../docs/reference/research/issue-145-live-20261124-2026-11-24.md): release resurrection (R3 part) fixed; spent allowance recorded as unproven.
* [PITR restore evidence 2026-11-18](../../docs/reference/research/issue-145-live-pitr-restore-evidence-2026-11-18.md).

## Open question

R3 "spent allowance": `assistant_allowance.used_calls` and `reserved_tokens` live only in SQL, so a point-in-time restore rewinds them (resurrecting spent allowance). Check code path, then decide fix.

## Findings

* Azure read-only at 2026-11-24T10:26Z: `retrofit` Standard, Online, zone redundancy false, backup storage redundancy Local, earliest restore 2026-11-10T10:26Z, long-term retention weekly/monthly/yearly `PT0S`, databases `retrofit` and `master` only (no throwaway copy).
* `assistant_allowance(id, calls, tokens, expires, used_calls, reserved_tokens)` is SQL only (`assistants.py` DDL ~1121). `_reserve` debits it. A PITR restore returns `used_calls` and `reserved_tokens` to the earlier, lower values: spent allowance is resurrected. This is a real defect tightly coupled to criterion R3.
* `_pool` inherits MAX(used_calls)/MAX(reserved_tokens) across rows for a new authority, so closing every row also holds under token rotation.
* Per-call recording outside SQL would add a blob write to every admission (latency, new failure mode); rejected. A restore cannot know what was spent, so the safe reapply is to close the ledger.
* Planning Readiness: Ready.
