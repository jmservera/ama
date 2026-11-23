---
title: Resident Showcase Criterion 2 Hosted Evidence r7 (Issue #462)
description: Read-only GitHub run history that resolves the one criterion the r6 live check left unproven, with the full per-criterion table
ms.date: 2026-11-23
---

## Scope and limits

Session `rpi-462-live`, 2026-11-23, second pass. Under the 2026-11-18 owner decisions (synthetic demo, desktop only) the [r6 check](./resident-showcase-live-r6-2026-11-23.md) left criterion 2 unproven because it assumed hosted run history needed a push. Read-only `gh` queries show that history is available. No source, infrastructure or Azure change was made and the live browser script was not re-run; r6 remains the live record.

## Evidence for criterion 2

Commands: `gh pr view 455`, `gh run list --branch <PR 455 head branch>`, `gh api repos/jmservera/ama/commits/<sha>`.

| Item | Observation |
|------|-------------|
| Dependencies | #444 closed; PR #455 merged 2026-10-25T21:25:42Z, head `2523a70b16` |
| Failed rubric run | One failure: Capstone Rubric Scorer run 40207492780 on head `b82a7c4c93` (2026-10-25T15:33Z), alongside Source projects CI run 40207492737. Step logs are no longer retrievable, so the cause is not asserted |
| Score commits | `b82a7c4c93` (72/100) and `2523a70b16` (73/100): author and committer `github-actions[bot]`, files limited to `.github/rubric/scores/latest.json` and `badge.svg`. No human-authored score edit on the PR |
| Rerun pattern | After the failure the head changed twice with new content (`b7966f5dfa` threat-model research and plan, `a3ce598429` threat model). Runs on `a3ce598429` and `2523a70b16` succeeded; no run was repeated on an unchanged SHA |
| Bypass | Final merged head had Source projects CI and the rubric run both successful; no skipped-gate bypass seen in the run list |

Limit: bot authorship shows the score file was not hand-edited in these commits; it does not prove the workflow's internal scoring. The clause "existing local previews remain available" was not re-tested in this pass.

## Per-criterion result

| Criterion | Result | Basis |
|-----------|--------|-------|
| 1. RPI artifacts and threat model | Proven for the demo | Dated artifacts for both 2026-11-23 passes; [threat model](./resident-demo-threat-model-2026-11-16.md); the October independent review is not re-derived |
| 2. #444/#455 and failed rubric resolved | Proven for the hosted-history clauses; local-preview clause not re-tested | Table above |
| 3, 4 (ticked) | Re-observed live in r6 | 36 Playwright checks on resident revision 0000026 |
| 5 (ticked) | Not re-run | No source change |
| 6. Pre-spend record | Proven for the demo | [r3](./resident-showcase-live-r3-2026-11-18.md); USD 700 owner decision supersedes the October cap; no fresh cost figure |
| 7. Deployed showcase in a browser | Proven on the demo, desktop only | r6; "gates passed before deploy" not claimed |
| 8 (ticked) | Unchanged | Digests recorded in r6; source commit behind them unconfirmed (private registry) |

The issue stays open: the issue body asks that it not close with unmet criteria, and the ticking of criteria 1, 2, 6 and 7 belongs to the owner. Absent HSTS on the resident app remains an optional follow-up needing a source change and the full tier. Refs #462.
