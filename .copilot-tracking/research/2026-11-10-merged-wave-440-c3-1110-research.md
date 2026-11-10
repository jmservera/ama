<!-- markdownlint-disable-file -->
# Merged-wave 440 correction C3 research (2026-11-10)

Task `440-merged-wave-c3-1110`, parent `440-merged-wave-1110`. Authorization: #440 correction C3 of five (C2 spent earlier, two remain after C3, no reset). Research disposition: executed. The seven original records of the parent task are immutable; this record and its siblings are new and append only. Prospective: written at 2026-11-10T02:20Z (tool `date -u`) before any merge, document edit or run.

## Evidence read

* Independent review findings (read from the session files `independent-440-merged-wave-1110/readiness-findings.json`): INCOMPLETE, not a Pass, two confirmed Medium documentation findings.
  * F-A: evidence pack and original changes record say 694 distinct tests and 562 distinct passes. R4b and R9c re-execute the same four orchestrator version and dependency-rule cases (R4b.log lines 1-2 and 111-112; R9c.log lines 1-4), beyond the five browser R5/R6 re-executions. The execution totals 699 RUN, 562 PASS, 137 SKIP stay. The distinct claim is to be omitted, with the nine known repeats disclosed. No project-qualified deduplication of every log was done, so no aggregate unique count is asserted.
  * F-B: log and index say all 132 resident skips are SQL opt-in. R3.log shows 129 SQL Server opt-in, 1 Azure SQL opt-in, 1 SQL replay-only exclusion on the JSON class and 1 JSON rollback-only exclusion on the SQLite-backed class. The 137 skipped executions include 5 browser skips later executed in R6. SQLite ran; no external SQL Server or Azure SQL service ran.
* Original observation log set `/tmp/i440-1110-PIVEGs/logs` with manifest `SHA256SUMS` digest `bf60e679516048770d27feac96f02d3f7deb8424b7b72c15cdfe7acdb4ebe599`, re-verified at start of C3 (all entries OK). Must remain byte-identical.
* Main fetched at 2026-11-10T02:20Z: `origin/main` `bcc99405cd243f41ac8295e7fe41de57a070f954`, which is PR 1351 (#152 empty-queue explanation) plus the earlier rubric bot commit `6f24e554a`. The original wave observation ended 02:12:36Z, so 1351 was rightly excluded then; the 699 executions are not retconned to it.
* `git diff da4f52abb origin/main` is 35 paths: 21 `.copilot-tracking` records of issue 152, `src/api/README.md` (+12), `src/api/checks/workbench_browser_check.py` (+20), `src/api/src/zava_forward/api/web/app.js` (+10/-), new `src/api/tests/test_queue_empty_state.py` (142), recipe digest in `docs/reference/research/retrofit-synthetic-data/scenario-manifest.json`, `docs/reference/log.md` (+4, the 152 recipe correction entry) and the rubric score file. `git merge-tree` of HEAD with `origin/main` writes a clean tree, so no conflict.
* Existing commands (source guides): Core `PYTHONPATH=tests python3 -m unittest test_scenario_manifest test_needs_inventory -q` (src/core/README.md); `python -m checks.workbench_browser_check` from `src/api` (src/api/README.md, starts its own loopback API with constructed data); `tests/test_queue_empty_state.py` has seven cases and runs the real `queueEmptyExplanation` helper from app.js in Node (v24.21.0 present).
* Old venv `/tmp/i440-1110-PIVEGs/venv` holds editable installs bound to this worktree path; to be proven by import origin after the merge before reuse.

## Findings and limits

* No runtime coverage producer was added by 152: an empty own queue says coverage Unknown, a deferred trusted producer is not part of the change. PRD AC-034 and AC-043 remain PARTIAL. Unknown stays Unknown and is not zero programme work.
* Still excluded: parent #89 aftercare, blocked #132/133 hooks, old a482/R15 worker. Real queue-worker serve stays fail-closed.
* Not proven and not claimed: actual model, release, budget, trusted resident binding, DPIA, live four-image rebuild, real AT, representative-user or WCAG audit, named professional approval, SQL Server, Azure SQL, hosted CI for the merge head.

## Planning Readiness

Ready.
