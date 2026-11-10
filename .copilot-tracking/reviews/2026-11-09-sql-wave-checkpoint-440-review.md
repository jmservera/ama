---
title: SQL feature-recovery wave checkpoint 440 review
ms.date: 2026-11-09
task_id: 440-sql-wave-checkpoint-1109
---

## Execution and scope

One post-implementation Review, executed once by the implementing session on the uncommitted candidate diff (pack +102, index +10, log +5) and the RPI records. It is authored and NOT independent. Review input for an independent reader: exact head of the final commit, the research and critique, the changes record, the external logs, and the commands in the pack. Boundary assessed: documentation and records only; no source was changed.

## Checks performed

* Re-read each Git-derived claim against its command: source equivalence, tree and head ids, parent, squash, document blobs, the later `origin/main` commit. Consistent.
* Re-read cited anchors (`store.py:939-947`, `1035`, `1060`; `sqlstore.py:224`, `258`; `mssqlstore.py:46`, `181`, `199`, `314`, `323`; `server.py:1242-1268`; `app.js:677-707`; `src-ci.yml:3-6`, `326`). Verified lines for the guard, busy timeout, abandon and trigger.
* Checked brief constraints: exclusions kept; BRD draft, PRD in-review, ADR statuses unchanged and not approved; no closure, tick or human approval inferred; `Refs #440` only; negative statements bounded; existing owners named (#1292, #1297, #81, #1240, #123); no product, infra, tool or workflow change; no SQL admission and the reason stated; raw failures retained with hashes; current checks kept apart from historical and hosted.
* Documentation validation per the changes record: append-only, ASCII, tables, anchors.

## Findings

* R1 Open, Medium. The pack's SQL-wave table cites `sqlstore.py:595-` and `store.py:1035` for ordinal and unresolved-order behavior; the fine-grained semantics (legacy heuristic assessment, zero-ordinal repair) were read from source comments and the PR body, not exercised on real SQL in this task. The pack labels the SQL rows historical or implemented-unverified. An independent reader should confirm the descriptions against the code.
* R2 Open, Medium. The claim that no hosted check executes the priority suite on SQL Server rests on the workflow selection and the `mssql` job log; whether `src-core` discovery lists the priority file was not read per test. The pack says unverified. Independent confirmation is recommended before the owners act on F1.
* R3 Open, Low. F2 (SQLite concurrent opener failure) has an unproven cause; one occurrence in four runs and the cause hypothesis (busy timeout 5000 ms under load) are suggestions only.
* R4 Open, process. No independent exact-head review and no hosted CI exists for the commit that will carry this record. The coordinator's publication gate applies.
* R5 Informational. The overlapping first Core and API runs were a process choice; the serial Core rerun supplies the clean result.

## Outcome

Conformant for the bounded documentation scope with R1 to R4 open, routed to the independent exact-head reviewer and the issue owners. Not a statement of merge readiness, approval or acceptance. No further Review or correction cycle is run in this task; no correction cycle was consumed.
