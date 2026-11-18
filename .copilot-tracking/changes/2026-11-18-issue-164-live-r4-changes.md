---
title: Issue 164 r4 changes
ms.date: 2026-11-18
---

No source change; documentation and evidence only, FOCUSED tier. The live probes and offline tests were executed during research (disclosed: the implement-start witness records the changes file, which was written after the evidence run; no source edit followed).

Files: `docs/reference/research/issue-164-live-20261118T1707Z-2026-11-18.md`, `docs/reference/README.md` (index row), `docs/reference/log.md`, `.copilot-tracking/evidence/2026-11-18/issue-164-live-r4/*`, phase artifacts.

## Per-criterion table

| Criterion | Proven or unproven | Why |
| --- | --- | --- |
| Thresholds approved; chat task registered with reviewer and enable state | Partly proven | Registered, disabled, unapproved, function named. Thresholds `proposed`, individual `unknown`; a person must approve. |
| Results bound to serving-model/control versions, approved thresholds, outcomes | Unproven | No actual-model chat result; thresholds unapproved; no reviewer. |
| Competent human exercises block seeded critical suggestions | Unproven | Needs competent people; offline panel is not human effectiveness. |
| Actual calls under approved payload/provider handling and finite authority | Partly proven | Engineering caps labelled; no spend. No chat-call authority; unknown liability on meter. |

Ticked criteria not re-audited beyond 54 offline tests (OK) and live refusal/abstention samples. No criterion newly tickable.

Validation: `unittest -v` in `src/agents` for three chat modules, 54 OK; Markdown/link review; `git diff`. mypy, ruff and src tests not applicable (no src change).
