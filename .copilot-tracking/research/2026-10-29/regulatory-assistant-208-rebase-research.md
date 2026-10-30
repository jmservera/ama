---
title: Regulatory assistant PR 506 rebase research
ms.date: 2026-10-29
---

## Research brief

Bring draft PR #506, Refs #208, onto origin/main without pushing or Azure
operations. Preserve both sides' intent and original adverse RPI evidence.
Audience: implementation and coordinator. Output: convergence for planning.
Posture: focused, selected for the explicitly bounded integration task.
Evidence root: `.copilot-tracking/`. No interaction is needed: the caller
explicitly requested all four phases and supplied conflict policy.

## Direction controls and extensions

Repository instructions and RPI phase skills apply. Source remains under src,
tests outside packages. Main owns rubric and scenario manifest conflicts.
Web guidance is applicable only if web edits become necessary; no redesign.
Research specialists are not needed for this tightly coupled local trace.
The user authorizes rebase and local commit, not push, Azure or issue closure.

## Questions and cycle 1

1. What must be preserved from the branch and main?
2. Which checks cover integration and pinned source drift?
3. What acceptance cannot be claimed from local checks?

### Wider

The worktree is clean on the requested open draft topic branch. Two branch
commits add regulatory routing/usage and preserve the original Review.
Main is `5653547507f3056f09a726a18516237728da5e5b`.
Reflection: continue this topic; do not restart feature work or replace its
original evidence.

### Deeper

CI runs Ruff, formatting and mypy per project, plus isolated Ruff/format for
regulatory_ux_check.py (C3). Original checks cover core regulatory/privacy/rule
modules, agents gates and API chat/alerts (C4). /tmp/mv provides all tools.
Reflection: run these selectors with local source paths first, preventing
shared editable installs from selecting another worktree.

### Contrarian

Main changed the scenario manifest; its hashes can be invalidated by retained
branch changes to the draft DPIA and UX synthesis. Main's manifest copy is
necessary but may not be sufficient: run test_scenario_manifest and reconcile
only pinned hashes if the test proves drift. Original Review is Complete /
Not accepted with publication and human gates unmet (C5). Historical rubric
success is not CI evidence for the new head.
Reflection: no new feature or human-acceptance claim; no full API discovery
needed for this integration. Heavy/full publication gates remain distinct.

## Evidence log

* C1: `src/README.md:64` describes component unit, Ruff and mypy commands.
* C2: `src/README.md:75` distinguishes local gates from hosted/human approval.
* W1: https://github.com/jmservera/ama/pull/506 retrieved 2026-10-29;
  open draft, requested branch/base, Refs wording, historical rubric pass only.
* C3: `.github/workflows/src-ci.yml:92` isolated browser-check quality controls.
* C4: `.copilot-tracking/changes/2026-10-27/regulatory-assistant-208-changes.md:57`
  original scoped selectors and their results.
* C5: `.copilot-tracking/reviews/logs/2026-10-27/regulatory-assistant-208-review.md:42`
  original independent execution and unmet acceptance.
* C6: `src/core/pyproject.toml:35` and `src/api/pyproject.toml:55`
  existing strict typing and namespace configuration.

## Alternatives and synthesis

Select the requested rebase and scoped regressions. Reject merge because the
caller explicitly selected rebase; reject branch-wide overwrite because it
would lose either current-main contracts or original routing work. Defer
full publication and hosted CI to coordinator; no push is authorized.
All three questions are covered. No additional research cycle is warranted
until actual conflict/test evidence reveals a material gap.

## Decisions and readiness

Research disposition: executed, Complete. Planning Readiness: Ready.
Self-check: scope, three waves, evidence, alternatives, constraints and
residual publication/human uncertainty recorded.
