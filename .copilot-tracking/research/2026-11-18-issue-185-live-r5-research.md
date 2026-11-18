---
title: Issue 185 live re-verification research (round 5)
description: Opening research record for re-verifying the two unticked criteria of issue 185 on the synthetic demo
ms.date: 2026-11-18
---

Refs #185. Disposition: reused plus executed. Planning Readiness: Ready.

## Scope and decisions

* Synthetic desktop demo; live Azure authorised (group `ama`, cap USD 700, no drills, no Key Vault rotation, no production changes). Billing reconciliation, DPO/Legal approval and person-run AT testing are not needed.
* Unticked criteria: (3) credentials issued and stored without appearing in source or logs; (4) teardown removes all simulated identities.
* Tier: FOCUSED, docs only. No `src` change, so no FULL gate and no `rpi-checks.py --all`.

## Existing evidence (reused)

* [Three live runs](../../docs/reference/research/issue-185-live-device-identity-evidence-2026-11-18.md) and the [fourth audit](../../docs/reference/research/issue-185-live-r4-audit-2026-11-18.md) already prove issuance, no-leak and in-job teardown with an adverse hub-count observation that the audit later closed.

## Gaps to close this round

* Re-read the live hub state now (device count, network and auth settings, leftover jobs and role assignments).
* Re-run the repository credential hygiene scan and the targeted tests, retaining output.
* Decide whether a new live identity run is needed: not unless the hub-wide count is non-zero or the retained log is missing; a fresh run on a shared hub risks the id collision seen in run 3.
