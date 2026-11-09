---
title: Infrastructure integration topic 136 corrective C1 details
description: Phase details for the corrective C1 amendment
ms.date: 2026-11-08
---

## Amendment sections, in order

1. Identity, supersession rule: original records stay as dated history; this amendment governs current use; the original critique and Review are not edited.
2. F1 corrected 144 identity map: Git lineage observations and the session UUID kept in separate tables.
3. F2 corrected gate order, with the `src-ci.yml` trigger observation and the statement that Source CI is absent for this head.
4. F3 complete coverage table: one row per file, columns file, kind, wired from, static status, owner, unknown or approver. Nine top-level units and twenty modules.
5. Superseded statements list: original location and corrected wording.
6. Unchanged gates: five 136 criteria unmet, 440, 107 and 118 verification, named human decisions, no 144 unblocking.

## Method

* Wired-from comes from `grep` of `^module` declarations at the pinned head; status is static reading only.
* Owner defaults to the repository owner as in the README register unless a named human or role appears in a source file; unknowns are stated, not invented.
* No Bicep compile or test is run.

## Stop conditions

`origin/main` drift; any need for a test, service, Azure, private data or a non-tracking edit; wording that implies acceptance, approval, CI success or 144 unblocking.
