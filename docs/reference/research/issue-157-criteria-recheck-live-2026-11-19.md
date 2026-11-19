---
title: Per-user chat epic (#157) criteria recheck, 2026-11-19
description: Per-criterion proven or unproven record for the open acceptance criteria of epic #157 on the synthetic demo
author: AMA programme
ms.date: 2026-11-19
ms.topic: reference
---

## Scope

Synthetic demo, desktop only. Owner decisions of 2026-11-18 apply. Issue state was re-read with `gh issue view` on 2026-11-19. No Azure resource was created or changed and no credential was read. The live chat probe from 2026-11-18 is reused, not repeated: [recheck note](./issue-157-live-chat-epic-recheck-2026-11-18.md).

## Per-criterion table

| Criterion | State | Proven or unproven | Basis |
| --- | --- | --- | --- |
| Complete the #440 stabilization checkpoint | Unticked | Unproven | #440 is open. Its issue-triage criterion needs filing and owner approval of any deferral or pivot ([drafts](./stabilization-checkpoint-triage-440-live-2026-11-18.md)); its PR-artifacts criterion needs a pull request and an independent review of the coordinator change. Neither is available to a local-only task |
| If accepted, child features are accepted | Unticked | Unproven | #159, #162 and #163 are closed. #164 is open: approval of thresholds and registration of the chat task with an accountable reviewer is an owner action. #159 screen-reader testing is excluded by owner decision for the demo. Break-glass policy moved to #2129 |
| Decision accepted or epic closed | Ticked | Not reopened | ADR 0004, 2026-10-15 |
| No memory used as evidence for a controlled decision | Ticked | Not reopened | Merged #1552 |
| Chat consumption bounded and reported | Ticked | Not reopened | Merged #1547 and #1558 |

## Result

Every remaining criterion needs an owner decision or a pull request. No code or test could prove them, so no source change was made.
