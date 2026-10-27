---
title: Resident readiness PR 454 review corrections research
ms.date: 2026-10-27
---
<!-- markdownlint-disable-file -->

## Research Brief

Investigate the two unresolved PR #454 review threads for owner-authorised
documentation corrections on the existing branch. Audience: owner and PR
reviewers. Output mode: convergence, preparing planning. Success requires
retained independent requirements-quality assessment before G0, and explicit
RB-20 dependency on RB-19 without broadening OD-53.

## Research Parameters

Focused posture (bounded caller scope). Evidence root: `.copilot-tracking/`.
Internal candidates: resident PRD, draft backlog, historical quality and RPI
records. External candidates: PR #454 GraphQL reviewThreads and owner #441
comment 6392158254. Non-goals: runtime changes, requirement acceptance,
architecture registration, merging. No uv, secrets or push to main. Caller
explicitly limits validation to Markdown/links/diff (changed gate at most),
overriding the standing full-gate publication instruction for this task.

## Extension Registry and Provenance

* Repository instructions: selected for document provenance and branch safety.
* RPI research/plan/implement/review: selected for ordered dated evidence.
* Documentation skill: selected for documentation corrections.
* Independent requirements-quality reviewer: selected for the requested fresh
  assessment, not fictional customer approval.
* Research delegation: skipped; this is one tightly coupled evidence trace.

## User Participation and Direction Controls

The explicit full-loop request authorises automatic continuation through Review
and targeted PR replies/resolution. No routine clarification is needed.
Only the two unresolved threads may be resolved. Preserve original FAIL and
open findings. Rebase is authorised only because GitHub reports CONFLICTING;
normal commits otherwise, never merge the PR.

## Research Questions and Prior Knowledge Gate

* Q1: What assessment and G0 dependency does the owner require?
* Q2: Does RB-20 preserve the PRD S18 -> S17 dependency?
* Q3: What conflicts and historical evidence must be preserved?

Initial read confirms exactly two unresolved threads, an open matching PR,
a clean worktree and a conflicting mergeability result. Historical Review
records author self-review plus scoped corrections, not a complete fresh
requirements-quality assessment. Cross-session lookup found no matching recent
session; repository artifacts and owner direction are authoritative.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

GraphQL threads identify missing independent assessment before acceptance
and a grouped RB-19/RB-20 prerequisite row. Initial backlog and historical
Review read. Reflection: inspect current PRD and owner direction before choosing
the smallest correction; do not treat scoped critique as full assessment.

#### Wave 2: Deeper

Owner comment requires fresh independent requirements-quality assessment of the
actual corrected candidate before owner acceptance, not merely a scoped
applicability critique. PRD S18 explicitly depends on S17. RB-20 scope and
dependency row both omit RB-19. G0 has no RB-G1 prerequisite. Reflection:
correct both representations and require assessment plus disposition before G0.

#### Wave 3: Contrarian

The existing scoped assessment explicitly says "Not a full-PRD pass" and leaves
six inherited findings unreviewed. It therefore cannot substitute for the
requested fresh assessment. Negative dispatch/suspension tests do not require
OD-53 positive activation, but suspension still needs a dispatch policy to
suspend. Separating RB-20 -> RB-19 does not gate negative tests on OD-53.
Read-only merge-tree confirms one conflict, in the append-only KB log.

## Evidence Log and Findings

| ID | Evidence | Finding |
| --- | --- | --- |
| W1 | https://github.com/jmservera/ama/pull/454#discussion_r4369374300 (retrieved 2026-10-27) | Full independent requirements assessment missing |
| W2 | https://github.com/jmservera/ama/pull/454#discussion_r4387554699 (retrieved 2026-10-27) | RB-20 must depend on RB-19 |
| W3 | https://github.com/jmservera/ama/issues/441#issuecomment-6392158254 (retrieved 2026-10-27) | Corrected candidate assessed before owner acceptance; preserve failed history |
| C1 | docs/prds/zava-forward-retrofit-programme-demonstrator.md:1129 | S18 -> S17 |
| C2 | docs/prds/zava-forward-retrofit-programme-demonstrator.md:1246 | Audience correction already present; no PRD requirements edit needed |
| C3 | .copilot-tracking/changes/2026-10-25/resident-prd-backlog-readiness-441-draft-backlog.md:94 | RB-20 narrative omits RB-19; grouped graph at line 123 repeats defect |
| C4 | .copilot-tracking/changes/2026-10-25/resident-prd-backlog-readiness-441-draft-backlog.md:104 | G0 lacks RB-G1 prerequisite |
| C5 | .copilot-tracking/reviews/plans/2026-10-25/resident-prd-backlog-readiness-441-plan-critique.md:30 | Existing independent assessment explicitly scoped, not full PRD |

## Parent Synthesis and Decision State

Accepted: explicit RB-20 -> RB-19; full independent assessment bound to exact
PRD bytes; G0 prerequisite; append-only historical correction. Rejected:
claiming a quality pass, closing inherited findings through author judgement,
or substituting the earlier scoped critique. Deferred: substantive inherited
quality remediation, owner acceptance, live gates and implementation.
No further cycle needed: both thread defects and authority boundaries are
evidence-backed; broader research cannot change these bounded corrections.

## Risks and Self-check

Quality assessment may remain FAIL/BLOCKED. That is valid evidence, not an
acceptance gate pass. Rebase may alter candidate bytes, so assess after conflict
resolution. Original records must remain available. No legal claims or new
source retrieval are needed. All questions answered; evidence and paths checked.

## Planning Readiness

Ready. Research disposition: executed, complete.
Parent continuation: Plan, with W1-W3 and C1-C5; no research blocker.
