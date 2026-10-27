---
title: Issue 441 owner follow-up plan
description: Prospective plan for one bounded owner-authorised correction batch
ms.date: 2026-10-25
---

* [x] Phase 1: Research (done before edits; see research file).
* [x] Phase 2: Independent plan critique, then apply compatible findings.
* [x] Phase 3: Backlog edits: split RB-17/RB-18 (task registry, evaluation, release gate) from RB-19/RB-20 (OD-53 gate for positive activation); fix dependency, hierarchy and RB-21/22 wording; align RB-11 promotion wording.
* [x] Phase 4: Proposal alignment of the staff-promotion sentence; check PRD, addendum and index for the same two defects (PRD expected unchanged).
* [x] Phase 5: Append-only log entry, changes record, link and diff validation, original review, state, merge origin/main, commit. No push, PR-body edit, full gate or issue creation.

## Integration and final-gate extension (appended 2026-10-25, before any change)

* [ ] Phase 6: Non-rewriting merge of origin/main c8d16059 (issue 444 resident preview merge) into 8e9b83f5. Expected conflicts only in append-only docs/reference/log.md, docs/reference/README.md index and the bot-owned rubric score file. Keep both intents; stop and report any other or ambiguous conflict.
* [ ] Phase 7: Record integration evidence (changes record appended), commit with privacy-safe identity and Copilot trailer, freeze the exact clean head.
* [ ] Phase 8: Capacity-admitted full gate: tools/rpi-checks.py --all --lock-timeout 0 to the absent directory /tmp/ama-441-owner-followup-final-gate1; official --verify-receipt against fresh origin/main. Stop after the verified local result or failure; no push, PR edit, merge, acceptance, or issue creation.

No product or requirement edit is planned. A critique is not needed: the decisions are mechanical (keep both sides of append-only files).
