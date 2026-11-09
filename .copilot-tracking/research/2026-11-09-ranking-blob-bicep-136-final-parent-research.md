# Research: integrate the frozen #1258 SQL-main parent into #136 (2026-11-09)

Refs #136, Refs #1258. Slug `ranking-blob-bicep-136-final-parent`. Research disposition: executed; Planning Readiness: Ready. Native record only; independent coordinator review remains required.

## Subject and target

* Branch `feat/ranking-blob-bicep-136-1109`, HEAD `3783ea0fc5cd34dd62a0477283a99a15fae818cd`, tree `d2c0034cb6d3fd681e41c051be3889624b756602`, clean tracked tree (ignored `*.egg-info` from earlier editable installs only). Reviewed source `95fcaf561a9f046671d2cdf1bac8a6619f703610`; original source Review: 0 findings (`.copilot-tracking/reviews/2026-11-09-ranking-blob-bicep-136-review.md`, unchanged).
* Frozen parent `9b1e2567c2d0a2173b562103cd27508f75181526` (tree `b88cc90f4a4dd48a51b15e526b734e975fa036c5`), local tip of `fix/ranking-archive-ancestor-durability`. It is the #1258 SQL-main integration: `origin/main` `8d6f029cac004506953f36606862168bbe9d9412` (PR 1308) merged into the c5 source `52f9b61bb22c5ceaaed0f9bf6a55dab7a7a59cb8`, which this branch already contains.
* Merge base of HEAD and the parent: `52f9b61bb`; the parent is 11 commits ahead of it. `git merge-tree --write-tree HEAD 9b1e2567c2` reports a clean result (tree `061cb2575f189a13a532a86d824265bbe2471f3a`), no conflict, before any edit.
* Fetched `origin/main` today is `ef28d4da42d83b111d48f14df9b70e3c4932a477`, newer than the `8d6f029c` the parent carries. The brief fixes the scope to the parent; main is NOT merged here. The difference is disclosed as an unmet integration item.

## Parent handoff facts (read: coordinator `handoff-1258-sql-main-integration.md`)

* Blob archive selection and uncertain-write handling kept alongside main's `_order_unresolved`/`ORDER_NOTE` and `CommittedReloadError` 409 routes. Parent critique one (Revise, 3 findings applied), Review one (conformant, Minor). Parent correction cycles: five of five spent, zero used.
* ADVERSE retained: `src/api/tests/test_ranking_publication_wiring.py` fails `ruff` (10 errors: 9 E501, 1 I001) in the parent, byte-identical to `52f9b61b`; not fixed there because no cycle or authority exists. `git diff --check` exit 2 comes from main's own committed log file. Neither is a #136 defect, and neither may be fixed here: parent source fix is out of scope.
* Not run in the parent: SQL Server, browser, `rpi-checks`, any model call.

## Prior evidence to preserve

* Original source review (0 findings), C5 integration review, validation-capture review (Approve, four Low notes) and state files: unmodified.
* Coordinator `136-independent-verification-proof.txt` (SOURCE_EQUIVALENCE_MATCH, ALL_READONLY_VERIFICATION_PASSED for frozen `3783ea0fc`): unmodified and not rewritten.
* Retained external logs `logs-136-validation-capture/run-rhvN6X/` (`SHA256SUMS` sha256 `9fe10ef4...7446d5`): not touched.
* Open adverse items stay open: log 40 harness error (first API form exit 1, no test executed), plain `ruff check` RUF100 on `# noqa: S307`, plain `ruff format --check` exit 1 with the earlier "exit 0" claim unreproduced, and the lost raw integration-lane logs (not reconstructed).
* The task mentions original V1-V3 blocked metadata. No record under `.copilot-tracking/` for #136 uses such labels, so none is renamed or reinterpreted; every existing record is left byte-identical, which preserves whatever metadata it holds.

## Risks and checks implied

* Overlap files: both lineages touch `src/core/.../store.py`, `src/api/.../server.py`, core and API READMEs and tests. The merge is clean, so the proof is a post-merge test of provider, runner, API contracts and infra controls, not an assumption.
* Correction budget: productive cycles for this child are 1 of 5 (four remain, no reset). This task is a merge and validation, not a correction, so it adds none unless a selected check fails and a scoped correction is later authorized.
* The pin `ruff==0.17.1` with `--isolated --select E,F,I,B,UP --target-version py312 --line-length 100` is the authoritative form (`.github/workflows/src-ci.yml`); host or default line length 88 is not used.
* Ambient `python3` resolves to the primary checkout and is invalid; an owned venv with editable installs of this worktree is required, with imported paths printed before any unit run.

## Not in scope

Full gate, `rpi-checks`, deployment, SQL Server, browser, role grant, WORM or retention activation, spend, model calls, parent source fix, main merge, push, PR, board.
