---
title: Issue 107 release admission research
description: Research for the five-assistant proposal service RAI release admission delta
ms.date: 2026-10-15
---

## Disposition

Research disposition: executed. Planning Readiness: Ready.

## Evidence

* Issue #107 (parent #104): the five base criteria (capability IDs/registry version/allowlist/trigger, contractor and unknown denial, separate purpose principal off by default, SQL identity/dedup/leases, no controlled-domain write) are already delivered by `mvp/zavaforward_mvp/assistants.py` and `mvp/tests/test_assistants.py` (50 tests), on the AI task registry (#105).
* Unmet: the RAI release admission criteria. No release record, admission recheck, serving-version attestation or legacy dispatch gate existed (grep for release/attest/serving in `mvp/zavaforward_mvp`).
* Legacy dispatch goes through `Ai.run` with `ai.gate` set in `sqlstore.py`.
* Owner decisions: ADR 0004 accepted, Azure only, owner Juan Manuel Servera, constructed fixtures only, portable SQL, no controlled-domain writes.

## Open items (not invented)

* Actual authorised approver names and real release evidence: owner decision (`ZF_ASSIST_RELEASE_APPROVERS` is operator config).
* Actual serving-version attestation from Azure OpenAI and Azure SQL race evidence (CON-009/AC-057): needs real deployment.
* JSON dev store has no durable release store and is not gated.

## PR 287 review-fix research (2026-10-15)

* mssql CI failure: `tests/release_support.py` ran SQLite `CREATE TABLE IF NOT EXISTS` on SQL Server (48 errors, "Incorrect syntax near the keyword 'IF'"). `SqlStore.release_block` also used SQLite `julianday` for the clock, which fails on SQL Server and denies silently.
* `ai.py` calls `strong` for strong paths and `read_document`, but the gate bound only `ai.fast` and only provider/endpoint/deployment.
* Legacy dispatch had a pre-dispatch check only; `_chat` returns text without the model name.
* Planning readiness: Ready.
