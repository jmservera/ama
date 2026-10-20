<!-- markdownlint-disable-file -->
# RPI Phase Details: Authenticated roster transport design (#360), recovery cycle

## Metadata

* Task ID: demo-transport-plan-360-recovery
* Task slug: demo-transport-plan-360-recovery
* Related plan: .copilot-tracking/plans/2026-10-20/demo-transport-plan-360-recovery-plan.md
* Evidence sources: .copilot-tracking/research/2026-10-20/demo-transport-plan-360-recovery-research.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
|----------|------|--------|-----------------|
| P01 | Correct and disclose in the runbook design | ready | P01, P01-T01, P01-T02 |
| P02 | Records and clarifications | ready | P02, P02-T01 |
| P03 | Review, freeze and gate | ready | P03, P03-T01 |

<!-- rpi:phase id=P01 -->
## P01: Correct and disclose in the runbook design

### Context

The existing section already carries T1-T8, AAD v2, trust assumption, threat table, S0-S7, DN1-DN5 and a 13-row checklist. Research confirmed it and found qualified-wording and coverage gaps (Merge overwrite semantics W2, Activity Log content uncertainty W3, execution ID known to controller C9).

### Intent

Targeted edits, not a rewrite.

### Boundaries

* Included: wording, two threat rows, disclosure paragraph.
* Excluded: new options, claims of success, cost figures, any change outside the section.

### Likely Targets

* infra/README.md: design section.
* docs/architecture/cutover-evidence-pack.md: entry.

### Dependencies

* None

### Validation Expectations

* Link and ASCII review; git diff limited to allowed files.

### Completion Evidence

* Diff hunks and changes record.

### Unresolved Items

* None for the design; DN1-DN5 stay open by design.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Sharpen authentication claim and add threat rows

#### Context

Requirements table says "Authorization: Entra and Azure RBAC"; "Integrity" relies on AEAD. C5 shows no worker authentication. W2: Merge updates existing names; C8 shows the worker guards by intersection, but a different principal with tags/write could still overwrite or delete.

#### Intent

State plainly that access control is Entra/RBAC and result authenticity is key possession; add threat rows for overwrite of an owned frame name by another tag writer (detected by AEAD, causes refusal) and Activity Log exposure unknown.

#### Boundaries

* Included: README section edits.
* Excluded: other sections.

#### Likely Targets

* infra/README.md: threat table and requirements table.

#### Dependencies

* None

#### Validation Expectations

* Rows cite W2 and W3 with URLs.

#### Completion Evidence

* Diff hunk.

#### Unresolved Items

* Whether Activity Log records tag values (recorded as unverified).

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add process disclosure to runbook and evidence pack

#### Context

Coordinator audit: first draft authored without skills.

#### Intent

One short dated paragraph in each of the runbook design status block and the evidence-pack entry naming the recovery artifacts and stating the first draft is unverified history superseded for verification.

#### Boundaries

* Included: short paragraphs.
* Excluded: claims of independent acceptance.

#### Likely Targets

* infra/README.md, docs/architecture/cutover-evidence-pack.md

#### Dependencies

* P01-T01

#### Validation Expectations

* Wording review.

#### Completion Evidence

* Diff hunk.

#### Unresolved Items

* None

<!-- rpi:phase id=P02 -->
## P02: Records and clarifications

### Context

Log is append-only; old artifacts are history.

### Intent

New entries and appended notes only.

### Boundaries

* Included: append to log, update index sentence if needed, append clarification sections to old artifacts.
* Excluded: editing existing log entries, renaming or deleting artifacts.

### Likely Targets

* docs/reference/log.md, docs/reference/README.md, old .copilot-tracking draft files.

### Dependencies

* P01

### Validation Expectations

* git diff shows additions only in old artifacts and log.

### Completion Evidence

* Diff stat.

### Unresolved Items

* None

<!-- rpi:task id=P02-T01 -->
### P02-T01: Log, index and clarification notes

#### Context

Old state JSON wrongly says completed; append a clarification without removing fields (add a new key only).

#### Intent

Honest history.

#### Boundaries

* Included: append-only changes.
* Excluded: deletions.

#### Likely Targets

* docs/reference/log.md, old state JSON (additive key), old md artifacts (appended section).

#### Dependencies

* P01

#### Validation Expectations

* diff has no removed lines for these files, except index sentence if edited.

#### Completion Evidence

* Diff stat.

#### Unresolved Items

* None

<!-- rpi:phase id=P03 -->
## P03: Review, freeze and gate

### Context

Local gate required by repository instructions.

### Intent

Single review, commit, gate, receipt.

### Boundaries

* Included: rpi-review once, commit, gate.
* Excluded: push, PR, merge.

### Likely Targets

* tools/rpi-checks.py run only.

### Dependencies

* P01, P02

### Validation Expectations

* Receipt verifies against fresh origin/main.

### Completion Evidence

* Receipt path and hash.

### Unresolved Items

* Gate queueing on shared lock.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Commit and run the full gate

#### Context

Other tasks hold the heavy lock; the runner queues. Commit set: infra/README.md, docs/architecture/cutover-evidence-pack.md, docs/reference/README.md, docs/reference/log.md, .copilot-tracking recovery artifacts and appended clarifications. Fetch origin/main, record SHA, run PATH="/tmp/rpi-413-tools:$PATH" PYTHONDONTWRITEBYTECODE=1 python3 tools/rpi-checks.py --all --base SHA --out NEWDIR, then --verify-receipt. Allowlist check: git diff --name-only against base contains only those paths; denylist: no budget/benefits, cohort, Finance, map files. ASCII check on added lines; link review of added URLs.

#### Intent

Frozen candidate.

#### Boundaries

* Included: commit with noreply email and trailer.
* Excluded: amend, outer flock, killing others' processes.

#### Likely Targets

* none

#### Dependencies

* P01, P02, review

#### Validation Expectations

* --verify-receipt passes.

#### Completion Evidence

* Receipt JSON.

#### Unresolved Items

* None

## Dated Correction 2026-10-20

P01-T01 scope extended only by the spending-gate wording in infra/README.md and the evidence pack row; no new tasks.
