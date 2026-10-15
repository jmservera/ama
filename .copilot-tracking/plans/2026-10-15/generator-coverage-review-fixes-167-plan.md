---
title: Generator coverage PR review repair plan
description: Bounded consistency and CLI exit fixes for PR 312
ms.date: 2026-10-15
---

## Task Metadata

Task `167-review-fixes`, slug `generator-coverage-review-fixes-167`.
Parent `167` / `src-generator-coverage-167`. Branch feat/src-generator-coverage-167.

## Executive Summary

Enforce covered/delivered equivalence, expose missing or deferred needs as
open gaps and return CLI exit 1 for them. Replace routing_validated with
routing_shape_validated and issue_existence=not-assessed. Use ordinary
TemporaryDirectory in CLI tests. Keep the canonical partial-child baseline
successful without implying output conformity or owner approval.

### What You May Not Know

The provenance register registers datasets, not issues; consuming_issues does
not list most child closure routes. Neither is a complete issue allowlist.
The user explicitly permits honest shape-only checks instead of issue
existence validation. No GitHub lookup, hardcoded issue registry or invented
approval is required.

## Sources

Research disposition reused/Ready: supplied PR #312 findings, issue #167
acceptance, src/core/src/zava_forward/core/synthetic/coverage.py,
src/core/tests/test_generator_coverage.py, public needs-inventory.json and
provenance-register.json. No new research artifact is needed.

## User Decisions and Requirements

* Fix both findings and test all four mutations; run the full short RPI loop.
* Work only on the supplied topic branch/worktree; commit artifacts and push
  to that branch, no new PR, main push, force push or merge.
* Code stays in src; no private data, forbidden SQL or configuration paths.
* Use /tmp/zf164/bin ruff/mypy and the requested core unittest invocation.
* Keep Refs #167 and unmet acceptance criteria unticked.

## Goals

Make report semantics and CLI failure status accurately distinguish closure
consistency, open gaps and unverified issue existence.

## Scope and Non-Goals

Modify the existing coverage module, its tests, core/pack READMEs, knowledge
index/log and repair tracking artifacts. No removals or new production/test
files. Maximum additions: two focused test methods plus expanded existing
tests. Canonical inventory/scenario/provenance files remain unchanged; no
generated targets. No generator output, issue registry, live data or approval.

## Functional Requirements

* Covered requires delivered; delivered requires covered.
* Missing needs and deferred closures are reported in open_gaps by need ID.
  CLI writes that honest JSON and returns 1; partial child routes remain valid.
* Issue identifiers remain shape-checked only, explicitly not existence-checked.
  Remove routing_validated; expose routing_shape_validated and issue_existence.
* Malformed/contradictory input raises ValueError and CLI emits no success JSON.
* TemporaryDirectory() uses its normal location and cleans itself up.

## Non-Functional Requirements

Deterministic JSON, stable ordering, no input mutation, standard library only,
typed new code, unchanged human/consent/release controls.

## Acceptance Criteria

* Mutations cover #99999 honestly unassessed, issue-less deferred partial
  (open gap and CLI 1), covered child (ValueError/CLI 1), and unchanged child
  flipped missing (open gap and CLI 1).
* Covered deferred and partial/missing delivered are also rejected.
* All requested core tests, ruff lint/format and mypy pass, with exact commands
  and results in changes; repeatable baseline CLI remains exit 0.
* Documentation, index, log and PR claims reflect the narrower contract.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Repair and verify

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement consistency, open-gap reporting and mutation tests

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Synchronize docs and execute requested checks

<!-- rpi:phase id=P02 -->
### [x] P02: Review and publish

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Review once, commit evidence and push existing branch

## Critique Disposition

One independent final-candidate critique executed: Pass, no findings.
Evidence: .copilot-tracking/reviews/plans/2026-10-15/generator-coverage-review-fixes-167-plan-critique.md.
No revision or additional decision required.

## Follow-Up Items

* Existing issue #167 generator-convention, owner mapping and output/platform
  acceptance gaps remain outside this repair; do not mark them complete.

## Handoff

Details: .copilot-tracking/details/2026-10-15/generator-coverage-review-fixes-167-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-15/generator-coverage-review-fixes-167-changes.md.
P01/P02 complete: nine coverage tests and all 307 core tests pass; ruff lint,
format check and mypy pass. One Review Complete/Conformant for the bounded
repairs. Commit 0f1b556 pushed and remote/PR head verified; existing PR body
updated honestly. Closeout tracking commit persists final publication evidence.
No unresolved repair decision or blocker. CI and owner merge remain separate.
