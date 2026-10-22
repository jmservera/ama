<!-- markdownlint-disable-file -->
# RPI Phase Details: Paid execution plan #126, post-change forecast correction

## Metadata

* Task ID: 126-postchange-correction
* Task slug: paid-execution-plan-126-postchange-correction
* Related plan: .copilot-tracking/plans/2026-10-22/paid-execution-plan-126-postchange-correction-plan.md
* Evidence sources: .copilot-tracking/research/2026-10-22/paid-execution-plan-126-postchange-correction-research.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
|----------|------|--------|-----------------|
| P01 | Correct wording | ready | P01, P01-T01, P01-T02 |
| P02 | Validate and publish | ready | P02, P02-T01 |

<!-- rpi:phase id=P01 -->
## P01: Correct wording

### Context

Lines in the 2026-10-22 subsection label 14:00Z figures current; the infrastructure state changed afterwards. The "retirement not authorized" sentence also needs to distinguish the owner-authorized cutover-test deletion (done, outside this proposal) from further retirement (still not authorized here).

### Intent

One consistent, dated, non-inventive account.

### Boundaries

* Included: subsection wording, index row, one log entry.
* Excluded: ceiling, thresholds, tranche definitions, history block text (only a cross-reference label if needed).

### Likely Targets

* docs/case_study_48_addendum.md
* docs/reference/README.md
* docs/reference/log.md

### Dependencies

* none

### Validation Expectations

* Search for "current", "no change", "S0" in the subsection: each use is correct or relabelled.

### Completion Evidence

* Diff and changes record.

### Unresolved Items

* Post-change forecast unavailable until cost data catches up.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Edit addendum subsection

#### Context

Add a dated post-change inventory note (91 resources at about 14:53Z, Front Door profile and WAF policy absent, demo API app minimum and running replicas 0, 61 cutover-test names remain, cost read unchanged by lag), relabel the table rows and limits, replace "S0 is the only current baseline", add the refresh gate, and fix the U-blocked sentence.

#### Intent

No contradictory claim.

#### Boundaries

* Included: subsection.
* Excluded: other sections.

#### Likely Targets

* docs/case_study_48_addendum.md

#### Dependencies

* none

#### Validation Expectations

* Arithmetic unchanged and traced.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Edit index row; append log entry

#### Context

Index row repeats the revision; log is append-only.

#### Intent

Consistency.

#### Boundaries

* Included: one row; one appended entry.

#### Likely Targets

* docs/reference/README.md
* docs/reference/log.md

#### Dependencies

* P01-T01

#### Validation Expectations

* Log diff is additions only.

<!-- rpi:phase id=P02 -->
## P02: Validate and publish

### Context

New head requires a new receipt in a new external directory; old receipt preserved.

### Intent

Evidence-backed update of PR #422.

### Boundaries

* Included: commit, gate with long lock timeout, verify, push, PR body.
* Excluded: merge, bypass.

### Likely Targets

* PR #422

### Dependencies

* P01

### Validation Expectations

* Official --verify-receipt against current origin/main.

### Completion Evidence

* Receipt path and hash.

### Unresolved Items

* none known

<!-- rpi:task id=P02-T01 -->
### P02-T01: Gate, verify, push

#### Context

Shared host lock.

#### Intent

Honest validation record.

#### Boundaries

* Included: as above.

#### Likely Targets

* none

#### Dependencies

* P01

#### Validation Expectations

* Receipt verified immediately before push.
