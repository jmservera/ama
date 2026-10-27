<!-- markdownlint-disable-file -->
---
title: Documentation PR preparation research
description: Focused evidence for preparing the three owner-authorized documentation PRs
ms.date: 2026-10-27
---

## Research Brief

* Task: docs-prs-rebase, dated 2026-10-27.
* Purpose and audience: prepare PRs #454, #439 and #429 for the coordinator's
  merge gate, without merging or changing any code PR.
* Scope: each authorized PR's own clean worktree, latest origin/main,
  documentation conflict/link repair, dated RPI evidence and publication.
* Non-goals: main pushes, code changes, issue closure, rewriting original RPI
  findings, private datasets, live deployment and unrelated PRs.
* Criteria: preserve both sides, append-only knowledge-base log, docs-only
  diff, honest local/hosted check evidence and exact-head mergeability.
* Requested output: committed research, plan, implementation and independent
  review evidence, then each PR's checks and mergeability.
* Output mode: convergence. Status: Complete.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | Are the branches safe and docs-only; how should conflicts and publication gates be handled? |
| Initial internal areas | docs/reference/README.md, memory.md, case study documents, src/README.md, tools/rpi-checks.py, Git worktrees |
| Initial external areas | GitHub metadata for the three explicitly authorized PRs |
| Posture | Focused, inferred from the bounded named-PR request |
| Explicit limits | No merges; exclude #461, #459, #428, #426, #425, #424, #423 and #421 |
| Research writes | Only research evidence and required session tracking |
| Resolved root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Selection and authority |
| --- | --- | --- |
| Instruction | Repository AMA guidance | Selected: branch safety, append-only history, documentation validation and publication gates |
| Skill | rpi-research | Selected: ordered Wider, Deeper and Contrarian evidence |
| Skill | documentation | Selected: local checks separate from hosted checks; repository commands override generic npm catalog |
| Specialist | RPI Researcher | Skipped: a small continuous branch-preparation trace is handled inline |
| Specialists | Independent critique and Review | Reserved for their later phases, not research |

## User Participation and Research Decisions

The user explicitly requests the whole ordered RPI loop and authorizes rebases,
force-with-lease pushes and ready transitions for only the three named PRs.
Non-interactive execution precludes routine questions. No merge is authorized.
The session is automatic for this bounded task; no follow-up work is selected.

## Scope and Success Criteria

Verify actual remote heads rather than trust stale local branches. Preserve
original evidence and uncommitted work. Any unresolved publication gate blocks
only publication and is reported, not bypassed.

## Task Research Requests and Direction Controls

* Include only #454, #439 and #429.
* Use separate existing worktrees under /home/azureuser/source/ama-wt where safe.
* Rebase latest origin/main, preserving both histories' document content.
* No closing keywords, merges, main pushes or changes to excluded code PRs.
* Preserve human approval boundaries and adverse original review outcomes.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | Do current local and remote heads match and have clean worktrees? | Straightforward | Answered |
| Q2 | Which docs validation and exact-head publication gates apply? | Depth | Answered |
| Q3 | Can both sides and append-only log entries survive a rebase? | Depth | Answered, execution verification required |

## Prior Knowledge Gate

Read the original case study, addendum opening, reference index opening and
owner memory. Existing branch tips are clean but older than the remote PR heads.
Do not treat their historical receipts or RPI approvals as current evidence.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

GitHub metadata confirms all three open drafts have only docs/, tracking and
the permitted rubric score file. Existing clean worktrees are available for
all three. The orchestration worktree is clean on chore/docs-prs-rebase with
no existing PR. Latest fetched main is
885ee05fc45122cf7a1ea4f7f003dc88bfda08ee.

Reflection: local branches lag remote; synchronize by fast-forward only before
rebasing, with explicit remote-head leases. Inspect the local gate contract
and rebase ancestry before selecting the implementation sequence.

#### Wave 2: Deeper

The existing #439 local branch has two unpublished commits. The existing #429
local branch has diverged from its remote and includes unrelated ancestry.
Preserve both local branches untouched; create fresh isolated preparation
branches/worktrees from the authoritative PR remote heads instead. #454 can
also use that uniform safe approach. Bind pushes to the original full remote
head SHA, not a mutable remote-tracking ref.

The repository has no universal docs lint/build command. Use scoped Markdown
and local path/anchor review plus git diff --check and semantic diff review.
The explicit repository instruction requires --all before publication even
though src/README.md also documents newer partial-tier policy. Follow the
stricter full gate rather than silently downgrade. All named executable
prerequisites are on PATH; Docker responds at version 29.9.0, Python is 3.12.3
and Trivy is exactly 0.76.0. Actual gate execution remains pending.

Reflection: isolate from local-only changes, preserve originals and perform
one final-candidate critique and one post-implementation Review. Full-gate
evidence must bind clean committed candidates, outside Git.

#### Wave 3: Contrarian

Challenged the hypothesis that existing worktrees can simply fast-forward:
#439 is two commits ahead, while #429 is eight local versus five remote commits
and includes code ancestry. Reusing these blindly risks publishing unrelated
work. Fresh remote-based preparation branches avoid moving/discarding that work.

All three PRs currently report CONFLICTING / DIRTY. Existing hosted checks
include skipped rubric jobs and cannot establish success for rebased heads.
Historical score files and review failures must be retained as history rather
than fabricated current acceptance.

Reflection: no new product scope, cloud work or retrospective source edits are
needed. Follow exact remote branch snapshots, repair conflicts explicitly and
defer merging to the coordinator. No second research cycle is needed because
remaining uncertainties are execution outcomes, not missing task decisions.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Remote-based isolated rebases | W1, W2 | Accepted | Protect local-only work and constrain publication to named PRs |
| Existing checks prove readiness | W2 | Rejected | All heads conflict; old/skipped checks are not new-head evidence |
| Partial gate sufficient | C1, C4 | Rejected for this run | Explicit complete-gate instruction remains applicable |
| Automatic merge | Caller scope | Rejected | Coordinator alone owns subsequent merge gate |

## Evidence Log

| ID | Finding | Source | Confidence |
| --- | --- | --- | --- |
| C1 | src/README.md describes full and changed-path receipt tiers and clean exact-head verification | src/README.md:48 | High |
| C2 | Source original framing is immutable; addendum retains proposal and approval boundaries | docs/case_study_48_original.md:1; docs/case_study_48_addendum.md:8 | High |
| C3 | Knowledge-base index routes retention, historical evidence and original outcome preservation | docs/reference/README.md:14 | High |
| C4 | Complete gate is required for every final candidate; docs use Markdown/link and diff review | .github/copilot-instructions.md:64 | High |
| C5 | Gate preflight binds tools, full matrix includes project, static, infra, migration, browser, SQL and images | tools/rpi-checks.py:1321; src/README.md:89 | High |
| W1 | Authorized remote heads: #454 d4863a2a; #439 3648875e; #429 002fc375 | https://github.com/jmservera/ama/pull/454 ; https://github.com/jmservera/ama/pull/439 ; https://github.com/jmservera/ama/pull/429 ; retrieved 2026-10-27 | High |
| W2 | All three drafts are CONFLICTING / DIRTY; existing checks do not prove rebased acceptance | Same three GitHub PR URLs, retrieved 2026-10-27 | High |

## Findings, Alternatives and Decision State

Q1: clean local worktrees do not imply matching remote heads (W1); isolate
remote snapshots and leave local-only commits intact. Q2: scoped documentation
review and the complete local gate apply (C1, C4, C5). Q3: preserve the entire
main log byte prefix plus each topic's new entries, and inspect semantic
conflicts rather than select ours/theirs wholesale.

Selected recommendation: three fresh remote-based preparation worktrees,
explicit rebase resolution, append-only log proof, scoped link review, committed
original RPI evidence, full gates, independent exact-head assessment and
explicit-lease publication only after prerequisites pass.

Rejected alternatives: merging main violates the requested rebase; resetting
existing branches risks local-only work; retaining old rubric scores as fresh
approval or substituting partial receipts misstates evidence.

## Open Questions, Risks and Further Research

Rebase conflicts, stale rubric evidence, dangling documentation links and actual
gate outcomes remain execution risks. A changed origin/main or remote PR head
invalidates the respective candidate or publication lease. No missing product
decision blocks planning. No unrelated discovery is needed.

## Planning Readiness

Ready (C1-C5, W1-W2). Research disposition: executed, complete.

## Closeout and Advisory Next Step

All three waves completed inline; bounded continuous investigation did not
justify research delegation. Self-check: questions answered, source provenance
recorded, exclusions preserved, execution outcomes not preclaimed. Automatic
parent continues to Plan; no further user confirmation is needed for the
explicitly authorized actions. Full-gate and independent-review requirements
remain pending and cannot be replaced by owner publication permission.

## Sources

* W1/W2: GitHub PRs #454, #439 and #429, retrieved 2026-10-27 using gh pr view.
