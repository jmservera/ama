<!-- markdownlint-disable-file -->

# Implementation Plan: fictional-form-review-97-fin001

| Field | Value |
| --- | --- |
| Task ID | 97-fin001 (parent 97-recovery) |
| Date | 2026-10-23 |
| Research | .copilot-tracking/research/2026-10-23/fictional-form-review-97-fin001-research.md |
| Details | .copilot-tracking/details/2026-10-23/fictional-form-review-97-fin001-phase-details.md |
| Critique | .copilot-tracking/reviews/plans/2026-10-23/fictional-form-review-97-fin001-plan-critique.md |
| Changes (implementation owns) | .copilot-tracking/changes/2026-10-23/fictional-form-review-97-fin001-changes.md |

## Executive Summary

Correct two false documentation claims (guide lines 28-29 and core README lines 935-936) that say the public fictional schema registers unchanged. It does not: the placeholder reviewer is intentionally refused, and only a derived copy with a registered reviewer substituted registers, staying Unapproved. Wording only; no runtime, test, fixture or authority change. Append a focused KB log entry. The complete local gate is intentionally not run under the owner's direction, is not claimed, and is still required on the final head before any publication. Readiness: Ready; critique dispositions recorded, no second critique.

## User Decisions and Requirements

* Owner authorized ONE extra ordered correction cycle for FIN-001; not a waiver (brief 2026-10-23).
* Do not weaken validation, alter fixture authority, invent reviewer approval, or change runtime or test behavior to make docs true.
* Correct both claims and any directly coupled same false claim; no unrelated inherited fixes.
* Use the manual edit tool for prose; append a KB log entry if synthesis changes; keep old artifacts and history.
* No push, PR mutation, merge, full gate, Docker, Azure or private data. Commit scoped correction and tracking with a Conventional Commit and the Copilot trailer.
* Finance FD-01..FD-14, template authority, binding and OQ-015 stay unapproved; criterion 1 unmet; no closing keywords or AC ticks.

## Goals

* Documentation states accurately how the public fixture and a derived copy behave under `register_schema`.

## Scope and Non-Goals

* In scope: the guide, the core README paragraph, one appended KB log entry (and frontmatter `ms.date` of the log if required by its convention), and this task's tracking.
* Non-goals: runtime, tests, fixture, registry, index description, dictionary, unrelated inherited issues.
* Examined and left unchanged: fixture statement at line 13 (conditional on a derived registration, true; fixture authority unchanged), index row 283, dictionary lines 328-333, provenance register and the 2026-10-20 log entry, because they use registered in the provenance-register sense.

## Functional Requirements

* FR-1: The guide no longer says the schema registers unchanged; it says the public file is refused and a derived copy with a registered reviewer registers as Unapproved.
* FR-2: The core README paragraph says the same.
* FR-3: A new log entry records the correction and keeps earlier entries.

## Non-Functional Requirements

* Plain ASCII, `*` bullets, no em dashes, claims traceable to C1-C8; no fabricated approval.

## Acceptance Criteria

* AC-1: A case-insensitive search of the guide and core README pack sections for unchanged, registers through, registers as and regist, reviewed by hand, leaves no sentence saying the public file registers unmodified.
* AC-2: From src/core with PYTHONPATH=tests:.:src, `python3 -m unittest test_form_review_pack test_synthetic_provenance` passes with no code change; `git diff` shows only the named docs and tracking; the command and result are recorded in the changes file.
* AC-3: Existing criterion, approval and authority wording is unchanged.

## Phase Checklist

* [x] P01 Correct documentation claims
* [x] P02 (commit pending Review) Append KB log entry, validate and commit

## Follow-Up Items

* None added by this plan. Original Review RV-001 and RV-002 and Finance decisions remain routed as before.

## Critique Disposition

Single critique executed (fresh worker, rpi-plan-critique), verdict Revise, 6 findings, all direct planner corrections, none needing a user decision. No second critique.

| Finding | Disposition | Applied in |
| --- | --- | --- |
| PC-001 | Accepted | Details P02-T01 (type, title, files, contradiction, ms.date) |
| PC-002 | Accepted | Details P01-T01, P01-T02 (wording a-d, provenance disambiguation) |
| PC-003 | Accepted | AC-1, AC-2, details P02-T02 |
| PC-004 | Accepted | Scope residual line |
| PC-005 | Accepted | Details P02-T03 and executive summary gate statement |
| PC-006 | Accepted | This table and readiness update |
