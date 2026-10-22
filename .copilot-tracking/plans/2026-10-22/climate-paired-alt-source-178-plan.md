<!-- markdownlint-disable-file -->

# Implementation Plan: climate-paired-alt-source-178

| Field | Value |
|---|---|
| Task ID | 178-paired-alt-source |
| Date | 2026-10-22 |
| Research | .copilot-tracking/research/2026-10-22/climate-paired-alt-source-178-research.md |
| Details | .copilot-tracking/details/2026-10-22/climate-paired-alt-source-178-phase-details.md |
| Critique | .copilot-tracking/reviews/plans/2026-10-22/climate-paired-alt-source-178-plan-critique.md |
| Changes | .copilot-tracking/changes/2026-10-22/climate-paired-alt-source-178-changes.md |

## Executive Summary

A usable paired hourly temperature and relative-humidity sample for Durham, North East England, was retrieved anonymously from the Open-Meteo Historical Weather API (ERA5 reanalysis; Open-Meteo publishes CC BY 4.0 API data terms and a non-commercial free tier; underlying C3S reuse is not independently verified) with NASA POWER as a cross-check. The plan adds an offline, hash-pinned validating adapter that rejects missing, misaligned, fabricated or inconsistent humidity, derives sample bounds from the retrieved records, and records them in a labelled "modelled, not observed" report. It integrates the result into the existing IoT synthesis, index and log. Licence confirmation, production precision and representativeness stay explicitly pending. The 2026-10-21 blocker and the Durham temperature-only evidence are preserved unchanged. No downstream issue work, no dataset changes.

## User Decisions and Requirements

* Owner 2026-10-22: investigate another source; demo accuracy is acceptable; keep it in the documentation as a pending point for production. No fabricated measurements and no false licence approval. Proposal-only integration through normal gates.
* Prefer an openly accessible source with documented licence and provenance, no credentials or paid subscription; a gridded or reanalysis source is acceptable if labelled modelled.
* Compare a small bounded set against existing candidates; retrieve a small fixed sample (location, date range, units, retrieval date, source, licence, attribution); derive bounds from the records.
* Preserve negative evidence (MIDAS login block) and the Durham temperature-only evidence separately.
* Do not alter the 60,000-home dataset, read private data, or implement #179, #180 or #193. No paid AI or Azure operations.
* Exact #178 criteria stay honest: licence human confirmation remains unmet.

## Goals

* A usable, labelled modelled paired source for the demo with reproducible derived bounds.
* Explicit pending production items.

## Scope and Non-Goals

* In scope: two raw fixtures, tools/climate_paired_bounds.py, tools/test_climate_paired_bounds.py, derived JSON report, synthesis section, index row, log entry, RPI artifacts.
* Non-goals: indoor model, importer or generator changes, live API calls in tests or the product, source approval, whole-issue closure, editing earlier evidence files.

## Functional Requirements

* FR1: Parse Open-Meteo archive JSON (hourly time, temperature_2m, relative_humidity_2m, dew_point_2m, units) and NASA POWER hourly JSON (T2M, RH2M, fill value, header).
* FR2: Reject: hash mismatch, non-HTTPS URL, unit mismatch, non-contiguous or duplicate hourly timestamps, series of unequal length, any null or fill value (no gap filling), RH outside 0..100, dew point above temperature, and RH inconsistent with a Magnus-formula value from temperature and dew point beyond 1.0 RH point (fixture maximum residual 0.852, ERA5 RH is integer-rounded), with tests at the boundary.
* FR3: Derive per-variable minimum, maximum, mean and 1st/99th percentiles (linear interpolation between order statistics, rank p*(n-1), rule recorded in the report; extremum ties list every timestamp), the paired RH at the temperature extremes, and monthly minimum and maximum, each with timestamps.
* FR4: Cross-source comparison keyed by canonical UTC timestamp (never positional zipping); require the exact common-hour set or fail; report common_hour_count, UTC basis and start/end; mean and mean-absolute difference: mean and mean-absolute difference for temperature and RH.
* FR5: Report records source, request URL, retrieval date, SHA-256, location requested and grid cell returned, model elevation, period, units, Open-Meteo published terms and attribution text kept distinct from unverified underlying C3S/ERA5 reuse rights, modelled label, an explicit statement that no approval of demo, downstream or production reuse is asserted, and status flags `observed: false`, `owner_reuse_approval: UNMET`, `production_status: pending`.

## Non-Functional Requirements

* Offline, deterministic, stdlib only; ASCII; follows the existing climate_station_bounds.py conventions (hash-pinned input, argparse CLI, sorted JSON).

## Acceptance Criteria

* AC1: Tests exercise each rejection path in FR2 for every parsed series (short temperature, dew point and RH series, unparseable and out-of-order times, one-hour-shifted second source) with constructed bad inputs, a hand-calculated percentile and tie case, acceptance at and rejection just above the RH tolerance, plus a golden check that the committed fixtures regenerate the committed report exactly.
* AC2: Existing tools tests (climate station bounds, blocker) still pass; blocker artifact and Durham report byte-unchanged.
* AC3: Synthesis section, index row and log entry state modelled source, derived bounds, W7 disagreement and production gaps; issue criteria remain unticked.
* AC4: Full tools/rpi-checks.py gate and receipt verification run, results reported as they are.

## Phase Checklist

<!-- Phase P01 -->
### [x] P01: Adapter, tests, report

<!-- P01-T01 -->
* [x] P01-T01: Write tools/climate_paired_bounds.py per FR1-FR5.
<!-- P01-T02 -->
* [x] P01-T02: Write tools/test_climate_paired_bounds.py per AC1.
<!-- P01-T03 -->
* [x] P01-T03: Generate docs/reference/research/climate-paired-bounds-178.json from the fixtures.

<!-- Phase P02 -->
### [x] P02: Synthesis, index, log

<!-- P02-T01 -->
* [x] P02-T01: Add synthesis section after the 2026-10-21 section, add index row, append log entry; add an explicit pending-production table.

<!-- Phase P03 -->
### [ ] P03: Gate and publication

<!-- P03-T01 -->
* [ ] P03-T01: Run tests, rpi-checks gate and receipt verification; push with lease; update PR 425 body.

## Follow-Up Items

* Production: station-grade or authorised source, commercial-use terms, licence confirmation, multi-year window, regional representativeness, ERA5-Land versus ERA5.
* Downstream #179 may consume the report as labelled modelled outdoor input after separate approval.

## Critique Disposition

Critique executed once (verdict Revise, PC-001..PC-005, all direct planner corrections; no user decision; no second critique). Full finding list: .copilot-tracking/reviews/plans/2026-10-22/climate-paired-alt-source-178-plan-critique.md.

* PC-001 applied: FR4 keyed by UTC timestamp, shifted-source test, golden common_hour_count.
* PC-002 applied: tolerance 1.0 RH point; independently confirmed fixture maximum residual 0.852; boundary tests.
* PC-003 applied: summary and FR5 separate Open-Meteo terms from unverified C3S rights; no approval asserted.
* PC-004 applied: FR3 percentile rule and tie handling.
* PC-005 applied: AC1 matrix extended.
