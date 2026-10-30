<!-- markdownlint-disable-file -->
---
title: Finance PR 510 main synchronization research
description: Focused evidence for rebasing the finance branch without changing approval boundaries
ms.date: 2026-10-29
---

## Research Brief

* Task identity: `finance-510-main-sync`, PR #510, Refs #96.
* Purpose/audience: local integration and CI readiness for the coordinator.
* Output mode: convergence, preparing planning.
* Scope: fetch/rebase `docs/finance-96` on `origin/main`, preserve both sides'
  intent, validate relevant source/tests, commit locally, independent Review.
* Non-goals: pushing, merging, Azure changes, private data, finance activation,
  issue acceptance or rewriting previous adverse evidence.
* Criteria: source only under `src/`, tests outside packages; main's rubric and
  scenario manifest; append-only log/index preservation; requested lint, format,
  mypy and focused unittest validation using `/tmp/mv`.

## Research Parameters and Direction Controls

Focused posture selected from the explicit bounded integration request.
The user explicitly requests all four phases in this invocation; no routine
phase-advancement interaction is needed. No publication is authorized.
The research root is `.copilot-tracking/research/2026-10-29/`.
No external research is needed beyond read-only GitHub branch/CI metadata.

## Extension Registry and Provenance

* Repository instructions: selected; preserve original case study, historical
  RPI evidence, controls, branch identity, privacy-safe commit attribution.
* RPI research/plan/implement/review: selected for phase evidence.
* Web/design skills: skipped; no UI change is planned.
* Research specialists: skipped; this is one coupled integration trace.
* Independent critique and Review: required in their respective later phases.

## Questions and Candidate Areas

1. What changed on main, and which replayed commits conflict?
2. Which current CI selectors and pinned source checks cover the finance diff?
3. Do historical defect reports remain applicable after later corrections?

Starting areas: Git ancestry, source CI workflow, core/API project configuration,
finance source/tests, scenario manifest and original finance RPI artifacts.

## Prior Knowledge and Participation

The worktree was clean on `docs/finance-96`. Fetch succeeded. GitHub reports
PR #510 OPEN with `isDraft=false`, despite the task's draft description.
No PR metadata mutation will be made. The PR body describes historical defects;
later local commits must be checked before interpreting those as current.
No interaction is needed: the request supplies resolution and validation policy.

## Research Cycle Log

### Cycle 1: Wider

Read-only ancestry inspection found local/remote finance HEAD
`bafcb2415991a15eb3a16b781649a2ce7c749fcf` and fetched main
`8ee1b77f8983ddf39216da07ae60c63ef66431d6`. Main adds the merged #512
monitoring work; the finance branch has eight replayable commits. Overlap is
the reference index, append-only log and rubric score, not finance runtime.
Reflection: prioritize those three paths while retaining every finance fix.

### Cycle 1: Deeper

Read project configurations, Source CI, manifest/test and the prior rebase
changes record. `/tmp/mv` has Python 3.12.3, Ruff 0.17.1 and mypy 2.4.0.
Installed distributions' editables point at another worktree, so explicit
local/sibling `src` and `tests` paths must win import resolution. No dependency
installation or shared-venv mutation is necessary. The current manifest and
its four pinned sources have no main delta.
Reflection: run full configured core/API static scopes and focused finance,
source/staging, role-inventory, dependency and manifest tests. Full API
discovery is unnecessary; do not claim lock admission.

### Cycle 1: Contrarian

Compared the PR's historical rejection with later source-guard commits and
their original independent Review. RV-001/002 were addressed in separate
later work; do not treat the original rejection as the current implementation
verdict or rewrite it. Hosted checks have not failed executable jobs:
Source CI and rubric run 40960065828/40960065833 are `action_required` with
empty jobs. PR metadata is not draft. Preserve both facts rather than claiming
green CI or changing remote metadata.
Reflection: this task can establish local integration readiness only. Hosted
approval/push and whole-finance acceptance remain separate.

### Parent Synthesis and Re-entry

Accept C1-C6 below. Select the caller's rebase with additive resolution, main
rubric/manifest preservation and focused validation. Reject merge because
the user explicitly requests rebase. Reject all-side conflict checkout for
log/index because it loses independent contributions. Defer feature redesign,
PR metadata refresh and approval/CI activation to the coordinator.
One completed focused cycle covers the material questions; another cycle
would revisit the same ancestry/configuration evidence without changing the
resolution policy. Actual conflicts are implementation evidence, not an
unresolved research decision.

## Evidence Log

| ID | Evidence | Finding |
| --- | --- | --- |
| C1 | `docs/reference/README.md:55`; Git main diff; `docs/reference/log.md:8142` on main | Monitoring and finance navigation/log entries overlap and must both survive. |
| C2 | `.github/rubric/scores/latest.json:5`; Git main diff | Score metadata differs; main's copy is authoritative for this task. |
| C3 | `.github/workflows/src-ci.yml:43`; `src/core/pyproject.toml:30`; `src/api/pyproject.toml:53` | Existing package lint/format/mypy and external tests define the validation surface. |
| C4 | `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json:46`; `src/core/tests/test_scenario_manifest.py:21` | Four public sources have pinned hashes; run manifest regression without inventing pins. |
| C5 | `.copilot-tracking/reviews/logs/2026-10-29/finance-510-source-guards-review.md:159`; commit `5ce4bae3` | Later independent source-guard Review is Conformant; original adverse Review remains historical. |
| C6 | [Source CI run](https://github.com/jmservera/ama/actions/runs/40960065828), retrieved 2026-10-29; `gh pr view 510`; `/tmp/mv` tool probes | Hosted Source CI awaits action with no jobs; local tools exist, but editables target a sibling worktree. |

No web/regulatory claims or private data were needed. Recent session-history
lookup found no additional finance session; committed artifacts supply context.

## Findings, Alternatives and Decision State

Q1 answered by C1/C2: additive documentation conflicts and main-owned score.
Q2 answered by C3/C4/C6: existing package static checks and focused modules,
explicit local namespace paths. Q3 answered by C5: preserve both dated outcomes
and later source corrections. Current source behavior still needs regression
validation after rebase.

Risks: main may move after assessment; no push is authorized to generate fresh
CI. Missing human finance/template/Board authority remains outside this task.
No new approval or issue acceptance is inferred from local checks.

## Readiness and Re-entry

Research disposition: executed. Planning Readiness: Ready.
Self-check: brief, boundaries, extension provenance, participation, three waves,
source evidence, alternatives, risks and handoff are recorded; no source edits
were made in Research. Next parent action: Plan and one independent critique.
