---
title: Issue 86 focused-tier validation plan
description: Prospective focused tier, rationale and execution plan after the interrupted FULL
ms.date: 2026-11-08
---

Scope: issue #86 only. Tier for the #86 to #81 child: FOCUSED, per the owner's changed boundary as read by the coordinator. Rationale: the child PR targets the parent, not Main; the later #81 to Main integration keeps FULL. The earlier plan tier FULL is preserved unchanged as the prior record. Focused does not waive SQL feature tests for the changed storage and API: they must complete. Relevant component failure or a missing relevant check blocks.

## Steps

1. Commit this research, plan, details and one independent critique before any execution.
2. Currency: prove HEAD content equals the interrupted receipt head (only tracking files differ after commit; `src tools infra .github` trees equal `40ec31e2`), fresh fetch of Main and parent refs, PR #1243 base.
3. Static/type/unit: reuse same-head results from the interrupted receipt (core 2492 OK, API 1999 OK, static, infra, migration, browser) as historical same-code observations only, with the currency proof; rerun nothing duplicate. If the currency proof fails, stop and re-plan (critique F6); light reruns cannot replace invalidated evidence.
4. Actual SQL: under non-blocking `flock` on the canonical lock, after rechecking holder, RAM, CPU and disk, run the maintained `SQL_SELECTORS` from `src/api` against one owned disposable container, plus core `test_resident_decisions.MssqlResidentControls` with `ZF_RESIDENT_MSSQL=1`. Count actual `ok` per method, keep skips and failures, remove only the owned container, no global prune.
5. Preserve the receipt, console and logs untouched; copy nothing over them.
6. Changes and one author Review; commit; freeze ignored-clean.

## Stop conditions

Lock held, resources insufficient, drift in head, Main, parent ref or PR base, any SQL failure (reported, not hidden), a transport timeout beyond 7200 seconds (report, do not claim pass), a confirmed new product bug (report, no edit).

## Not claimed

No FULL, no images, scans or logo, no real AI, AT, receiver, cross-process or multiuser proof, no #1238 relaxation, no approval, tick or closure. Independent exact-head review (both parent deltas and Main-versus-final inherited hunks), hosted checks and publication remain.

## Critique amendments (F1-F5, accepted)

* F1: create database `rpi_disposable` after readiness and set `ZF_SQL_PASSWORD`, as the maintained runner does.
* F2: hold the canonical lock through setup, both suites and cleanup; before tests verify container ID, `ama.rpi.owner` label, running state and the loopback-only port.
* F3: pass criteria require nonzero successful execution of both suites; skips are classified by name and any skip outside the known JSON-only ones blocks.
* F4: resident complaint HTTP tests use SQLite; changed ranking/export API paths against MSSQL are explicitly not claimed unless the selectors prove them.
* F5: install `src/api/requirements.txt` with `--require-hashes` and run the driver probe (libltdl/libkrb5 CDLL plus `mssql_python`) in the evidence venv, recording output.
