---
title: Demo stabilization checkpoint 440 plan
ms.date: 2026-11-09
task_id: 440-demo-stabilization-checkpoint-1109
---

## Task metadata

* Task `440-demo-stabilization-checkpoint-1109`, slug `demo-stabilization-checkpoint-440`. Research: `.copilot-tracking/research/2026-11-09-demo-stabilization-checkpoint-440-research.md` (disposition executed, Planning Readiness Ready). Details: `.copilot-tracking/details/2026-11-09-demo-stabilization-checkpoint-440-details.md`. Changes record to be created by Implement: `.copilot-tracking/changes/2026-11-09-demo-stabilization-checkpoint-440-changes.md`.
* Branch `docs/demo-checkpoint-440-1109`, base and target `main` `df8e858b2150198e5e22c73d224a0d3592c73daa`.

## Executive summary

A documentation-only, dated, DRAFT current-main checkpoint is appended to the existing cut-over evidence pack. It pins main, qualifies BRD and PRD IDs and ADR status, traces the simulator to persistence to UI to Quality model to flag path hop by hop with source facts, classifies evidence (local observed, Azure observed, implemented-unverified, deferred, blocked, unknown), reuses the 184 evidence only as historical with proven Git equivalence, records three tiny observed test runs with exits, lists deduplicated gaps and owners, and recommends bounded CONTINUE with HOLD on closure. The index and log gain linked entries. Nothing is approved, ticked, closed or published. Key limit to know: the employee retained-value UI, actual Quality sensor input and attributed flag do not exist on main; they are in unmerged #1288.

## Sources

* Research file above; owner brief and coordinator audit `demo-critical-path-audit.json` (2026-11-09, attributed, not re-verified); `handoff-184-current-main-validation.md`; PR 1304 and PR 1222 bodies; #440 body and comment `6740015794`; existing pack sections of 2026-11-06 (sixteenth, retained-evidence verification) and 2026-11-08 (visible-demo), as format and baseline.

## User Decisions and Requirements

* Scope is only `docs/architecture/cutover-evidence-pack.md` plus the existing index (`docs/reference/README.md`) and append-only log (`docs/reference/log.md`) and RPI records. Preserve every historical adverse record, grade and acceptance tick.
* Pin actual main and tree; qualify document versions, blobs and status (BRD against PRD FR IDs; ADRs). Draft, not approved.
* Cover simulator, persistence, UI, actual Quality model, attributed flag, and auth, tenant, admin, manual, failure, consent, approval and package identity boundaries.
* Unmerged #1288 E3, #1292 E1, #144 new head, #189, #1295 and #1296 are excluded; main IoT PR 1304 is implemented, not demo-accepted; #1296 High REVISE eleven of 27 is an adverse unmerged candidate-policy outcome, no coordinator change.
* Retained 184 SQL 70 plus 10 and Agents/Core proof only as historical observed with Git equivalence; keep mutable-tag, image and log provenance limits; no relabelling of old logs as new.
* Tiny relevant existing tests only when needed; no full gate, SQL, browser, Azure, model, jobs, spend. Documentation needs no local runner.
* No new defect fix or issue write; record evidence, severity, minimum fix, test and dependencies if one were confirmed. Recommend bounded continue or fix; no pivot or deferral inference. No issue closure claim.
* Freeze clean local committed RPI and docs with relative links and diff review; no push, PR, board, issue or merge. Handoff to the coordinator files directory.

## Goals

* G1 A dated, source-qualified, honest current-main checkpoint that a reader can use to see what exists on main for the demo path and what does not.
* G2 Preserve all prior records and the #440 acceptance state unchanged.

## Scope and Non-Goals

* In: one appended pack section, frontmatter `ms.date` update, one index paragraph, one log entry, RPI records, local commit, handoff.
* Out: any `src/`, `infra/`, `tools/`, workflow, coordinator, BRD, PRD, ADR, memory or rubric edit; any new test; issue, PR or board writes; live or paid actions; rewriting earlier pack sections or log entries.

## Functional Requirements

* FR1 The section states the main SHA and tree, document blobs and statuses, ADR statuses, trigger PRs and comment, and the local ref note.
* FR2 A hop table cites source `path:line` for each hop and states the unmerged gap for UI, Quality input and flag.
* FR3 Evidence classification table plus a historical-evidence subsection with the Git equivalence command and result and the carried provenance limits.
* FR4 Current observations table with exact commands, producer exits, counts, skips, the two retained harness-import failures, the venv provenance and the external log location.
* FR5 Gaps and owners table (deduplicated), exclusions, recommendation, affected closure and dependent gates, independent lanes, exact resume conditions.
* FR6 Index paragraph with a working anchor link; log entry appended at end with date, scope and non-claims.

## Non-Functional Requirements

* NFR1 Markdown style of the target file; plain ASCII, no em dashes, no bolded-prefix list items, `*` bullets in new content. Relative links only.
* NFR2 Claims traceable to evidence; attributed coordinator statements labelled as such; no forecast stated as fact.
* NFR3 Append-only; existing lines other than frontmatter `ms.date` unchanged (verified by diff).

## Acceptance Criteria

* AC1 `git diff` shows only the three intended docs paths (pack, index, log) plus tracking records; pack diff is the frontmatter date plus an appended block.
* AC2 Every link in the new text resolves (checked locally with a script over the changed docs).
* AC3 The section contains no approval, closure, tick or live-acceptance claim and keeps #1288/#1292/#144/#189/#1295/#1296 explicitly excluded.
* AC4 Producer exits and counts in the text match the retained external logs.
* AC5 One critique and one review executed; their outcomes recorded.

## Phase Checklist

* [ ] P01 Write pack section
* [ ] P02 Index, log and frontmatter date
* [ ] P03 Validate (links, ASCII, diff, log counts)
* [ ] P04 Changes record, review, handoff, commit

## Critique Disposition

Critique `.copilot-tracking/plans/2026-11-09-demo-stabilization-checkpoint-440-critique.md`, verdict Revise, run once (rubber-duck; the worker returned findings inline and the planner recorded the file). All five findings are planner-applied, none needs a user decision, no second critique.

* PC-001 Applied: resume condition 5 now privacy-compatible (PRD AC-067).
* PC-002 Applied: work-package identity recorded as unknown.
* PC-003 Applied: ingress-header trust prerequisite added to auth boundary.
* PC-004 Applied: consent and window anchors corrected to sensor_consumer.py:603-611.
* PC-005 Applied: AC1 reconciled to three docs paths.

## Follow-Up Items

* F1 Observed outside scope: the #184 issue body text reported stale by the 2026-11-09 audit (owner #184). No issue is written.
* F2 SQL-backed observations on main (assistants 58 skipped, #1297) await a later admitted SQL window after #1292 releases the resource.

## Qualification C1 (2026-11-09, added after independent readiness review)

The key-limit sentence above ("do not exist on main") is superseded in scope: no retained-value UI, sensor input or attributed flag was identified in the inspected paths and a differently named path remains unverified. Original plan and critique outcome are not regraded. See the C1 plan `2026-11-09-demo-stabilization-checkpoint-440-c1-qualification-plan.md`.
