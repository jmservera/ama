---
title: Branch Lineage Instruction Improvement Intake
description: Approved scope, baseline, routing and acceptance for the branch-selection correction
ms.date: 2026-10-10
ms.topic: reference
---

## Scope and Route

Mode: improve. Source write boundary: .github/copilot-instructions.md, Branch
and Pull Request Workflow section only. Stage evidence belongs under
.copilot-tracking/hve-builder/2026-10-10/. Preserve all frontmatter and
unrelated instructions. Distribution wiring is not applicable: the existing
repository-wide instruction file is already its activation surface.

The owner identified an observed error: a research-to-PRD follow-up lost
branch ancestry by starting again from main, even though it continued the
same work. The purpose of the branch rule is to avoid direct work on main
and maintain coherent changes, not create a branch for each message or phase.
The owner explicitly requested a fresh main-based branch for this separate
instruction change. Clean worktree was confirmed; chore/branch-lineage-guidance
was created from fetched origin/main without altering the open PRD branch.

## Baseline

The existing rule requires topic branches and PRs, checks status/current
branch, creates a fresh branch when on main, and separates unrelated work.
It does not explicitly classify follow-ups, inherited unmerged work, PR
lifecycle or dependent child-branch bases. The publication bullet fixes
every PR base to main, so it must be made consistent with stacked branches.
Existing dirty-worktree protection, privacy-safe commit identity, required
checks and owner-controlled merge remain unchanged.

No research/exploration is needed: the target and user objectives are known;
bounded target/canonical-reference reads establish the baseline. No extension
survey, new source artifact, host capability or tool configuration is needed.

## Acceptance

* Continue an active coherent workstream across research, design, PRD,
  implementation and review iterations when a separate change is not justified.
* Use latest origin/main for unrelated work, a completed/merged workstream,
  or explicit owner direction; never treat a new message/file type alone as
  an unrelated task.
* Preserve ancestry with a dependent child branch when related work warrants
  isolation for risk, breaking changes or independent review; explain PR base
  and parent dependency without merging or rewriting history automatically.
* Consider reusing a known matching branch, separate worktrees, no-write
  questions, closed-unmerged/detached or ambiguous situations.
* Protect existing changes and preserve privacy, checks, PR delivery and
  owner merge authority. Ask only for material ambiguity or required safety
  approval, not for every coherent iteration.
* Keep the source amendment concise and limited to branch/PR routing.

## Classification and Gates

Major: the amendment changes model branch-selection and PR-base decisions.
Use fresh-context Medium-profile author/static-review stages, then
hve-builder-tester with contained simulation of Git/PR scenarios (no real
branch switches, destructive actions or remote writes in tests). Mechanical
validation uses Low profile after the final correction state. The approved
skill's canonical available profiles select gpt-5.6-terra for Medium and
gpt-5.6-luna for Low.

Overall outcome remains pending until required static, behavior and local
validation gates complete. Simulated conformance is not native Git-host
execution or enforcement of branch protection.
