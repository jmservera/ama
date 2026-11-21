---
title: Issue 184 live review
ms.date: 2026-11-20
---

Review executed once after implementation. Boundary: the uncommitted worktree diff against `origin/main` plus the live state.

## Outcome

Conformant for the demo with routed follow-ups; no material finding is open inside this task.

## Findings routed to later work

* The system-origin decode (`ZF_SIM_SYSTEM_ORIGIN`) and the `x509Certificate` auth type are security-relevant. They are opt-in and default off, with tests for spoof refusal, module refusal and SAS refusal, but need independent human review before use beyond the demo.
* The receiver exits with `RUN_DEADLINE` (exit 2) at every full window, so scheduled executions show Failed. Consider a clean exit for a completed window.
* The receiver has no checkpoint and replays the backlog each window; adding checkpointing would cut duplicate rejections.
* Device identities and Secret-volume key material persist until teardown; follow the stop and teardown steps in the research note.
* Hosted CI and the complete local gate are not run here.
