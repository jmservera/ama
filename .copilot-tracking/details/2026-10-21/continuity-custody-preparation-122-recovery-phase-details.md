<!-- markdownlint-disable-file -->
# RPI Phase Details: Non-operative custody preparation correction (#122)

## Metadata

* Task ID: continuity-custody-preparation-122-recovery
* Task slug: continuity-custody-preparation-122-recovery
* Related plan: .copilot-tracking/plans/2026-10-21/continuity-custody-preparation-122-recovery-plan.md
* Evidence sources: .copilot-tracking/research/2026-10-21/continuity-custody-preparation-122-recovery-research.md

## Phase Index

| Phase ID | Name                             | Status | Detail sections            |
|----------|----------------------------------|--------|----------------------------|
| P01      | Correct the README subsection    | ready  | P01, P01-T01, P01-T02      |
| P02      | Validate and record              | ready  | P02, P02-T01, P02-T02, P02-T03 |

<!-- rpi:phase id=P01 -->
## P01: Correct the README subsection

### Context

The subsection added in c9f65c48 sits under the issue #122 section of src/core/README.md. Research F5 shows the table implies roles that sources do not assign.

### Intent

Text that sources support and nothing more.

### Boundaries

* Included: the subsection only.
* Excluded: other README sections, other files.

### Likely Targets

* src/core/README.md: the decision-rights table, verification bullet, witness and sequence bullets.

### Dependencies

* none

### Validation Expectations

* Diff limited to the subsection; ASCII; anchors resolve.

### Completion Evidence

* changes record and git diff.

### Unresolved Items

* none

<!-- rpi:task id=P01-T01 -->
### P01-T01: Rework the decision-rights table

#### Context

OQ-017 names Sponsor, Programme, Safety, DPO/Legal and Assurance as owners of the question. OD-35 names Building Safety and Sponsor for override authority and restart evidence. No source names a drill authoriser, head custodian or competent-review holder.

#### Intent

Each row cites its source where one exists and otherwise states UNASSIGNED. No row names a person. Target rows (role / status):

| Row | Source cite | Target |
| --- | --- | --- |
| Suspend AI for a release or task | continuity.py `incident_owner` (free text on the record); OQ-017 | "incident owner recorded on the suspension" / "UNASSIGNED for actual use (OQ-017); recorded text is not verified authority" |
| Restart AI after an incident | OQ-017; OD-35 (Building Safety and Sponsor own override authority and restart evidence, not a holder) | "actual restart authority, distinct from the proposer" / "UNASSIGNED; OD-35 owners supply evidence and do not hold or delegate authority" |
| Accept corrective evidence | OQ-017 (competent-review authority) | "competent reviewer" / "UNASSIGNED (OQ-017)" |
| Authorise a drill and its witness | none | "not named by any source" / "UNASSIGNED and UNAPPROVED" |
| Custody of the external head copy | none | "not named by any source" / "UNASSIGNED" |
| Resident, safety, professional and Finance decisions | #221 section (manual casework, challenge, hazard response independent) | "their existing human owners" / "unchanged; AI and this protocol take none" |

#### Boundaries

* Included: table rows and the sentence after it.
* Excluded: new roles.

#### Likely Targets

* src/core/README.md: "Decision rights" bullet.

#### Dependencies

* none

#### Validation Expectations

* Read the table against C7 and C8.

#### Completion Evidence

* diff hunk.

#### Unresolved Items

* none

<!-- rpi:task id=P01-T02 -->
### P01-T02: Fix verification wording and label proposals

#### Context

`verify_export` checks bundle digest, ledger chain against bundle digests, recorded head, optional external head, completeness. `--by-year` sealed digest checks are a separate #114 step.

#### Intent

Accurate verification text; witness rule and sequence stated as proposed expectations. Whole-subsection disposition: intro paragraph gains a lead-in that every bullet is a proposed expectation, not an existing control; custody bullet names what `verify_export` checks (digest, ledger chain, recorded head, optional external head, completeness) with `--by-year` sealed-digest checks as a separate #114 step, and the pre-gate sentence is qualified as not evidenced in repository sources (inferred); witness bullet marked proposed because no source defines a witness role; sequence bullet marked proposed; communication, stop conditions and not-evidence bullets unchanged (they restate UNASSIGNED state and existing independence rules). Also restore the blank line before the following `## Synthetic home-specific cited chat (#214)` heading.

#### Boundaries

* Included: the whole subsection, disposed bullet by bullet.
* Excluded: code changes.

#### Likely Targets

* src/core/README.md

#### Dependencies

* P01-T01 (same hunk area)

#### Validation Expectations

* Compare to continuity.py verify_export.

#### Completion Evidence

* diff hunk.

#### Unresolved Items

* none

<!-- rpi:phase id=P02 -->
## P02: Validate and record

### Context

Local-first documentation checks only; no heavy gate.

### Intent

Show scope held and record history.

### Boundaries

* Included: anchor check, ASCII check, diff and status.
* Excluded: full gate, Docker, Azure.

### Likely Targets

* .copilot-tracking/changes/2026-10-21/continuity-custody-preparation-122-recovery-changes.md

### Dependencies

* P01

### Validation Expectations

* Script output, git diff --stat.

### Completion Evidence

* changes record.

### Unresolved Items

* none

<!-- rpi:task id=P02-T01 -->
### P02-T01: Local checks

#### Context

Prior run used a small anchor script.

#### Intent

Anchors resolve; added lines ASCII; only allowed paths changed; no criterion ticked.

Commands and expected results: a Python anchor check over README headings for the #122, #221 and #114 slugs prints no MISSING; `git diff -U0 HEAD -- src/core/README.md` filtered for non-ASCII added lines prints nothing; `git diff --name-only ca4baf75837de57c99718f7423716d5dc0b0e244` lists only src/core/README.md and .copilot-tracking/ paths; net README addition per `git diff --stat HEAD` stays within about 15 lines; no checkbox line changes and no gh write is issued.

#### Boundaries

* Included: README anchors for #122, #221, #114.
* Excluded: repository-wide gates.

#### Likely Targets

* src/core/README.md

#### Dependencies

* P01

#### Validation Expectations

* exit status and output.

#### Completion Evidence

* recorded commands.

#### Unresolved Items

* none

<!-- rpi:task id=P02-T02 -->
### P02-T02: Correction record

#### Context

Recovery brief: c9f65c48 was direct-authored; events.jsonl shows no skill activation before this run; session.start selectedModel is claude-sonnet-5.5.

#### Intent

A changes-record section "Historical correction" with: c9f65c48 SHA; directly authored without skill activation (coordinator events audit); the earlier continuity-custody-preparation-122 research, plan, details, changes, review files and state JSON, preserved unchanged; the earlier review is not a Review and its critique was not a critique; observed session.start selectedModel claude-sonnet-5.5, correcting the earlier default-model statement; first real skill invocation rpi-research at 2026-10-21T09:57:08.147Z.

#### Boundaries

* Included: changes record text.
* Excluded: editing the earlier files.

#### Likely Targets

* .copilot-tracking/changes/2026-10-21/continuity-custody-preparation-122-recovery-changes.md

#### Dependencies

* none

#### Validation Expectations

* Text states the adverse history and does not call the earlier files a Review.

#### Completion Evidence

* changes record.

#### Unresolved Items

* none

<!-- rpi:task id=P02-T03 -->
### P02-T03: Commit and freeze

#### Context

Repository rules: resolve `gh api user`, set repo-local noreply email, Conventional Commit, Co-authored-by trailer; no push.

#### Intent

One clean commit and a frozen exact head.

#### Boundaries

* Included: git config --local, commit, status check.
* Excluded: push, PR, heavy gate, rewriting c9f65c48.

#### Likely Targets

* README, plan, details, research, critique, changes, review and state files.

#### Dependencies

* P02-T01, P02-T02 and the Review artifacts

#### Validation Expectations

* `git status --short --ignored` empty; head and base SHAs recorded.

#### Completion Evidence

* changes record lists head, base and actual skill invocations.

#### Unresolved Items

* none
