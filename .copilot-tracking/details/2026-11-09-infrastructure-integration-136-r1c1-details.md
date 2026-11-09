---
title: Infrastructure integration 136 recovery correction R1C1 details
description: Phase details for the three bounded R1 corrections
ms.date: 2026-11-09
---

See the [R1C1 plan](../plans/2026-11-09-infrastructure-integration-136-r1c1-plan.md) and [R1C1 research](../research/2026-11-09-infrastructure-integration-136-r1c1-research.md).

* Phase 1 Amendment. Create the R1C1 amendment with three numbered corrections, the five-row unproven matrix with a link to the original topic-record matrix, and the six-file inventory.
* Phase 2 Qualifiers. Append a dated "Superseded in part by R1C1" section to the R1 plan, review and changes records. Do not alter existing lines.
* Phase 3 Evidence. Add R1C1 changes, review and state JSON. Verify the original 16 files are byte-identical to HEAD `b816656aa`, and the diff is tracking-only.
* Phase 4 Handoff. Write `handoff-136-c1.md` with HEAD, tree, current main, counts, AC matrix and a proposed PR body. Commit locally, no push.

Stop conditions: any need to edit an original file, any non-tracking path in the diff, or any unproven claim that would need a tick.
