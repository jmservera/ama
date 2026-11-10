---
title: Issue 1388 delayed-companion route-delivery race research
ms.date: 2026-11-10
task_id: 1388-delayed-route-1110
---

<!-- markdownlint-disable-file -->

## Disposition and scope

Research executed 2026-11-10 from 13:26Z (witness launch recorded first), before any source edit. Disposition: `executed`. Planning Readiness: Ready.

Scope is `delayed_companion` in `src/api/checks/workspace_scripts_browser_check.py` and a focused direct regression test. Pinned main and HEAD: `83503b74e0e5f555382436c0ae27f64cd200971f` (equals fetched `origin/main`; the only change over `65c2ab9d9` is `.github/rubric/scores/latest.json`, so the checker is unchanged from the diagnosed main). Checker sha256 before any edit: `43d1f4b900e95b84c9ce704d8bb897f1dd01296631abc3bb694add34e849b79d`, equal to the diagnosed main 65c value. No production code, retry policy or other checker is in scope.

## Ownership and contract-gap check (stop rule)

* GitHub #1388 (read-only `gh issue view`): OPEN, label `bug`, no comments, created 2026-11-10T13:24:00Z. Its body and acceptance criteria are the authority. The creation record is `.copilot-tracking/github-issues/issue-1388.md`.
* #1384 owns the exhaustion-count oracle and the employee checker; this task does not touch them. #133 owns aftercare hooks. No dependency on held #132 or on the unpublished #1384 candidate.
* `git log -- src/api/checks/workspace_scripts_browser_check.py` shows the delayed routine last changed in `d20bc50c4` (#597); no prior repair of the pending-count race exists in source history.
* Intended request identity: the route is registered only for the `/role-screens.js` asset pattern. `intercept` aborts request 1 and appends every later request to `pending`, so `pending` can only receive the second (intended retry) or a later duplicate; the first attempt can never enter `pending`. Waiting for `pending` to become non-empty therefore cannot release a different request, and `len(pending) == 1` still rejects a duplicate. No contract gap, so the stop rule does not apply.

## Original reproduction (durable summary of the coordinator diagnosis, not a raw bundle)

* Mechanism: the `wait_for_function` predicate (exactly one `head script[src]` for the companion) is satisfied by DOM insertion of the retry script (line 241). Playwright delivers the route to the Python callback asynchronously, so `assert len(pending) == 1` (line 246) can run while `pending` is still empty. Captured gaps were about 2 to 6 ms (for example request 700 ms, context close 702 ms).
* Diagnosis samples (3 per variant, fresh browser, run once): main 65c iso 0/12, seq without controls 1/12 (plain); frozen candidate 3f1fa48 iso 0/12, seq without controls 2/12 (plain, session_ended), seq with controls 0/12. All three failures were the exact count assertion. No evidence of control leakage; samples are too small for a rate.
* Original evidence lives in the coordinator session (`handoff-1384-delayed-diagnostic-1314.md`, `checks-1384-delayed-diagnostic-1314/`). This task does not copy it.

## Actual four delayed variants (call sites in `run_browser`, lines 346-349)

| Call | Scenario printed | Distinguishing assertions retained |
| --- | --- | --- |
| `delayed_companion(browser, base)` | navigation | My cases navigation, perspective status, hash and status unchanged after late load, companion evaluated once, original view invoked once on legitimate revisit |
| `delayed_companion(browser, base, timed_out=True)` | timeout and late load | Workspace unavailable shown within 7000 ms, `expect_failure`, two requests, then the late load settlement assertions |
| `delayed_companion(browser, base, sign_out=True)` | sign-out | Sign out, `pending[0].abort()`, no Workspace unavailable heading |
| `delayed_companion(browser, base, session_ended=True)` | same-document 401/login | Constructed 401 rejects with the session-ended message, sign-in heading, `me === null`, route controller not aborted |

Command for all of them with the whole checker: `python3 -m checks.workspace_scripts_browser_check` from `src/api` (documented in `src/api/README.md`). The isolated command for the four variants is an inline driver that calls the real `delayed_companion` four times inside the existing `main(run, synthetic_data)` harness (recorded in the plan).

## Pump primitive (read from the source and Playwright sync API)

* The sync API dispatches route callbacks while Python is inside a Playwright call. `page.wait_for_timeout(ms)` is a browser-side timer that returns only after the dispatcher ran, so a short `wait_for_timeout` slice inside a loop pumps delivery. `time.sleep` would block the dispatcher thread and is prohibited.
* `wait_for_timeout` is already used in this file (line 153). No new helper, CLI or production consumer is needed.

## Selected approach

* In `delayed_companion`, after the existing DOM-ready `wait_for_function`, loop `page.wait_for_timeout(10)` while `pending` is empty and a monotonic clock is under a fixed 5.0 s deadline; then keep an exact `assert len(pending) == 1` with a message that names zero versus duplicate. The deadline is a guard, not a production wait; it is not extended and there is no retry-until-green.
* Direct regression: drive the real `delayed_companion` with minimal test-local doubles (browser, context, page) and patch only the module-level collaborators the routine calls before the count (`expect`, `sign_in`, `observe_companion`) plus the module clock. The doubles capture the routine's own `intercept` callback and deliver it only when the routine pumps `wait_for_timeout`, so DOM-ready (`wait_for_function` returns) strictly precedes delivery. A sentinel raised on the first post-count page interaction stops the real routine right after the count. Controls: prompt (delivered before DOM-ready, succeeds), zero (never delivered, bounded explicit failure), double (two delivered, fails), plus cleanup (`context.close` called in `finally`) and the first-request abort.
* A pure fixed sleep is not the only proof: the old routine fails deterministically because delivery is gated on a pump call it never makes.
* Rejected: relaxing to `>= 1`, taking the first request, `time.sleep`, longer `expect` timeouts, repeating until green, helper frameworks, loader or retry changes, touching exhaustion/parser/employee code.

## Environment and baseline evidence (original source, before edits)

* The system Python imports no WT-pointing project install and the existing venvs (`ama-venv-1384-workspace-oracles-1110`, `ama-venv-133-parent-workspace-1110`) import `zava_forward.*` from other worktrees, so they were not reused. Own venv `/home/azureuser/.cache/ama-venv-1388-delayed-route-1110` (pip, editable `src/core[sql,blob]`, `src/agents`, `src/api[dev]`): `zava_forward.{core,agents,api}` resolve to this worktree; playwright 1.64.0, ruff 0.17.1, mypy 2.4.0 (the configured pins), Python 3.12.3. Install log `/home/azureuser/.cache/ama-venv-1388-delayed-route-1110.install.log`. Nothing was installed globally.
* Before the venv, the existing selector `test_browser_asset_urls test_workspace_scripts` ran on system Python and passed (11 tests), using unpinned user-site tooling (ruff 0.17.3, mypy 2.4.1); that run is not used as pinned-tool evidence.
* Browser admission: one non-queued `flock -n /tmp/ama-rpi-heavy.lock` acquisition (lock file existed, acquired immediately, no HOLD). Raw outputs are in `checks-1388-initial-1110/` in the coordinator session.
* B1 whole checker on original source (2026-11-10T13:27:52Z start): exit 1. Passed leaflet 1 and 2 failures and `/role-screens.js` recovery, then failed in `exhaustion` at `assert len(requests) == count` (line 148, the old exhaustion oracle owned by #1384). It stopped before any delayed variant, so it gives no delayed coverage.
* B2 four delayed variants on original source, isolated, one run each: plain PASS, `timed_out` PASS, `sign_out` FAIL (`AssertionError` with an empty message, consistent with the unlabelled `assert len(pending) == 1`; the driver did not capture a traceback), `session_ended` PASS. This is a fresh original-source observation of the intermittent race (one of four) and is preserved as adverse evidence, not rerun to chase green.

## Risks

* Patching the module clock and Playwright collaborators in the regression ties it to the routine's call order up to the count; the sentinel approach keeps that dependency to the first post-count call.
* The real race is load dependent; the real-browser variants cannot prove absence, so the deterministic regression is the proof and real runs are corroboration with first and adverse results kept.
* `checks/*.py` is excluded from `ruff format` and has relaxed lint per `pyproject.toml`; the new test is strict-mypy and formatted.

## Follow-ups

* After this fix reaches main, #1384 takes mechanical adoption and must still pass its own BOTH browser checks (not waived here).
