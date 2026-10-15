---
title: Stock fabric link 168 implementation plan
description: Bounded src migration and acceptance evidence plan
ms.date: 2026-10-15
---

Task: 168 / stock-fabric-link-168. Status: Ready, critique corrections applied.

## Executive Summary

Reuse and relocate PR 246's fabric generator to core; preserve v1 seeded draws.
Add honest per-case stock reference resolution, reject ambiguous register
identities, and provide a non-destructive CLI writing private results via
ZF_DATA. Verify against fictional 60,000-row stock and retained 980-case builder.
No private corpus, owner ratification or live Azure/AI acceptance is claimed.

## User Decisions and Requirements

* Full RPI loop with committed research, plan, details, changes and review.
* Worktree and branch fixed by user; src-only new code/tests, pip only.
* Accepted ADR 0006, parity matrix and merged moves are authoritative.
* Cite SN-01 and existing coverage CLI; preserve existing seeds and identifiers.
* No .env, .vscode, issue-cache edits, private data, deployment or main pushes.
* Refs #168; leave evidence/owner-dependent criteria unchecked.
* Local suites, ruff, mypy, synthetic app run and Docker attempt before CI.

## Goals

Make stock fabric reusable from installed core without support imports; retain
the existing generator lineage and distinguish stock references from unit truth.

## Scope and Non-Goals

Core synthetic module/tests; migration import/provenance wiring and minimal
core-operation call-site substitutions in support;
existing generated tests and directly related docs. No new stock generator,
database schema, AI behavior, approval, resident consent or workload edges.
SN-01 bounded maintenance is explicitly requested at the existing volumes;
the broader inventory owner review is not represented as satisfied.

## Functional Requirements

* Every case has one resolution or explicit reason for being unlinked.
* Missing/blank/unknown/duplicate stock references cannot silently link.
* Duplicate/invalid case IDs fail explicitly instead of losing rows.
* Shared valid anchors remain visible and are not called verified unit links.
* Fabric rows retain v1 draws, labels and documented assumption weights.
* CLI defaults inputs/outputs via ZF_DATA, refuses repo destinations and
  nonempty snapshots, and emits summary, hashes, revision and optional case links.
* Builder/EPC consume core; builder attaches per-case resolution and only
  generates fabric/EPC for uniquely matched register rows.

## Non-Functional Requirements

Typed new module/tests with no lint/type exemptions; core imports no workload;
no new dependency or SQL; deterministic output independent of register ordering
at the row level. CLI errors are explicit and do not produce success reports.

## Acceptance Criteria

* Local: exact 60,000 fabric rows; every one labelled; stable IDs and unchanged
  seeded attribute payload; same seed byte equality and changed-seed variation.
* Local: complete 980-case accounting; missing, blank, ambiguous and shared
  links plus duplicate case rejection and SQLite restart coverage.
* Local: assumption-labelled summary, revision and payload hashes; private-safe
  CLI with output containment and no overwrite.
* Issue: actual retained private-stock acceptance stays unverified.

## Phase Checklist

<!-- P01 -->
### P01: Migrate and resolve

* [x] P01-T01 Move fabric to core, type it, preserve draws, add resolution model
  and safe CLI; wire builder/EPC and source revision.
* [x] P01-T02 Add focused semantic/scale tests and extend generated integration
  coverage; keep approval/consent semantics untouched.

<!-- P02 -->
### P02: Evidence and delivery

* [x] P02-T01 Update core README, knowledge-base synthesis/index and append log;
  record unchecked criteria and owner decisions.
* [x] P02-T02 Run all five src suites, ruff/format/mypy, synthetic local app,
  coverage CLI and Docker attempt. Record commands/results and limits.
* [ ] P02-T03 Review once, commit and push artifacts/code and open PR to main.

## Locked Test Ownership and Validation

New semantic owner: src/core/tests/test_stock_fabric.py (one new test module
maximum). Extend existing test_generated_dataset.py for builder integration;
remove no tests. Canonical generator: core/synthetic/stock_fabric.py, old
support/zf_stock_fabric.py removed, no shim/copy. Generated targets: only fresh
temporary paths, never committed. At most one test added to an existing
cross-project test file if needed for actual app integration; prefer existing
API suites plus loopback smoke. Full-scale standalone test uses fabricated
register IDs, no private records. No production runtime changes required.

## Critique Disposition

Executed once: .copilot-tracking/plans/2026-10-15/stock-fabric-link-168-critique.md.
Verdict Revise; all seven findings accepted as direct planner corrections:

* PC-001: core attach_fabric owns resolution/enrichment; support substitutes
  calls only, retaining existing EPC generation after validated selection.
* PC-002: per-case source-register match, explicit non-unit scope and shared
  flag; legacy home counters explicitly defined as anchor counts; correct note.
* PC-003: new typed semantic test drives retained builder with exactly 60,000
  fictional rows and checks all 980 cases against fabric from that same input.
* PC-004: valid IDs are nonblank strings without surrounding whitespace,
  preserved verbatim. Bulk fabric rejects malformed/duplicate IDs before writes;
  diagnostic link report marks ambiguous/invalid references explicitly.
* PC-005: core revision fingerprints module, provenance and destination helper;
  legacy support revision retains 16 hex and includes the moved dependency
  closure. Test changed source bytes, root-independent fingerprint and golden
  pre-move A/B/C mapped/fallback seeded values.
* PC-006: new typed integration test closes SQLite then reopens and compares
  anchor, resolution, fabric/EPC for all cases. Top-level link report is
  seed-only metadata, not a new SQL document.
* PC-007: keep all new semantic/integration assertions in the new typed,
  non-exempt test owner. Existing generated tests receive import and revision
  expectation updates only; no widened exemptions or unrelated cleanup.

No significant/divergent owner decision. No repeated critique.

## Follow-Up Items

* Owner: supply/regenerate private stock or explicitly defer; confirm SN-01
  inventory scope and mapping and whether unit-level linkage is required.
* Owner: decide reconciliation of 980-case home.built/type and stock fabric.
* Authorized environment: actual AI/SQL Server/Azure/human acceptance.

## Handoff

Research: .copilot-tracking/research/2026-10-15/stock-fabric-link-168-research.md.
Details: .copilot-tracking/details/2026-10-15/stock-fabric-link-168-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-15/stock-fabric-link-168-changes.md.
Continue automatically after compatible critique dispositions are applied.
Implementation evidence: P01 and P02-T01/T02 complete. One post-implementation
Review complete, outcome Defects found: RV-001 destination containment needs
later implementation; owner/private/live gates remain unverified. P02-T03
pending authorized draft topic-branch delivery, not another source/review pass.
