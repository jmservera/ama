---
title: Issue 435 research, capstone pitch status reconciliation
ms.date: 2026-11-17
---

## Scope

Refs #435. Focused tier, documentation only. Base origin/main eb51af5c9. Disposition: executed (bounded measurement of existing artifacts). Planning Readiness: Ready.

## Measurements (2026-11-17)

* Issue acceptance list ticks criteria 3, 5, 6 (comment: PR 1566 proved them); criteria 1, 2, 4 open.
* All relative links in docs/capstone/pitch/*.md, docs/capstone/tokenomics-qa-brief.md and docs/capstone/README.md resolve (script check, zero broken).
* docs/capstone/pitch/tokenomics-placement-draft.md status table still says criteria 3, 5 and 6 are "Unmet" and "No revised deck exists", although capstone-assessment-challenge.md (criterion 5), the 2026-11-12 statement audit and Q&A brief (criterion 6) exist on main. Stale.
* docs/capstone/pitch/README.md says the rehearsal notes "hold the unperformed 15-minute run sheet".
* tokenomics-rehearsal-notes.md Rehearsal Record is entirely blank and states no rehearsal was performed; criterion 3 requires a rehearsal inside the timed route. The issue tick for criterion 3 is therefore not supported by repository evidence (adverse finding, preserved, not resolved by fabricating a record).
* Criterion 1: owner placement decision recorded 2026-11-13; no deck rebuild claimed. Criterion 4: owner authorised up to USD 5.00; batch adapter on main, no live run. Criterion 2: no mentor confirmation.

## Findings routed

* F1 Fix stale statuses in the placement draft (criteria 5 and 6 point to delivered artifacts; criterion 3 stays open per blank record).
* F2 Add a regression test that pitch docs links resolve and the draft does not contradict the delivered artifacts.
* F3 Criterion 3 tick needs human reconciliation (presenter rehearsal or untick); no change to the issue made here.

Unmet or unproven: 1 (deck rebuild), 2, 3 (no performed rehearsal), 4 (no run).
