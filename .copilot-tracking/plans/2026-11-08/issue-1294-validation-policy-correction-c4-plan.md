<!-- markdownlint-disable-file -->
# Plan: issue-1294-validation-policy-correction-c4

* Task ID: issue-1294-validation-policy-correction-c4 (bounded correction C4, parent: issue-1294-validation-policy-correction-c3; fourth and final cycle)
* Base: HEAD 2f1aa2e4d42b79364b95622d6198975203c1417e, tree 97b940c4824d22ddb7bd9a6d54fc926beb960f77; origin/main fa7ae0c9770e890f82482456bfcb8e97f1e05429
* Research: .copilot-tracking/research/2026-11-08/issue-1294-validation-policy-correction-c4-research.md
* Details: .copilot-tracking/details/2026-11-08/issue-1294-validation-policy-correction-c4-phase-details.md
* Changes record (implementation owns): .copilot-tracking/changes/2026-11-08/issue-1294-validation-policy-correction-c4-changes.md

## Executive Summary

Eight C3 readiness findings were all confirmed against the workflow, selector and runner. Plan: in one batch, correct src/README.md (selected-project hosted checks, separate data guard, widening from accompanying paths, partial-receipt BASE RELAXED versus exact-base full receipts, SQL example path, self-contained focused command with failed-run-only resume); add an append-only log correction; record provenance corrections for the C3 dirty pre-run status and the exact report-4 tested boundary; record the strict loader probe. Then obtain an independent fresh-context HVE static assessment of the complete corrected targets (targeted closure if Revise), then a fresh full independently designed and graded behavior run on the final state, then Review and commit. Focused tier. Proxy profile (host cannot bind subagent models). No hosted CI claim. At most two behavior attempts; a final Revise is reported as Revise.

## User Decisions and Requirements

* Fix confirmed contract or evidence defects in one coherent batch, not cosmetic preferences; disposition every finding with evidence.
* Obtain canonical independent HVE static assessment (or targeted closure) of complete corrected targets; record blob/hash identities, executor, verdict, stage status, scope; behavior simulation and RPI self-review are not substitutes; preserve the earlier self-assessment as historical; state the blocker if unavailable.
* README: correct selected project checks, unconditional data guard, widening from accompanying paths, BASE RELAXED vs exact-base full receipts, SQL example path, self-contained focused example; verify against the CI selector and runner.
* Strict read-only loader probe failing on loader.errors and checking the exact three flattened IDs; new provenance corrections for the C3 dirty pre-run status and report-4 tested boundary; no rewriting of retained raw evidence, reports or append-only history.
* Behavior stage after the complete correction under actual final-state and correction-run rules; capture source identities and later edits; proxy honesty; retain-sandbox; do not check the human box.
* Raw-patch whitespace findings recorded separately from source-document diff check. Preserve everything; no push, PR, board, rebase, cleanup, workflow/source change.

## Goals

* Guide statements match src-ci.yml, tools/ci-affected.py and tools/rpi-checks.py behavior.
* Independent final-state static and behavior evidence with honest labels and identities.

## Scope and Non-Goals

* In scope: src/README.md; docs/reference/log.md (append); C4 tracking evidence; sandbox 5; report 5 (and 6 if a second attempt is needed); static review log.
* Non-goals: workflow, tool, source, SQL, infra, Docker, installs, branch protection, instruction files unless static review finds a confirmed defect, cosmetic rewrites, a fifth cycle.

## Functional Requirements

* FR1 (F2) README states: project unit, lint and type steps run only for selected projects (selection fails open); a README-only change touching exactly `src/README.md` (or `src/<project>/*.md`) selects no project, namespace or mssql; `src-no-working-data` and `src-changes`/`image-paths` run separately whenever the workflow starts; unknown `src/` directories, dependency manifests and accompanying non-src paths widen selection; hosted results are not observed.
* FR2 (F3) README separates full receipts (exact base; rerun on any later commit, correction, base or tool/image change) from partial receipts (BASE RELAXED may keep the receipt valid; verification failure, other changes or expired checks require a new run).
* FR3 (F5) SQL example uses `src/core/src/zava_forward/core/mssqlstore.py`; hosted column states core selects all projects, namespace and mssql.
* FR4 (F6) Focused command block fetches origin/main and sets BASE_SHA; `--resume` shown separately only for a failed receipt.
* FR5 (F4) Strict loader probe recorded; C3 count-only probe qualified by a provenance correction.
* FR6 (F7, F8, whitespace) Provenance corrections in the C4 changes record and report 5; raw evidence untouched.
* FR7 (F1) Independent static assessment, targeted closure when Revise, then final-state behavior run.

## Non-Functional Requirements

* Read-only Python with PYTHONDONTWRITEBYTECODE=1; ASCII; workspace-only outputs; no filesystem-root search; append-only log.

## Acceptance Criteria

* AC1 Each README claim in FR1-FR4 matches the selector probe and workflow evidence recorded in sandbox 5 checks.
* AC2 Loader probe exits 0 with the runner path and 1 without; outputs retained.
* AC3 Static review log with file and blob hashes, executor agent type, rubric, label "proxy independent static assessment, not canonical host-bound HVE stage", verdict, status, scope; static record hashes equal the committed targets; behavior report 5 with proxy label and source identities.
* AC4 Source-document `git diff --check`, link scan, ASCII and append-only checks exit 0; raw-patch whitespace recorded separately.
* AC6 Tier basis recorded: documentation and guide only; no workflow, tool, dependency, Dockerfile, SQL, security-control or deployment change; README edit does match the Source CI path filter; hosted CI unobserved; reclassify if static review forces an instruction-file change.
* AC5 Prior artifacts, sandboxes, reports and pycache intact; focused tier recorded.

## Phase Checklist

<!-- rpi:phase P01 -->
* [x] P01 Guide and log corrections
  * [x] P01-T01 README corrections (FR1-FR4)
  * [x] P01-T02 Append log correction (FR5)
<!-- rpi:phase P02 -->
* [x] P02 Independent static assessment and closure (FR7)
  * [x] P02-T01 Fresh-context static review of the corrected targets; closure if Revise
<!-- rpi:phase P03 -->
* [x] P03 Final-state behavior loop (FR7)
  * [x] P03-T01 Behavior attempt(s), cap two
<!-- rpi:phase P04 -->
* [x] P04 Validation, Review, commit
  * [x] P04-T01 Focused checks and probes (FR5)
  * [x] P04-T02 Changes record with provenance corrections (FR6), Review, commit

## Critique Disposition

| ID | Severity | Disposition |
|---|---|---|
| PC-001 | High | Applied: any source edit after the static stage needs a targeted static closure on the edited hunks and original finding IDs before the next behavior attempt; the final static record states sha256 and blob IDs equal to the committed targets; a still-Revise closure is reported Revise (details P02-T01, P03-T01). |
| PC-002 | Medium | Applied: AC3 and P02-T01 require the label "proxy independent static assessment, not canonical host-bound HVE stage", the executor agent type and rubric; dispatch failure is a recorded deferral, never a Pass. |
| PC-003 | Medium | Applied: resume example uses the failed receipt's recorded base, not a fresh origin/main; fetch and BASE_SHA only for the fresh run. |
| PC-004 | Medium | Applied: the receipt paragraph cross-references the BASE RELAXED rule (verify prints BASE RELAXED, else rerun); full-tier exact-base wording unchanged. |
| PC-005 | Low | Applied: note image-paths dependency; markdown inert rule worded "markdown directly in src/ or under a project directory"; selector run on the real candidate file list after the final edit. |
| PC-006 | Low | Applied: probe command text and environment saved as a new sandbox 5 check file; states import and name resolution only, no browser run. |
| PC-007 | Medium | Applied: F7/F8 corrections go in the P01-T02 correction entry and the changes record independent of report 5; report 5 and the record state the outcome entry and tracking records were appended after grading and not simulated. |
| PC-008 | Low | Applied: AC6 and a changes-record section record tier, basis, planned checks, ran versus not ran, hosted CI unobserved. |

## Follow-Up Items

* Host model binding for subagents (proxy limitation) remains a residual limitation.
* Human acceptance of behavior and static proxy evidence; independent exact-head assessment; hosted CI observation after publication.
