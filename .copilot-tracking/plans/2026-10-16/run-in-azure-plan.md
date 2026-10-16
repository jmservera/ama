---
title: In-VNet staff initialization plan
description: Implementation-ready candidate for Refs #360
ms.date: 2026-10-16
---

Task: 360-run-in-azure. Research: .copilot-tracking/research/2026-10-16/run-in-azure-research.md.

## Executive Summary

Add a SQL-only worker to the existing proof image and a private management-plane
transport which clones the existing initializer job into an ephemeral manual job.
Secrets carry the roster and a fresh encryption key; only encrypted results go
to logs. Cleanup removes job secrets on success/failure/timeout. Keep directory
work and seeded generation under operator login; restart inside the worker.
No live Azure execution is authorized.

## User Decisions and Requirements

* Refs #360, offline only; build only under src/ and infra/.
* Explicit mode and automatic fallback for blocked local SQL; existing ama
  environment and SQL-admin identity, no network changes.
* Preserve seeded roster and directory authority; no identities in CLI/logs/Git.
* Counts-only status, honest acceptance audit, fake-az tests, docs and PR.
* Do not modify the issue body; coordinator owns merge-time checkboxes.

## Goals

Finish staff binding from a laptop without private SQL connectivity.

## Scope and Non-Goals

Change setup, shared initializer preparation, proof image and offline tests.
No infrastructure deployment, image build, private dataset read, new identity,
SQL/Key Vault policy changes or tenant approval.

## Functional Requirements

* Discover and validate source init job, SQL admin identity, environment and
  private SQL settings; never forward unvalidated template commands/env.
* Run candidate, check and apply/verify as independent bounded executions.
* Resolve directory people locally; worker has no Graph client/token.
* Explicitly refuse Azure work under dry-run; check/list create temporary jobs
  but do not write SQL. Status must explain management-plane writes.
* Retry neither an uncertain apply nor a failed job automatically.
* Restart serving replicas inside the worker after SQL verification. Author
  infra/staff-initializer-rbac.bicep for an API-scoped custom role containing
  only app/revision/replica reads and revision restart; no operator token.

## Non-Functional Requirements

Private mode-0600 body files outside Git; per-run AES-GCM authenticated encryption,
bounded/chunked ciphertext logs, strict result validation, bounded polling,
cleanup even when start/worker/log retrieval fails. No raw exceptions/payloads.

## Acceptance Criteria

* Fake az proves explicit/automatic paths, source mismatch refusal, job failure,
  timeout, encrypted transport, private files and deletion.
* Worker uses canonical protected/atomic SQL installation and verifies no drift.
* Existing setup and initializer tests remain green; Ruff on changed Python and
  CI-gated files, targeted mypy and local app smoke.
* Runbook supplies exact single command, image build and private-host fallback.
* Live authorization/image/network/SQL/browser evidence remains Not run.

## Phase Checklist

### P01 Transport and SQL worker

* [x] P01-T01 Extract shared SQL preparation; implement worker and image COPY.
* [x] P01-T02 Add validated ephemeral-job execution and wire setup fallback.

### P02 Evidence and delivery

* [x] P02-T01 Add transport/worker tests and documentation.
* [x] P02-T02 Run local validation and record changes for one Review.

Source implementation and validation are complete. One Review executed:
Complete, outcome Residual work. Commit 37af66e is published on the topic
branch and PR #370 targets main. Only the separately authorized live and
operational follow-ups remain; no unimplemented source tasks.

## Test Ownership and Boundaries

Transport tests: infra/tests/test_staff_azure.py; integration:
infra/tests/test_setup_entra.py; worker/SQL:
infra/tests/test_initialize_workbench_staff.py and test_staff_azure.py.
Remove none. Add at most two Python modules and one test file; image is the
only generated build target, not built here. Semantic tests cover SQL verification
and result confidentiality, regression tests preserve local behavior.

## Critique Disposition

Executed once; verdict Revise. All eight findings accepted for direct correction:
PC-001 worker restart with API-only role; PC-002 use documented CLI JSON-line
job logs while the worker remains alive for retrieval, fail closed if inaccessible;
PC-003 exact ARM-ID/environment/subnet/admin guards before secret upload;
PC-004 fallback only on preflight (never uncertain apply/validation);
PC-005 one replica, no retries, post-commit verification;
PC-006 collision guard, owned stop/delete with absence polling;
PC-007 versioned AES-GCM envelope bound to run/operation/input, strict chunks;
PC-008 explicit image helper/manifest copies and local manual-roster enrichment.

Public CLI source inspected on 2026-10-16:
https://github.com/Azure/azure-cli-extensions/blob/main/src/containerapp/azext_containerapp/_params.py
defines job logs show --execution/--replica/--container/--format json/--tail
(maximum 300) and warns a replica may disappear after pod cleanup. The worker
therefore holds its completed encrypted response for 60 seconds before exit;
the client reads during Running, then requires Succeeded. Log endpoint access
is a deployment prerequisite, never inferred from fake az.

Wire contract: one bounded AES-GCM ciphertext, fresh 32-byte key/12-byte nonce,
AAD run+operation+input SHA-256; numbered 1500-character chunks, maximum 128
chunks, no missing/duplicate/conflicting records. Input maximum 12 KiB.
Cleanup budget (90 seconds) separate from the 600-second execution deadline; reserve random
job ID, refuse existing resource, stop on uncertain start, delete and poll 404.
Local candidate/check fallback may run after process failure because those modes
cannot write SQL; explicit validation responses are terminal. Never move an
uncertain local apply to another host.

## Follow-Up Items

Authorized live image build/deployment and tenant/private SQL/browser acceptance.

## Handoff

Changes: .copilot-tracking/changes/2026-10-16/run-in-azure-changes.md.
