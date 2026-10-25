---
title: Resident PRD and backlog readiness changes record
description: Changes, overlap reconciliation and divergences for issue 441 readiness slice
ms.date: 2026-10-25
---

## Changes

* PRD v0.21.0: NFR-021, AC-139, applicability and precedence section, delivery sequencing and first milestone, checklist, OQ-030/031, version history.
* Aligned: unregistered proposal, addendum, residents journeys note, KB index row, append-only log entry.
* Created: draft backlog (RB-01 to RB-24, governance items), research, plan, details, critique, review, state.
* Unchanged: BRD, original case study, legal snapshots, owner memory, src, infra, ADR registry.

## Overlap reconciliation (checked 2026-10-25, origin/main 5d79aaee)

| Item | Head | Shared paths | Result |
| --- | --- | --- | --- |
| PR 424 | a74652aa | docs/reference/README.md, log.md | Index/log merge conflicts possible; no PRD/BRD overlap |
| PR 426 | 419857b4 | README.md, log.md, ADR 0002 | As above; ADR registry untouched here |
| PR 439 | 3648875e | addendum, README.md, log.md | Addendum ms.date and text lines may conflict; rebase at publication |
| Issue 444 | local a3e527fd, unpushed | README.md, log.md, code | Reused, not duplicated |

Recheck is repeated immediately before publication.

## Divergences

* Candidate edits preceded the critique artifact (non-interactive run); disclosed in the critique.
* Pre-existing broken relative links in the addendum and log (capstone assets, mvp anchors) were not fixed (out of scope).

## Correction cycle 1 (2026-10-25)

* PRD: Staff/core applicability row narrowed to staff-audience requests; added unlisted resident class, staff-limit check on promotion, 5 MB unit note, open sample-definition items; header and Last Updated aligned to 0.21.0.
* Backlog RB-03 lists the new open items. Index unchanged; log entry appended.
* Prior commit 2b3f6715 and its receipt (/tmp/rpi-441-gate-1792892963) are retained; they do not cover the new commit. The first gate attempt ended BLOCKED on the global heavy lock timeout, not a functional test; the retry passed.
