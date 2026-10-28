<!-- markdownlint-disable-file -->

# Implementation Plan: climate-paired-source-178

| Field | Value |
|---|---|
| Task ID | 178-paired-continuation |
| Date | 2026-10-21 |
| Research | .copilot-tracking/research/2026-10-21/climate-paired-source-178-research.md |
| Details | .copilot-tracking/details/2026-10-21/climate-paired-source-178-phase-details.md |
| Critique | .copilot-tracking/reviews/plans/2026-10-21/climate-paired-source-178-plan-critique.md |
| Changes | .copilot-tracking/changes/2026-10-21/climate-paired-source-178-changes.md |

## Executive Summary

Anonymous retrieval of official paired North-East temperature/humidity records is not possible: MIDAS Open file bytes require a CEDA login and EA Hydrology has no humidity or dew point. The plan records a hash-free but fully dated access-evidence blocker as a machine-readable JSON artifact, adds a regression test that the artifact cannot be read as bounds, updates the climate synthesis, index and log, and names the exact owner action. No bounds, thresholds or source approvals are produced.

## User Decisions and Requirements

* Owner 2026-10-15: use Met Office (UKCP18) and EA OGL data where available, otherwise clearly labelled synthetic data (issue 178 comment).
* Synthetic fallback must never be presented as observations or fulfil record-derived bounds.
* No account creation, credentials, paid services, private data or prohibited scraping; no silent source substitution; licence/reuse owner confirmation stays UNMET.
* No indoor or retrofit equations (#179+). No push, PR or merge; coordinator runs the full gate.

## Goals

* Deliver a grounded input/bounds artifact or a precise evidence-backed blocker. Evidence supports the blocker.

## Scope and Non-Goals

* In scope: blocker evidence JSON under docs/reference/research/, focused test, synthesis/index/log update.
* Non-goals: bounds, thresholds, alternative-source retrieval, importer changes, model code, whole-issue closure.

## Functional Requirements

* FR1: Artifact lists each probed endpoint, test date, outcome class, licence statement observed, and listing-only station year coverage.
* FR2: Artifact states bounds status `unavailable`, humidity status `unavailable`, owner reuse approval `UNMET`, and no synthetic substitution.
* FR3: Artifact names the owner action: an authorised human uses their own existing CEDA account, supplies the licence text and files, owner records reuse approval and confirms station choice; or owner explicitly approves another source. No agent account creation.
* FR4: Artifact records probe method (curl, no cookies, 2026-10-21 01:23-01:25Z), MIDAS licence observed on the CEDA catalogue page retrieved 2026-10-21 (README licence file itself Unauthenticated), UKCP18 disposition (projections plus observations family; no anonymous hourly paired historical product identified; not probed as a data source, not a substitute) and synthetic-fallback disposition (owner-permitted only as clearly labelled synthetic, never observation, never record-derived bounds; none produced here). Retest trigger: owner action, CEDA access policy change, or new official anonymous paired source.

## Non-Functional Requirements

* No secrets or IDs; ASCII; plain tracking paths; existing conventions for docs.

## Acceptance Criteria

* AC1: JSON validates and the focused test passes. Test asserts required statuses and that no key named like min/max/bound/threshold/percentile holds a number (recursive scan).
* AC2: Synthesis subsection, README index row for the #178 climate topic (found by its text, not line number) and log entry updated; issue criteria remain unticked.
* AC3: Original research, plan, critique, details, changes, review artifacts committed.

## Phase Checklist

<!-- Phase P01 -->
### [x] P01: Evidence artifact and regression

<!-- P01-T01 -->
* [x] P01-T01: Create docs/reference/research/climate-paired-source-blocker-178.json from research W1-W5.
<!-- P01-T02 -->
* [x] P01-T02: Add tools/test_climate_paired_blocker.py asserting required fields/statuses and absence of numeric bounds.

<!-- Phase P02 -->
### [x] P02: Synthesis, index, log

<!-- P02-T01 -->
* [x] P02-T01: Add subsection to iot-sensor-analytics-research-plan.md and update index row in docs/reference/README.md.
<!-- P02-T02 -->
* [x] P02-T02: Append log entry to docs/reference/log.md.

## Follow-Up Items

* Owner/authorised human with own CEDA account supplies MIDAS qcv-1 CSVs, or approves alternative no-login source; then add adapter and derive bounds (new task).
* Existing tools/climate_station_bounds.py reuse for hourly adapter is a candidate for that task.

## Critique Disposition

Critique executed once (verdict Revise, PC-001..PC-007, all direct planner corrections): PC-001 applied (catalogue licence retrieved today, FR4); PC-002 applied (FR4 dispositions); PC-003 applied (AC1 recursive numeric scan); PC-004 applied (P01 unchecked, this section); PC-005 applied (AC2); PC-006 applied (FR4 method/retest); PC-007 applied (FR3). No user decision required, no second critique.

## Corrective Plan Addendum (2026-10-21, after failed complete gate)

Original research, critique, plan and Review remain unchanged; no second original Review. Gate failed 2026-10-21T03:40:37Z with only CRITICAL GHSA-6q48-6c7w-9gw2 (certifi 2026.7.22, fixed 2026.10.19). Scope: reuse the four requirements files from shared commit a3257c71 only, provisional until own complete gate and independent assessment.

* [x] C01-T01: Apply the exact four requirements files and verify pin/hash consistency.
* Climate source semantics, blocker status and all #178 criteria unchanged (unmet).
