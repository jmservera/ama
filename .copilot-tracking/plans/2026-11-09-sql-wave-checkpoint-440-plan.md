---
title: SQL feature-recovery wave checkpoint 440 plan
ms.date: 2026-11-09
task_id: 440-sql-wave-checkpoint-1109
---

## Task metadata

* Task `440-sql-wave-checkpoint-1109`, slug `sql-wave-checkpoint-440`. Research: `.copilot-tracking/research/2026-11-09-sql-wave-checkpoint-440-research.md` (disposition executed, Planning Readiness Ready). Details: `.copilot-tracking/details/2026-11-09-sql-wave-checkpoint-440-details.md`.
* Branch `docs/demo-sql-checkpoint-440-1109`, base and target `main` `8d6f029cac004506953f36606862168bbe9d9412`.

## Executive summary

A documentation-only, dated, DRAFT checkpoint is appended to the existing cut-over evidence pack after PR 1308 (the #1292 SQL feature-recovery wave) merged. It pins main, the squash and the PR head, proves source equivalence, classifies the retained real-SQL 142 and 91 and the hosted evidence with their limits, adds a small set of fresh current-tree local checks, keeps raw failures, compares findings with existing owners and gives a bounded recommendation with exact closure and resume conditions. Source SQL merge is not full demo acceptance.

## User Decisions and Requirements

* Genuine RPI in order; this research, plan, details and critique are committed BEFORE any check run or documentation edit.
* Preserve every earlier pack section, log entry, historical adverse record and the old merged #440 branch, `b270` and DF8 records; append only. `Refs #440` only.
* No `src`, `infra`, `tools`, workflow, coordinator, BRD, PRD, ADR, memory or rubric change. Pure documentation needs no local gate; no `rpi-checks`, no full gate.
* Exclude unmerged #1288, #189, #1258, #1259, #136, #1298; any provider, dataset or private readings path; WORM, migration and legal approval. BRD draft, PRD in-review and ADR statuses stay not approved.
* Consume the original 142 and 91 real-SQL results only with exact source equivalence and dated classification; current checks stay separate and are never relabelled. No SQL admission is planned (decision recorded in research); if the critique or later evidence makes one required, exactly one non-queued owned admission applies and a missing or busy resource blocks only that row.
* Negative UI, model or flag claims are bounded to the inspected paths. No epic closure, tick, human approval, source-policy relaxation or pivot is inferred.
* No push, PR, board, issue write, deploy or merge. Local frozen candidate and handoff only.

## Goals

* G1 A dated, source-qualified record of what 1308 changed on main and what evidence does and does not cover it.
* G2 Separate, honest evidence classes: local observed (current), local observed historical (source-equivalent), hosted observed, implemented-unverified, deferred, blocked, unknown.
* G3 Preserve adverse history and the open #1292 and #440 acceptance state unchanged.

## Scope and Non-Goals

* In: one appended pack section, frontmatter `ms.date` stays `2026-11-09` (already current), one index paragraph, one log entry, RPI records, local commits, handoff file in the coordinator files directory.
* Out: anything in the user decisions above; new tests; fixing F1; creating issues.

## Functional Requirements

* FR1 Identities table: main, tree, squash, parent, head, head tree, merge time, previous pin, the rollup stated as 18 successful check runs plus the successful `rubric/score` status, document blobs and statuses.
* FR2 Source equivalence table with the exact Git commands and results (head against main, E2 frozen head against main for production source, the one test-file difference).
* FR3 Requirement trace (document-qualified; issue-attributed items labelled) and a SQL-wave behavior map read from source with `path:line`.
* FR4 Evidence table by class with consumed historical, hosted and current rows; the hosted `mssql` subset limit (priority suite not selected) and the main push run state; retained raw failures.
* FR5 Current local observations: exact commands, working directories, producer exit codes, counts, skips, import origins, external log location and sha256 prefixes; harness failures retained.
* FR6 Findings and owners (deduplicated, existing owners only), exclusions, bounded continue/fix/proposed-pivot statement with exactly affected closure and resume conditions.
* FR7 Index paragraph with a working anchor, and one appended log entry.

## Non-Functional Requirements

* NFR1 ASCII only, `*` lists, no em dashes, no bold-prefix list items, relative links, heading hierarchy unchanged.
* NFR2 Every dated claim names its source; Git-derived facts carry the command; coordinator-reported facts are labelled.
* NFR3 Scratch space only in an `mktemp -d` owned directory outside the repository; logs not committed.

## Implementation Phases

1. P1 Environment and import origins: create `mktemp -d` venv, editable installs of this worktree's `src/core`, `src/agents`, `src/api`; print module `__file__` for each package and assert the path is under this worktree.
2. P2 Targeted local tests (each with producer exit, tee to the owned log directory, no pipe masking exit):
   * Core, `src/core`, `PYTHONPATH=tests`: `tests.test_priority_order`, `tests.test_resident_decisions`, `tests.test_sqlstore`, `tests.test_journey_store`.
   * API, `src/api`, `PYTHONPATH=../core/tests:../agents/tests:tests`: `tests.test_case_journey`, `tests.test_auth`, `tests.test_entra_authoritative`, `tests.test_role_endpoint_inventory`, `tests.test_role_matrix`, `tests.test_assistants`.
   * Record counts and skips; SQL classes skip without admission and those skips are not SQL evidence. A failing selected test is not waived: record raw, diagnose, and if a product defect, report it and do not fix.
3. P3 Write the pack section, index paragraph and log entry. Do not rewrite existing content; `ms.date` already 2026-11-09.
4. P4 Documentation validation only: Git diff scope (docs and tracking only), ASCII and em dash check on added lines, anchor and link check of added links, log append-only check (prefix of old log unchanged), no excluded path touched.
5. P5 Original single Review, state update, commit, handoff.

## Acceptance Criteria

* AC1 Diff touches only the pack, `docs/reference/README.md`, `docs/reference/log.md` (appended) and `.copilot-tracking/` records; earlier lines unchanged except none removed.
* AC2 Every command in the record was actually run with an observed exit code, or is explicitly labelled Git/hosted read; no fabricated current SQL execution.
* AC3 Source equivalence commands reproduce empty results.
* AC4 Raw failures are retained and linked by sha256 prefix.
* AC5 No approval, tick, closure, live, model, SQL or hosted-for-this-commit claim is made.

## Risks

* R1 Hosted state for `8d6f029ca` is in progress at read time; the record states the observation time and does not infer success.
* R2 A selected local test may fail for environment reasons; retained raw and classified, not hidden.
* R3 Reviewer may want a fresh SQL run; recorded as a non-required, owner-decidable resume condition with the single non-queued admission rule.
