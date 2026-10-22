<!-- markdownlint-disable-file -->
# RPI Phase Details: Paid execution plan #126, revised USD 700 demo budget

## Metadata

* Task ID: 126-demo-budget-700
* Task slug: paid-execution-plan-126-demo-budget-700
* Related plan: .copilot-tracking/plans/2026-10-22/paid-execution-plan-126-demo-budget-700-plan.md
* Evidence sources: .copilot-tracking/research/2026-10-22/paid-execution-plan-126-demo-budget-700-research.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
|----------|------|--------|-----------------|
| P01 | Revise costed plan synthesis | ready | P01, P01-T01, P01-T02 |
| P02 | Validate and publish | ready | P02, P02-T01 |

<!-- rpi:phase id=P01 -->
## P01: Revise costed plan synthesis

### Context

The 2026-10-20 subsection states a USD 500 total, thresholds 400/450/475, R 30 and options S0 to S2 (S1, S2 need Front Door retirement or SQL idling). Fresh evidence moves the observed figure and the owner ceiling.

### Intent

Current-ceiling subsection; USD 500 history preserved.

### Boundaries

* Included: addendum subsection, index row, log append, ms.date.
* Excluded: other sections, source code, infrastructure.

### Likely Targets

* docs/case_study_48_addendum.md: revise the subsection.
* docs/reference/README.md: revise the index row.
* docs/reference/log.md: append an entry.

### Dependencies

* none

### Validation Expectations

* Arithmetic re-computed from the research table; no identifiers in the diff.

### Completion Evidence

* Diff and changes record.

### Unresolved Items

* U unknown; role assignment unverified.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Update addendum subsection

#### Context

Replace the ceiling, rerun observed and forecast, restate envelope and thresholds on 700 (E at most 655; review 560; pause 630; stop 665), add B1 private-Blob option and keep T1 to T3 as bounded additions, mark the prior text "history, 2026-10-20".

#### Intent

A reader sees one current decision and dated history.

#### Boundaries

* Included: subsection only.
* Excluded: Front Door retirement as an option (not authorized).

#### Likely Targets

* docs/case_study_48_addendum.md

#### Dependencies

* none

#### Validation Expectations

* Each number traces to the research table.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Update index row and append log entry

#### Context

Log is append-only and shared with other loops; keep every existing entry.

#### Intent

Index points to the revised subsection; a new 2026-10-22 entry records the change.

#### Boundaries

* Included: one row, one appended entry.
* Excluded: earlier entries.

#### Likely Targets

* docs/reference/README.md
* docs/reference/log.md

#### Dependencies

* P01-T01

#### Validation Expectations

* git diff shows only an addition in the log.

<!-- rpi:phase id=P02 -->
## P02: Validate and publish

### Context

Repository requires the full local RPI gate and receipt verification before push.

### Intent

Evidence-backed publication to existing draft PR #422.

### Boundaries

* Included: commit, gate, receipt, push, PR body.
* Excluded: merge, review checkboxes, closing keywords.

### Likely Targets

* PR #422 body.

### Dependencies

* P01

### Validation Expectations

* tools/rpi-checks.py --all with the external receipt, then --verify-receipt.

### Completion Evidence

* Receipt path and hash.

### Unresolved Items

* Docker, SQL or other prerequisites may block the gate; record, do not fake.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run gate and update PR

#### Context

Heavy gates serialize on the existing lock.

#### Intent

Pushed branch, updated PR text, honest validation record.

#### Boundaries

* Included: as above.
* Excluded: bypass flags.

#### Likely Targets

* none

#### Dependencies

* P01

#### Validation Expectations

* Receipt verifies against the current origin/main.
