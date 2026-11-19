---
title: Issue 462 live r3 research
description: Opening research for a third live check of the synthetic resident showcase
ms.date: 2026-11-18
---

## Scope

Task `issue-462-live-r3`, session `rpi-462-live`. Research disposition: executed. Planning Readiness: Ready.
Tier FOCUSED: documentation and evidence only, no `src/` change.

Authority: owner decisions 2026-11-18 (synthetic demo, desktop only, live Azure in resource group `ama`, cap USD 700,
no drills, no Key Vault rotation, no production change). Billing reconciliation, DPO/Legal approval and
person-run assistive-technology tests are not needed for the demo.

## Prior evidence

* `docs/reference/research/resident-showcase-live-proof-2026-11-18.md` and `...-live-recheck-2026-11-18.md` already
  prove criteria 6 and 7 on the demo; criterion 2 (rubric on a pushed head) and the source commit behind the image
  digest stay unproven; a forward cost forecast was not produced.

## Gaps this run targets

1. Fresh browser proof of login, correct-case data and negative paths on the current revision.
2. Criterion 2: read-only `gh` evidence for #444, #455 and the rubric workflow history.
3. Source identity of the deployed image (deployment record, repo history, ACR access).
4. A forward cost estimate from actual cost data.

## Credential handling

Credentials are read at runtime by script only, never printed. The script asserts they are absent from output.
