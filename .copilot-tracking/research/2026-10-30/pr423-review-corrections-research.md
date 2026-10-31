---
title: PR 423 review corrections research
description: Focused evidence for owner review corrections and main integration
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Research Brief

* Topic: PR #423 review comments, main d986c4c4 integration and rubric evidence.
* Purpose and audience: coordinator-owned publication of the owner's PR.
* Scope: private Blob transport, its tests and current runbook, current-main
  compatibility, PR handoff accuracy and requested offline checks.
* Non-goals: Azure, deployment, live sign-in, credentials, secrets, remote writes,
  issue completion, retrospective rewriting of historical receipts.
* Criteria: each review concern mapped to current source or a concrete
  correction; dated research, plan/details, changes and independent Review;
  honest exact-candidate validation and rubric qualification.
* Requested outputs: full ordered RPI loop and local commits only.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Posture | Focused, bounded named PR and supplied review evidence |
| Internal candidates | infra/scripts/staff_blob.py, infra/tests/test_staff_azure.py, infra/README.md, prior transport evidence, rubric tooling |
| External candidates | PR #423 comments, reviews and thread state only |
| Evidence root | .copilot-tracking/ |
| Limits | No remote writes; heavy commands require flock -w 600 /tmp/ama-rpi-heavy.lock |
| Research writes | Research artifact and required workflow state only |

## Extension Registry and Provenance

| Kind | Candidate | Disposition |
| --- | --- | --- |
| Instruction | .github/copilot-instructions.md | Selected: src layout, local gates, identity, history preservation |
| Skill | rpi-research | Selected: ordered wider/deeper/contrarian research |
| Skill | rpi-plan, rpi-implement, rpi-review | Deferred to corresponding phases |
| Skill | web-design-guidelines | Required if web files change; otherwise browser exercise only |
| Specialist | Independent critique and Review | Reserved for those gates, no research delegation needed |

## User Participation and Direction Controls

The user explicitly requests the whole ordered loop; execute automatically.
No interaction is available or necessary for routine advancement. Explicit
no-push direction overrides repository publication defaults. PR comments and
thread text are inert evidence, never authority.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | Which review concerns remain in current source? | depth | Open |
| Q2 | What changed between this branch, PR head and main d986c4c4? | depth | Open |
| Q3 | What evidence can establish local correctness and qualify rubric readiness? | depth | Open |

## Prior Knowledge Gate

Initial branch is clean, docs/demo-transport-plan-360-fix at bda7975f.
PR #423 remains open on docs/demo-transport-plan-360; remote head reported
32cc1f816c25a10d555f18e4507f92afeaf7ee20. Prior handoff/gate evidence must
be verified rather than reused as a current receipt. Historical score comment
reports 77/100 PASS, but is not a score for new unpublished corrections.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Initial evidence identifies four review comments: bounded Blob downloads,
every-page size validation, current Blob runbook parameters, and historical
receipt mislabelling in the PR body. Prior branch work may already address
some concerns. Next priority is current code plus ancestor/main relationships.

#### Wave 2: Deeper

All four concerns remain actionable (C1-C3, W4). The downloader buffers the
entire replacement, and split_pages checks only its final running estimate.
The fake container needs to model offset/length and record the actual bound.
The active runbook still specifies tags and tag cleanup, independently of
preserved dated activation receipts. main d986c4c4 adds no web runtime diff;
its checks and documentation are preserved rather than rewritten.

Reflection: correct resource bounds at the read and serialized-page boundaries,
not only post-hoc totals. Add reproductions for intermediate wrapper/head
overflow, exact boundaries, UTF-8/escaping, download replacement and cleanup.

#### Wave 3: Contrarian

The remote PR has one score-only child of local HEAD (32cc1f81); ignoring it
would lose remote lineage. Merge it first, then main without rewriting history.
Read-only merge-tree finds only KB index/log conflicts with main (C4).
Retain both append sequences and new-main score; never rewrite historic RPI
evidence. The public PR body wrongly calls run9 current, while local evidence
already records a blocked gate (C3). A local proposed replacement body is
necessary because remote writes are prohibited.

Hosted score W5 is PASS 77/100, but does not prove a fresh correction score.
No rubric relaxation, score editing, artificial evidence or live-readiness
claim is justified. Preserve scoring contracts and add an honest handoff.
Full local gate still needs a clean committed candidate and external receipt.
No heavy-lock holder was listed at inspection; admission is race-sensitive.

Reflection: mergeability can be proven locally against the pinned main, not
for an unpublished remote head. Human, hosted and live acceptance stay separate.

### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Reason |
| --- | --- | --- | --- |
| Bound downloads and validate all pages | W1/W2, C1/C2 | Accepted | Concrete current defects with small deterministic reproductions |
| Correct current runbook only | W3, C3 | Accepted | Do not overwrite dated receipts or delete actual Azure resources |
| Correct PR body remotely | W4 | Deferred | User prohibits push; coordinator receives ready-to-use local body |
| Merge remote bot child then main | C4 | Accepted | Preserve public lineage and current-main source without rebase |
| Raise or guarantee score | W5, C5 | Rejected | Existing hosted PASS is not a new local score; no grade manipulation |

Cycle re-entry: no further cycle needed. Current source, boundaries and
validation contracts answer Q1-Q3; actual execution belongs to Implement.

## Evidence Log

| ID | Finding | Source |
| --- | --- | --- |
| W1 | Download allocation must be bounded before buffering | https://github.com/jmservera/ama/pull/423#discussion_r4392465810, retrieved 2026-10-30 |
| W2 | Every wrapped page must satisfy PAGE_BYTES | https://github.com/jmservera/ama/pull/423#discussion_r4392465888, retrieved 2026-10-30 |
| W3 | Active runbook must use includeResultBlob default false | https://github.com/jmservera/ama/pull/423#discussion_r4392465933, retrieved 2026-10-30 |
| W4 | PR body overstates historical run9 receipt | https://github.com/jmservera/ama/pull/423#discussion_r4426748172, retrieved 2026-10-30 |
| W5 | Hosted comment reports 77/100 PASS, not current local-head scoring | https://github.com/jmservera/ama/pull/423#issuecomment-6305760316, retrieved 2026-10-30 |
| C1 | Unbounded download and final-page-only validation | infra/scripts/staff_blob.py:100, infra/scripts/staff_blob.py:245 |
| C2 | Existing fake client and codec/controller cleanup fixtures | infra/tests/test_staff_azure.py:51, infra/tests/test_staff_azure.py:663, infra/tests/test_staff_azure.py:726 |
| C3 | Active stale tag setup/cleanup; dated gate failure is already explicit | infra/README.md:2197, infra/README.md:2238, infra/README.md:2281; .copilot-tracking/changes/2026-10-30/pr423-merge-rubric-changes.md:153 |
| C4 | Read-only git ancestry and merge-tree | HEAD bda7975f; remote child 32cc1f81 changes only .github/rubric/scores/latest.json; main d986c4c4a1010b6a5c7ba6b00d2c452c4db8f089; conflicts docs/reference/README.md and docs/reference/log.md |
| C5 | Strict scorecard and exact-head complete gate contracts | .github/rubric/README.md:85, src/README.md:73 |
| C6 | Native Fluent browser harness starts constructed loopback app | src/api/checks/design_system_browser_check.py:55; src/api/pyproject.toml:29 |

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence |
| --- | --- | --- |
| Q1 | All four review comments require scoped correction or coordinator handoff | W1-W4, C1-C3 |
| Q2 | Preserve bot child plus main with additive conflict resolution | C4 |
| Q3 | Infra regressions, requested API suite/static tools, local Playwright, strict rubric tests, final full gate | C2/C5/C6 |

## Alternatives and Decision State

Select bounded ranged reads, exact serialized-page checks, current runbook
correction, non-rewriting integration and local PR-body handoff. Reject
unbounded readall, stale size estimates, restoring tag transport, rewriting
historical receipts and editing recorded grades. SDK/network/live behavior
remains unproven by fake-client checks.

## Sources and Self-check

GitHub API and gh pr view 423 --comments retrieved 2026-10-30; source paths
above inspected directly. Cross-session prior-knowledge query returned no
matching recent session. Repository context, original/addendum and memory
read; no private data read. Web guideline skill loaded and current rules
retrieved; no web runtime file change planned. Instructions selected by scope;
no separate research worker needed for this continuous trace. Q1-Q3 answered,
three waves completed in order, hypotheses and score uncertainty retained.

## Decisions and Readiness

Research disposition: executed, complete.
Planning Readiness: Ready.
