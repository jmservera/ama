---
title: Faster local gate implementation plan
ms.date: 2026-10-27
---

Task: #470 / faster-gate-470. Status: Ready after direct critique dispositions.

## Executive Summary

Add a conservative changed-path tier, bounded parallel group scheduling, and
same-candidate failed-group resume without reducing any full-tier check.
Scope-aware verification defaults to full; partial verification is explicit.
Measure this tooling branch's fast tier, not a prohibited full benchmark.

## User Decisions and Requirements

* Implement --changed, --jobs N, --resume and receipt scope in tools/rpi-checks.py.
* Unmapped paths select the full matrix. Preserve exact-commit receipt binding.
* Keep one host lock and serialize shared SQL/build/environment resources.
* Correct coordinator policy: parent/sub-issue stacks, risk-tiered local tests,
  verification images retained through receipt verification.
* Run unit tests and one measured fast tier; never run the full gate here.
* Commit, push topic branch, open PR to main using Refs #470 only.

## Goals

Reduce unnecessary checks and repeated successful work with honest evidence.

## Scope and Non-Goals

Runner, tests, directly related documentation/coordinator policy and dated RPI
evidence. No cache/image-reuse optimization, Azure, full benchmark or merge.

## Functional Requirements

* Deterministic path mapping includes transitive project/setup dependencies.
* Receipt records mode, paths, selected groups and full/partial scope.
* Verify recomputes selection and rejects partial evidence by default.
* Preserve per-group trusted command order under parallel completion.
* Resume accepts only failed immutable receipts for the same clean identity,
  tools, evidence, successful environments and live images. Never execute
  receipt-provided argv. Use a new external attempt directory; reference and
  verify the immutable parent receipt for reused groups. Recreate only needed
  runtime setup in trusted setup groups, never rerun successful test groups.
* Schedule only ready groups; fail dependent groups when their prerequisite
  failed. Serialize editable metadata updates, namespace-vshared operations,
  API environment mutations, SQL and image builds.

## Non-Functional Requirements

Use the standard library, conservative affinity/cgroup CPU and available-memory
worker bounds, unique concurrent logs, reliable child cleanup, and unchanged
scan freshness/skip policies. Insufficient resources fail explicitly.

## Acceptance Criteria

Selection, scope, command-order invariance, resume invalidation/reuse and
resource scheduling have unit coverage. Existing mutation tests remain.
A real changed-path run is timed on a committed branch candidate; verification
is explicit partial, never a full-gate claim. PR distinguishes historical full
timings from the measured fast tier and unmeasured parallel full projection.

## Phase Checklist

<!-- P01 -->
### P01: Implementation

* [x] P01-T01: Add selection/scope and group dependency contracts.
* [x] P01-T02: Refactor dispatch/state for bounded concurrency and safe resume.
* [x] P01-T03: Add tests and update coordinator/source gate documentation.

<!-- P02 -->
### P02: Validation and publication

* [ ] P02-T01: Run tools unit tests, focused Ruff/mypy and measured fast tier.
* [ ] P02-T02: Preserve independent Review, commit, verify final exact HEAD,
  push and open a PR to main.

## Test Ownership and Change Budget

Canonical tests: tools/test_rpi_checks.py. Removals: none. Add at most 18
test methods using parameterized subtests for path mappings and invalidations.
Semantic coverage: selection, receipt scope, resource/dependency scheduling,
resume identity checks. Regression coverage: existing command/evidence mutation
suite remains mandatory. Generated targets: external logs/receipts only.
Validation: `python3 -m unittest discover -s tools -p test_rpi_checks.py`;
focused pinned Ruff/mypy; one `--changed` run. No full gate.

## Critique Disposition

One independent critique executed, verdict Revise. All findings are compatible
planner-owned corrections, applied without a second critique:

* PC-001: concrete mapping/bootstrap table added to details.
* PC-002: conditional verifier and explicit partial opt-in added to details.
* PC-003: replace in-place resume with immutable parent/new-directory attempts.
  Successful group evidence is verified in its original environment; fresh
  setup groups prepare only environments needed by the remaining groups.
* PC-004: all project/namespace installs precede parallel snapshot readers;
  namespace and API shared-venv consumers remain ordered.
* PC-005: conservative two-CPU/four-GiB worker reservation, one-GiB headroom,
  affinity/quota and host/cgroup availability constraints.
* PC-006: inspect trusted selection before timing; abort if full is selected.

## Follow-Up Items

Full parallel benchmarking remains unmeasured by explicit owner instruction.
Shared pip cache and image reuse are deferred to avoid freshness-policy changes.

## Handoff

Research: .copilot-tracking/research/2026-10-27/faster-gate-470-research.md.
Details: .copilot-tracking/details/2026-10-27/faster-gate-470-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-27/faster-gate-470-changes.md.
