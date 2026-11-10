<!-- markdownlint-disable-file -->
# Phase details: issue-1294-validation-policy-priority-e1

## P01 Merge main

* `git merge --no-commit origin/main` already staged cleanly at research time. Commit as `merge: origin/main into docs/demo-priority-validation-1294-1109`. Verify `git diff origin/main HEAD --stat` afterwards touches no tool file.

## P02 Edits

* src/README.md coverage section: add to Local-only list the retained sensor analysis suite (`test_sensor_analysis_mssql`, `ZF_SENSOR_MSSQL=1`, eight pinned tests, exact count, zero skips, run in the SQL group; hosted mssql job does not run it); add `--changed` rule: core paths containing `sensor` and three listed dependency paths select `mssql`. SQL example row: add that the SQL group includes the retained sensor suite, hosted CI does not run it. Keep dated verification note (2026-11-09).
* .github/rubric/README.md step 3: replace "complete local gate" with the selected-tier gate (the complete gate for a full-tier candidate).
* .github/copilot-instructions.md: "non-gate tooling".
* Verify tools/rpi-checks.py facts by grep before writing (SENSOR_MSSQL_*).

## P03 Static review

* Dispatch a fresh-context read-only reviewer with the full target list: copilot-instructions.md, coordinator agent (whole Local validation tiers, receipt, publication steps), src/README.md (local gate, coverage, receipt, CI), tracking-retention-policy.md, rubric README step 3, docs/reference/log.md tail, docs/reference/README.md index entries. Reviewer verifies claims against workflow, ci-affected, rpi-checks and reports file:line findings. Closure pass if Revise.

## P04 Behavior

* Dispatch independent proxy design/execution/grading with cases: documentation-only, small employee-chat, SQL (core store and sensor path), Bicep/security, mixed docs plus infra, mixed docs plus chat, workflow/tool classification, absent/skipped CI semantics, stale-base receipt. Label proxy simulation; no real test execution simulated as real.

## P05 Finish

* Checks on final head: `git diff --check`, ASCII scan of changed policy docs, markdown link check of changed docs, stale-wording grep, selector probe. Append log entry. Review file. Commit with identity and trailer. Freeze clean.

## Amendments from critique (2026-11-09)

* P02 also: coordinator step 8 focused-candidate sentence; rubric README steps 1 and 3 selected-tier; sensor rule only for non-inert paths (probe `src/core/src/zava_forward/core/sensor_notes.md`).
* P05 order: commit candidate plus evidence; run checks and the single Review on that exact SHA; repeat if any later edit.
