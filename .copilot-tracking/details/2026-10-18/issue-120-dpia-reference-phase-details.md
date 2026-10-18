---
title: Issue 120 DPIA reference phase details
description: Evidence and completion expectations for bounded implementation
ms.date: 2026-10-18
---
<!-- markdownlint-disable-file -->

# RPI Phase Details: issue-120-dpia-reference

## Metadata

Task ID: issue-120. Date: 2026-10-18.
Plan: .copilot-tracking/plans/2026-10-18/issue-120-dpia-reference-plan.md.
Evidence: .copilot-tracking/research/2026-10-18/issue-120-dpia-reference-research.md,
especially C1-C12 and the retained failing-first direct/HTTP log.

Validation precondition (PC-001): create ignored `.venv/task-tmp` and export
TMPDIR as its absolute path before all subsequent Python test/probe commands.
Record `tempfile.gettempdir()` in execution evidence. Docker binds the same
task-owned directory to `/scratch` with TMPDIR=/scratch and writable permissions
for UID 10001, retaining read-only root. Clean only task-owned generated scratch
contents. Preserve all original adverse outputs. No shared fixture changes.

## Phase Index

| Phase | Name | Status | Task |
| --- | --- | --- | --- |
| P01 | Failing-first regressions | Complete; 3 selected tests fail on unchanged base, 13 failures | P01-T01 |
| P02 | Predicate and documentation | Complete; shared status predicate, narrow prose | P02-T01 |
| P03 | Verification and reconciliation | Complete; local/image 23+2, configured checks and boundary proof pass | P03-T01 |

<!-- rpi:phase id=P01 -->
## P01: Add failing-first bounded regressions

Existing 16 tests miss the contradiction. Own changes only in existing
test_timecapture.py, no shared fixture/server edits. Use literal SQLite DDL and
INSERTs to seed matching invalid request, activation and acknowledgement with
distinct managers, not the fixed admission methods. Use fallback and existing
SharedStoreTests.make_store; compare every row before/after and restart.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Exercise token rejection and retained history

* Matrix: absent, empty, whitespace, yes/true/on/1 with mixed case/outer whitespace.
* Fresh fallback: run all four denied actions, assert no file or parent directory.
* Seed invalid history with current references and current notice version; status
  must report invalid even if requested/activated diagnostics retain history.
  No new rows in any of the four tables; existing rows retained unchanged.
* Valid D1 and DPIA-2026-007 and non-prefix strings: verify trimmed refs in
  requests, activation, entries. Existing notice, aggregates and own entries
  tests stay authoritative and unchanged.
* Mutate the same instance's env valid-to-bareflag, deny all writes; change to
  D2, require new request and activation. Preserve valid-to-valid semantics.
* Actual authenticated HTTP: construct synthetic local data in temp directory,
  use existing App/handler and roles, assert 403 and reference error, no new
  time audit events and no new time store. Join owned server threads.
* Dependencies: critique completed. Completion evidence: preserved selected
  failures before source changes; later full suite with no skips.
* Maximum seven methods/two small shared test helpers, zero removals.

<!-- rpi:phase id=P02 -->
## P02: Implement predicate and narrow documentation

C2-C3 show both enable and capture gates already depend on status.
No changes to `_refs`, SQL, schema, connections, audit/HTTP or import graph.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Wire shared status admission

Derive bool(dpia) and stripped lower/casefold not in the four-token set.
Use the result in both DPIA reason and dpia_recorded. Keep reason plainly
about recording a DPIA reference, with boolean-flag rejection explained.
Keep flag-off reason precedence unchanged. Module doc/README may name tokens,
but must explicitly state presence is not authenticity/legal approval.
Dependency: P01 failures recorded. Completion: smallest source diff and AC1-AC6.

<!-- rpi:phase id=P03 -->
## P03: Verify and reconcile handoff

Keep actual pass/fail/skip outcomes distinct. Configured formatter and mypy
have pre-existing legacy exclusions for the affected files; report honestly.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Run focused checks and prove boundary

From src/api run installed task venv with
`PYTHONPATH=tests:../core/tests:../agents/tests ... -m unittest test_timecapture -v`.
Rerun research probe separately, never overwrite its adverse original.
Run API `ruff check .`, `ruff format --check .`, `mypy`.
Compare source AST against git-show exact base: everything except status and
module prose must be identical, including DDL, statements, storage hooks and
imports. Retain original source/test/README SHA-256 and git blob hashes.
Use Docker only for a unique task image/container; no shared instance removal.
Build context src/; installed module hash must match the changed source. Run
non-root/read-only/cap-drop/no-new-privileges synthetic loopback tests/probe.
If practical runtime is blocked, record command and blocker, not a pass.
Do not use actual MSSQL if the boundary comparison proves it unchanged;
prior 2026-10-15 engine claims lack a reproducible exact log/count and remain
historical only. If SQL/runtime changes become necessary, stop affected scope
for coordinator authorization rather than silently expanding.
Completion: commands/logs, plan/details reconciled, changes record complete,
single original independent Review ready. No unresolved implementation question.

Observed completion: local 23 tests and 2 probe tests pass; installed hardened
image independently runs the same 23+2 with source hash match, UID 10001,
read-only root, zero effective capabilities and no-new-privileges. No skips.
AST proof and API configured checks pass; scratch empty after test cleanup.
Full actual commands, original failures and known exclusions are in the changes
record. No new MSSQL, browser, WCAG or human-governance acceptance claimed.
