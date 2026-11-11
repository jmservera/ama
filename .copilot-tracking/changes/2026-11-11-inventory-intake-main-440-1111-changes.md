---
title: Inventory and staff intake current-main checkpoint changes (Refs 440, 131, 132, 1362)
ms.date: 2026-11-11
task_id: 440-inventory-intake-main-1111
---

## Implementation start

Implement phase opened 2026-11-11T00:17:47Z (witness seq 4) after the plan, details and one critique existed and the `plan-done` marker (seq 3, 00:17:43Z) was recorded. Documentary checkpoint only. Plan, research and marker timing: `research-open` and `launch` were recorded together at 00:15:33Z after the research record existed, and `plan-done` and `implement-start` were four seconds apart; none of that attests earlier reading or planning time, which is shown only by commit order and the file contents.

## Process notes and deviations

* Preflights (strict duplicate-key state parse, schema check, `load_artifacts`) ran and passed before `research-open`, `plan-done` and `implement-start` (`ROOT/phase440-inventory-intake-preflight-1111.log`). No marker was recorded on a failed preflight; none failed.
* One edit of the details file (the five critique corrections) and the state phase updates were made with a Python or `sed` one-liner instead of the edit tool. The content is the intended content; this is a tooling-rule deviation, disclosed, not a behaviour change.
* The `research` file was edited once after `research-open` (a clock label and the exact predicate correction) so its current hash differs from the marker hash; research is not a guarded artifact in the witness, and the critique and review are untouched after their records.

## Environment

* Private venv `/tmp/ama-440-inventory-venv-1111` (Python 3.12.3); `pip install -e src/core -e src/agents -e src/api` exit 0 (`p1-venv.txt`). Namespace package paths and the editable `zava-forward-core`, `-agents`, `-api` locations all resolve under this worktree (`p1-origin.txt`); `resident_decisions.py` and `staff_intake.py` import from `src/core/src`. `checks` resolves to `src/api/checks`.
* `ZF_DATA`, `.env`, credentials, provider, Azure and production variables unset; `~/.zava-forward` absent before and after. `PYTHONPATH` carried only the existing test-helper directories (`tests`, `../core/tests`, `../agents/tests`).
* Raw directory: `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/inventory-intake-main-440-observation-1111/` (`*.out`, `*.err`, `*.exit`, `*.start`, `*.end` per command).

## Observations (all against pinned `0509ddcef14d9c2046791b283fad65229f536202`; times UTC)

| Id | Command (existing tests only) | Exit and result |
| --- | --- | --- |
| O1 | `cd src/core && PYTHONPATH=tests python -m unittest tests.test_resident_decisions -k inventory -v` (00:18:23Z to 00:18:34Z) | 0; ran 48, 31 ok, 17 skipped. All 17 skips are the `MssqlResidentControls` inventory cases (opt-in owned loopback SQL Server); the JSON class and the SQLite `SqlResidentDecisions` subclass ran the other 31 |
| O2 | `cd src/core && PYTHONPATH=tests python -m unittest tests.test_resident_decisions.JsonResidentDecisions.test_resident_acceptance_never_clears_technical_or_hazard_gates ...test_quality_dependencies_are_scoped_and_unknown_evidence_cannot_release -v` | 0; ran 2, 2 ok, 0 skipped |
| O3 | `cd src/api && PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest tests.test_resident_api -k inventory -v` | 0; ran 1 (`ResidentApi.test_http_household_inventory_is_opt_in_refusal_only_and_hidden`), ok. The test prints a logged traceback "Rule evaluation unavailable for ZF-1 ... The law store is not loaded; rule checks are unknown." from a swallowed rule-engine call; it is preserved in `o3-api-resident-inventory.err`, does not fail the test and shows the fixture runs without a law store |
| O4 | same environment, `tests.test_staff_intake_api -v` (00:18:36Z to 00:19:37Z) | 0; ran 90, 56 ok (run minus skipped; the final line is `OK` with no failure or error, and per-test status lines are interleaved with the logged "Rule evaluation unavailable for ZF-3" noise described for O3, which is preserved raw), 34 skipped: 30 `MssqlStaffIntakeApi` cases (needs `ZF_STAFF_INTAKE_MSSQL=1`) and 4 `JsonStaffIntakeApi` cases skipped because "the commit-time read dependency is an SQL store contract" (withdrawal, reissue, unrelated commit and existing validation token) |
| O5 | same environment, `tests.test_role_endpoint_inventory tests.test_content_standard -v` | 0; ran 42, all ok, 0 skipped. The role matrix includes the new `field-intake`, `field-capture`, `field-correct` and `field-acknowledge` routes |
| O6a | `tests.test_atlas_tensions_checker` before Playwright was present (00:20:03Z) | exit 1: `ModuleNotFoundError: No module named 'playwright'` (import error, 1 error, 0 tests run). Actual failure of a declared dependency in the private venv, preserved in `o6a-atlas-nobrowser.err`; not a product defect |
| O6 restore | `python -m pip install playwright==1.64.0` into the private venv (the version pinned by `src/api/pyproject.toml` dev extra) | exit 0 (`o6-restore-playwright.txt`); no global or shared install |
| O6a2 | same selector, no `ZF_BROWSER_TESTS` | 0; ran 20, 3 skipped (the opt-in Chromium class); not accepted as browser evidence |
| O6b | admission: `fuser /tmp/ama-rpi-heavy.lock` exit 1 (free), MemAvailable 8,236,612 kB, Chromium 1248 cached; `ZF_BROWSER_TESTS=1 ZF_BROWSER_SCRATCH=/tmp/z440inv flock -n /tmp/ama-rpi-heavy.lock timeout 900 python -m unittest tests.test_atlas_tensions_checker -v` (00:20:09Z to 00:20:14Z) | 0; ran 20, OK, 0 skipped, including the real-DOM negative controls for the exact Current design version field. Constructed synthetic data on a loopback owned server; the scratch directory was not left behind |
| O7 | `tests.test_staff_intake_browser` | Not run, blocked: it needs `ZF_STAFF_INTAKE_BROWSER=1` and the pinned `ZF_AXE_PATH` (axe-core 4.10.3); `ZF_AXE_PATH` is unset and a bounded search found no axe file. The prerequisite is not a declared Python package and was not installed or fetched. The screen's four axe states are therefore not observed on this head |

Selector classes that do not exercise the combined journey (an inventory-managed case, staff-mediated capture, then independent QA): every selector above. A scan of all `src/*/tests/test_*.py` found no function body that sets up an inventory and calls `accept_quality`, `submit_quality`, field capture or `staff_intake`, and none that calls QA accept or handover with tenure or inventory setup. The QA positive control (`test_recorder_is_denied_and_independent_qa_accepts` on the non-inventory case ZF-3) ran inside O4 and passed; the inventory-managed refusal control exists only as the shared gate (`resident_gate` returning the unchanged `TENURE_HOLD`, asserted in O1 with and without a scope binding) plus the static trace that `accept_quality` and `hand_over_quality` call `require_resident_clear`. This is implemented but unverified at the combined-journey level, not a defect.

## Source and main identity

* Worktree HEAD at the end of observation `0509ddcef14d9c2046791b283fad65229f536202`; `git status` showed only own `.copilot-tracking` files; no source edit, no commit yet.
* A fresh `git fetch origin main` at 2026-11-11T00:20:21Z read `7e2744cf7774825b21c73fffbc075b95755239cc` (tree `d77ac24dae1ebd84a9260161d2d1f610acf3f785`), one commit past the pin (`chore(rubric): record score 78/100`, 00:19:28Z) that changes only `.github/rubric/scores/latest.json`. `git diff --name-only 0509ddcef origin/main -- src infra` is empty, so the observed source equals current main source. No merge or rebase was made to refresh.

## Changes

* `docs/architecture/cutover-evidence-pack.md`: appended the dated section "Household inventory and staff intake current-main checkpoint (2026-11-11)" and updated `ms.date` to 2026-11-11. Earlier sections unchanged.
* `docs/reference/log.md`: appended a dated entry and updated `ms.date`. No index change was needed (no knowledge-base file was added, moved or retired).
* No source, test, workflow or dependency-manifest change. No new regression test, issue, push or GitHub write.
* `git diff --check` clean; touched text is ASCII; relative links point to existing files or to the review that is created in the next phase.

## Unmet or not run

* MSSQL cases (17 in O1, 30 in O4), JSON-class SQL-contract cases (4), the staff intake browser and axe journey (O7), and any combined inventory-to-QA journey: not run or no selector exists.

## Readiness correction (2026-11-11, additive; original claims above are kept)

* Root's finding: `git diff --check 0509ddce HEAD` on committed head `d174ab85347a49386c92a42aefe0513f6a3a9f58` reported "new blank line at EOF" at line 55 of this file. The earlier "`git diff --check` clean" claim ran before this file was staged and so did not cover it; that claim was incomplete for this file, not a full committed-range check.
* Correction: the trailing blank line at the end of this file was removed in a follow-up commit (no amend or rebase). The final committed-range result is in the follow-up handoff and the review amendment.
* Follow-up O7b (the original O7 blocked result above stays as recorded). Existing owned asset `/tmp/axepk/package/axe.min.js` reads `axe v4.10.3`, its package.json version is 4.10.3 and its sha256 `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb` equals the `AXE_SHA256` the test pins at `test_staff_intake_browser.py:19` (the test asserts it again at run time). Admission: `fuser /tmp/ama-rpi-heavy.lock` exit 1 (free), MemAvailable about 9.3 GB. Command, from `src/api` with the private venv: `ZF_STAFF_INTAKE_BROWSER=1 ZF_AXE_PATH=/tmp/axepk/package/axe.min.js PYTHONPATH=tests:../core/tests:../agents/tests flock -n /tmp/ama-rpi-heavy.lock timeout 900 python -m unittest tests.test_staff_intake_browser -v`, 00:36:53Z to 00:37:01Z, on head `d174ab85` (source tree identical to the pin). Result: exit 0, 2 run, OK, 0 skipped; five axe states printed with no violations (pack open nothing recorded, rejected capture inline error, recorded not acknowledged, acknowledged, duplicate reconciled). Raw: `o7b-*` files in the observation directory. Limit: constructed synthetic data, JSON store, loopback server, one browser; not accessibility acceptance, not MSSQL, not an inventory-managed case or QA journey.
* No install, fetch, queue, source, test or manifest edit; `~/.zava-forward` still absent.
* Disposition: the original owner-pending recommendation for a combined test stays as historical. Root has since routed one technical test-only E2 under existing #132 on `7e2744cf7774825b21c73fffbc075b95755239cc` in a separate worktree. It is not yet run or read here; the combined inventory-to-QA acceptance gap stays unverified until real results are read. No product, legal, consent or approval decision is made. Whole #131, #132 and #440 stay open; no #1420 expansion.