<!-- markdownlint-disable-file -->
# RPI Plan: iteration-scenario-manifest-103

## Task Metadata

Task #103; date 2026-10-17; implementation complete, Review Complete/Conformant.
Details: .copilot-tracking/details/2026-10-17/iteration-scenario-manifest-103-phase-details.md.
Critique: .copilot-tracking/reviews/plans/2026-10-17/iteration-scenario-manifest-103-plan-critique.md.

## Executive Summary

Complete the existing manifest's accountability and offline enforcement, not
the whole application. All eleven/nine full journey paths remain unavailable
in this iteration; existing partial IA evidence is separately preserved.
No data generation or invented approval is necessary.

## User Decisions and Requirements

* Exactly #103's two criteria; no dependencies, parent #100 hierarchy only.
* Full ordered RPI with one research manager refinement and one critique/review.
* Reuse inventory, #174 registry and existing tiny constructed test recipe.
* No private reads, stock regeneration, services, paid calls or UI changes.
* Commit all dated evidence, push requested branch, main PR Refs #103; no merge.

## Goals

* Prevent omitted/duplicate identities, unsupported status claims, stale source
  versions and identifying fixture substitution from passing silently.

## Scope and Non-Goals

Current public scenario manifest and needs inventory, existing synthesis/index/log,
offline shared Python validator and focused enforcement tests. No runtime
workflow/API/UI changes, no new registry or fixture population, no platform
or human acceptance.

## Functional Requirements

* Reuse exact canonical profile/workflow IDs; each has reason, profile/journey
  path, safe endpoint/unknown and separately scoped IA provenance.
* Existing fixture recipe is versioned and bound by source digests; disclose
  exact three-case IDs, role defaults and no implicit selection.
* Status vocabulary represented/unavailable/deferred. Represented requires
  scenario/fixture/check/result provenance; deferred requires explicit decision
  evidence. Current twenty entries unavailable; no false approvals.
* Preserve reciprocal inventory binding and pending owner status; existing
  #174 registry remains the evaluation registry.

## Non-Functional Requirements

* Validator is offline, typed, fail-closed with actionable ValueError; reads
  only explicit public repository files, never a working-data default.
* Tiny fixture metadata only, with synthetic/contains-real-data declarations,
  source allowlist and drift checks; no private dataset privacy attestation.

## Acceptance Criteria

1. Manifest is versioned and lists every profile and workflow as represented,
   unavailable or deferred.
2. Data stays constructed and non-identifying.

## Sources

Research: .copilot-tracking/research/2026-10-17/iteration-scenario-manifest-103-research.md.
C1-C5 and one Programme Manager review support this bounded solution.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Enforce and publish current manifest

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add failing contract/mutation tests

Lock test ownership: core tests own metadata integrity and mutation rejection;
existing needs-inventory tests own reciprocal bindings. No browser changes or
browser rerun claims. Existing IA fixture/source contents remain unchanged.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Implement validator and version manifest

At most one helper module and one new test file; no new dataset payload or
registry. Update existing inventory only for reviewed date/version and SN-11
truthfulness. Retain old manifests through Git history. No removals.

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Validate and document exact criterion evidence

Targeted core unittest (including mutations and inventory), scoped Ruff/mypy,
Markdown/link/diff inspection. Dependencies restored only after missing import.
Existing CI core discovery runs enforcement automatically.

## Dependencies

None. #100 hierarchy and closed #174 prior art are not dependencies.

## Critique Disposition

One final-candidate critique executed: Complete/Pass, zero PC findings.
No revisions or further critique required.

## Follow-Up Items

* Full eleven/nine journey and human/application acceptance remain separate
  FR-035/CON-007 work, not acceptance claims of this offline iteration.

## Handoff

Changes record: .copilot-tracking/changes/2026-10-17/iteration-scenario-manifest-103-changes.md.
P01-T01/T02/T03 complete. 29 focused tests, scoped Ruff/format/mypy,
12 new relative links/anchors and whitespace checks pass. One
post-implementation Review Complete/Conformant. No blocker; parent publishes
the committed artifacts and main PR, then stops as requested.
