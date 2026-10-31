---
title: Browser asset matcher implementation evidence
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Metadata

Task ID: pr-594-browser-asset-matchers-568. Implementation date: 2026-10-30.
Plan: `.copilot-tracking/plans/2026-10-30/browser-asset-matchers-568-plan.md`.
Details: `.copilot-tracking/details/2026-10-30/browser-asset-matchers-568-phase-details.md`.

## Execution Status

Complete, full plan scope. P01/P01-T01/P01-T02/P02/P02-T01/P02-T02 complete. No active implementation markers remain.

## Execution Summary

Implemented one anchored asset matcher across seven harnesses, preserved behavior assertions, added five regression test methods and the related guide, and ran locked browser/engineering validation. One original critique Complete / Revise is preserved; PC-001 rejected as inapplicable, PC-002 accepted and incorporated before implementation.

## Approved Boundary and Planned Validation

New helper/test, seven named browser checks and API guide only. No app/UI/dependency change, Azure, secrets, remote write or closing keyword. Validate original CI sequence, all seven affected harnesses, relevant units, Ruff lint/format and typing using task-owned pip environment and shared heavy lock. Generated outputs stay external in this session's `files/`.

## Completed Work

### P01-T01: Shared asset instrumentation

Added `checks/asset_urls.py` and updated all seven identified browser checks. Routes/unroutes/waits, request failures, DOM observation, coverage and asset ordering/count selection now use the anchored pattern. Origin-bound page routes preserve the deny guard. Leaflet still asserts real body/MIME/length and now revalidation plus byte-derived ETag.

### P01-T02: Tests and guide

Added five test methods covering bare/query/segment variants, false positives, native route/wait/unroute, off-origin denial, DOM observer and actual CDP counts, plus coverage filtering/duplicate/missing-view semantics. Updated the API guide with matcher behavior and locked CI commands. Validation pending.

## Implementation-Time Plan and Detail Updates

### Preserve actual warm-cache evidence

P01-T01 / PC-002 compatible disposition clarified: do not add Playwright routing to the asset-cache context, since routing disables browser cache and invalidates the existing warm-cache proof. Page fault-injection matchers in other checks bind to the owned origin; shell now has the local-only context guard. This is an immediately relevant correction preserving approved cache intent, not a new product decision or another critique. Plan and details reconciled.

### Correct the newly exercised employee retry count

P01-T01 / P02-T01: original CI sequence, workspace scripts and loading/briefing all passed after correction. Employee workspace then failed its old total-two ops request assertion: proper versioned interception now exercises the actual initial request plus two bounded retries before document reload. Assert that exact initial three-attempt budget, then exactly one further ops request after reload. This preserves and strengthens actual retry/reload proof rather than merely increasing an arbitrary count. Remaining checks resume after this surgical in-scope assertion correction; original failed output is preserved in `fixed-validation.log`.

## Validation Record

Original pre-edit CI sequence failed at the exact case-journey fallback timeout; see Research C7 and external `baseline-ci.log`.

Post-edit API `ruff check .` and `ruff format --check .` passed. All five `test_browser_asset_urls` methods passed under the heavy lock, including actual Chromium routing/waits/unroute, off-origin abort, DOM observation and CDP `(1, 1)` counts for bare/query/segment variants. Initial lint exposed import ordering and loop capture in new test callbacks; formatter/import sorter and explicit callback bindings resolved those before test execution.

### Commands and outcomes

All commands ran from `src/api` with task-owned pip environment on PATH and `PYTHONPATH=tests:../core/tests:../agents/tests`. Browser and unit chains used exactly `flock -w 600 /tmp/ama-rpi-heavy.lock bash -c 'set -e; ...'`.

| Check | Command / scope | Result |
| --- | --- | --- |
| Baseline CI | `python -m checks.design_system_browser_check`; workflow curl for axe; `python -m checks.regulatory_ux_check --axe <axe> --out <baseline.json>`; `python -m checks.case_journey_browser_check --axe <axe> --out <baseline-directory>` | Expected failure: original journey fallback timeout |
| Corrected CI | Same three browser commands and pinned curl, fresh `fixed-*` outputs | Passed all three; genuine plain-enhancement fallback and browser zoom exercised |
| Workspace scripts | `python -m checks.workspace_scripts_browser_check` | Passed actual initial/retry failures, delayed lexical execution, late-load/navigation/sign-out/401 and real Leaflet revalidation |
| Loading briefing | `python -m checks.loading_briefing_browser_check --axe <axe> --out <fixed-loading-briefing>` | Passed all shell, companion, law/helper and async/axe scenarios |
| Employee workspace | `python -m checks.employee_workspace_browser_check` | Passed after exact three-before/one-after reload count correction |
| Chat widget | `python -m checks.chat_widget_browser_check --axe <axe> --out <fixed-chat-widget>` | Passed including actual shared script recovery and employee/resident behavior |
| Case-view UX | `python -m checks.case_view_ux_browser_check --axe <axe> --out <fixed-case-view>` | Passed both failure paths, geometry, keyboard/touch and zero-violation focused axe scans |
| Asset cache | `python -m checks.asset_cache_browser_check --out <fixed-asset-cache>` | Passed both actual sites' warm legacy reuse, same-origin turnover, CSS/JS/shared/vendor and ETags |
| Selected units | `python -m unittest test_browser_asset_urls test_static_assets test_workspace_scripts test_chat_widget_focus test_case_journey test_design_system test_accessibility_baseline test_content_standard -q` | 73 tests passed, 5.980s |
| API lint/format | `ruff check .`; `ruff format --check .` | Passed, 64 formatted files |
| Strict new-code lint/format | `ruff check --isolated --config 'src = ["src", "tests"]' --select E,F,I,B,UP --target-version py312 --line-length 100 checks/asset_urls.py tests/test_browser_asset_urls.py`; `ruff format --isolated --line-length 100 --check checks/asset_urls.py tests/test_browser_asset_urls.py` | Passed |
| Type check | `mypy` | Passed 122 source files |
| Optional strict whole-case-view probe | Isolated Ruff on current and `git show HEAD:src/api/checks/case_view_ux_browser_check.py` | Same ten pre-existing B023/E501 diagnostics; not the repository CI criterion |
| Diff | `git diff --check` | Passed |

Python 3.12 task-owned pip installations target this worktree's `src/core`, `src/agents`, `src/api[dev]`; Playwright 1.64.0, Chromium 156.0.8078.4. No uv, cloud or live model used. Original checked-out HEAD: `b5ef6a1229b7d634868507db3ad8dca77678c890`.

### External evidence identities

Root: `/home/azureuser/.copilot/session-state/7dc0069c-bd97-46db-8804-627147673f47/files/`.

| File | SHA-256 |
| --- | --- |
| `baseline-ci.log` | `b61a9587e4ed95b8a2b78a3f9839d158b50efa299fd7a9c2c9d6aaa4c8bd0545` |
| `fixed-validation.log` | `493fe2f9bf3a1905a39db805e4d5f971d0b56f633e7cb50f6f2f3690ba7abe98` |
| `remaining-validation.log` | `d13ba1d567e2dd9b39102586465b571ac4e6f06a5b9a8141f0b2983af855c4bc` |
| `axe-4.10.3.min.js` | `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb` |

Before/after outputs remain original, not rewritten after corrections. `fixed-validation.log` includes successful CI/workspace/loading checks and the initial employee count failure; `remaining-validation.log` proves the repaired employee check and every remaining command. Generated screenshots/JSON are external only.

## Pre-Review Reconciliation

Ready: plan markers/details/summary are current; full-plan evidence, exact commands, adverse intermediate output and final passing results agree. No implementation blocker or remaining active work. One independent original Review is next.

## Blockers

None.

## Remaining Work

None within the implementation plan.

## Follow-Up Items

Hosted rerun, publication gate and human/live approval remain outside local correction.
Optional legacy isolated case-view lint cleanup is follow-up-only, not a new correction requirement.

## Return-to-Caller State

Automatic parent owns continuation; full-plan implementation Complete / Review-ready. Proven: original local CI browser failure before edits, passing original CI sequence after matcher correction, all seven affected checks, 73 selected units and lint/types. Not proven: hosted rerun, full publication gate, live employee deployment, human approval or WCAG acceptance. Segment tests prove instrumentation only.
