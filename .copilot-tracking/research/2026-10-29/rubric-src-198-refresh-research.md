<!-- markdownlint-disable-file -->
---
title: PR 507 main refresh research
ms.date: 2026-10-29
---

## Research Brief

Bring draft PR #507, branch `feat/rubric-src-198`, up to date with
`origin/main`, retaining additive documentation and main-owned rubric/scenario
inputs. Audience: coordinator and independent reviewer. Output: convergence
for implementation planning. Scope excludes Azure operations, pushes, issue
closure, legacy application source and unrelated repairs.

## Research Parameters and Direction Controls

Focused posture, selected for the owner's bounded integration request.
Use `/tmp/mv`; validate relevant lint, format, typing and tests. Full API
suite requires the shared heavy lock. Preserve original RPI evidence.
User explicitly requests all four phases and authorizes this rebase and a
local commit, but no push. No automatic-session continuation beyond this
bounded task is inferred.

## Extension Registry and Participation

Repository instructions and RPI phase skills selected. Web/design and Azure
skills skipped: no web implementation or infrastructure action is intended.
Inline research selected because the git integration is one continuous trace.
No interaction required: branch, resolution policy and validation scope supplied.

## Prior Knowledge and Questions

PR #507 is OPEN and draft; its only branch commit is `4e494f56`.
The worktree was clean before recording this evidence. Fetched origin.

1. Which paths conflict, and which authoritative main changes supersede the PR?
2. Which current local checks exercise the surviving delta?
3. What acceptance/publication limitations must remain explicit?

## Research Cycle Log

### Cycle 1: Wider

Inspected PR metadata, branch-only commit, project commands and current CI.
`git merge-tree --write-tree --name-only HEAD origin/main` identifies three
conflicts: cut-over evidence pack, KB index and append-only log.
Reflection: the integration is additive documentation, not application migration.

### Cycle 1: Deeper

Compared branch rubric inputs to main and read scenario validation and project
configuration. Main rubric differs in five files, including its recorded score;
the explicit main-copy policy therefore applies to the whole rubric directory,
not only conflicted files. `/tmp/mv` has Python 3.12.3, Ruff 0.17.1 and mypy
2.4.0; its editable installs point at a different worktree. Explicit local
source/test paths are necessary to prevent validating another checkout.
Reflection: retain main's rubric/scenario bytes and run scenario integrity plus
namespace/dependency checks against this checkout.

### Cycle 1: Contrarian

Checked the premise that green focused tests imply publication readiness.
They do not: original historical acceptance gaps and Review remain unchanged;
the required exact-head publication receipt and hosted CI cannot be claimed
from an unpushed local commit. The user prohibits pushing and Azure operations.
The source README offers a small-change tier, while repository instructions
still require a complete gate before publication; preserve that stricter
boundary rather than claiming either receipt exists.
Reflection: do not repair superseded rubric tests or invent fresh scores.
No further research cycle is needed for this bounded local integration.

## Evidence Log

| ID | Evidence | Finding |
| --- | --- | --- |
| C1 | `.github/copilot-instructions.md:72` | Complete exact-head local gate remains a publication prerequisite. |
| C2 | `src/README.md:52` | Project-local Ruff/mypy/unittest commands and tests outside packages. |
| C3 | `src/core/pyproject.toml:40` | Strict mypy uses local source/test namespace roots. |
| C4 | `src/api/pyproject.toml:52` | API typing also uses sibling core roots. |
| C5 | `src/core/tests/test_scenario_manifest.py:21` | Current manifest validates pinned public source provenance. |
| C6 | `.copilot-tracking/changes/2026-10-27/rubric-src-198-changes.md:22` | Original outcome includes deck failure/runtime skips; preserve, not overwrite. |
| W1 | https://github.com/jmservera/ama/pull/507 (2026-10-29 via gh) | Open draft, main target, branch feat/rubric-src-198; Refs #198. |

Fetched main: `5653547507f3056f09a726a18516237728da5e5b`.
Original head: `4e494f56`. Merge-tree found the three documentation conflicts.
No external search, cloud operation or worker was needed.

## Findings, Alternatives and Decision State

Accepted: rebase the requested branch, preserve both additive document sides,
restore all rubric files and the scenario manifest from fetched main, then
validate the actual surviving documentation-only delta and source contracts.
Rejected: retain branch rubric tests over main (violates explicit owner policy);
merge instead of rebase (violates explicit requested method); claim CI success
without pushing (unsupported). Deferred: whole-issue historical acceptance,
complete publication gate and fresh hosted checks to the coordinator.

## Planning Readiness

Ready. Research disposition: executed, complete. All three waves complete.
No unresolved implementation decision. Owner merge, historical acceptance and
publication gates remain separate, not blockers to a local no-push refresh.
Self-check: scope, evidence IDs, alternatives, readiness and limits recorded.
