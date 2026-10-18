---
title: Issue 76 current-stage blockers phase details
description: Task-level execution and evidence requirements
ms.date: 2026-10-18
---

Task ID: 76. Status: P01/P02 and P03-T01/T02/T03 complete; publication pending.
Primary owns plan and details; tightly coupled planning performed inline.
P03-T03 original Review executed Complete / Residual work, no defects; bounded
correction Conformant. P03-T04 publication remains, not yet claimed complete.
Main moved to observed 9c648b2006e8b2e563823ea7d5aabdf7f1ac7096; no
integration is authorized or performed. Publication preserves exact original
base and frozen source boundary; coordinator controls any integration.
Six new test methods, no removals; lifecycle SQL method also uses real child
writers for SQLite and actual MSSQL. No production deviations or source
correction cycles used. Evidence and historical failed attempts are in changes.

<!-- P01 -->
## P01: Canonical stage semantics

### P01-T01

Use supplied fully signed synthetic DATA case as positive control; independently
remove funding, technical sign-off or resident decision without mixing causes.
Compare early/final/post-final stages through Store and SqlStore and HTTP.
Future requirements remain in blockers with current_stop false. Current holds
must dominate selection and keep hazard clocks. No mocking canonical evaluator.
Record exact red command and failures on original production base. Author and
run the P02-T01 certified-index upgrade regression in this same pre-source gate.
Record unchanged production source hashes against original base.

### P01-T02

In taskqueues.context compute actual final-check applicability; pass it to each
funding/resident/technical block. Compute active list once; use it for selection
and blocked membership. Remove now-redundant final-check fallback if covered:
pending handoff must not hide a current final-check reason/action. Keep helper
and gate semantics unchanged. Reuse READY_STAGE if import cycle can be avoided;
local existing stage string is acceptable without broad stage refactoring.

<!-- P02 -->
## P02: Durable membership compatibility

### P02-T01

Add internal membership evaluator revision to SQL fingerprint; public VERSION
unchanged. Seed deliberately stale old-format certified flags and reopen;
expect repair to explicit IDs/flags without body, rowversion, seq or ledger
change. Check generation increment. This tests migration, not merely new seeds.
Place the shared portable regression in SqlQueueMembership. Remove seed then
reopen with self.make_store(self.seed), preserving the identical string path
so inherited MSSQL make_store does not wipe. Certify the literal original
fingerprint [VERSION, as_of, controls.today(), ranking.CURRENT], retaining all
other valid inputs and schema; wrong flags must be repaired by internal revision.

### P02-T02

Use existing save/lock and SQL generation machinery. Clear prerequisite, observe
previously warm second connection, reopen with no seed for SQL; JSON save/reopen
parity. Actual local SQL Server must exercise same new inherited SQL tests.
Use task-owned uniquely named container bound to loopback ephemeral host port,
synthetic credentials, no volumes and prompt cleanup; never touch other services.

<!-- P03 -->
## P03: Validation and publication

### P03-T01

Sanitize inherited environment with env -i for every application/test probe;
explicit test helper PYTHONPATH contains tests only, never mvp or source paths.
Set TMPDIR explicitly to $PWD/.venv/issue76-tmp (absolute workspace path) and
verify tempfile.gettempdir() under that same sanitized environment. Clean only
task-owned scratch after all child processes stop.
Installed editable packages from task-local .venv. Record exact commands,
counts, failures/skips honestly. Run taskqueues/sqlqueues/API, coupled stock,
technical/finance/workflow/building/projection suites; configured full component
lint/format/mypy. Docker application smoke is relevant if feasible to prove
packaged backend behavior, not UI acceptance. No browser needed without web edits.

### P03-T02

Component guides explain inactive future requirements, actual final-check stop
and internal persisted membership migration. Preserve historical measurements.
Freeze candidate with git diff digest and individual source/test SHA-256 before
one Review. Changes artifact records commands/results, source boundary and
original critique/review hashes; adverse originals never overwritten.

### P03-T03

One independent Review worker activates rpi-review and assesses frozen diff,
plan and actual evidence. Write only original review artifact under reviews/logs.
Original finding set remains even if correction receipt is necessary. No second
Review or claim of independent closure; maximum two source correction cycles.

### P03-T04

Reconcile every plan checkbox, actual validation and state. Verify remote main,
report movement without rebase; get gh api user and configure local noreply
email for both author/committer. Conventional Commit plus Copilot trailer.
Commit all task artifacts only. Push topic normally, create main PR with only
Refs #76 issue reference. Declare exact base/head, source/artifact boundary and
unmet acceptance. Do not merge or edit issue/board; stop for coordinator review.
