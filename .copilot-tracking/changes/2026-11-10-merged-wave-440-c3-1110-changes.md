<!-- markdownlint-disable-file -->
# Merged-wave 440 correction C3 changes (2026-11-10)

Task `440-merged-wave-c3-1110`. Plan: `.copilot-tracking/plans/2026-11-10-merged-wave-440-c3-1110-plan.md`. Records written prospectively at 2026-11-10T02:20Z and committed before the merge.

## Errata to the immutable original records (append-only)

* `.copilot-tracking/changes/2026-11-10-merged-wave-440-1110-changes.md` line 27 and the evidence pack: "694 distinct tests, 562 distinct passes" is withdrawn. The execution totals 699 RUN, 562 PASS, 137 SKIP stand. At least nine executions are repeats: five browser tests (R5 skipped, R6 executed) and four orchestrator version and dependency-rule cases run in both R4b and R9c. No unique total is asserted because no complete project-qualified deduplication was done.
* The original review record's conformance statement that rests on the 694 figure is likewise qualified by this erratum; its outcome (conformant with qualifications RV1-RV3) is not rewritten, and the independent review remains INCOMPLETE.
* Original state `skip (132 distinct, SQL opt-in/by-design)` and the log/index wording: the 137 skips are 5 browser skips, 129 SQL Server opt-in, 1 Azure SQL opt-in, 1 SQL-replay-only exclusion (JSON class) and 1 JSON-rollback-only exclusion (SQLite-backed class). No external SQL Server or Azure SQL service ran.
* The adverse R4 usage error and the R7 handled law-store tracebacks stay as originally recorded.

## Edits made (apply by edit tool, no shell redirection)

| File | Change |
| --- | --- |
| `docs/architecture/cutover-evidence-pack.md` | Corrected the count and skip sentence in the observation notes (withdrawal marked in place); appended the C3 addendum section |
| `docs/reference/README.md` | Corrected the one index line, added a pointer to the C3 addendum |
| `docs/reference/log.md` | Appended an erratum and observation entry; the original entry and the 152 recipe entry are intact |
| C3 RPI records | research, plan, details, critique, state, this record, review |

## Merge

Fetched `origin/main` `bcc99405c` at 2026-11-10T02:20Z; ordinary `git merge --no-ff` at 02:21:02Z gave `da842ed19` (parents `807c5ea67`, `bcc99405c`), tree `7d287ebd`, clean, no conflict. After the merge the diff to `origin/main` lists only the 440 own files. `origin/main` later moved to `2bfd5e075` (rubric bot only, `.github/rubric/scores/latest.json`) at 02:21:48Z; not merged.

## Observation (new scratch `/tmp/i440-c3-1110-obs`, `SHA256SUMS` `63e6cb507dce0c19f7e1a927397aa981c0693b7cbdb6b73151e19218e9d2a1e9`)

| Run | Start to end UTC | Exit | Result |
| --- | --- | --- | --- |
| C1 `test_queue_empty_state` (api) | 02:21:12 to 02:21:12 | 0 | 7 RUN, 7 PASS |
| C2 `test_scenario_manifest test_needs_inventory` (core) | 02:21:12 to 02:21:13 | 0 | 19 RUN, 19 PASS |
| C3 `checks.workbench_browser_check` with `ZF_BROWSER_TESTS=1` | 02:21:13 to 02:21:25 | 0 | 108 PASS, 0 FAIL, seven role empty-explanation checks pass, no-match check passes, reflow 320/390/1280 pass |
| C4 recipe digest | 02:21 | n/a | `56409ec2...ac7df9` equals the manifest |

Module origins of core, agents, api, orchestrator and importer proven under this worktree `src/` tree; the old venv was reused only after that proof. Old logs manifest `bf60e679...e599` re-verified, all OK, before and after. Nothing failed; no new defect; no code edited. Ledger: C3 of five used, two remain, no reset.
