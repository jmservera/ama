---
title: Plan - #1297 correction C2
date: 2026-11-09
task_id: issue-1297-c2
---

## Executive Summary

Apply the pinned Ruff 0.17.1 formatter to tools/rpi-checks.py so the infrastructure format check passes. Formatting only; sensor selection semantics are unchanged. No heavy validation here.

## User Decisions and Requirements

* Correct only the formatter violation using the pinned Ruff version; preserve C1 semantics and all evidence.
* Run focused tests, ruff lint, ruff format check (exact gate flags and version), mypy; external scratch; no heavy workloads.
* Research: .copilot-tracking/research/2026-11-09/sensor-mssql-gate-1297-c2-research.md.

## Goals

`ruff format --isolated --line-length 100 --check` passes for tools/rpi-checks.py and tools/test_rpi_checks.py.

## Scope and Non-Goals

* In: formatting of tools/rpi-checks.py lines 745-748.
* Out: behavior, tests, #184, speculative selection widening.

## Functional Requirements

* `changed_groups` behavior is identical before and after.

## Non-Functional Requirements

* Pinned ruff 0.17.1 and mypy 2.4.0 in an external venv; no new ignored files in the worktree.

## Acceptance Criteria

* Pinned format check exit 0; lint, mypy and tools tests pass; the diff touches only the formatter hunk.

## Phase Checklist

* [x] P01 Apply pinned formatter and validate

## Critique Disposition

Not run. The change is a mechanical, behavior-preserving format of one expression with an unambiguous tool-produced diff, so a final-candidate critique adds no information; recorded as an explicit skip, not a pass.

## Follow-Up Items

* Coordinator: fresh current-base full gate; the C1 failed receipt is historical.
* C1 residuals RV-002 and RV-003 and the #184 overlaps remain.
