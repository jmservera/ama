---
title: Stock fabric link 168 phase details
description: Evidence and completion boundaries for the bounded implementation
ms.date: 2026-10-15
---

Task 168 / stock-fabric-link-168.

<!-- P01 -->
## P01: Migrate and resolve

<!-- P01-T01 -->
### P01-T01: Core implementation and existing consumer wiring

Research C3/C4/C8/C9. Move existing stock fabric implementation without a
second generator or compatibility copy. Preserve random call order and v1
seed string. Use TypedDict records and Mapping inputs. Link against counted
stock IDs rather than a set; reject invalid/duplicate case IDs, mark ambiguous
stock references unlinked with reason. Shared anchors remain allowed source
references with explicit warnings, not unique dwelling assertions. Preserve
legacy report counters, add per-case resolutions and case metadata; no runtime
reseed or home-field reconciliation. Update existing support consumers' imports and minimally replace their
enrichment call site with core attach_fabric; no new resolution algorithm in
support. Fingerprint the moved dependency closure, retaining legacy support
16-hex revision shape and core full-SHA revision shape.

Reuse provenance.prepare_output/source_revision/file_hashes and output_dir.
CLI accepts register CSV and optional cases JSON, defaults through ZF_DATA,
validates all input before opening fresh output directory; no stdout raw
records, no repository destination or symlink escape. Summary contains declared
weights, seed, version and revision. Optional linked case JSON retains history
and consent unchanged. Errors exit nonzero visibly.

<!-- P01-T02 -->
### P01-T02: Exact semantic and regression evidence

Core owns tests. Use 60,000 fictional ID/locality/form rows, assert exact count,
uniqueness and synthetic labels, deterministic draws and totals. Freeze a small
legacy-v1 golden payload before the move. Test negative case/stock IDs, complete
unlinked reasons, shared-anchor counts and order independence. CLI tests use
temp dirs, ZF_DATA, exact-byte reruns, hashes and nonempty/repo/symlink refusal.
The new non-exempt typed test owner drives the retained builder against one
60,000-row register and checks all 980 cases against that same fabric input.
It closes SQLite before reopening and compares all case linkage/fabric/EPC
metadata, histories and consent; top-level link report remains seed-only.
Existing generated tests receive only migration import/metadata expectation
updates; all new behavioral assertions live in the typed test owner.

<!-- P02 -->
## P02: Evidence and delivery

<!-- P02-T01 -->
### P02-T01: Documentation

Research C7: cite SN-01 in PR and synthesis. Replace obsolete generator command
with installed core CLI. Historical 980/825 claims stay historical, not rerun
evidence. State private register generator unavailable, reconciliation pending,
assumptions not company facts, source anchor not unit proof. Index and append
log; do not update memory or original case study.

<!-- P02-T02 -->
### P02-T02: Local verification

Missing distributions and tools were observed at intake. Create ignored
worktree-local .venv with python3 -m venv and pip-install editable src projects
with development tools. Run each project's unittest discovery with README
PYTHONPATH fixtures where required, ruff check/format and mypy. Run coverage CLI
against public inventory. Run loopback application with fictional data and
SQLite; verify health/case resolution and no forced AI activation. Attempt
Docker image build once, recording permission denial if present.
Document every invoked command and outcome, retries, skips and limits.
Do not read credentials or call real inference/deploy without prerequisites.

<!-- P02-T03 -->
### P02-T03: Review and PR

One post-implementation RPI review against plan and command evidence. Do not
loop implementation/review; route residual findings. Resolve gh identity and
set repository-local privacy-safe email, Conventional Commit plus prescribed
trailer. Commit all task artifacts, push only named topic branch; PR base main,
Refs #168, command/results table and unchecked original acceptance items.
CI is the authority for unavailable image/SQL checks; do not merge.

## Execution Reconciliation

P01-T01/T02 and P02-T01/T02 completed with the evidence in the changes record.
P02-T03 completed one Review, implementation commit d72bc87, authorized topic
push and draft PR #316 to main. Review outcome Defects found; RV-001 remains
open for later implementation. GitHub reports concurrent-main conflicts and
no CI checks, not a passing remote result. Private corpus/owner reconciliation,
actual model/SQL Server/Azure/human gates remain unverified; this is lifecycle
execution completion, not original issue acceptance. No further source edits.
