---
title: Issue 176 implementation plan
description: Bounded offline provenance and acceptance audit
ms.date: 2026-10-16
---

Task: 176. Slug: synthetic-determinism-176.

## Executive Summary

Complete the available offline provenance improvement and independently audit
all three issue criteria. The original stock register generator is absent;
neither new fixtures nor passing sensor tests establish its reproduction.
Preserve that gap in the PR instead of claiming complete issue acceptance.

## User Decisions and Requirements

* Deliver in the existing worktree, build in src/ and infra/ only.
* Offline only; no private data, Azure, setup-entra or legacy tree changes.
* Produce research, plan, changes and review; tests, related READMEs, reference
  index and append-only log; push PR using Refs #176.
* Named human legal, compliance, DPO, consent, safety and financial authority
  stays unchanged. Exercise owner is Juan Manuel Servera, not an agent.
* Do not edit issue checkboxes; coordinator audits them at merge.

## Goals

Make fabric snapshot replay inputs explicit; retain current deterministic
scale/sensor behavior and surface acceptance gaps with executable evidence.

## Scope and Non-Goals

Edit existing fabric CLI/test, related READMEs and KB log/index only, plus RPI
artifacts. No new generators, outputs, dependencies or source migrations.
No real stock reconstruction, policy approval, live reset, Azure or AI calls.

## Functional Requirements

* Optional --as-of must be strict ISO, clock-free, recorded as unknown when
  omitted; label only, not a filter or date of real evidence.
* Hash exact consumed register and optional case bytes without publishing
  their content or paths; preserve algorithm version and row bytes.
* Reject invalid dates and nonempty refresh destinations before writes.

## Non-Functional Requirements

Type-safe, pip-installed core, tests outside package, deterministic UTF-8
output. No runtime dependency additions; preserve current default behavior.

## Acceptance Criteria

| Issue criterion | Planned evidence / boundary |
| --- | --- |
| Every generator, including stock and sensors, reproduces | Fabric CLI and scale/sensor exact byte tests; original stock generator unavailable, criterion remains unmet |
| Manifests record seed, version, generator revision | Existing support regressions and source CLI assertions, augmented fabric input/date provenance |
| Refresh policy defines cadence, approvals and live protection | Existing proposed policy, clarified replay inputs and retained owner approval gap; refusal tests; no live reset |

## Phase Checklist

<!-- P01 -->
### P01: Provenance and regressions

* [x] P01-T01: Add fabric date and consumed-input fingerprints.
* [x] P01-T02: Extend existing CLI test coverage without changing golden draws.

<!-- P02 -->
### P02: Evidence and delivery

* [x] P02-T01: Run targeted tests, ruff, mypy and local CLI smoke.
* [x] P02-T02: Update documentation and per-criterion audit, append log.
* [ ] P02-T03: Run one post-implementation review, commit and publish Refs PR.

## Locked Test and Change Budget

Test ownership: src/core/tests/test_stock_fabric.py, with existing
test_synthetic_determinism.py, test_sensor_stock.py and test_generated_dataset.py
run unchanged. Removals: none. Maximum additions: two test methods in the
existing stock-fabric test file; no new production or test files.
Canonical targets: stock_fabric.py and these docs; generated targets: none.
Semantic coverage: explicit/unknown/invalid dates, exact input digests,
input/seed/date sensitivity. Regression coverage: unchanged draws,
linked case histories, nonempty destination protection, all snapshot bytes.

## Critique Disposition

One final-candidate critique executed; verdict Revise, then directly disposed.
PC-001 accepted: every review finding needs explicit disposition before delivery;
unresolved in-scope correctness/privacy/write defects block successful delivery.
Only unrelated follow-ups and the already disclosed acceptance gaps may be
deferred. A blocked implementation may only publish with that status explicit.
PC-002 accepted: preserve newline="" CSV semantics from the captured bytes,
test BOM/quoted CRLF, independent raw input mutations and absent cases;
date-only changes must leave every non-summary payload unchanged.
Both corrections fit the locked budget. No second critique or human decision.
Implementation readiness: Ready for the bounded offline slice.

## Follow-Up Items

Obtain the original register generator, pinned OSM inputs and runtime before
claiming stock reproduction. Owner must approve or amend refresh policy.
No operational legal or deployment approval is inferred.

## Handoff

Research: .copilot-tracking/research/2026-10-16/synthetic-determinism-176-research.md.
Details: .copilot-tracking/details/2026-10-16/synthetic-determinism-176-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-16/synthetic-determinism-176-changes.md.
