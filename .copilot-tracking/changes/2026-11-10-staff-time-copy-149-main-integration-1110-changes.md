---
title: Parent 149 component-only main integration changes
ms.date: 2026-11-10
task_id: 149-copy-main-integration-1110
---

## Changes (2026-11-10, after plan and single critique)

* Fast-forward only, no reset: local `a04668ae94b5c2f38e6c55ed789db245e8c71d16` to owned parent `befe28e48bb5d916dfda000321a0d31059e92989` (tree `a05c35128390805b18a88e4791229b11ef1b2456`).
* Pre-merge records commit `68ce891f088b74adf3429617d1a58e7695e319e2` (research, plan, details, critique only).
* Ordinary merge (`--no-ff`, no conflict, exit 0) of pinned main `ddeebd01694ddb46b456451d9ac6390347e51aaa` (tree `b917297ef34bc3e7e7948f9e46ffe6b7e66e6c88`): merge commit `19e2ec981e1964b884b8c640e99571fc75d4f06e`, tree `0ba46247138ecc17a5431dfd393216b03d09521b`, parents `68ce891f...` and `ddeebd01...`.
* Product delta against the pin is exactly `timecapture.js` (blob `14e0b5adbd9f183986b01bbe095b7189c10059f1`) and `test_timecapture_copy.py` (blob `f7cac3acd97407bed67d8a08e9263171c67b1f2f`), both identical to the parent blobs before the merge. No product edit was made by this task; no conflict resolution was needed.
* Timestamp correction: the committed research, plan and critique first carried clock labels 00:44Z, 00:45Z and 00:47Z that were ahead of the actual clock (`date -u` read 00:38:58Z at start, 00:39:57Z after the browser run). They were corrected in the freeze commit to the actual window; commit order, not the labels, proves the plan preceded the merge.

## Validation (focused tier; raw logs in `/tmp/zf-149-1110/logs/`; venv `/tmp/zf-149-1110/venv`)

| Id | Result |
| --- | --- |
| V1 `v1.log`, `v1-pip.log` | exit 0. `zava_forward.api`, `.core`, `.agents` resolve under this worktree (`src/api`, `src/core`, `src/agents`). Ruff 0.17.1, mypy 2.4.0, Playwright 1.64.0 (declared pins), Python 3.12.3, Node v24.21.0 |
| V2 `v2-nobrowser.log` | exit 0, 12 run, 5 skipped (opt-in browser cases; not accepted as evidence) |
| V3 `v3-browser.log`, `v3.exit` | one nonqueued `flock -n /tmp/ama-rpi-heavy.lock` admitted (lock free), `ZF_BROWSER_TESTS=1`, exit 0, 12 run, OK, 0 skipped, all 5 `StaffTimeGuidanceBrowser` cases `ok` (7 `StaffTimeGuidanceText` cases `ok`) |
| V4 `v4.log` | `test_timecapture`, `test_content_standard`, `test_workspace_scripts`, `test_role_screens`, `test_static_assets`: exit 0, 62 run, OK, 0 skipped (matches 26+18+5+8+5) |
| V5 `v5-check.log`, `v5-format.log` | `ruff check .` exit 0 "All checks passed!"; `ruff format --check .` exit 0 "135 files already formatted" (whole `src/api` project) |
| V6 `v6-mypy.log` | project `mypy` from `src/api`, exit 0, 212 source files, no issues (not single-file) |
| V7 `v7-node.log`, `v7-diffcheck.log` | `node --check timecapture.js` exit 0; `git diff --check HEAD~1 HEAD` exit 0 |
| V8 | blob identity as above, equal to parent |

Environment: `cd src/api`, `PYTHONPATH=tests:../core/tests:../agents/tests`; no `ZF_DATA`, credential, provider or Azure variable; `ZF_BROWSER_SCRATCH` unset.

## Not run

Full API suite, full local gate or receipt, SQL and mssql store tests, Azure, provider or model calls, private data, axe, assistive technology, human or DPO review, hosted CI on this head. The main delta moved Core, Agents and API server code that this component does not use; the focused checks above do not assert those areas.

## Unmet criteria (literal)

* No hosted CI exists for the merged head.
* No independent exact-head assessment has run yet; it must precede publication.
* No push, PR, issue or board action; nothing published.
* Whole 149 and whole 153 acceptance, production acceptance and assistive-technology acceptance are not established; no criterion is ticked.
* Origin main is now `3b8d3209893e49b240ec3484b5f1067ec6ec5a61`, newer than the pin; it is not integrated.
