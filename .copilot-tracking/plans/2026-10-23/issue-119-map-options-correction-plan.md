<!-- markdownlint-disable-file -->

# Implementation Plan: issue-119-map-options-correction

Task ID: 119. Slug: issue-119-map-options-correction. Date: 2026-10-23.
Research: .copilot-tracking/research/2026-10-23/issue-119-map-options-correction-research.md
Details: .copilot-tracking/details/2026-10-23/issue-119-map-options-correction-phase-details.md
Critique (single): .copilot-tracking/reviews/2026-10-23/issue-119-map-options-correction-plan-critique.md
Changes (owned by implement): .copilot-tracking/changes/2026-10-23/issue-119-map-options-correction-changes.md
Parent task: 119 / issue-119-map-options-recovery (preserved unchanged).

## Executive Summary

An independent review of head 0e7c9f9a found two Medium defects in the options
proposal. MAP-001: the cost paragraph still presents USD500 as the owner ceiling
and the provisional USD 535.41 as governing evidence, though the addendum
records a replacement USD 700 all-in ceiling, an unchanged 2026-10-25T16:02Z
expiry and unknown headroom. MAP-002: vendor claims that the recovery research
said were draft-unverified are written as established, although the recovery
plan's AC1 and PC-001 recorded the labels as applied. This plan corrects the
document and its repeats in one pass, links the addendum, adds dated corrections
and an honest acknowledgement, and keeps every historical artifact unchanged.
No provider is selected, no web retrieval, no spend, and both original issue
criteria stay unmet. This is the single owner-authorized extra correction cycle;
a further finding or phase-order deviation stops the work. Readiness: Ready for
implement after one critique.

## User Decisions and Requirements

* Owner 2026-10-23: "Authorize one additional ordered correction cycle"; exactly one extra correction, no waiver of review, local validation, receipt currency or human gates.
* Reconcile the proposal with the addendum USD 700 synthesis and link it; keep USD500 and USD535.41 as dated superseded history, never current liabilities or a fresh forecast; no paid execution without verified all-in headroom and finite separate approval; no resource retirement authority.
* Correct all affected vendor statements consistently using retained draft/unverified labels and no new web retrieval; no provider selection or binding licence, cost, processor or DPA decision.
* Preserve original research, critiques, plans, dispositions, implementation, Reviews and failed gates; append an honest dated acknowledgement; do not renumber earlier artifacts or mark a human criterion passed.
* Documentation only; no credentials, Azure, cloud, private data or paid operation. Stop before the full gate, push, PR write or merge. Commit locally with privacy-safe identity and the Copilot trailer.

## Goals

* Make the options proposal state budget and vendor evidence status accurately and consistently.
* Record the correction cycle honestly in tracking, index and log.

## Scope and Non-Goals

* In scope: docs/reference/research/ux/map-tile-provider-options.md, the ADR 0002 map delta wording, docs/reference/README.md index paragraph, docs/reference/log.md (append), dated tracking artifacts and a new state file.
* Non-goals: addendum edits (read-only source of truth), UI or source changes, vendor verification, provider choice, the full gate.

## Functional Requirements

* FR1: The options document defines an evidence-status legend and labels every vendor claim not re-read in recovery as draft, unverified; W1 and W2 content is labelled re-read 2026-10-20.
* FR2: The cost paragraph states USD500 and USD 535.41 as dated superseded history, states the current USD 700 all-in ceiling, expiry and Unknown headroom, links the addendum subsection, and keeps no-spend, finite-approval and no-retirement boundaries.
* FR3: The ADR 0002 delta repeats the draft label for Azure geography and the Entra premise.
* FR4: The index paragraph and an appended log entry describe the correction precisely.

## Non-Functional Requirements

* ASCII punctuation, `*` bullets, no em dashes, relative links; append-only log; git diff --check clean; no deletion of earlier tracking text.

## Acceptance Criteria

* AC1: No vendor statement from an unread page (Azure Learn pages, OS docs, OS terms status, MapTiler pages, ODbL copyright page, Protomaps, Geofabrik) appears without a draft, unverified label in the table, bullets, cost method, unverified list or ADR delta.
* AC2: The proposal contains no sentence presenting USD500 or USD 535.41 as the current cap or current forecast; the addendum link resolves; Unknown headroom, expiry 2026-10-25T16:02Z, finite separate approval and no retirement authority are stated.
* AC3: Original tracking artifacts have no diff; corrections are new 2026-10-23 artifacts plus the append-only log entry.
* AC4: The corrected changes record acknowledges the earlier PC-001 and AC1 completion claim was not borne out.
* AC5: Both issue criteria remain unmet; screen reader NOT RUN; no closing keyword.
* AC6: Focused checks (diff, ASCII, links, accessibility static test) pass; Review is performed once on the committed-candidate diff; no full gate here.

## Phase Checklist

<!-- P01 -->
* [x] P01: MAP-002 evidence-status labels (P01-T01 legend and status paragraph; P01-T02 table rows A to E; P01-T03 Option bullets, Entra premise, cost method sentence and unverified list intro; P01-T04 ADR 0002 delta)

<!-- P02 -->
* [x] P02: MAP-001 cost paragraph reconciliation (P02-T01 rewrite paragraph as history plus current addendum position and link)

<!-- P03 -->
* [x] P03: Index, log and honest tracking (P03-T01 index paragraph and ms.date; P03-T02 append log correction; P03-T03 changes record and new state file with acknowledgement)

<!-- P04 -->
* [x] P04: Validate, Review and commit (P04-T01 diff, ASCII and link checks and accessibility static test; P04-T02 one Review; P04-T03 commit)

## Critique Disposition

Critique executed once (fresh worker, rpi-plan-critique), verdict Revise, 0 Critical, 0 High, 4 Medium, 2 Low. No second critique. All findings were planner-direct and applied; no user decision was needed.

| ID | Disposition |
| --- | --- |
| PC-001 | Applied: P01-T05 adds a claim inventory and a label grep; AC1 is checked by them. |
| PC-002 | Applied: Row A privacy and no-DPA labels, Row B split, Read column note and named bullets in P01-T05. |
| PC-003 | Applied: P02-T01 covers Row E, the unverified list, the USD500/535.41 grep, the addendum refresh gate; the log entry says it supersedes only the earlier wording. |
| PC-004 | Applied: README and ADR 0002 frontmatter ms.date updates in P03-T01. |
| PC-005 | Applied: acknowledgement lives only in the new 2026-10-23 changes record and state file; no 2026-10-20 or 2026-10-21 artifact is touched. AC3 reads accordingly. |
| PC-006 | Applied: P04 stop rule for a Medium or higher Review finding. |

## Follow-Up Items

* Owner or procurement verification of vendor pages, rates, terms and DPA.
* Human screen-reader run of the list alternative (issue criterion 2).
* Refreshed post-change all-in forecast before any tranche.
* Fresh exact-head complete gate by the coordinator once the heavy-gate owner releases the lock.
