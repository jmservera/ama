# Issue 1837 plan (run b), 2026-11-27

Refs #1837. Tier: focused (test-only; no src change, so no full gate).

## Critique (one pass, executed)

Verdict: proceed. Findings, applied directly: (1) record the live-load flakes honestly (workbench keyboard test timed out once at load 10-20, passed alone and on rerun; `nomination_browser_check` timed out on the same page, outside the 1837 standalone-form scope); (2) the inherited failure-path test read the feedback text immediately after the response event, which races the script handler and failed once under load, so wait for the feedback text first. Live Azure writes stay withheld (irreversible shared-demo records).

## Steps

* Fix the race in `test_route_form_failures_show_feedback_keep_form_usable_and_write_nothing` with a `wait_for_function` on non-empty feedback.
* Re-run the file's tests (record fresh output), the standalone-form and challenge axe checks, mypy and ruff.
* Write a research note under `docs/reference/research/` and the per-criterion table in the changes record.
