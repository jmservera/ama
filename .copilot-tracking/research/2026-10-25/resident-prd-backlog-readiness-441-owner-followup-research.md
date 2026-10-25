---
title: Issue 441 owner follow-up research
description: Evidence for the bounded RB-17/18 versus RB-19/20 gating split and staff-promotion wording alignment
ms.date: 2026-10-25
---

## Authority and lifecycle

* Owner authorised one bounded follow-up at 2026-10-25T20:42Z after two correction cycles (issue 441 comment 6394712046 asked for it). It does not accept the PRD or backlog and does not authorise runtime release. PR 454 is OPEN and draft; the working tree was clean on branch docs/resident-prd-backlog-readiness-441.
* Local head 3e0b33ff was fast-forwarded to remote bot head d98598d7 (score JSON only). origin/main is ea5577b2 (infra, core seed merge, unrelated docs); it is integrated by non-rewriting merge.

## Defect 1: R4 gate conflation

* Backlog dependency row "RB-17 to RB-20 | RB-15, RB-01 ..., plus external OD-53 gate" applies OD-53 to all four items. RB-17 and RB-18 are blocked by RB-17 text "separate task registry entry, evaluation and release".
* PRD evidence: FR-067/AC-121 to AC-123 (resident-answer task, FR-036 registry entry, matching evaluation and release, human review default, abstention). FR-070/AC-129 to AC-131 and PR442-S17 ("S15/S16; OD-53 evidence before any positive activation"): deny-by-default dispatch, with a positive simulated-outbox test needing reconciled BRD FR-044/AC-084 and OD-53/RULE-028 policy. PRD line 1297 R4 row and PRD line 114 keep OD-53 operationally open.
* Conclusion: RB-17/18 gate = task registry, evaluation and release (not OD-53). RB-19/20 gate = OD-53 routine-dispatch policy before any positive activation; deny-by-default and per-message review negative paths need no OD-53. RB-19/20 also follow RB-17/18 (S17 depends on S15/S16).

## Defect 2: staff-promotion wording

* PRD target applicability table (staff/core evidence row): promotion of a resident file into staff evidence is a separate staff action subject to NFR-002; over-limit refused or recorded exception; only the 100 MB total counting is open.
* Proposal precedence paragraph says "any promotion of a resident file into staff evidence" stays an open engineering/owner question, which conflicts with the PRD guardrail. Backlog RB-11 says "promotion to staff evidence is separate" without the guardrail; RB-03 already includes the staff-limit check.
* Conclusion: align proposal and RB-11 to the PRD guardrail; keep the 100 MB counting question open.

## Boundaries

Unsigned PRD, unregistered proposal (id null), G0 acceptance, inherited findings, no date. Original resident-preview (444) and Azure-showcase scopes unchanged. No code, BRD, legal snapshots or memory.
