---
title: In-VNet staff initialization phase details
description: Task-level evidence and completion expectations for Refs #360
ms.date: 2026-10-16
---

Task: 360-run-in-azure.

## P01

### P01-T01

Use existing initializer SQL position/identity checks, transaction and audit.
Factor Graph retrieval from preparation, passing validated person objects from
operator login. Worker imports existing initializer without invoking its CLI.
Connection uses inherited mssql-python and SQL-admin MSI. Candidate results,
summaries and failure status must be encrypted with a secret-held random key.
Never print tracebacks or plaintext SQL/roster data.

### P01-T02

Use existing Azure private body helper with management-plane job create/start,
execution-status and authenticated environment-log capture, stop/delete cleanup.
Validate API and init job
share one ama environment, exactly the expected init identity and private SQL
administrator. Reuse only source image/registry, safe resource limits and explicit
SQL env. Roster goes into secretRef, never command args. Failures print exact
private-host fallback. Read-only SQL checks disclose transient control-plane work;
dry-run never runs jobs. No new identity/network or storage permission.
The standalone API-only custom role in infra/staff-initializer-rbac.bicep
grants the existing MI app/revision/replica reads and revision restart only;
deployment is not run. The worker verifies SQL then uses its own MI to execute
the canonical restart/replica convergence helper. Source image/assets must be
built and pinned separately, never repaired by embedding untracked source.

## P02

### P02-T01

Fake az owns complete job lifecycle and records arguments, private ARM body files,
encrypted output and cleanup. Assert directory calls never originate in worker;
local and explicit/blocked paths remain covered. Reuse canonical initializer tests
to verify immutable bindings, role/supplier coverage and preserved history.
Docs must distinguish operator-owned Graph work from job-owned SQL/restart.

### P02-T02

Run existing infra suites and targeted Ruff/mypy, local synthetic app smoke without
private data; no Azure build/validation. Review once after implementation and
record criteria as proved locally or unmet live. Privacy-safe commit and PR with
Refs #360; no issue checkbox edits or merge.
