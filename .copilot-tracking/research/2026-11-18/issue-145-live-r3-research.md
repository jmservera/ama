---
title: Issue 145 live run 3 research
ms.date: 2026-11-18
---

## Scope

Refs #145. Run 3 against the demo (resource group `ama`, cap USD 700, no drills of production, no Key Vault rotation). Prior runs: r1 (restore, raw output not retained) and r2 (read-only). Gap to close: retain raw probe output for a fresh point-in-time restore, re-check ledger verification, retention vs #121, reconciliation and resurrection. Identifiers redacted in all evidence.

## Prior evidence read

* `docs/reference/research/issue-145-live-pitr-restore-evidence-2026-11-18.md` (r1)
* `docs/reference/research/issue-145-live-run2-reverification-2026-11-18.md` (r2)
* State files r1/r2 are not modified; r3 state is `issue-145-live-r3-state.json`.

## Method (planned)

Restore `retrofit` to a throwaway database, run a throwaway Container Apps job (existing orchestrator image and managed identity) that prints counts, chain verification, native ledger verification attempt and the release/allowance table contents, capture raw logs, delete both.

Planning Readiness: Ready.
