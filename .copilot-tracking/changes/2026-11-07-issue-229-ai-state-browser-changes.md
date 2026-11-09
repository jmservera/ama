# Changes: issue #229 AI state browser check

Plan: [plan](../plans/2026-11-07-issue-229-ai-state-browser-plan.md). Tier FOCUSED, test-only. Date 2026-11-07.

## Files

* `src/api/checks/data_operator_ai_state.py` (new, Playwright-free): synthetic ai_task records, staff override, expected phrases, constructed empty contract.
* `src/api/checks/data_operator_browser_check.py`: fixture adds the records; new register section (entry not auto-opened, keyboard open, Quarantined vs fallback rows, workflow-only absent, Unknown banner, owner not an appointment, placeholder recovery, no audit-trail claim, no controls, Tab reach, reflow) and intercepted unavailable and empty scenarios; browser-observed no-write and no-model-request assertions.
* `src/api/tests/test_data_operator_ai_state.py` (new): real `ExceptionRegisterMixin` contract rendered by the real `role-screens.js` in Node.
* `src/api/README.md`: one paragraph on the new coverage and its limits.

No UI, API, schema, auth, SQL, deployment, model, provider, policy or recovery change.

## Amendment after Review

Review finding (medium): the no-model-request assertion could count the landing view's own `/api/ai/priority` read. Applied directly: wait for networkidle and count requests only from the register interaction onward. No second Review (one-pass rule).

## Validation (own pip venv at /tmp/zf229-scratch/venv, src/core, agents, api installed with pip -e, PYTHONDONTWRITEBYTECODE=1, external caches)

* Focused unittest discovery with PYTHONPATH=../core/tests:../agents/tests: test_data_operator* (12), test_exception_register* (34), test_capacity_browser_check (5), test_browser_harness_scratch (4), test_browser_asset_urls (6): all exit 0.
* `ruff check .` exit 0; `ruff format --check .` exit 0 (checks/ is excluded from format by repo config); `mypy` exit 0 (193 files).
* Server-only smoke through `main()` with an urllib probe (no Chromium): real server returned state ok, banner unknown, Quarantined and fallback failed_ai_run items, no workflow-only item, empty unrouted.

## Not run (pending, not passed)

* The actual synthetic operator-browser run (`python -m checks.data_operator_browser_check`, real Chromium and pinned axe): needs the coordinator's explicit admission to the shared heavy/browser resource. Playwright selectors were verified only by reading against role-screens.js. The new browser section is therefore unexecuted evidence.
* `rpi-checks.py --changed`, independent exact-head assessment, hosted CI, parent gates, AT and human acceptance.
