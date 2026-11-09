---
title: Issue 164 F2 correction1 phase details
description: Phase details for the receipt-declared wording and execution-completeness correction
ms.date: 2026-11-08
---

## Phase 3 design

* Wording constants: `SERVING_DECLARED_FALSE` begins `declared not exercised: receipts declare memory_used false (declared by receipts, not independently observed panel consumption)`; unknown begins `unknown: receipts or execution incomplete`; deviation begins `deviation: receipts declare memory_used true`. `INTEGRATED_MEMORY` and the component scope text avoid observed claims.
* `run_scenario` returns `execution_complete`: a local flag set true after the non-AI probe, false on the outer exception or constructor failure.
* `memory_scope`: coverage is the declared-false statement only when every result has `execution_complete` true, receipts exist, every receipt has boolean `memory_used` and none is true. Otherwise unknown, or deviation if any receipt declares true. Adds `incomplete_scenarios`. Component probe counts are always summed from results.
* Static open item reworded to neutral component-only text referencing `summary.memory_scope`. README paragraph reworded.

## Phase 3 tests (existing file)

* Mixed good plus constructor-failed scenario: unknown, incomplete id listed, gate outcome unchanged.
* Late partial probe: probe turn then a turn with an unknown `before` op: probe count 1, incomplete, unknown.
* Expected assertion failure keeps the declared-false statement (not blindly unknown).
* Declared false, declared true and unknown wording; static open item never says observed or consumed.
* Update the hand-built `memory_scope` rows to carry the new marker.

## Phase 4

From `src/agents` in `/tmp/f2-164-venv` with `PYTHONDONTWRITEBYTECODE=1`, external pycache prefix, ruff and mypy cache directories: `unittest tests.test_chat_eval tests.test_chat_heldout`, ruff format check and check, mypy, each exit code captured separately, plus the new cases run against the b2f blob.

## Critique amendments (applied before implementation)

* CR1-001: record `turns_asked`; evidence complete only when `execution_complete` and receipts equal turns asked.
* CR1-002: unknown takes precedence over deviation; true declarations counted separately.
* CR1-003: gate row recomputes or falls back to unknown for stale scopes lacking the new fields.
* CR1-004: static open item reworded; bindings salt unchanged.
