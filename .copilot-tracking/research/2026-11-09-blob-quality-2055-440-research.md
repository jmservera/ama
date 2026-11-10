<!-- markdownlint-disable-file -->
# Research: Quality parent topic plus merged Blob checkpoint, issue 440 (2026-11-09)

Task `blob-quality-2055-440`. Refs #440 #1288 #1258 #1259 #136 #1292. Research disposition: executed (new worktree, new sources). Planning Readiness: Ready.

## Identities (resolved by fetch and git, not assumed)

* Worktree `issue-440-blob-quality-2055`, branch `test/demo-blob-quality-checkpoint-440-1109`, clean at start, HEAD `3483815492f331b1254d46bee7be783584977ef2`, tree `3aebb1da13c452da48f49da1b8d063a3df1fbdd0`.
* Fetched `origin/main` `a04668ae94b5c2f38e6c55ed789db245e8c71d16` (contains Blob/Bicep #1328, checkpoint #1329, bot score metadata #1330). It is an ancestor of HEAD (`git merge-base --is-ancestor`), so HEAD already holds main; `HEAD..origin/main` is 0 commits.
* Declared parent `feat/demo-recovery-quality-1288-1109`, PR #1331 (OPEN, base `main`, MERGEABLE). Published head `581207e18fedd66d9e24704a663dbb5f7b870d50`; hosted at read time: `src-agents` FAILURE (E501, the line E8 wraps), `src-api` IN_PROGRESS, others SUCCESS. HEAD is 2 local commits ahead: `f44028c10` (E8 plan) and `348381549` (the E8 wrap). E8 is unpublished and under independent assessment. No hosted success is assumed for `348381549`.
* Quality is NOT merged-main functionality. Everything about Quality below is parent-topic, source-qualified to this HEAD.

## Documents (unchanged versus main; statuses not promoted)

BRD 0.21.0 draft `34d88395`; PRD (Zava Forward) 0.21.0 in-review `c788b917`; PRD (proper-warm) `f7f9b767`; addendum `28c19242`; original `0aec2d80`; ADRs 0001 `d42fa5c4`, 0002 `cbe21530`, 0003 `d6064539`, 0004 `9406c2e7`, 0005 `4d610335`, 0006 `956da1a3`, 0007 `abb21088`. Blob ids equal at HEAD and at `origin/main`. BRD and PRD FR numbers collide, so every requirement trace must name its document. The earlier erroneous PRD FR-016/017 resident or complaints join stays preserved as an error and is not reused; PRD FR-016/017 are provider-package and quality-disposition records.

## Architecture and overlap

* Quality delta versus main is 144 files (src: Core `ai*.py`, `assistants.py`, `sensor_consumer.py`, `sensor_view.py`, `simulation_lane.py`; API `server.py`, web `assistants.js`, `case-workspace.js`, `ops.js`; ten API tests). It touches no ranking, Blob, infra or Bicep file.
* Only shared file with main's Blob wave is `server.py`: main adds `ArchiveWriteUncertainError` handling in `/api/ranking/publish`; the parent adds the simulation lane, Quality and inventory routes. The recorded main integration preserved both intents with no conflict. Core `ranking*.py`, `store.py`, infra and ranking tests are byte-identical to main.
* `git diff 2aa038043 HEAD -- src infra tools .github '*.toml'` shows only `dispatch.py` (E8, 5 lines, AST-equal per the E8 record) and rubric score data. Hence the retained main-integration runs (tree of `2aa038043`) remain valid historical inputs for Core, API and infra; only Agents is affected by E8, and its 303-test run is E8-specific.

## Existing evidence and its limits

* Retained raw logs (session files `logs-1288-main-integration/`, `logs-1288-e8/`): summing the `Ran N tests` and `skipped=N` lines gives 761 discovered and 100 skipped across the Core, API and infra suites listed in the integration record (58 assistants SQL, 31 + 7 + 4 other skips). The "861 discovered" figure in the task brief is not reproducible from the retained logs (difference exactly 100); the checkpoint reports 761/100 and flags the discrepancy rather than copying 861. E8 Agents: 303 ran, OK (`unittest-after.log`).
* Those runs are historical source-qualified reuse at the pre-E8 tree, not fresh at HEAD, and are labelled so.
* Quality AI: real-provider simulation route code-disabled; ordinary-assistant post-fence suspension race, local-only socket shutdown and final SQL audit persistence remain unproven (parent records). SQL605/1skip is historical at `5827ebede`.

## Missing observation and selection

`checks/quality_sensors_browser_check.py` (Quality-parent file, absent on main) is the existing local journey of retained readings against the Quality model snapshot with a mock provider: it covers unavailable, stale, withheld, attributed-unapproved and denied states, role denials and a manual path, on a constructed SQLite fixture under an owned temporary root, loopback server only. No retained evidence shows it was run at an integrated (post-Blob) head: the integration record states no browser run. It is the one necessary missing public-synthetic observation. Prerequisites: Python 3.12, Playwright 1.64.1 and Chromium (user cache present), `openssl` for the loopback lane tests (not needed by the check), `--axe` is optional and the axe bytes were not located, so no axe run unless the file exists. No SQL Server, Azure, model or credential is involved. The check writes its fixture under `cwd/.q<random>` and removes it itself; it will be run from an owned directory.

Heavy admission: the shared lock `/tmp/ama-rpi-heavy.lock` was free at read time; browser check will use one nonqueued `flock -n`; busy means record BLOCKED and continue traceability.

## Gaps and owners (no defect asserted)

#1288 Quality (parent unmerged, whole acceptance open), #1258 and #1259 (ranking archive durability, remote atomicity, live Blob), #136 (infra, from-empty deployment), #1292 (priority-order recurrence, startup cause UNKNOWN), #184 and #189 (live simulator, live criteria), #81 (SQL legs). The one confirmed documentation-level discrepancy (761 vs 861) belongs to this checkpoint's own evidence statement, not a new issue.

## Ledger

Inherited: #440 original NeedsFixes5 and Q1 (one finite qualification, unreset) remain; #1288 E1-E8 spent (E9-E10 remain, not consumed here). This checkpoint is not a counter reset and consumes none.
