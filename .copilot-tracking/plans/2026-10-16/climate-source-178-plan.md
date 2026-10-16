<!-- markdownlint-disable-file -->
# RPI Plan: Historical climate source

## Task Metadata

* Task ID: 178
* Task slug: climate-source-178
* Plan date: 2026-10-16
* Status: ready for offline documentation only
* Details: .copilot-tracking/details/2026-10-16/climate-source-178-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-16/climate-source-178-plan-critique.md

## Executive Summary

Publish an honest offline source-selection audit in the existing sensor
research plan, linking the current synthetic implementation and its exercise
limits. Full issue acceptance is blocked by absent retrieved records and
dataset licence evidence. No runtime change can remove that evidence gap.

## User Decisions and Requirements

* Deliver issue 178, audit all criteria honestly, publish a PR with Refs #178.
* Offline only; no Azure, private data, legacy-tree or Entra script changes.
* Owner comment dated 2026-10-15 selects Met Office (UKCP18) and Environment
  Agency OGL data where available, otherwise clearly labelled synthetic data.
* Licence remains open until owner confirmation; invent no climate figures.
* Preserve Juan Manuel Servera's exercise Legal, Compliance and DPO boundary.
* Record research, plan, changes and review; update READMEs and append KB log.

## Goals

* Make source selection, retrieval and reuse approval distinct and auditable.
* Prevent synthetic bounds being represented as measured climate evidence.

## Scope and Non-Goals

Four documentation targets: existing sensor research plan, reference index,
reference log and core README; plus requested RPI evidence. No executable
change, importer, fabricated observations, full PRD acceptance or operational
approval. No new knowledge-base page is needed.

## Functional Requirements

* Compare every named candidate across coverage, resolution and reuse evidence,
  explicitly marking unavailable facts rather than asserting product claims.
* Record selected fallback, external source status, null retrieval/licence
  evidence and the local packet needed for reproducible observed extrema.

## Non-Functional Requirements

* Zero climate numbers represented as sourced without retrieved observations.
* No remote source retrieval, deployment or private data access.
* All new relative links resolve; Markdown/diff review passes.

## Acceptance Criteria

* Audit the three issue criteria individually without weakening their meaning.
* Each unavailable dataset fact and each unmet criterion is explicit.
* Do not tick issue criteria or imply that this PR completes the source task.
* Link the existing generator and tests without changing their behavior.

## Sources

Research C1-C5 in
.copilot-tracking/research/2026-10-16/climate-source-178-research.md.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Publish bounded offline evidence

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Update source decision and acceptance audit

Add candidate matrix, owner direction, retrieval/licence register, acquisition
contract, observed-bounds derivation procedure and unchanged safety boundary.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Connect maintainer documentation

Update the core README and reference index, then append the reference log.
Depends on P01-T01.

<!-- rpi:phase id=P02 -->
### [ ] P02: Validate and publish

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Validate and record review

Review only changed documentation and all added local links. Record every
unmet criterion; executable tests, Ruff, mypy and app run are not applicable
because no executable/configuration surface changes. No test additions or
removals; maximum new executable files zero. Canonical target is the existing
research plan; no generated target.

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Commit, push and create PR

Use verified GitHub privacy-safe identity, prescribed trailer, existing clean
topic branch and Refs #178. Leave issue body and merge decision untouched.
Depends on P02-T01.

## Critique Disposition

One independent final-candidate critique executed; verdict Pass for the
offline audit only. PC-001 is a non-blocking publication control: apply
directly by retaining the three unmet criterion dispositions in the final
documents and PR. No divergent user decision and no second critique.

The single Review is complete: Not accepted for full issue delivery because
the three original criteria remain unmet. The bounded documentation work
passes its local checks. Publish a draft contribution only; do not infer
source approval or task acceptance.

## Follow-Up Items

* Retrieve and retain historical records plus licence evidence under a later
  authorization or receive an equivalent local evidence packet.
* Obtain the owner's dataset-specific reuse confirmation, then derive and
  review bounds before changing synthetic plausibility expectations.
