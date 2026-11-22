---
title: Issue 440 post-demo deferral wording for criteria 7 and 8 (draft, 2026-11-22)
description: Draft replacement text for the issue 440 body that defers its two unticked criteria until after the synthetic demo, with the evidence that each cannot be proven now
ms.date: 2026-11-22
ms.topic: reference
---

Scope: synthetic demo, desktop only. Refs #440. This note is a draft for the owner. The GitHub issue was not edited, no issue was filed, no source changed and no Azure resource was touched. Owner approval is required for a deliberate deferral, so the wording below is a proposal and not a recorded decision.

## Why the two criteria cannot be proven for the demo

| Criterion | Blocking fact | Evidence |
| --- | --- | --- |
| 7 Triage into issues, gate epics, owner approval | Drafts D1 to D4 and the epic gating exist, but the criterion needs filed issues and owner approval of requirement changes, pivots and deferrals. A worker cannot supply owner approval, and D1 touches SQL, which takes the full validation tier. | [2026-11-18 triage](./stabilization-checkpoint-triage-440-live-2026-11-18.md), [2026-11-19 refresh](./issue-440-live-checkpoint-refresh-2026-11-19.md) |
| 8 Research, plan, changes and independent review artifacts in the PR; Major HVE Builder review | Needs a pull request, which the coordinator publishes, and a reviewer other than the author. The coordinator behaviour change is outside the demo work. | Same two notes |

## Proposed replacement for the two unticked criteria

Replace the two unticked lines in the issue body with the following. Keep both boxes unticked.

```markdown
- [ ] Triage confirmed findings into deduplicated, independently scoped RPI bug/refactor issues with severity, reproduction, requirement/ADR links, acceptance criteria and explicit dependencies. Gate affected epic closure/dependent feature expansion on blocking findings only; independent work continues. Owner approval is required for requirement changes, architectural pivots and deliberate deferrals.
  Deferred until after the demo (proposed 2026-11-22, awaiting owner approval). Drafts and epic gating are recorded in docs/reference/research/stabilization-checkpoint-triage-440-live-2026-11-18.md and refreshed in issue-440-live-checkpoint-refresh-2026-11-19.md. Filing the issues and recording the owner decision remain open. Not passed.
- [ ] Deliver genuine research, plan/details, changes and independent review artifacts in the PR. Treat the coordinator change as a Major HVE Builder behavior change with static review, behavior testing and host validation. Record actual unresolved blockers; no unsupported acceptance ticks or issue closure.
  Deferred until after the demo (proposed 2026-11-22, awaiting owner approval). Needs a published PR and a reviewer who is not the author; neither exists for the demo. The HVE Builder review of the coordinator change has not been run. Not passed.
```

## Limits

* The demo owner decisions of 2026-11-18 waive billing reconciliation, DPO and Legal approval and person-run assistive-technology testing. They do not waive owner approval of deferrals.
* The issue stays open until the owner approves the deferral or both criteria are met.
