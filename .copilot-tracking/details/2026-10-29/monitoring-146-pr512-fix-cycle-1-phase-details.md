<!-- markdownlint-disable-file -->
# RPI Phase Details: Workbook fuzzy-union correction

## Metadata

* Task ID: issue-146-pr-512-fix-cycle-1
* Task slug: monitoring-146-pr512-fix-cycle-1
* Date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/monitoring-146-pr512-fix-cycle-1-plan.md
* Research: .copilot-tracking/research/2026-10-29/monitoring-146-pr512-fix-cycle-1-research.md (C1-C4)

## Phase Index

| Phase | Status | Details |
| --- | --- | --- |
| P01 | Complete | P01-T01, P01-T02 |
| P02 | Complete locally | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Correct and validate source contract

Context: Fuzzy resolution operates on union sources; projecting inside the absent source is the reported binding defect. Typed datatables must still establish empty schemas. Scope is source-only; no live table/error simulation is claimed.
Intent: Fix both source expressions and preserve calculations.
Targets: infra/monitoring-workbook.json, infra/tests/test_monitoring_workbook.py, infra/README.md.
Boundaries: No other workbook panels, infrastructure parameters or runtime logic.
Dependencies: Research Ready and critique dispositions closed.
Completion evidence: Red/green shape regression; exact unchanged suffix after samples statement; local scoped tests and lint.
Unresolved items: None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Regression and source correction

Load the workbook using json.loads and index items by name. One subTest per query checks the initial statement against a constructed exact expected typed fallback/bare table/post-union project statement. Assert initial statement equality so nested source projection, missing fallback, wrong table or moved/missing outer projection fail.
Requests schema: TimeGenerated:datetime, _ResourceId:string, ItemCount:int, Success:bool, DurationMs:real.
Availability schema: Same four shared fields, without DurationMs.
Run test against old source first. Preserve failure evidence, then change source. Test exactness is deliberate for this source-binding contract; harmless formatting changes may require updating its expected shape.
Add a short README explanation of the fallback boundary and source-only testing limit.
No new helper abstraction, dependencies or generated files. Completion: both old subtests fail, new subtests pass, existing query suffixes unchanged.
Actual evidence: Old workbook produced two subtest assertion failures; corrected workbook passes. Structural comparison against starting HEAD confirms unchanged query suffixes, panel metadata and all other workbook content. README documents source-only contract. New test formatted with existing Ruff.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Validation

Use the five existing infra test modules from the prior monitoring/rebase evidence plus the new module. REQUIRE_AZ_BICEP=1 prevents missing compiler from becoming an unnoticed skip. Existing test_bicep_policy compile_bicep invokes only local az bicep build, not a cloud operation.
Run JSON parse, isolated Ruff check with E,F,I,B,UP, target py312 and line length 100, and isolated format --check on the single new module. Record actual outputs/counts and errors explicitly; no unrun full suite or publication receipt claimed.
Use external session storage for validation logs; do not touch latest.json. Completion: all scoped required checks pass with zero skips.
Actual evidence: 92 tests passed in 71.576s, zero skips; valid JSON; isolated Ruff E,F,I,B,UP/py312/100 and format --check passed on the new module. git diff --check passed. Log pointers and actual command groups are in the changes record.

<!-- rpi:phase id=P02 -->
## P02: Review and local commit

Context: User requests one full RPI correction cycle, not publication.
Intent: Preserve independent review and commit source/evidence locally.
Boundaries: Review writes only its dated artifact; no Azure operations or remote writes.
Dependencies: P01 test results reconciled into plan/details/changes.
Completion evidence: One independent Review result, local commit metadata and clean status.
Unresolved items: Full publication gates and operational approval are future boundaries, not local acceptance.

<!-- rpi:task id=P02-T01 -->
### P02-T01: One independent Review

Use a fresh worker, provide source diff from starting head, canonical plan/details/critique/changes and exact log locations. Require Review execution separate from outcome and findings grounded in the correction. Preserve original adverse findings. Route any newly found work to a later task, not a second Review.
Actual evidence: Single independent Review execution Complete / outcome Conformant, zero RV findings or local blockers. Reviewer inspected all original logs, independently ran the new test/JSON/diff checks and verified exact workbook invariants. No second Review and no final-head/publication approval claimed.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Commit and handoff

Resolve gh api user (already returned id 8036360/login jmservera), configure repository-local privacy-safe identity for both author and committer. Stage finite task-owned file list and commit with required trailer and Refs #146.
Record completed local task separately from automatic session status. No follow-up source work without selection. Do not push. Final verification checks actual commit, changed paths and clean status; evidence cannot self-contain its final commit hash.
Actual evidence: Local commit 64096930e0c219184500fa00015d29f54e942c3f contains exactly ten task-owned paths. Commit metadata has expected privacy-safe author/committer, Refs #146 and exact Copilot trailer; status was clean after commit. This metadata-only finalization records completed P02 and session handoff. No new source or second Review.
