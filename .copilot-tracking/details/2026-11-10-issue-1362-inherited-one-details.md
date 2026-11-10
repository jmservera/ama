---
title: "Details: issue 1362 inherited one correction"
description: Phase details for the exact Current design version field assertion
author: Copilot
ms.date: 2026-11-10
ms.topic: reference
---

## Phase 1: baseline (no source edit)

* Environment: `python3 -m venv --system-site-packages /tmp/ama-1362-env`, then `pip install playwright==1.64.0 ruff==0.17.1 mypy==2.4.0` (the declared dev pins in `src/api/pyproject.toml`); the system site had 1.64.1, 0.17.3 and 2.4.1. Cached Chromium 156.0.8078.4 launches under 1.64.0. Record version and import origin in the logs.
* Working directory `src/api`, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH` of the worktree `src/api`, `src/core/src`, `src/agents/src`, `src/api/src` and `src/core/tests`. Scratch and logs external under `ROOT/phase1362-inherited-one-evidence-1110/`.
* Commands: `python -m unittest tests.test_atlas_tensions_checker -v`; `python -m checks.atlas_tensions_browser_check`; `python diag_1362.py control` and `mask` (the D1 script, copied unchanged, drives the real served Technical queue and the real `check_technical`, mutating only the associated dd).
* Expected baseline classes: `10` and duplicate label pass on the natural fixture; `2`, Unknown, empty and missing label pass on the mask fixture; positive control passes.

## Phase 2: checker edit (`src/api/checks/atlas_tensions_browser_check.py`)

* New module constant `DESIGN_VERSION_FIELDS`, an in-page function over the Design version section returning, for every `dt` whose trimmed text is exactly `Current design version`, `{value, visible}` where `value` is the trimmed `innerText` of the immediately following `dd` (or `null`) and `visible` is `dt.checkVisibility() && dd.checkVisibility()`.
* New `check_design_version(section, expected, where)`: exactly one field; visible; value non-blank; value equals `str(expected)` exactly. Each is a separate `check` call so the failure names the cause.
* In `check_technical`: locate the one `section.screen-record` whose heading is exactly `Design version`, assert it is one, scroll it into view (panels use `content-visibility: auto`), call the helper with `technical["design_version"]`, and drop `str(technical["design_version"])` from the substring loop. `design_name` and the note stay whole-panel substring checks (unchanged, out of scope).

## Phase 3: regressions (`src/api/tests/test_atlas_tensions_checker.py`)

* Add a `_Section` double whose `evaluate` returns the supplied field rows, and `DesignVersionFieldTests` covering: exact `1` passes; `2`, `Unknown`, `10`, empty and whitespace value, missing label (no field), duplicate label (two fields, first correct) and an invisible field each raise `AssertionError`. The helper takes only the field rows, never the panel text, so a `1` in another field cannot satisfy it; the browser negative control proves the in-page script.
* RED evidence: unchanged checker lacks the helper (import error) and the D1 baseline diagnostic shows the whole-panel false passes.

## Phase 4: verification

Unit module, `tests.test_role_screens_conformance`, atlas trace test (from `src/core` as in earlier corrections), full Atlas browser check with the named cases at 1280 and 320 as the check defines them, D1 diagnostic control and mask on the candidate, `ruff check`, `ruff format --check` (line length per `pyproject.toml`), `mypy --strict` on both files with an external cache and no bytecode.

## Phase 5: records

Changes record (including the debit of the one inherited cycle and the conservative remaining minimum of zero), single Review, state, witness events, local commit with both identities and the Copilot trailer, freeze handoff `ROOT/handoff-1362-inherited-one-1110.md`.
