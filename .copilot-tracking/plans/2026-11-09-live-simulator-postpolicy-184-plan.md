---
title: "#184 post-policy validation plan (prospective)"
ms.date: 2026-11-09
---

Task id 184-postpolicy, slug live-simulator-postpolicy-184. Parent: 184-recovery. Research: [research](../research/2026-11-09-live-simulator-postpolicy-184-research.md). Details: [details](../details/2026-11-09-live-simulator-postpolicy-184-details.md). Critique: [critique](../plans/2026-11-09-live-simulator-postpolicy-184-critique.md).

## Objective

Reconcile the frozen local candidate with current origin/main (76db469b) preserving both intents, then validate the actual modified and impacted core, api, infra and runner surface under the owner-selected demo-targeted tier. No new source, Hub, template family or web surface. Correct only tightly coupled test or fixture failures, and only if a planned check fails.

## Phases

* [x] P1 Commit these prospective records (research, plan, details, critique) as their own local commit before any merge or check, so ordering is visible in Git history.
* [x] P2 Merge origin/main 76db469b locally with `git merge --no-ff`; no rebase, no force, no remote write. Expect no conflicts; on any conflict preserve both intents and record it. Verify ancestry (HEAD contains 14ce745 and 76db469) and that only docs/policy paths arrive.
* [x] P3 Re-verify environment: editable imports resolve to this worktree; record versions. Install pinned ruff 0.17.1 and mypy 2.4.0 into the venv only after the first run fails for absence.
* [x] P4 Non-heavy checks (run now, independent of the lock): core unit sensor*, device*, live*, resident_sensors; api unit live*, iot*, sensor*, test_sensor_sql_check, test_live_control, test_live_receiver_sql (offline skips reported separately); tools test_rpi_checks; ruff check and format check and mypy on modified and impacted Python files; az bicep build and lint of the two live job templates and the existing Hub templates; infra unit tests test_iothub_module, test_bicep_policy, test_container_contract.
* [x] P5 Heavy actual-SQL checks, owned disposable SQL only: `sensor_sql_check.py` default (expect exactly 70 tests, zero skips, six selectors) and `--selector analysis` (exactly 10, zero skips, accepted exit 0). Start only under a non-queued `flock -n` admission of /tmp/ama-rpi-heavy.lock; if busy, retry between other work at bounded intervals, never wait blindly, never stop the other lane's container. If never admitted, report blocked plainly; no CI or cloud fallback.
* [x] P6 Static assertions for guards (read, plus the tests above): receiver cap 100, 14 day expiry, admin cohort grant, rejected data-quality, replay, window and dedup; required tuple growth is exactly two names; no skip-blind escape in the analysis path; no secret in changed files; C5 Low gap status.
* [x] P7 Write changes, review, state and handoff; commit frozen local candidate; record HEAD, tree, main SHA, diff summary, path inventory.

## Checks selected before running (owner demo-targeted tier)

Rationale: the parent touches SQL, infra and the gate tool, which are higher-risk categories under the permanent policy; the owner's demo authorization replaces only the blanket local gate with modified and impacted module checks. No `rpi-checks --all` or `--changed`, no receipt, no deployment, no Azure sign-in, no real model or billable message. Exact commands are in the details file.

## Success criteria

* All planned checks exit 0 with counts matching the selectors, or the failure or blocker is reported plainly with its exact output.
* Default SQL 70 tests, zero skips; analysis 10 tests, zero skips; offline opt-in skips are labelled separately.
* Exact two-name tuple growth; zero new heavy gates; shared lock respected.
* Clean frozen local commit with the genuine records.

## Out of scope

Sibling 1288 or 1292 imports, rebasing, remote branch work, PR, push, issue or board writes, closing or ticking criteria, owner memory, global Docker pruning, private data, credentials, live Hub traffic.

## Amendment A1 (recorded after P4 results, before the edit)

* Finding from this pass: the runner's own contract (`ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100`, and `ruff format --isolated --line-length 100 --check`) fails on tools/test_rpi_checks.py at lines 668 and 740 (two E501 plus formatting). The same files on origin/main pass, and the diff shows the long lines are the earlier recovery edit (tuple-derived counts). The earlier handoff had stated lint was not run; it is a defect in that edit, not a pre-existing one.
* Correction scope: formatting only, `ruff format --isolated --line-length 100 tools/test_rpi_checks.py`; no logic, tuple or count change. A failing selected check is not waived.
* Cycle accounting: C1 to C5 spent the five scoped review-correction cycles. This is a format fix to the recovery pass's own edit, found by this validation, not an independent-review correction; it is disclosed for the coordinator and spends no authorization beyond the owner's tightly coupled test-fixture allowance. Rerun after the edit: ruff check and format under the gate contract, mypy --strict tools, tools unit tests (102), and later the full planned set at the final head.
* Separate finding F1 (not fixed here): test_iot_stream.PublisherTests.test_actual_send_rate_after_connect_and_preparation_across_devices failed once at 0.04998 < 0.05 (time.monotonic jitter under shared load) and passed on three isolated reruns. The test and src/api/src/zava_forward/api/iot_stream.py are unchanged by this parent (both from main). Recorded with its first failure, never waived; proposed as a separate flake fix draft for the coordinator.

## Amendment A2 (recorded after the project mypy run, before the edit)

* Finding from this pass: `python -m mypy` in src/core (the project command the runner and hosted CI use, strict) reports 3 errors, all in parent-added src/core/src/zava_forward/core/sensor_sql.py (calls to the untyped mssqlstore connection_string and _Conn). In src/api it reports 53 errors: 46 are the absent optional playwright stubs (prerequisite missing in this venv; not parent code), 2 are in main tests unchanged by the parent, and 5 are in parent-added src/api/tests/test_live_control.py (SensorIngestion not explicitly exported, unused ignores). Earlier passes never ran project typing.
* Correction scope: typing comments only, following the repository convention (`# type: ignore[no-untyped-call]` is already used in core); no behavior change. Edit sensor_sql.py and test_live_control.py comments only, then rerun mypy for both projects, ruff check and format, and the affected unit tests (core live/sensor, api test_live_control, test_live_receiver_sql). The remaining playwright-stub and main-test errors are reported as pre-existing or environment and are not edited.
* Cycle accounting: as A1 (C1 to C5 spent; recovery validation finding in the parent's own added lines, disclosed for the coordinator).
