---
title: AC-034 to AC-043 disposition correction 1, plan amendment
description: Amendment to the original plan for review findings R-1 to R-5, documentation only
ms.date: 2026-11-12
---

## Scope

Amends [the original plan](ac-dispositions-134-1112-plan.md) for one coherent doc-only batch answering the independent review `rpi-134-review-2220-result.json` (external, session 38e61c82). The original critique (Revise, eight findings), original review (Complete with open items) and the review's own Revise verdict stay preserved and unedited. Six partial and four deferred stay. No tick, owner approval, source change, executable gate, push, PR or issue action. A4 and E1 to E4 stay spent, E5 and E6 unadmitted; no renewal.

## Ordering disclosure

The edits to the pack and the log entry were applied in the same working session immediately before this amendment file was written, so this amendment records the intended batch and is not strictly earlier than the edit. The independent closure review below assesses the result.

## Batch

| Finding | Correction |
| --- | --- |
| R-1 | Owner cells name #134 as the only open owner; #83, #85 and #90 are labelled closed historical evidence. The reading paragraph says so |
| R-2 | AC-038 reconciles the 2026-10-17 "closure pending" wording with the #85 closing comment (independent final-head review, merged PR 388) and keeps the one JSON-only skip in each run |
| R-3 | AC-043 cites the actual probe (pack lines 7123 to 7124) and labels the #1029 and #1152 tests related isolation, not manifest coverage |
| R-4 | Drop the unanchored "eight fixtures"; name selectors 231, 231q, 231p and 231qp as selector names, not a story count |
| R-5 | The `origin/main` identity is qualified as read-time history |

The log is append-only: a correction entry is appended and the earlier entry is untouched. The README states no main identity and needs no change.

## Validation

Link and diff review only (`git diff --check`, ASCII check, anchor resolution). One targeted independent closure review by a subagent with explicit `claude-sonnet-5.5`, no second round.
