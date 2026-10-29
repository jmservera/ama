---
title: Finance PR 510 main refresh research
description: Focused evidence for the requested main rebase
ms.date: 2026-10-29
---

## Research Brief

Task ID / slug: `finance-510-refresh-2327`. Audience: coordinator of PR #510.
Output: convergence on a safe local rebase and CI-equivalent focused checks.
Scope: Refs #96; preserve existing finance implementation and historical RPI
outcomes. No issue completion claims, remote writes, Azure actions or private data.
Focused posture follows the user's bounded explicit full-loop direction.
Research root: `.copilot-tracking/research/2026-10-29/`.

## Direction Controls and Extensions

User explicitly requests Research, Plan, Implement and Review without pushing.
Repository case study, addendum, reference index/memory, component guides and
local-gate instructions apply. RPI phase skills selected. No web changes planned;
web skills and domain research specialists not applicable. Research inline:
the branch comparison is a single continuous trace. No worker executed.
Prior-knowledge lookup for finance sessions in the last seven days returned
no rows. Existing dated finance artifacts supply useful historical evidence.

## Questions and Evidence

* C1: `docs/reference/README.md:67` records the finance engineering boundary:
  Held drafts, Unapproved schemas, no operational approval.
* C2: `src/README.md:69` defines local gate and focused validation boundaries;
  repository instructions additionally require complete-gate attempt.
* C3: `src/core/pyproject.toml:35` and `src/api/pyproject.toml:54`
  define project-local mypy, source and test roots.
* C4: `.copilot-tracking/changes/2026-10-29/finance-510-refresh-2221-changes.md:17`
  documents the previous refresh, cross-worktree editable-install risk,
  PYTHONPATH isolation and previously passing focused checks.
* C5: Git intake: clean `docs/finance-96`, HEAD `088b53939e9f4e752adf7c436a0f336f2a67390c`;
  origin/main `c764a0120b0c9c0b7f5cd608ce50ff54667192f8`.
  Remote finance `8020965bff1d36dab5fbbf87e00df3966fc1db5e` is one
  score-only bot commit ahead. PR OPEN, targets main, actually non-draft;
  no draft-state change authorized or performed.

## Research Cycle 1

### Wider

Fetched origin and inspected PR, ancestry, changed paths, historical checks and
component configuration. Remote finance adds only rubric score data. Current
main advances through paper review and IoT integration. Reflection: retain the
remote bot commit by fast-forward before the explicitly authorized rebase.

### Deeper

Read-only merge-tree detects conflicts in rubric score, reference README index
and append-only reference log. Source/API README auto-merges. `/tmp/mv` has
Python, Ruff and mypy. Component-local source/test paths must precede existing
editable installs. Reflection: resolve each replay against the pinned main tree,
preserving all documentation entries; verify source composition, not just markers.

### Contrarian

Conflict-free does not imply CI success or human acceptance. Prior financial
Review outcomes remain historical and must not be rewritten. Actual remote PR
is non-draft despite the task wording. Rubric automation may diverge from main;
the user explicitly selects main's rubric and manifest. Heavy lock admission is
necessary but insufficient for claiming a complete gate. Reflection: no full API
discovery needed for a documentation-only rebase; run relevant modules and a
nonqueued complete-gate attempt after final commit.

## Synthesis and Decision State

Accept: fast-forward the score-only remote commit, rebase origin/main, choose
main for all rubric files and scenario manifest, retain both sides elsewhere.
Reject merge instead of rebase (contradicts explicit direction). Reject push,
Azure fallback, issue-completion claims and altered historical outcomes.
No new feature changes intended. Re-entry only if source conflicts or test
failures reveal missing evidence. One cycle covers the bounded scope.

Research disposition: executed. Planning Readiness: Ready.
Uncertainty: actual replay conflicts and local/hosted results remain unobserved.
Hosted CI cannot run on the new local head without coordinator publication.
Artifact self-check: evidence, limits, alternatives and all three waves recorded.
