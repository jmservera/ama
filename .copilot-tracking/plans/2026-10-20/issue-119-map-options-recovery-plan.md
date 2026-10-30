<!-- markdownlint-disable-file -->

# Implementation Plan: issue-119-map-options-recovery

Task ID: 119. Slug: issue-119-map-options-recovery. Date: 2026-10-20.
Research: .copilot-tracking/research/2026-10-20/issue-119-map-options-recovery-research.md
Details: .copilot-tracking/details/2026-10-20/issue-119-map-options-recovery-phase-details.md
Changes (owned by implement): .copilot-tracking/changes/2026-10-20/issue-119-map-options-recovery-changes.md

## Executive Summary

Recovery plan after a process defect: the earlier draft (commit 69fa487a) was
hand-authored without the RPI skills. This plan re-checks that draft against
the evidence actually re-read (OSM policy, Azure pricing page, code, tool availability) and labels the remaining draft claims unverified, makes small evidence-driven corrections, discloses the defect
in dated append-only clarifications, and runs the full local gate. No provider
is selected, nothing is bought, no UI is edited, and the actual screen-reader
test (issue criterion 2) stays an unmet human gate. Readiness: Ready for implement
after one critique.

## User Decisions and Requirements

* Owner direction #126 comment 6290697705: research licence, cost and privacy options for review; retain the accessible list; no purchase, selection or approval; no private coordinates on the wire.
* Do not rebuild or swap framework or provider; integrate into existing map, UX and architecture synthesis.
* Real screen-reader test only if genuinely available; otherwise honest unmet gate; engineering evidence labelled as such.
* Coordinator: no edits to infra runbook, budget/benefits synthesis, form schema pack, cohort docs; index and log append-only; no push, no PR, no closing keywords.
* Coordinator intervention: preserve the draft and adverse history; disclose, do not backdate or delete; first-class skill-driven phases; one critique and one Review.

## Goals

* Evidence-verified, honestly caveated options document and protocol, ready for independent assessment.
* Accurate process disclosure.

## Scope and Non-Goals

* In scope: docs/reference/research/ux/map-tile-provider-options.md, wcag-conformance-baseline.md section, ADR 0002 delta (read for consistency), index and log append, tracking artifacts and state.
* Non-goals: UI or provider changes, purchases, provider selection, whole-app audit, #126 or other issues.

## Functional Requirements

* FR1: Unverified secondary claims (OS pricing, Azure DPA) are labelled as such wherever they appear.
* FR2: Add the discrepant secondary OS leisure-view rate note as unverified.
* FR3: Append a dated clarification to the log and to the original draft tracking artifacts recording the pre-RPI status.

## Non-Functional Requirements

* ASCII punctuation, `*` bullets, no em dashes; append-only index and log; git diff --check clean.

## Acceptance Criteria

* AC1: Claims re-read in recovery (W1, W2, C1-C5) are confirmed; every other draft vendor claim (OS, MapTiler, Azure geography/auth, DPAs) is labelled draft-unverified in the options doc. No document states a vendor price, free allowance or DPA term as established fact where only a secondary source exists.
* AC2: Screen-reader criterion is recorded as unmet; no claim of a run.
* AC3: Clarifications are appended, not rewritten.
* AC4: Order: implement edits, then changes record, then the single Review record, then commit, then the full gate; if gate prerequisites (SQL, browser, scanner) are missing the task is Blocked and no cloud fallback or skip is used. Receipt verifies at the final HEAD; no push.
* AC5: WCAG baseline section and ADR 0002 delta state the screen-reader gate as unmet and engineering evidence as not a screen-reader run; the DPO/personal-data question stays open and unanswered.
* AC6: Zero deletions in the diff of pre-existing tracked lines other than mechanical ms.date.

## Phase Checklist

<!-- P01 -->
* [x] P01: Verify and correct the options document (P01-T01 add OS secondary-rate note; P01-T02 confirm wording is neutral, no selection; P01-T03 audit options doc, baseline and ADR for every secondary or unverified price/DPA statement, unmet screen-reader gate and open DPO question)
<!-- P02 -->
* [x] P02: Append dated process clarifications (P02-T01 log entry; P02-T02 short appended note to the six original markdown artifacts only; a separate recovery state file; original JSON untouched; record commit 69fa487a and the gate-run pid history)
<!-- P03 -->
* [x] P03: Validate and gate (P03-T01 git diff --check, ASCII, accessibility baseline test; P03-T02 commit and full local gate with external receipt)

## Critique Disposition

Critique: .copilot-tracking/reviews/2026-10-20/issue-119-map-options-recovery-plan-critique.md, verdict Revise, applied once, no second critique.

* PC-001: applied; summary and AC1 narrowed to what was re-read; others labelled draft-unverified.
* PC-002: applied; P01-T03 audit.
* PC-003: applied; AC5 and P01-T03.
* PC-004: applied; appends limited to markdown originals, original JSON untouched, AC6.
* PC-005: applied; P02-T02 records commit ids.
* PC-006: applied; AC4 ordering and Blocked path.
* PC-007: applied; AC5.

## Follow-Up Items

* Human or assistive-technology screen-reader run of the map list.
* Owner-approved verification of provider paid rates, terms and DPAs.
* Owner provider decision (not made).

## Correction continuation 2026-10-20 (P04, rpi-implement)

<!-- P04 -->
* [x] P04: Correct the budget wording after independent assessment (Defects on e69a2ed5). P04-T01 options doc cost paragraph; P04-T02 append log entry; P04-T03 align details, changes and state. AC7: the doc states the USD500 total calendar-month cap including accrued and forecast cost across `ama` and other scopes, requires separate finite costed plan approval before any paid execution, authorises no spend and treats unknown headroom as blocking. The earlier receipt for e69a2ed5 (SHA256 9ece9317...a959) is historical after this commit; a fresh full gate is queued by the coordinator.

## Security gate regression continuation 2026-10-21 (P05, rpi-implement)

<!-- P05 -->
* [x] P05: Discovered cross-cutting gate regression, not a map-domain defect. The final-head gate image scans reported fixed CRITICAL GHSA-6q48-6c7w-9gw2 (certifi 2026.7.22, fixed 2026.10.19) in the API, importer and orchestrator images. P05-T01 bump the transitive hash-locked certifi pin in the four requirements.txt lockfiles (core, api, importer, orchestrator); P05-T02 focused reproduction; P05-T03 align tracking. No ignore file, baseline, severity change or skip. The coordinator reuses this fix for hosted PR 424 and runs the fresh full gate. The old gate receipt is historical.

## Budget evidence continuation 2026-10-21 (P06, rpi-implement)

<!-- P06 -->
* [x] P06: Independent assessment (Needs work at a3257c71) found the cost paragraph omitted the known resource-group-only provisional forecast USD 535.41, already above the USD500 total October cap, plus unknown non-RG liabilities. Reworded minimally, labelled a coordinator-supplied forecast with no in-repo source and not live. The a3257c71 gate receipt is historical.
