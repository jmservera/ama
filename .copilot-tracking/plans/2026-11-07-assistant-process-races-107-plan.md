---
title: Plan for OS-process race and restart tests (#107, C10)
description: Two test cases and a minimal test-only worker, prepared locally with actual SQL left unverified
ms.date: 2026-11-07
---

Research: [research](../research/2026-11-07-assistant-process-races-107-research.md). Details: [details](../details/2026-11-07-assistant-process-races-107-details.md). Critique: [critique](2026-11-07-assistant-process-races-107-critique.md).

## Decisions

* Test-only delta: `src/api/tests/test_assistant_release.py` plus one adjacent helper `src/api/tests/assistant_process_worker.py` (not discovered as a test). No production, tool, workflow, dependency or README change, no schema, approval or attestation change.
* New mixin `ProcessRaces` is added to the bases of the existing `SqliteUnleasedRevocation` and `MssqlUnleasedRevocation`, so the runner's SQL selection reaches it with no runner change.
* Preparation only: no SQL service, container, image, scanner, browser, FULL or `--changed` runner and no lock acquisition. The SQLite proxy is not SQL acceptance; SQL cases skip without `ZF_TEST_MSSQL=1` and that skip is disclosed.
* A failing case that shows a confirmed source defect stops production work; preserve the evidence and route it separately.
* No push, PR, tick or closure; later publication uses `Refs #107` and `Refs #104`.

## Cases

* [ ] Case 1: four OS processes race three eligible proposals under a shared allowance of two calls; then restarted processes with a larger configuration face a fresh proposal.
* [ ] Case 2: a pending proposal, a barrier, revocation through a separate connection, then racing processes and restarted processes.

## Phases

* [ ] Phase 1: critique this plan once; commit the prospective records.
* [ ] Phase 2: add the worker and mixin; run light checks without services.
* [ ] Phase 3: changes record, one author Review, state, freeze clean; hand off the exact future SQL plan.
