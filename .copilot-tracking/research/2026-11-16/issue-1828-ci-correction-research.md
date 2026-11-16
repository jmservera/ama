---
title: Issue 1828 CI correction cycle 2 research
description: Research for the hosted src-api mypy failure on PR 1829 head 8e9324b
ms.date: 2026-11-16
ms.topic: reference
---

## Scope

* Second correction cycle of #1828 (first: `issue-1828-review-correction`, head 8e9324bc69a59bc4efbd128fa50d1cf7974649e7, base main 18d3de459f20018e91fab3af87ab0d89123661c6). Original and first-correction research, plan, details, critique, changes, review, evidence and witnesses are preserved unmodified. The first-correction independent exact-head review Pass is historical for the new head.
* Tier FOCUSED: one unit test patch target, tracking artifacts and external browser evidence. No application, authorization, consent, map or keyboard behaviour change; no workflow, gate, dependency or Dockerfile change.
* Sources: issue #1828, captured log `/tmp/issue-1828-src-api-ci-failure-43919746064.log`, `docs/reference/README.md`, `docs/reference/memory.md`, the first-correction research and plan. The change touches no web UI file, so the web-design-guidelines rules have no changed web file to review (disclosed, not a conformance claim).

## Finding

Hosted `src-api` run 43919746064 job 133483906173, step Type check, failed on the exact head after 17m28s: `tests/test_map_viewport_premise.py:97: error: Module "checks.map_fullscreen_browser_check" does not explicitly export attribute "time"  [attr-defined]`. The test used `patch.object(check_module.time, "monotonic", monotonic)`; mypy treats the check module's `import time` as private (not re-exported).

## Evidence

* Reproduced locally from `src/api` with `/tmp/1828/venv/bin/python -m mypy` (Python 3.12.3, mypy 2.4.0 as pinned in `pyproject.toml`, project distributions installed editable from this worktree): the same single error (`.copilot-tracking/evidence/2026-11-16/issue-1828-ci-correction/mypy-failing-first.log`). Ruff 0.17.1 installed. No install needed.
* The patched object is the global `time` module's `monotonic`, so patching it by dotted string target (`checks.map_fullscreen_browser_check.time.monotonic`) resolves the identical object at runtime and keeps the deterministic virtual clock; mypy does not inspect a string target.
* Heavy lock `/tmp/ama-rpi-heavy.lock`: `flock -n` succeeded and `fuser` showed no holder at 17:55Z, so the full browser check can run on the new head.

## Options

| Option | Result |
| --- | --- |
| `patch("checks.map_fullscreen_browser_check.time.monotonic", monotonic)` | Same runtime target, no import change, passes mypy; selected |
| `import time` in the test and `patch.object(time, "monotonic", ...)` | Same effect, adds an import; equivalent |
| Add `__all__`/`as time` re-export in the check | Changes the harness module for a test concern; rejected |
| `# type: ignore` | Weakens the type check; rejected |

## Planning readiness

Ready. Research disposition: executed (the baseline mypy reproduction ran before the research-open witness; the order is disclosed in the changes record).
