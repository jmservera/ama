---
title: Issue 133 aftercare criteria changes
task_id: 133-aftercare-criteria-2035
date: 2026-11-13
---

## Changes

* `src/core/src/zava_forward/core/aftercare.py`: wider savings, blame and causation patterns; negated-claim exemption; `propose_pack` no longer writes concern history; restore refuses a closed remedy with no outcome or evidence.
* `src/api/src/zava_forward/api/web/aftercare.js`: evaluator shows households raising a concern with denominator, closure-unresolved count, out-of-scope count, baseline windows and per-home unresolved denominators; malformed figures read Unknown.
* Tests: `test_aftercare.py`, `test_aftercare_intake.py`, `test_aftercare_screen.py`.

## Divergence

Code edits began before the plan file was written; the plan and details were authored afterwards and the single critique ran on plan plus diff. No other divergence.

## Validation (pip venv `/tmp/venv-133ac-2035`, removed before commit)

* core `test_aftercare*`: 119 tests OK (15 skipped, existing); api `test_aftercare*`: 25 OK; `test_content_standard` and `test_accessibility_baseline`: 34 OK.
* `ruff check` and `ruff format --check` on core, agents, api: clean. `mypy` in core, agents, api: clean.
* `python -m checks.aftercare_browser_check`: all PASS (not assistive technology or human acceptance).
* Not run: full local RPI gate, hosted CI. Tier: focused (software tests and UI text, no infrastructure, permission or deployment change).
* `src/agents` has no aftercare tests or module; the pack lives in core.
