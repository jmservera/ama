---
title: Issue 109 sensor-review stack integration plan critique
ms.date: 2026-11-10
task_id: 109-integration-preparation-1110
---

One pass by the planning agent (no new agents permitted); verdict: compatible with changes. Not independent. The one critique is not repeated for this task.

| # | Finding | Disposition |
| --- | --- | --- |
| 1 | The first draft of the plan listed main-owned Registry and workspace-oracle tests as required checks. They do not overlap child files, widen the DEMO targeted tier toward a gate and may need `azure-iot-hub` that the child venv lacks. | Applied: demoted to conditional, run only on unexpected change or Root request; failures are adverse main-owned results, not repaired. |
| 2 | The merged child-parent remote head `P` is unknown. A squash or rebase merge of PR #1395 would break the assumption that `2b050647b` is an ancestor, and a naive merge could then re-add or conflict on child content. | Applied: plan and details record ancestry, compare trees, recompute the dry merge for `P`, and forbid source transplant. |
| 3 | A staged `--no-commit` merge leaves dirty source at `implement-done` and `review-done`; `commit-complete` needs a clean tree and a commit whose content equals the reviewed snapshot. | Applied: sequence kept as merge staged, check, review, commit, record literal HEAD. A refusal stops and is preserved, not healed. |
| 4 | Main may move between preparation and admission, and the preparation commit moves HEAD before `implement-start`. | Applied: precondition 3 re-reads main and flags overlap with the child net source set; the preparation commit is tracking-only so the witness source-change qualification stays empty. |
| 5 | SQL skips could be misreported as passes, and `flock` contention could invite polling. | Applied: pass requires all cases run, 0 skips, exit 0; one non-queued `flock -n` attempt with holder identification, BUSY stops that check. |
| 6 | The scoped mypy exemption and unforced `ConflictError` and `CommittedReloadError` coverage could be lost in a later summary. | Applied: carried as explicit gaps in plan, details and the changes record. |
| 7 | The #440 sensor checkpoint could be misread as already covered by the existing NomUX and Bicep record, or as something this loop implements. | Applied: stated as distinct and due, Root-routed, with no owner pivot or deferral approved here. |
| 8 | Closing-keyword risk in the eventual PR. | Applied: `Refs #109 #111` only with unmet criteria listed. |

No significant or divergent issue needing a user decision. No finding conflicts with a confirmed decision.
