---
title: "HVE Builder static review: AMA Backlog Delivery Coordinator at d7d7fdee3"
description: "Review-mode static assessment of the coordinator agent after #1903, #1843 and #1821; source artifact read-only"
ms.date: 2026-11-18
---

## Scope

* Mode: review (source read-only; evidence files only)
* Target: `.github/agents/ama-backlog-delivery-coordinator.agent.md` (1089 lines, sha256 `b688648e2761d09ba03fb33a12fc729e0028202e3a66d8e27fda4768eb211dce`)
* Source identity: HEAD `d7d7fdee3c2a123e777c1c6ad1496610a6a80502`; the target is unmodified in the worktree
* Change classification: Major (decision rules, stage gates, write authority and safety behavior changed by 20f0b166f #1903, f1df574bb #1843, df8887766 #1821)
* Standards: `hve-builder` review-rubric.md and requirements-catalog.md; repository Markdown conventions
* Reviewer context: the lead parent ran the review directly. No fresh-context reviewer was dispatched because the parent task disallowed nested delegation. This is a disclosed independence limit.
* `tools:` configuration not inspected (tool-configuration boundary). Frontmatter is `name` and `description` only; no non-tool capability surface to preserve or change.

## Reuse of prior evidence

| Prior evidence | Status at HEAD | Basis |
| --- | --- | --- |
| `2026-11-15/coordinator-instructions-*` (static, behavior, validation) | Not reusable | Reviewed a different working-tree state (gemini-4-carbon default, `/mnt/tmp` launcher, 5-cycle cap, 10 to 30 minute cadence); HEAD now states two correction cycles, 10 minute cadence, `claude-sonnet-5.5` default, no `/mnt/tmp`. Source identity differs. |
| `2026-11-05/06` #1204 behavior reports 001 to 011 | Historical only | Predate #1843, #1821 and the #1903 port; useful as the origin of the liveness contract, not as evidence for HEAD. |
| `2026-10-23/issue-440-host-native-2.md` | Reusable as context for host validation | Shows native `/agent` discovery needs an enforced sandbox and was not achieved; see the host record. |
| Rubric dimension outcomes for frontmatter, ASCII punctuation | Re-checked fresh | `grep` for non-ASCII bytes returned no matches. |

## Dimension assessment

| Dimension | Status | Evidence |
| --- | --- | --- |
| Architecture fit, Subagent design | Pass | One coordinator purpose; delegates backlog review to `hve-core-all:github-backlog-manager` (step 1), implementation to tmux RPI workers (step 5), review to `code-review-*` (step 6). Frontmatter unchanged in shape. |
| Workflow contract | Pass | Liveness (lines 68 to 183), classification table (184 to 259), schedules (275 to 347), validation tiers and steps 1 to 10 agree on the eight-session cap, 20/15 PR drain thresholds, two correction cycles (lines 52 to 56, 959 to 962) and the five-state table. The behavior run found no contradiction in these gates. |
| Outcome and structure | Pass | Outcome and stop rules precede the steps (lines 3 to 20, 68 onward). |
| Emphasis calibration | Revise-level observation, Medium | See F1. |
| Load timing, Reference discipline | Pass with note | Long (1089 lines) but single-purpose, always loaded when invoked; canonical docs referenced by link. See F6. |
| Safety and enforcement | Pass | Owner delegation bounded to run-owned PRs (lines 21 to 38); no force push of `main`; finite cleanup manifest; human gates preserved; evidence not assertion. |
| Evidence fidelity | Pass | Step 6 requires source identity, execution status, verdict, fidelity and profile limits for HVE evidence; states simulation is never native acceptance. |
| Model fit | Pass with note | `model:` omitted, so the directly invoked agent uses the session model; worker model rules at lines 786 to 800 are explicit. See F2. |
| Stale-pattern absence, Convention conformance | Pass | No non-ASCII characters, no em dashes; `*` lists; fenced blocks carry a language. |

## Findings

No Critical or High findings.

| ID | Severity | Dimension | Location | Finding | Smallest change |
| --- | --- | --- | --- | --- | --- |
| F1 | Medium | Emphasis calibration | lines 155, 159, 186, 214, 291, 904 | The "never claim 'nothing changed' while open issues are unclassified" rule is restated six times with slightly different conditions. Drift risk: lines 186 to 214 and 904 add differing exceptions (session cap, drain). | Keep the full rule once (Liveness, lines 159 to 183) and cross-reference it from lines 186, 291 and 904. |
| F2 | Medium | Workflow contract | lines 786 to 789 versus 854 to 856 | An unavailable requested model is a loop-only blocker with "no silent fallback", yet a failed start is "retried once in the same worktree". The simulation showed an executor must infer whether to retry with the same unavailable model and whether it is a human blocker. | State that a model-unavailable failure is not retried with the same model, is ledgered as route repair, and asks the owner for a substitute. |
| F3 | Low | Workflow contract | lines 24 and 21 to 38 | "run opened or adopted" is never defined, so ownership of an already-published PR (for example a receipt run on PR 2100) is ambiguous. | Define how adoption is recorded (for example `approved_actions` in session SQL). |
| F4 | Low | Workflow contract | lines 199 | "exhausted `#1296` correction-cycle budget" uses an issue reference the file never defines; elsewhere the cap is two correction cycles (lines 52 and 959). | Replace with "after two correction cycles (step 6)". |
| F5 | Low | Convention conformance | line 750 | "Then run:" precedes the launcher instructions that follow "Write a unique launcher", reading as a duplicated lead-in. | Delete the stray "Then run:" line. |
| F6 | Low | Portability and maintenance | line 340 | The verbatim approved delivery snapshot has missing spaces ("above20", "than50", "until15"). Because the file mandates verbatim snapshots, a fix needs the owner re-approving the snapshot. | Owner re-approves a corrected snapshot, then edit the text and the live schedule together. |
| F7 | Low | Safety and enforcement | lines 761 to 765 versus 643 to 644 | The tmux launcher runs `copilot ... -p "$(cat "$brief")"` without stdin redirected, while gate runs require `< /dev/null`. The 2026-11-15 evidence used a launcher with `< /dev/null`. Whether the omission causes hangs is unobserved here. | Add `< /dev/null` to the `copilot` line if the hang risk is accepted by the owner; otherwise record why not. |

## Verdict

* Static verdict: `Pass` (no Critical or High findings; 2 Medium and 5 Low advisory findings, none blocking under the rubric)
* Closure: not applicable; no corrections were made (review mode).
