---
title: In-VNet staff initialization plan
description: Implementation-ready candidate for Refs #360
ms.date: 2026-10-16
---

Task: 360-run-in-azure. Research: .copilot-tracking/research/2026-10-16/run-in-azure-research.md.

## Executive Summary

2026-10-17 rebase-only continuation: verify the existing plan, rebase the
run-owned branch onto fetched origin/main c9ba95f with GIT_EDITOR=true,
preserve both workstreams and stop on ambiguous source intent. Existing
critique is reused, not rerun: no new behavior, test additions/removals,
generated targets or implementation decisions. The caller explicitly
authorizes rebase and this branch's force-with-lease push only.

<!-- P04 -->
### P04: Rebase verification and publication

* [x] P04-T01: Rebase onto origin/main; combine index/log conflicts without
  dropping #176 recovery/source evidence or existing #175 delivery.
* [x] P04-T02: Fresh isolated pip venv; targeted staff/pipeline and full infra
  tests, exact recorded Ruff/format/mypy commands and git diff --check.
* [x] P04-T03: One bounded rpi-review of resolutions and preservation; record
  local completion evidence. Review Complete, outcome Residual work.

P04 local RPI execution is complete. Publication is the parent-owned final
action after this evidence commit: push once with explicit lease, update
PR #370 as Refs #360, report final SHA and stop. Publication has not occurred
at this record's write time; PR readback/final response supply that receipt.
No follow-up or tracking-only repush.

Test ownership and removals: unchanged, none. Maximum additions: zero.
Canonical targets: conflict resolutions and existing dated artifacts only.
Docker is denied on this VM; no bypass or image-build claim. Local compiler
checks are allowed offline, but no Azure service calls/writes are authorized.
Planning verification: Complete/Ready; existing final-candidate critique and
dispositions remain applicable, with no new critique execution claimed.

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

## Correction cycle 1 (2026-10-17)

Task identity remains 360-run-in-azure. Research complete, Ready. Candidate
readiness: Ready after one cycle-specific critique; earlier critique is retained
as historical implementation evidence, not repeated.

### Correction executive summary

Install the existing hashed `src/api/requirements.txt` before full infra
discovery in both MVP validation and src namespace CI. Reuse the existing
workflow dependency validator and mutation patterns to prevent removal,
unhashed substitution or late installation. No application/runtime or guard
changes. Preserve commit 126ecae's manifest context and decoded-result timeout
tests; independently demonstrate both catch in-memory regressions.

### Correction requirements and boundaries

The owner's explicit full-loop instruction authorizes each phase and
same-branch commit/push/PR update, not automatic follow-up work. Use a new
/tmp Python 3.12 venv and pip, never uv. The old MVP installation was reproduced
there: 21 staff tests, 14 failures/four errors, missing cryptography. Test code
must continue using real crypto. All prior deployment/acceptance blockers
remain honest and unchanged; no Azure/data/credential/live Graph work.

### Correction goals and acceptance

Both known full-infra workflow steps explicitly install the same hash-pinned
operator/runtime dependencies before tests. Full infra suite must pass with
`REQUIRE_AZ_BICEP=1`, zero skips. Existing CI Ruff/format checks and targeted
mypy pass. Dependency mutations, proof context mutations and real timeout
mutations must fail at their intended assertions. Record exact commands,
results and assessed source boundary; no overall live acceptance claim.

<!-- P03 -->
### P03: CI dependency correction and publication

* [x] P03-T01: Add identical hashed requirements installation in both workflows
  and extend existing workflow prerequisite/mutation tests.
* [x] P03-T02: Clean pip reproduction, full infra and existing lint/format/type
  checks; execute preserved image and timeout regressions plus mutations.
* [x] P03-T03: One cycle-specific Review, artifact reconciliation, privacy-safe
  Conventional Commit, push same branch and update PR #370 with Refs #360.

### Correction test ownership

Owner: `infra/tests/test_pipeline.py` for dependency contract, at most two
new test methods and a small extension to the existing validator. Removals:
none. No new tooling or dependency manifest; reuse the generated runtime lock.
Canonical edits: two workflow YAMLs and that test module. Generated targets:
none. Directly related quality-gate instructions in infra/README.md also
receive the same dependency command and clean-environment explanation.
Existing `infra/.dockerignore` and `test_staff_azure.py` corrections
must remain byte-for-byte unchanged. Mutation harness stays outside the
repository under the session files directory. No test skipping/crypto mocking.
Full infra discovery validates real encryption/decryption and lifecycle paths.

### Correction follow-ups

Only prior RV-001/RV-002/RV-003, outside active P03. New CI results after push
are not assumed from local passes. Stop after the requested publication.

### Correction critique disposition

Execution: Complete, once for this correction candidate. Verdict: Revise,
PC-009 only. Disposition: rejected because replacing /tmp with a project-local
venv conflicts with explicit caller direction and contradicts observed evidence.
The parent already created /tmp/ama-360-correction1-YRmaea and reproduced
the failure there with pip (21 tests, 14 failures/four errors); the worker's
reported environment restriction is not a parent restriction. Keep the required
/tmp venv. No significant unresolved decision and no repeated critique.
Planning execution: Complete. Readiness: Ready.

### Correction completion receipt

P03 complete. Research, Plan, Implement and Review explicitly complete.
Correction source commit 6976ae9649de291409c771986b818b83e0ebc8ae pushed on
feat/run-in-azure-360; PR #370 updated with Refs #360. Full infra suite rerun
at that committed head: 307 passed, no skips. The following receipt commit
changes tracking artifacts only, not the validated workflows/source/docs.
No further RPI task/session starts. RV-001/RV-002/RV-003 remain unmet.
