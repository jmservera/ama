<!-- markdownlint-disable-file -->

# Phase Details: issue-152-mobile-empty-c4-1110

Plan: .copilot-tracking/plans/2026-11-10/issue-152-mobile-empty-c4-1110-plan.md

<!-- P01 -->
## P01: Extend, bind, validate

* P01-T01 In `workbench_browser_check.py` add `own_queue_empty_failures(page, expect_empty) -> list[str]` and call it in place of the 1280-only block. Loop `(320, 390, 1280)`: `page.set_viewport_size`, then for empty roles `li.empty` `wait_for(state="visible")`; collect failures from locator count, `inner_text`, `bounding_box` (inside `innerWidth`, width and height positive) and `evaluate` of `el.scrollWidth <= el.clientWidth` plus document `scrollWidth <= innerWidth`. Nonempty: assert `count() == 0`. Negative: on the first empty-queue role, add a style tag hiding `li.empty` at 320, assert the helper returns a failure, remove the tag by handle, restore 1280. No sleeps.
* P01-T02 Recompute SHA-256 of the harness and replace only the `recipe` value in `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json`. Add one sentence to the existing README empty-state paragraph naming the 320/390/1280 observation and its limits. Append a log entry following the 2026-11-10 precedent if repository rules require; no index change.
* P01-T03 Create `/tmp/ama-c4-venv`, install `-e src/core -e src/agents -e "src/api[dev]"` from this worktree; verify versions and import origins; run served harness, Core `test_scenario_manifest test_needs_inventory test_generator_coverage`, `tests.test_queue_empty_state tests.test_workbench tests.test_workbench_live_defaults`, ruff check, ruff format --check, mypy in src/api.
* P01-T04 Single review with refreshed web guidelines, commit with local noreply identity and Copilot trailer, witness events, handoff.
