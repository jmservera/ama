---
title: Employee acceptance review-thread research
description: Focused investigation of PR 601 cluster containment and hosted browser execution
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Research Brief

* Target: the two unresolved Copilot threads on PR #601 for issue #570.
* Purpose/audience: evidence for a bounded acceptance-adapter correction.
* Scope: map producer, acceptance projection/tests, API CI browser step and workflow hash pin.
* Non-goals: application map changes, live sign-in, secrets, Azure changes, full local gate, issue closure.
* Criteria: real producer-derived regression; cluster-only tolerance; strict point/geographic validation; three hosted Chromium executions without skips.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Posture | Focused, inferred from the caller's named files and exact failure |
| Evidence root | .copilot-tracking/research/2026-10-31/ |
| Internal candidates | src/core/src/zava_forward/core/insights.py; src/api/checks/employee_acceptance_check.py; src/api/tests/test_employee_acceptance_check.py; .github/workflows/src-ci.yml; tools/rpi-checks.py; src/api/README.md |
| External candidates | PR #601 review threads only |
| Limits | Pip only; no secrets; merge main first; do not wait for full local gate; CI is the requested gate |
| Research writes | Research and required lifecycle state only |
| Completion basis | Both bounded questions answered with code evidence and contrarian checks |

## Extension Registry and Provenance

| Kind | Candidate | Disposition |
| --- | --- | --- |
| Instructions | AMA repository guidance, all paths | Applied; retain dated evidence and prior adverse outcomes |
| Skill | rpi-research | Selected; focused inline wider/deeper/contrarian cycle |
| Specialist | hve-core-all:rpi-researcher | Skipped; single tightly coupled trace does not justify delegation |
| Web skills | UI implementation/review skills | Not applicable; no web UI files changed |

## User Participation and Direction Controls

Caller explicitly selected this follow-up from the running automatic #570
session, ordered all four phases and authorized non-force publication and
thread resolution. No routine questions are needed or available. The caller's
current CI-only publication direction supersedes prior local-gate blockers
for this follow-up, without rewriting their historical records.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What tolerance handles producer centroids without weakening other validation? | Straightforward | Answered |
| Q2 | How does hosted CI guarantee all three maintained browser tests execute? | Straightforward | Answered |

## Prior Knowledge Gate

Read the original #570 and correction session records, repository index,
memory, both case-study documents and API acceptance guide. Prior live
identity attestation remains unavailable and is not part of this repair.
`git merge --no-edit origin/main` returned Already up to date. Reviewed main:
`e64c6e6c9da407682de59b926944424f94f50671`; starting HEAD:
`62290cb850ad8ce6cad224ef4522e8ee6e3210f8`. Worktree was clean.

## Research Cycle Log

### Cycle 1

* Wider: traced producer, consumer, maintained CLI, discovery and browser
  setup. C1-C5 establish two bugs in acceptance evidence, not application
  authorization. Reflection: keep the producer unchanged and repair the
  adapter/CI at their own boundaries.
* Deeper: executed the real producer with 501 fictional colocated cases:
  latitude `54.90000000000044`, longitude `-1.600000000000014`, exact original
  bounds `[54.9, -1.6, 54.9, -1.6]`, total 501, shown 1. The maintained CLI
  checks testsRun == 3, successful execution and zero skips. Reflection:
  a cluster-only absolute degree tolerance and post-install CLI invocation
  address the exact failures.
* Contrarian: examined oversized/relative tolerances and modifying core.
  Relative tolerances introduce coordinate-dependent slack; point markers do
  not use accumulated centroids and need no slack. Geographic/bounds validity
  must remain strict even when cluster containment has slack. Discovery is
  intentionally allowed to skip absent Chromium but cannot be acceptance.
  Reflection: retain exact range/order checks; use 1e-9 degrees absolute
  containment tolerance (approximately 0.11 mm latitude), reject beyond it,
  and preserve the strict CLI's fail-on-skip exit contract.
* Synthesis: accept both bounded repairs (C1-C5). Reject core changes,
  global/relative tolerance and removing discovery qualification.
* Re-entry: not needed; all material questions have executable/code evidence.

## Evidence Log

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Core accumulates coordinates then divides for centroids; bounds use original extrema | src/core/src/zava_forward/core/insights.py:143-179 | High |
| C2 | Acceptance applies exact containment to both points and clusters after strict geographic checks | src/api/checks/employee_acceptance_check.py:168-225 | High |
| C3 | Fresh discovery can skip three browser regressions only for missing executable | src/api/tests/test_employee_acceptance_check.py:245-251 | High |
| C4 | Maintained CLI enforces exactly three successes and zero skips | src/api/checks/employee_acceptance_check.py:469-482 | High |
| C5 | Discovery precedes installation; browser step omits maintained acceptance CLI | .github/workflows/src-ci.yml:79-114 | High |
| C6 | Workflow bytes are pinned; edit requires updated same-commit digest | tools/rpi-checks.py:53-61 | High |
| C7 | Documented acceptance command provides test import paths and no live credentials | src/api/README.md:66-105 | High |

| ID | Source | Retrieved |
| --- | --- | --- |
| W1 | https://github.com/jmservera/ama/pull/601#discussion_r4431764865 | 2026-10-31 |
| W2 | https://github.com/jmservera/ama/pull/601#discussion_r4431764882 | 2026-10-31 |

## Findings, Alternatives and Decisions

Q1: cluster-only 1e-9 degree slack preserves strict raw coordinates, ordered
geographic bounds, points and counts (C1-C2). Q2: invoke the maintained CLI
after Chromium setup with the documented environment (C3-C5/C7), updating
the workflow pin in the same commit (C6).

No new legal, operational or live identity claims. Earlier full-gate blockers
remain historical; this follow-up follows explicit CI-only caller direction.
Missing source distributions were confirmed by ModuleNotFoundError and
installed with pip in a task-owned external venv; source import now works.

## Sources and Self-Check

Codebase evidence and both GitHub review comments are sufficient. No general
web sources used. Both questions answered; three ordered waves recorded;
alternatives challenged; no secrets or source edits during research.

## Planning Readiness

Research disposition: executed. Planning Readiness: Ready. Parent continues
the selected automatic loop; no ordinary decision blocker remains.
