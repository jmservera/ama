<!-- markdownlint-disable-file -->
# RPI Phase Details: issue-1294-validation-policy

## Metadata

| Field | Value |
|-------|-------|
| Task ID | issue-1294 |
| Plan | .copilot-tracking/plans/2026-11-08/issue-1294-validation-policy-plan.md |
| Research | .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-retry-research.md |

## Phase Index

* P01 Baseline and edit the policy files
* P02 Validate and freeze

## P01: Baseline and edit the policy files

### Context

Research C9 to C11 and C23 identify the wording to change; C1 to C21 supply the facts the new text must state truthfully.

### Intent

Tiered policy with identical rules in each file; each rule stated once and linked, not copied, where possible (guide is the canonical source).

### Boundaries

Only the in-scope files. No workflow, tool or application edits.

### Likely Targets

* .github/copilot-instructions.md (the gate paragraph beginning "Every final RPI candidate")
* src/README.md (Local RPI gate section; new subsections before "Gate speed controls")
* .github/agents/ama-backlog-delivery-coordinator.agent.md (Local validation tiers; steps 5 and 6 only if text conflicts)
* docs/reference/method/tracking-retention-policy.md (line 14)
* docs/reference/log.md (append), .copilot-tracking/github-issues/issue-1294.md (create)

### Dependencies

Research complete.

### Validation Expectations

AC1 and AC3 via grep and git diff; later P02.

### Completion Evidence

Diff of the targets; changes record.

### Unresolved Items

None.

### P01-T01: Record HVE baseline of the four target passages

#### Context
hve-builder improve mode needs a baseline of existing behavior before mutation.
#### Intent
Capture current claims (blanket gate, default `--changed`, tier text) in the changes record.
#### Boundaries
Read-only on targets.
#### Likely Targets
The four files above.
#### Dependencies
None.
#### Validation Expectations
Baseline notes cite file and line.
#### Completion Evidence
Baseline section in the changes record.
#### Unresolved Items
None.

### P01-T02: Rewrite the instruction gate paragraph

#### Context
C9: lines 72-75 state a blanket gate and `--changed` default and conflict with C10 and C11.
#### Intent
State: during development run targeted local tests; small and documentation-only candidates run the planned relevant local checks plus applicable hosted CI and do not run a blanket `--changed`; major features, SQL, infrastructure, deployment, security-sensitive changes and releases keep the complete gate and verified full receipt; mixed takes strictest; absent, path-filtered or skipped CI is not success; local-only coverage stays local or direct; independent exact-head review, hosted CI where it applies and human approvals remain; keep the full-gate mechanics sentences unchanged.
#### Boundaries
Do not alter the retention-policy paragraph, branch rules or other sections.
#### Likely Targets
.github/copilot-instructions.md
#### Dependencies
P01-T01
#### Validation Expectations
AC1; link to `../src/README.md#local-rpi-gate` still resolves.
#### Completion Evidence
Diff hunk.
#### Unresolved Items
None.

### P01-T03: Add coverage reconciliation and examples to src/README.md

#### Context
C1 to C21: the guide owns the canonical policy and the CI/local reconciliation.
#### Intent
Rewrite the owner-policy lead; add "Hosted CI versus local gate coverage" (triggers, selection, executed checks, local-only list, CI truthfulness) and "Policy examples" table (documentation, small employee chat/browser, SQL, Bicep/security, mixed) with tier, required local checks, hosted expectation and what must not be claimed. Describe `--changed` as an optional focused aid, not a default; keep it as the way to obtain a scoped receipt when wanted. State the ruleset observation as dated, not a protection change.
#### Boundaries
No change to the speed-controls or measuring sections.
#### Likely Targets
src/README.md
#### Dependencies
P01-T01
#### Validation Expectations
Each example fact reproduced in P02-T01.
#### Completion Evidence
Diff hunk.
#### Unresolved Items
None.

### P01-T04: Align coordinator tiers and retention policy wording

#### Context
C11 already has tiers; it needs strictest-wins wording, targeted-first, hosted-CI truthfulness and local-only direct checks, referencing the guide. C23 says the complete gate generically.
#### Intent
Minimal edits to the Local validation tiers section; reword retention sentence to the selected-tier gate.
#### Boundaries
No change to Human blockers, merge or step logic beyond a conflicting phrase.
#### Likely Targets
coordinator agent file; docs/reference/method/tracking-retention-policy.md
#### Dependencies
P01-T03
#### Validation Expectations
HVE static review.
#### Completion Evidence
Diff hunks.
#### Unresolved Items
None.

### P01-T05: Add issue record and knowledge-base log entry

#### Context
Brief requires issue-1294.md; repository requires log append when a knowledge-base file materially changes.
#### Intent
Create the issue record with issue facts (title, number, URL, created 2026-11-08T21:33:27Z, no template, no labels, no assignees, state, author, body); append a log entry without editing earlier entries.
#### Boundaries
Append only.
#### Likely Targets
.copilot-tracking/github-issues/issue-1294.md; docs/reference/log.md
#### Dependencies
P01-T02 to T04
#### Validation Expectations
Format matches issue-608.md.
#### Completion Evidence
Files present.
#### Unresolved Items
None.

## P02: Validate and freeze

### Context
Focused tier plus HVE Major gates.

### Intent
Run direct checks, HVE static review, behavior simulation and host validation; record actual outcomes.

### Boundaries
No heavy gate, Docker, installs, push, PR.

### Likely Targets
Diff and tracking artifacts.

### Dependencies
P01

### Validation Expectations
AC2 to AC5.

### Completion Evidence
Changes record and review artifact.

### Unresolved Items
Whether hve-builder-tester simulation is available in this host; if not, record Deferred.

### P02-T01: Reproduce example selections read-only and run link/diff/stale-wording checks

#### Context
Examples must be testable.
#### Intent
Import `tools/rpi-checks.py` by path and call `changed_groups` for example path lists; call `ci-affected.select`; run a link check on changed Markdown and grep for stale phrases.
#### Boundaries
No bytecode writes (PYTHONDONTWRITEBYTECODE=1), no gate run.
#### Likely Targets
Read-only.
#### Dependencies
P01
#### Validation Expectations
Outputs match the example table.
#### Completion Evidence
Commands and exits in the changes record.
#### Unresolved Items
None.

### P02-T02: HVE static review, hve-builder-tester simulation, host validation

#### Context
Behavior-bearing instruction mutation, Major.
#### Intent
Invoke hve-builder-tester (simulation) for five scenarios; static review against the rubric; host validation (git diff check, markdown links).
#### Boundaries
Contained simulation only.
#### Likely Targets
Evidence under .copilot-tracking/hve-builder/2026-11-08/.
#### Dependencies
P01
#### Validation Expectations
Pass or honest Revise/Deferred.
#### Completion Evidence
Report paths.
#### Unresolved Items
None.

### P02-T03: Changes record, original review, commit and freeze

#### Context
Brief requires four artifacts and a clean commit.
#### Intent
Write changes and review, commit with privacy-safe email and trailer, verify clean.
#### Boundaries
No push.
#### Likely Targets
.copilot-tracking/changes, reviews
#### Dependencies
P02-T01, P02-T02
#### Validation Expectations
git status clean (except preserved first-attempt untracked files, see changes record).
#### Completion Evidence
HEAD and tree.
#### Unresolved Items
First-attempt untracked research file must be preserved: decide commit vs leave (leave untracked unmodified; report).
