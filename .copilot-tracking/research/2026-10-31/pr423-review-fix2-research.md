---
title: PR 423 review corrections research
description: Focused integration and bounded Blob review investigation
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Research Brief

Owner PR #423, Refs #360, starts at 7eba6116 on
docs/demo-transport-plan-360-fix2. Research prepares the explicitly requested
Research, Plan, Implement, Review loop. Scope is merging origin/main without
rebasing or losing existing work and correcting four named review threads.
Non-goals: Azure, private data, secrets, publication, PR body edits and issue
closure. Output mode: convergence. Status: Complete.

## Research Parameters

Focused posture selected for named internal defects. Evidence root:
.copilot-tracking/. Questions: how to preserve both merge intents; how to enforce
download/page allocation bounds; which active RBAC parameter the runbook needs;
what current provenance can honestly claim. No external research needed.
Research is read-only except dated research and required workflow state.
Heavy commands require flock -w 600 /tmp/ama-rpi-heavy.lock; pip, not uv.

## Extension Registry and Provenance

Repository .github/copilot-instructions.md selected for branch, evidence and
privacy constraints. rpi-research selected for ordered wider/deeper/contrarian
research. Python/infra source and existing tests are primary evidence.
Web/design and legal extensions skipped: no web or regulatory changes.
No specialist research delegation: one tightly coupled bounded investigation.

## User Participation and Direction Controls

The owner explicitly requests the full loop, local merge and local commit;
retain this direction without asking for routine advancement. No push, Azure,
secrets or PR body edits. Preserve append-only log entries and take main's
latest rubric JSON. Supplied defect descriptions are claims to verify.

## Prior Knowledge Gate

Working tree was clean; branch and PR head match the supplied ancestry.
Cross-session PR lookup returned no matching records. Existing code already
has a ranged download and an all-pages serialization check; investigate exact
guarantees rather than removing these prior corrections.

## Research Questions

| ID | Question | Status |
| --- | --- | --- |
| Q1 | What integration conflicts need both intents retained? | Answered |
| Q2 | Does Blob reading bound actual allocation after replacement? | Answered |
| Q3 | Does every serialized plaintext page fit the wrapper-inclusive limit? | Answered |
| Q4 | Which initializer and runbook instructions are current? | Answered |
| Q5 | Does integrated candidate provenance have a successful receipt? | Answered |

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Branch/PR inspection confirms an open owner PR and a clean child worktree.
Fetch identifies resident chat improvements on main and a divergent rubric
snapshot. The four target surfaces and existing infra tests are selected.
Reflection: preservation requires a real merge; prior transport safeguards
need exact regression evidence, not wholesale replacement.

#### Wave 2: Deeper

All four unresolved threads were retrieved read-only from GitHub. The current
head already contains the requested download range, wrapper-inclusive all-page
check, exact counterexample and active default-off Blob runbook. Existing tests
assert the ranged read and cleanup. The tracking record already says no
successful integrated receipt exists. Baseline unittest fails on the missing
installed core namespace; restore with pip in an external isolated venv.
Reflection: retain these built corrections; strengthen the read itself with
an explicit byte count and add exact regressions at the no-upload boundary.

#### Wave 3: Contrarian

Readall is ranged here, contrary to the thread's earlier source boundary, but
an explicit bounded read also constrains the consumer API independently. Reject
removal of the download range or all-page check. Dated tag activation commands
are history and must not be rewritten with Blob parameters; clarify past-tense
language and non-revoking incremental cleanup instead. Merge-tree inspection
finds only latest.json conflicted; the log needs preservation verification,
not speculative editing. Historical run9 cannot qualify a new merged commit.
Reflection: no wider research is warranted; all questions have source evidence.

#### Parent Synthesis and Disposition

Accept ranged download plus explicitly bounded read; preserve page algorithm
and reinforce existing tests. Accept main's rubric JSON and both parent
ancestries/content. Reject rebase, tag-history rewrite, PR body edits and any
promotion of historical receipts. Defer publication and live acceptance.

## Evidence Log

| ID | Source | Finding |
| --- | --- | --- |
| C1 | infra/scripts/staff_blob.py:254 | Download is already ranged to MAX_BLOB + 1 but ends in readall; explicitly bound the consumer read too. |
| C2 | infra/scripts/staff_blob.py:127 | Existing all-pages check measures wrappers/head; retain and exercise it. |
| C3 | infra/tests/test_staff_azure.py:720 | Replacement regression already checks range, allocation and owned job cleanup. |
| C4 | infra/tests/test_staff_azure.py:786 | Exact requested near-boundary counterexample and multi-page limit controls already exist. |
| C5 | infra/README.md:2242 | Active examples use includeResultBlob=false; opt-in true needs storage and approval; cleanup retains ciphertext. |
| C6 | infra/staff-initializer-rbac.bicep:11 | Blob grant defaults false and scopes writer to staff-results. |
| C7 | .copilot-tracking/changes/2026-10-30/pr423-merge-rubric-changes.md:161 | Prior record disclaims a successful integrated receipt; make newest candidate boundary explicit. |
| C8 | infra/README.md:2717 | Historical relay receipt still uses present-tense parameter wording; clarify dated scope without rewriting performed commands. |
| C9 | .github/rubric/scores/latest.json:1 | Read-only merge-tree against ec2d784255c3377ab39e5d2d1b5140e76c8e7f36 identifies this as sole conflict. |

## Alternatives and Decision State

Select minimal hardening and durable qualification of already built fixes.
No source algorithm rewrite is justified for Q3. Both obsolete historical
commands and adverse RPI outcomes remain intact. Independent critique and
Review will assess this candidate once each.

## Risks and Residual Uncertainty

No live SDK/private-route/MI verification; fake SDK behavior is offline only.
No full-gate receipt exists for the new candidate. Publication is not requested;
the complete exact-head gate, hosted checks and owner approval remain separate.
PR description correction is reserved to the owner. No external citations or
new regulatory claims are involved.

## Planning Readiness

Ready. Research disposition: executed. Focused scope is covered by one complete
ordered cycle; no material unresolved design question remains. Artifact
self-check: scope, three waves, evidence, alternatives and uncertainty recorded.
Parent next action: Plan, then Implement and one Review as explicitly requested.
