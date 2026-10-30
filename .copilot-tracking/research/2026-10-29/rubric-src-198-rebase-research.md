---
title: PR 507 conflict rebase research
ms.date: 2026-10-29
---
<!-- markdownlint-disable-file -->

# Task Research: rubric-src-198-rebase

## Research Brief

Research the current divergence of draft PR #507 from origin/main, preserving
both documentation histories and authoritative upstream rubric/scenario inputs.
Audience: local implementer and publishing coordinator. Output: convergence
for an explicitly requested full Research/Plan/Implement/Review loop.
Non-goals: pushing, Azure changes, issue closure, unrelated application fixes.

## Research Parameters

Focused posture, selected for the caller's named branch, conflict and commands.
Evidence root: .copilot-tracking/. External scope: GitHub PR metadata only.
Research writes only research evidence and lifecycle state. No interaction is
required: the caller explicitly advances all four phases and authorizes rebase
and local commits, but not an ongoing automatic follow-up session.

## Extension Registry and Provenance

* Repository instructions: selected for branch, evidence and local validation.
* RPI skills: selected sequentially for the four requested phases.
* Web, security and regulatory skills: skipped; no corresponding changes.
* Research specialists: skipped; a single coupled Git integration trace.

## Direction Controls

* Reuse feat/rubric-src-198, open draft #507, Refs #198 only.
* Rebase origin/main; preserve both append-only histories and index entries.
* Keep origin/main's entire .github/rubric tree and scenario manifest.
* Use /tmp/mv; no full API suite without successful shared-lock admission.
* No Azure resource changes or push. Preserve earlier adverse RPI evidence.

## Prior Knowledge Gate

Read original/addendum, KB index/memory, prior refresh state and changes.
The prior task already ran a full loop and ended Not accepted; do not rewrite
that outcome. This is a new bounded rebase task with its own stable identity.
Initial worktree clean; no rebase currently active. Earlier refresh's
56535475 base is stale; fetched main is 356a3cfb.

## Research Questions

| ID | Question | Status |
| --- | --- | --- |
| Q1 | What branch work and new upstream edits must be reconciled? | Answered: index and log conflicts; no application delta |
| Q2 | Which inputs are authoritative, and which tests apply? | Answered: main rubric/manifest; core/API static and focused dependency/manifest tests |
| Q3 | Does successful local integration prove hosted CI success? | Answered: no push means no fresh hosted result |

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inspected clean Git status, open draft PR metadata, branch-only commits and
dated refresh evidence. Three local-only commits carry documentation and
historical tracking, not application code. New main includes substantial
unrelated work; scope remains integration, not porting new features.

Reflection: prioritize exact conflict surface and current validation contracts.

#### Wave 2: Deeper

`git merge-tree --write-tree --name-only HEAD origin/main` predicts conflicts
only in docs/reference/README.md and docs/reference/log.md. Main's index has
new #110/#184, #218/#219, #208/#217 and #157-related updates; branch adds #198.
Main's log appends other workstreams after their shared prefix; branch appends
two #198 entries. Keep upstream paragraphs and all branch additions.
Main rubric differs only in recorded latest score. Manifest unchanged, but
run its validator anyway to detect any newly stale pinned public source.
Existing /tmp/mv supplies Python 3.12.3, Ruff and mypy; system pytest 9.1.1.

Reflection: restoring entire files from one side would lose independent work;
manual conflict reconciliation must keep both appended tails and index entries.

#### Wave 3: Contrarian

Prior refresh had 18 rubric failures; main now has a newer score snapshot, so
do not reuse old counts. Run the existing full rubric-script suite locally,
but never modify the authoritative rubric to mask inherited failures.
Hosted #507 checks currently show rubric/score passing with baseline 77/100
and no scored artifact changed. That is not evidence for the unpushed new HEAD.
The current src guide distinguishes focused validation from publication gates;
no full publication receipt is claimed in this no-push task.

Reflection: source-free rebasing can restore ancestry and selected local
checks but cannot establish fresh hosted CI without the prohibited push.
Accepted: rebase plus content-preserving resolution and focused validation.
Rejected: blanket ours/theirs for documentation, new rubric repairs, whole
application suite. Deferred: coordinator's exact-head publication/hosted CI.
No new research cycle needed: all bounded questions have direct evidence.

## Evidence Log

| ID | Source | Finding |
| --- | --- | --- |
| C1 | .copilot-tracking/rpi-sessions/2026-10-29/rubric-src-198-refresh-state.json:1 | Prior loop blocked after Review; new task must retain it |
| C2 | .copilot-tracking/changes/2026-10-29/rubric-src-198-refresh-changes.md:23 | Prior rebase, selected tests and 18 inherited rubric failures are historical |
| C3 | src/README.md:69 | Focused checks apply to small documentation/tooling tasks; hosted acceptance remains separate |
| C4 | src/core/pyproject.toml:23 and src/api/pyproject.toml:29 | Existing Ruff and strict mypy commands and test paths |
| C5 | src/core/tests/test_scenario_manifest.py:21 | Real repository validator checks pinned sources without changing metadata |
| C6 | docs/reference/README.md:45 and docs/reference/log.md:8034 (origin/main) | Independent upstream entries must survive replay |
| W1 | https://github.com/jmservera/ama/pull/507, retrieved 2026-10-29 | Open draft, expected head and main base |
| W2 | https://github.com/jmservera/ama/actions/runs/40880365306, retrieved 2026-10-29 | Existing rubric score success is historical, not new-candidate CI |

## Planning Readiness

Research disposition: executed, Complete. Planning Readiness: Ready.
Self-check: three ordered inline waves, evidence IDs, alternatives, constraints
and residual hosted uncertainty recorded. No research source edits.
Parent next action: Plan under the caller's explicit four-phase request.
