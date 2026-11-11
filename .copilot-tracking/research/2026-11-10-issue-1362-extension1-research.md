---
title: "Research: issue 1362 extension E1 visible associated version"
description: Research for the checker-only fix that makes the associated Current design version assertion require genuinely visible text
author: Copilot
ms.date: 2026-11-10
ms.topic: reference
---

## Scope and authority

* Task `issue-1362-extension1`, parent `issue-1362-inherited-one`. Owner approved up to five additional corrections on 2026-11-10 23:13 for the existing checker scope. This task is E1; four remain after it. The earlier inherited correction (spent) and its conservative minimum of zero are unchanged history. No push, PR, GitHub write or product change.
* Research disposition: `executed`, targeted. Original findings and the D3 records are consumed, not re-diagnosed.

## Evidence consumed

* Independent review `ROOT/independent-1362-inherited-one-1352/functional/functional-findings.json` (head `1f91d6dc`): the original whole-panel substring Medium is resolved; one new Medium: `Element.checkVisibility()` with no options ignores `visibility:hidden` and `opacity:0`, so a CSS-hidden correct-valued associated field passes (`dt.checkVisibility() && dd.checkVisibility()` at `DESIGN_VERSION_FIELDS`).
* D3 `ROOT/handoff-1362-visibility-d3-1358.md` and `ROOT/checks-1362-visibility-d3-1358/run-1280.log`, `run-320.log`: real served synthetic fixture, real unchanged `check_technical`, Playwright 1.64.0, Chromium 156.0.8078.4. Positive control PASSED; `dd` and `dt` with `visibility:hidden` and with `opacity:0` all PASSED wrongly at 1280 and 320. Default `checkVisibility()` was true in each case; `checkVisibility({visibilityProperty:true, opacityProperty:true})` was false in each case (observed only).
* Original run-count deviation (one extra browser run, one probe, two extra diagnostic executions) is preserved unchanged.

## Current state

* Merged ordinary `origin/main` `6d4cd624` into the branch (clean, no conflict, no rebase): head `a6c8df61`. The checker blob `dad25ca526a24b7718aeb9c45b477c16b5199081` and test blob `b53e39d9dde911207d4b91b21546f10c5d53711b` are identical to the reviewed `1f91d6dc` blobs, so the defect is not already fixed and not materially different. Unit baseline 17 tests OK.
* Scenario manifest: `src/core/src/zava_forward/core/synthetic/scenario_manifest.py` binds the `recipe` to `src/api/checks/workbench_browser_check.py` and the workbench manifest, not to `atlas_tensions_browser_check.py` (searched by file name). No recipe SHA update is expected; the integrity tests need not run for this change.
* Existing browser tests in this directory use an opt-in `ZF_BROWSER_TESTS=1` skip guard (`tests/test_chat_panel.py`).

## Findings and options

* Smallest fix: pass `{visibilityProperty: true, opacityProperty: true}` to both `checkVisibility` calls in `DESIGN_VERSION_FIELDS`. These options also cover ancestor opacity and visibility. `contentVisibilityAuto` stays off (the panels use `content-visibility: auto` and a scroll-into-view; enabling it would break the 320px rendering already fixed with `textContent`).
* Coverage gap: the existing `visible=False` double cannot exercise the in-page extraction. Add an opt-in real-Chromium regression (`ZF_BROWSER_TESTS=1`) using `page.set_content` with the real `check_design_version`: positive, `dd`/`dt` `visibility:hidden`, `dd`/`dt` `opacity:0`, wrong value. Run it set, so it is not skipped; the default unit run reports it as skipped and the handoff states that.
* Rejected: a Python-side fallback, a timeout increase, a broad `except`, skipping the assertion, `innerText` use.

## Planning Readiness

Ready.

## Limits

Local assertions are not host or model attestation. No axe, assistive technology, WCAG, usability, live or whole-issue acceptance. Playwright 1.64.1 and harness-leak history for D1 stay adverse.
