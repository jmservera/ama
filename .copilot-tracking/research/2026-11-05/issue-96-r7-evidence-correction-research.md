<!-- markdownlint-disable-file -->
# Research: issue 96 r7 evidence correction

Dated 2026-11-05. Refs #96. Frozen candidate `cbb78c2737bd3c30b560b6cc6cceef000c0b5f75`. Evidence only; no application change. The r6 artifacts and the r5 research are preserved unchanged; this record corrects their handoff diagnosis and disclosure and does not replace them.

## Evidence inspected

* Immutable failed receipt `/tmp/ama-96-gate-r7/receipt.json` (status `failed`, `resume_eligible` true, 258822 bytes) and logs `/tmp/ama-96-gate-r7/0051-project-api.log`, `0043-project-core.log`, `0065-static.log`. `/tmp/ama-96-gate-r7.log` is the console log.
* Policy source: `tools/rpi-checks.py` `EXPECTED_SKIP_REASONS`, `SQL_NOT_APPLICABLE` and `check_skips` (lines ~96-140 and ~1456-1510).
* Skipping test source: `src/api/tests/test_resident_summary_ai_ui.py` lines 52-57.

## Finding 1: the r6 handoff diagnosis was wrong

The final return said "about 3 MssqlApiTests skips" were the cause and treated SQL skips as unexpected. That is not supported.

* `0051-project-api.log` is a discovery run (`unittest discover -s tests -v`, `integration` false, env only `PYTHONPATH`, no `ZF_TEST_MSSQL`). It reports `Ran 1930 tests`, `OK (skipped=344)`.
* The 344 skip lines (counted from the log) are: 210 "needs a SQL Server (ZF_TEST_MSSQL=1)", 58 "needs disposable SQL Server (ZF_TEST_MSSQL=1)", 37 "owned local MSSQL opt-in", 11 "opt-in loopback SQL Server", 8 "opt-in isolated local SQL Server", 7 "opt-in loopback MSSQL", 5 "Chromium is installed by the later browser-check step", 2 "opt-in Chromium journey", and one each of "opt-in local Chromium", "opt-in local Playwright", "JSON does not have a SQL COMMIT acknowledgement boundary.", "opt-in local browser", "Opt-in rendered check requires local Playwright browser." and one Chromium launch failure.
* All of these reasons except one are members of `EXPECTED_SKIP_REASONS`. SQL opt-in skips in a non-integration discovery run are policy-expected; the SQL-enabled phase runs later with `ZF_TEST_MSSQL=1`. (The `SQL_NOT_APPLICABLE` strictness applies only to `integration` commands, and the only integration command in the receipt, `0128-infra.log`, did not skip.)
* The single reason outside policy is `Chromium is not available: BrowserType.launch: Executable doesn't exist at <output>/chromium/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell`, from `test_resident_summary_ai_ui.ResidentSummaryAiUi.test_ai_success_fallback_and_reduced_motion`. The test catches the Playwright error and calls `skipTest` with a free-form message containing the exception, so it cannot match any fixed expected reason and `check_skips` raised `Unexpected required integration/dependency skip`.

Policy-qualified root cause: one skip whose reason is outside the maintained expected-skip set (Chromium missing at the pre-browser-install discovery phase), not the SQL opt-in skips. The earlier return truncated the reported list at a point where only SQL reasons were visible and mislabelled the cause.

## Finding 2: other receipt observations

* `0065-static.log` lines beginning `FAILED required group: ...` are deliberate fixture output of `tools/test_rpi_checks.py` inside an `OK` run, not gate failures.
* The static, infra, image and logo steps completed before the block; this proves nothing about a passing receipt, because the receipt is failed and cannot be used.

## Finding 3: retention and process disclosure (r6 handoff omissions)

* An earlier gate attempt, `/tmp/ama-96-gate-r6`, was interrupted by a 60-second `timeout` I imposed (its failed receipt said "Dirty owned snapshot retained"), then deleted with `rm -rf` and not preserved. Its console log `/tmp/ama-96-gate-r6.log` remains. Its contents were not archived and are not reconstructed here.
* Before that I also deleted generated worktree scratch (`src/*/src/*.egg-info`, `src/core/.ruff_cache`) with `rm -rf`, and the gate itself had blocked on those ignored inputs.
* The r7 run was started with `nohup`/background and watched with repeated long `sleep` polls (240-595 s), which the continuation brief discourages.
* Inspection of finite issue-owned records (`.copilot-tracking/*/2026-11-05`, `.copilot-tracking/rpi-sessions/2026-11-05`, no `.copilot-tracking/archive*` directory) found no archive or restore record for r6 or the deleted scratch. Neither was backed by a demonstrated archive or restore under the tracking retention policy; no backup is inferred.

## Resume point (not started)

* The gate resume depends on accepted tooling reaching `main`: first #1209 (reviewed workflow pin fix), then #1208 (reported clean and natively tested at `57da478bee37140034959f472f84a7f8becb75a7`, not merged; this record does not verify its content or whether it addresses the Chromium skip). `57da478be` is not an ancestor of this branch and no sibling code is copied.
* Then: rebase or re-evaluate against the final candidate and current `origin/main`, run fresh selected-tier validation, admit with a nonqueued actual heavy-lock holder, use only a task-owned SQL container, no cloud fallback, no change to skip policy, and verify the receipt externally.

## Planning readiness

Ready for a documentation-only correction. No source evidence for application changes; criteria C1, C5 and the rest of C6 stay unmet.
