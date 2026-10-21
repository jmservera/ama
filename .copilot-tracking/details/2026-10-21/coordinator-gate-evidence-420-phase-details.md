<!-- markdownlint-disable-file -->
# RPI Phase Details: PR420 gate-evidence correction

## Metadata

* Task ID: 420-gate-evidence
* Task slug: coordinator-gate-evidence-420
* Related plan: .copilot-tracking/plans/2026-10-21/coordinator-gate-evidence-420-plan.md
* Evidence sources: .copilot-tracking/research/2026-10-21/coordinator-gate-evidence-420-research.md

## Phase Index

| Phase ID | Name                        | Status | Detail sections        |
|----------|-----------------------------|--------|------------------------|
| P01      | Correct evidence wording    | complete | P01, P01-T01, P01-T02  |
| P02      | Validate, review and freeze | complete | P02, P02-T01           |

<!-- rpi:phase id=P01 -->
## P01: Correct evidence wording

### Context

validation-01 line 29 conflates "no general doc lint/build command" with "application gates not required" (research C1, C3, C4).

### Intent

Truthful row, scoped verdict, preserved original wording elsewhere.

### Boundaries

* Included: validation-01 line 29 and verdict; new validation-02.
* Excluded: author-01, review-01 (no gate claim, C6, C7), agent source (C5), original static-only history.

### Likely Targets

* .copilot-tracking/hve-builder/2026-10-20/coordinator-sonnet-55-validation-01.md: row and verdict.
* .copilot-tracking/hve-builder/2026-10-21/coordinator-sonnet-55-validation-02.md: correction record.

### Dependencies

* none

### Validation Expectations

* Diff versus f3e8a8f1 shows only tracking files changed; `git diff --check` clean.

### Completion Evidence

* Changes record lists edits with before and after text.

### Unresolved Items

* none

<!-- rpi:task id=P01-T01 -->
### P01-T01: Edit line 29 and verdict scope in validation-01

#### Context

C1, C2, C9.

#### Intent

Replace the row with: complete local RPI gate not run in this mechanical stage, remains separately mandatory on the final exact head before publication; repo-wide doc lint/build has no general command. Scope the verdict to mechanical validation and add a dated correction note pointing to validation-02.

#### Boundaries

* Included: line 29, verdict line, one correction note.
* Excluded: any other row or claim of execution.

#### Likely Targets

* .copilot-tracking/hve-builder/2026-10-20/coordinator-sonnet-55-validation-01.md

#### Validation Expectations

* Row no longer says "none exist or required" for the gate.

#### Completion Evidence

* Diff and grep.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add dated validation-02 correction record

#### Context

C3 to C6; launch clarification.

#### Intent

Draft original quote, why false, corrected wording; after P02-T01 runs the focused checks append them with exact commands and results (never before they run); HVE validation disposition (static/mechanical; behavior gate unchanged: skipped, not run), and that the coordinator owns the full gate.

#### Boundaries

* Included: frontmatter per repository convention, tables.
* Excluded: claims of gate or receipt.

#### Likely Targets

* .copilot-tracking/hve-builder/2026-10-21/coordinator-sonnet-55-validation-02.md

#### Validation Expectations

* Every listed check has a command and result from this session.

#### Completion Evidence

* File exists and matches the changes record.

<!-- rpi:phase id=P02 -->
## P02: Validate, review and freeze

### Context

Launch clarification supersedes the old brief's worker full-gate.

### Intent

Focused checks, one Review, commit, freeze.

### Boundaries

* Included: git diff checks, tracked-source diff, markdown frontmatter sanity, review artifact, commit.
* Excluded: tools/rpi-checks.py --all, heavy lock, push, PR, merge.

### Likely Targets

* .copilot-tracking/reviews/logs/2026-10-21/coordinator-gate-evidence-420-review.md
* .copilot-tracking/changes/2026-10-21/coordinator-gate-evidence-420-changes.md

### Dependencies

* P01

### Validation Expectations

* Clean worktree after commit; HEAD recorded.

### Completion Evidence

* Review artifact and final state record.

### Unresolved Items

* none

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run focused checks and HVE validation; one Review; commit evidence

#### Context

hve-builder validation conventions: mechanical stage only.

#### Intent

Clean frozen head, gate left to coordinator.

#### Boundaries

* Included: as P02.
* Excluded: as P02.

#### Likely Targets

* as P02

#### Validation Expectations

* git fetch origin main with base SHA recorded; gh api user noreply email set locally; grep that validation files say the gate is not run and separately mandatory; diff of validation-01 limited to line 29, verdict line and correction note; one Conventional Commit with Copilot trailer, no amend; git status clean; git diff f3e8a8f1..HEAD --stat limited to tracking.

#### Completion Evidence

* HEAD SHA in the final report.

<!-- rpi:phase id=P03 -->
## P03: Gate-failure dependency correction

### Intent

Clear certifi advisory GHSA-6q48-6c7w-9gw2 with only the four lockfile files from shared commit a3257c71; no tracking or map edits from that commit.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Reuse four requirements lockfiles from a3257c71

* Boundaries: only the four requirements.txt files; no other pins, scans or controls; src/agents has no certifi pin and is unchanged.
* Validation: byte comparison to a3257c71, pin/hash consistency check, grep for old pin, pip --require-hashes download of the pinned wheel, git diff --check. No build or full gate.
* Completion evidence: changes record P03-T01.

