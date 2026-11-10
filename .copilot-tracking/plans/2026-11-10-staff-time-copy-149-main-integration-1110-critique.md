---
title: Parent 149 component-only main integration critique (single, final candidate)
ms.date: 2026-11-10
task_id: 149-copy-main-integration-1110
---

## Critique (executed once, 2026-11-10T00:47Z, before the merge; verdict: approve with direct applications)

Executed against the plan and details as the final candidate. Not repeated for this task.

| Id | Finding | Disposition |
| --- | --- | --- |
| K1 | V4 lists test modules that import server and SQL-adjacent helpers; with the main delta they could skip silently when a dependency is absent. | Applied: skip ids and reasons are recorded per module and any skip in required scope blocks a ready claim. |
| K2 | Browser admission could be mistaken for queued waiting. | Applied: exactly one `flock -n`; busy means exit 1 and the exact pending step, no loop. |
| K3 | Global editable installs point at the primary checkout, so a plain `python` would test the wrong Core/API. | Applied in research and V1: new venv from this worktree with pinned dev extras; V1 asserts resolved paths. |
| K4 | A merge commit could be mistaken for new product work. | Applied: V8 and Phase 3 require product blobs identical to the parent and a non-tracking diff limited to the two files. |
| K5 | Origin main already moved past the pin. | Applied: the pin is used as instructed; the newer tip is recorded as not integrated. |
| K6 | Tracking commit before the merge keeps the merge commit clean and own records separable. | Applied in Phase 1. |

No conflict with the confirmed owner decisions; none rejected. No significant or divergent issue needs a user decision.
