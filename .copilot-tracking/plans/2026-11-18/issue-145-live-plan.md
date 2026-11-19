---
title: Issue 145 live PITR plan
ms.date: 2026-11-18
---

# Plan: point-in-time restore proof on the demo SQL (Refs #145)

* Tier: FOCUSED. No `src/` edit; documentation and tracking only. No `rpi-checks.py --all`.
* [x] Phase 1: record SQL tier, backup and retention configuration read-only (az sql show, str/ltr policy).
* [x] Phase 2: restore `retrofit` to a point 15 minutes in the past as throwaway `retrofit-pitr145` (S0, Local backup storage) from the control plane.
* [x] Phase 3: from a throwaway Container Apps job (`job-145-pitr-probe`, same managed identity, in-VNet because SQL public access is disabled) read table counts and verify the audit hash chain with `zava_forward.core.ledger` plus the native ledger digest check, on source and restore.
* [x] Phase 4: reconcile restored against source audit prefix (count, head at restore point), cases, chat, sensor, assistant and resident tables.
* [x] Phase 5: delete the restored database and the job; confirm with az list.
* [x] Phase 6: write the research note with a per-criterion proven/unproven table, update the knowledge-base index and log.
* Boundaries: #114 drill (`drill114src`, `job-drill114-erase`) is not touched or rerun. No Key Vault, no production change, no secret read.
