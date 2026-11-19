---
title: Issue 164 r6 changes
description: Changes record with per-criterion proven or unproven table
ms.date: 2026-11-19
---

Refs #164. Demo, desktop, focused tier. No source changed; no real-model call; no Azure write; no spend. Only read-only `az containerapp show`.

Files: research note `docs/reference/research/issue-164-live-r6-2026-11-19.md`, index and log entries, `.copilot-tracking/` artifacts and evidence.

Validation: `src/agents` `test_chat_eval`, `test_chat_heldout`, `test_chat_eval_revocation_effort`: 89 tests OK. mypy, ruff and rpi-checks not applicable (no src or infra change; no `--all`).

| Criterion | Status | Basis |
| --- | --- | --- |
| Thresholds approved; chat task registered with reviewer and enable state | Partly proven | Registered, disabled, function named; thresholds only proposed, no named individual. Approval is a person decision. |
| Results bound to serving model and control versions, approved thresholds and reviewers | Unproven | No actual-model chat result; nothing approved to bind. |
| Competent human exercises block seeded suggestions | Unproven | Needs competent people; waiver covers assistive technology only. |
| Actual calls need finite payload, call, token, budget, expiry authority | Unproven | No chat call authority recorded; no calls made. |

Outcome: every remaining criterion is production-only or needs a human; no code built.
