<!-- markdownlint-disable-file -->

# RPI Plan: climate-paired-alt-source-178-attribution-corr2

## Task Metadata

* Task ID: 178-paired-alt-source-attribution-corr2
* Task slug: climate-paired-alt-source-178-attribution-corr2
* Plan date: 2026-10-22
* Planning status: Ready; one critique completed, PC-001 resolved directly.
* Phase details: .copilot-tracking/details/2026-10-22/climate-paired-alt-source-178-attribution-corr2-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-22/climate-paired-alt-source-178-attribution-corr2-plan-critique.md

## Executive Summary

Carry NASA POWER API name/version out of the hash-checked raw response and into
the generated report, replacing the wildcard attribution with per-source identity,
precise version and retrieval date. Unavailable or imprecise metadata will be
explicitly UNVERIFIED without changing climate-input validation.

### What You May Not Know

The raw fixture already identifies POWER Hourly API v2.10.3; the parser currently
drops it. This is attribution correction only, not licence or owner/legal approval.
The final committed candidate requires a new complete local gate and official
current-base receipt verification before push. The shared heavy lock is a
publication dependency, not permission to interfere with another gate.

## Sources

* .copilot-tracking/research/2026-10-22/climate-paired-alt-source-178-attribution-corr2-research.md: C1-C7, completed ordered research.
* tools/climate_paired_bounds.py and tools/test_climate_paired_bounds.py: canonical generator and test owner.
* docs/reference/research/climate-paired-sample-178/nasa-power-merra2-durham-2023-raw.json: immutable source metadata.
* src/README.md: complete gate and official verifier contract.

## User Decisions and Requirements

* Complete Research, Plan, Implement and Review in order for this distinct dated correction.
* Preserve branch/worktree, prior decisions, original adverse findings and all issue acceptance states.
* Correct published PR #425 provenance from retained metadata, or mark unavailable provenance unverified.
* No licence/reuse approval, malformed-input changes, station-grade expansion, merge or issue closure.
* Resolve authenticated GitHub identity before commit; use local noreply identity and required trailer.
* Commit correction/evidence only; wait for heavy-lock release before full gate, verify against current origin/main, then push without force. Keep PR draft/open and #178 open.

## Goals

* Make precise provenance reproducible from source bytes, not a hardcoded report patch.
* Expose uncertainty without inventing metadata or changing existing validation behavior.

## Scope and Non-Goals

* In scope: generator, focused test owner, generated bounds report, small synthesis/index/log updates and corr2 RPI evidence/state.
* Excluded: raw fixture edits, unrelated data-error handling, model accuracy, source choice, downstream work or acceptance changes.

## Functional Requirements

* FR1: parse_power retains optional API name/version from header.api; unavailable/non-string/blank fields become unavailable metadata, not data rejection.
* FR2: report sources.nasa_power_merra2.api carries the retained fields. Its attribution uses the source's name, numeric major.minor.patch version (optional v prefix), and retrieved_on.
* FR3: absent, malformed or imprecise API identity/version yields explicit UNVERIFIED attribution, never a guessed version.
* FR4: build_report does not mutate shared LICENCE state; source metadata or dates cannot leak across report builds.

## Non-Functional Requirements

* Existing malformed-input rejection tests and data statistics remain unchanged.
* Source metadata is only provenance from hash-checked bytes, not independent service verification or legal approval.
* No new dependency or broad reformat; narrow lint uses installed/pinned Ruff in an external environment if unavailable.

## Acceptance Criteria

* Correction criterion C-A1: retained fixture produces POWER Hourly API v2.10.3 and retrieval date 2026-10-22 in both source provenance and attribution.
* C-A2: constructed different precise metadata and dates flow through; a subsequent missing-metadata report remains UNVERIFIED with no shared-state mutation.
* C-A3: optional metadata absence/non-object/non-string/blank/wildcard cases remain parseable and explicitly UNVERIFIED.
* C-A4: complete committed report regenerates; raw fixture hashes, statistics and approval flags remain unchanged.
* C-A5: python3 tools/test_climate_paired_bounds.py -q and narrow lint pass; independent Review execution/outcome retained honestly.
* C-A6: exact committed head/current origin/main complete gate, official verifier and independent exact-head publication assessment pass before push; reverify immediately before push. This is a publication condition, not an issue acceptance criterion.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct source-bound provenance

* Dependencies: Research Ready, one final-candidate critique disposed.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Carry optional metadata and render precise/unverified attribution

* Expected result: FR1-FR4; no raw fixture or unrelated validator changes.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add focused tests, regenerate report and update related documentation

* Dependencies: P01-T01.
* Expected result: C-A1-C-A5, generated CLI output matches committed report.

## Test Ownership and Validation Lock

* Canonical owner: tools/test_climate_paired_bounds.py.
* Exact removals: none. Maximum additions: four test methods; use subtests for metadata variants.
* Semantic coverage: exact/changed source identity/version/date, explicit unverified behavior and repeated-build isolation.
* Regression coverage: all existing rejection, statistical, monthly and full fixture regeneration tests.
* Canonical target: tools/climate_paired_bounds.py.
* Generated target: docs/reference/research/climate-paired-bounds-178.json, using documented CLI and existing hashes/URLs/date/location.
* Evidence: focused unittest output, narrow Ruff check, git diff --check, structural report comparison.
* Formatting: do not reformat whole existing files merely to adopt new style.

## Dependencies

* Source metadata exists and retained hashes are known (Research C5-C6).
* Publication needs a released shared lock, required gate tools and a stable current base.
* Independent critique and post-implementation Review are distinct one-pass executions.

## Critique Disposition

Execution Complete, verdict Revise, one Medium finding. PC-001 is resolved directly:
C-A6, this handoff and P01-T02 details explicitly retain independent exact-head assessment
after the final gate. No user decision or repeat critique is required.

## Follow-Up Items

* Original licence/reuse confirmation remains with owner/legal; station-grade production precision and regional coverage require a separately selected task. Neither is correction scope.

## Handoff

* Changes record: .copilot-tracking/changes/2026-10-22/climate-paired-alt-source-178-attribution-corr2-changes.md.
* P01, P01-T01 and P01-T02 complete; 30 focused tests, narrow Ruff, exact CLI regeneration and structural comparison passed. Parent continues to one Review.
* Preserve original implementation Review; commit correction and dated evidence, wait for shared-lock release, then run full gate in a new external directory.
* Fetch main and officially verify against current origin/main immediately before independent exact-head publication assessment. Retain assessment externally without altering the candidate; fetch and reverify immediately before push.
* Any assessment failure or changed head/base/inputs/tools/images blocks publication. Corrections require a new gate. Do not repeat the task's original Review or critique.
