<!-- markdownlint-disable-file -->
# Research: Blob plus Quality merged-main qualification, issue 440 (2026-11-09)

Started 2026-11-09T22:52:08Z (fetch at 22:52:08Z). Continuation of the parent-topic checkpoint ([research](2026-11-09-blob-quality-2055-440-research.md); original O1 exit 1 preserved). Disposition: executed for the delta only. Document identities and traces from the original research are reused because the BRD, PRD and ADR blobs are unchanged between local HEAD and main.

## Identities

* origin/main `1b7a1719bee088ce2823bff45242e319bc928295`, tree `dd2bedcb8f4e73266e143be09bf72474c62db9fd`: squash merge of PR 1331 at 2026-11-09T22:47:40Z. Because it is a squash, parent-topic commit `348381549` and the local child `6c2173dc3` are NOT ancestors of main.
* PR 1331 final head `f995774ca2415f6ae8903b6f45683dd55432eff1`; its tree equals main's tree (empty `git diff f995774 origin/main`). Hosted checks read via gh: all listed SUCCESS (src-api, src-agents, mssql, src-core, src-orchestrator, src-importer, rubric). Durations, independent APPROVE, c160 319 tests with 1 skip are coordinator-reported or historical, not re-read here.
* Source delta from the parent-topic `348381549` to main (src): 5 files, +117/-10: the browser check (E9), one line in `assistants.js`, three API tests (E10/E11). E9 made the check expect the guarded-off refusal and reach later steps through the seed path. No Blob, ranking or infra delta.

## Findings for planning

* Corrected successor is the same command `checks.quality_sensors_browser_check` with `--axe` (bytes verified inside the check against the pinned 4.10.3 hash 880970c0...a68bb; existing copy `/tmp/axe-4.10.3.min.js` matches) and `--out`.
* Heavy lock `/tmp/ama-rpi-heavy.lock` was free at a nonblocking probe, 22:52Z.
* Original O1 raw bytes, hashes and versions remain in the session files and the preserved scratch dir.
* Historical suites are reusable only where executable inputs are identical: main tree equals the f995774 tree, so hosted results at that exact head cover Core, API, Agents and SQL. No local broad rerun.
* Open owners: #1288 (closure, residuals), #1258/#1259/#136 (Blob live), #1292 (priority). No new defect known before observation.
* BRD 0.21.0 draft, PRD 0.21.0 in review, ADRs 0001-0007: statuses not promoted. PRD FR-008 controlled gates; FR-016 provider package; FR-017 quality disposition. Each trace names its document.
* Planning readiness: Ready.
