# Issue 444 focus, loading and error-announcement follow-up: changes

Date: 2026-10-26. Plan: ../../plans/2026-10-26/issue444-focus-followup-plan.md. Base `origin/main` acafc6ee04e3612cd62349ab9e4a0af3b24e8109. Native session 7f0c39c0-54e7-4fa8-8e0f-bffad1161d56.

## Source changes

* `src/api/src/zava_forward/api/resident_preview/web/index.html`: `#status` empty in markup (no loading text without JavaScript); `role="alert"` removed from `#error`; `#error-title` gains `aria-describedby="error-text"` (critique C1).
* `src/api/src/zava_forward/api/resident_preview/web/resident.js`: `load(fromRetry)` focuses `#main` before hiding the error (C2); `render(view, announce)` sets "Your progress has loaded." after a retry only; `fail()` unchanged (focus error heading).
* `src/api/src/zava_forward/api/resident_preview/web/resident.css`: removed `main:focus{outline:none}` so the global focus-visible ring applies to the skip-link target.
* `src/api/checks/resident_preview_browser_check.py`: revoked step now reloads then asserts the visible panel; new `check_retry_focus_and_announcements` (held-request real server flow at 320px) and `check_skip_target_and_no_script`. Total passes 36 to 58.
* `src/api/tests/test_resident_preview_api.py`: `test_page_focus_and_announcement_contract` over the real loopback HTTP server.

No server, grant, projection, fixture, schema, infrastructure or documentation change. No README change was needed.

## Failing before

Before the fix (unchanged web files): probe recorded `activeElement` BODY during retry loading and after recovery (research artifact). The new HTTP contract test failed on the static loading text, and the new browser check failed at "error container is not also an alert live region". After the fix the same tests pass.

## Validation (local, from src/api, venv `/mnt/ama-rpi-gates/issue444-focus-followup/venv`, pip-installed `src/core`, `src/agents`, `src/api`, Playwright 1.64.0 Chromium)

* `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p "test_resident*.py" -q`: 28 tests OK, 1 skipped (pre-existing).
* `python -m checks.resident_preview_browser_check`: 58 PASS, complete.
* `ruff check .` and `ruff format --check .`: clean. `mypy`: one pre-existing unrelated error (`checks/sensor_sql_check.py` optional `mssql_python` not installed because `--no-deps`).
* No full repository gate, Docker or image build, per instruction.

## Deviations and not done

* Loading text keeps "..." and the button label "Try again" keeps repository plain-language casing; the fetched guideline prefers "…" and Title Case. Routed Low follow-up.
* theme-color, color-scheme, translate=no, touch-action, text-wrap, raw-JSON footer remain routed Low follow-ups.
* Announcements are asserted through DOM roles, live-region text and focus in Chromium only; no screen-reader speech test. No comprehensive accessibility, screen-reader or resident acceptance claim. Issue #444 criteria are not ticked and the issue is not closed.

## Integration with main fcf7e127 (2026-10-26)

Normal merge of origin/main fcf7e12735c9e4e69f83df9d643ec8e28a981409 into the branch: no conflicts, no log.md or rubric-bot file edit by this branch, no source change from integration. Prospective note: `.copilot-tracking/plans/2026-10-26/issue444-focus-followup-main-fcf7e127-integration-plan.md`. Cheap recheck: `tests.test_resident_preview_api` OK (merged tree). Browser and full suites not rerun (no new concern); the complete gate awaits coordinator admission.
