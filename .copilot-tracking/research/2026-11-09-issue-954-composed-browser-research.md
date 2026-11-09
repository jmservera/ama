# Research: issue 954 composed-source browser validation (2026-11-09)

Task `issue-954-composed-browser`, parent `issue-954-c3-types`. Validation-only continuation. Local only: no push, PR, issue, board, live provider, credential, model or spend.

## Disposition

Research executed 2026-11-09 on clean head `271ea14404207ff9021febd5a23e2950e1df9be2` (tree `1cacd240c41aaa25dc4f89aa1705626c699f3b2e`, branch `test/demo-photo-validation-954-1109`). No validation of this task has run before this record. Planning Readiness: Ready.

## Correction budget

This is not a correction cycle. No source correction is authorized and none is made; the budget is unchanged: C1, C2 and C3 spent, two of five remain, no reset or extra grant.

## Evidence

* C3 left exactly one selected check unrun: the actual synthetic Chromium run of `src/api/checks/photo_flag_stale_browser_check.py`. The single nonqueued `flock -n /tmp/ama-rpi-heavy.lock` attempt exited 1 because the 1292 original-load diagnostic held the lock (session file `evidence-954-c3/holder-check.txt`, `unadmitted-note.txt`). That run is historical and unchanged.
* Per the coordinator, the controls 189 holder finished (17:09:28 to 17:10:02), so one actual holder check and one nonqueued admission are owed for this pending check.
* Checker git blob SHA-256 on this head is `620301300f3f3dc541e2d1bb577e5331a89e2e440c6a56466a62bd19f324a6db` (the typed checker, unchanged since the C3 fix `8af0fb82e`). It must be identical before and after the run.
* Earlier C2 quiet receipts (503 and 403) bound the pre-typing checker `3e89042d...a42a`; they remain historical and are not reused as a pass for this composed source.
* Environment: `python3` (3.12.3) with worktree-first `PYTHONPATH` (api, core, agents `src` and `tests`) resolves `test_auth`, `test_mvp`, `playwright.sync_api` and the worktree `zava_forward` modules (probed read-only). Chromium assets exist in `~/.cache/ms-playwright` (chromium-1248). The C3 owned venv `/tmp/zf-954-c3-venv-Ryof6Y` no longer exists, so it is not relied on; no restore was needed because no declared dependency is missing.

## Main and comparison base

* Fetched `origin/main` is `2b6d80a2580444751d4b85fc8eaa2c15f367855d`. The branch contains main `3a9767d5cf728c5e3be76813ce0bfdac4c06841e` (ancestor, merged in `2d9c14952`).
* Main moved after `3a9767d5c` by only the rubric score commit `700bf11e1` and the pure documentation commit `2b6d80a25` (PR 1317). `git diff --name-only 3a9767d5c origin/main` lists documentation, `.github/rubric/scores` and `.copilot-tracking` paths only; no file under `src/`, `infra/`, `tools/` or workflows. Runtime-source equivalence is therefore qualified as: base `3a9767d5c` and current main `2b6d80a25` have no runtime-source delta (documentation, rubric score and tracking only); the tested head `271ea1440` is `3a9767d5c` merged with the checker change, and nothing is claimed about a merge with `2b6d80a25` beyond the clean trial below.
* The actual comparison base for the hosted rubric and the earlier gate is `3a9767d5c`; the current target is `2b6d80a25`. This record does not claim the committed `.github/rubric` score equals the new main. A trial `git merge-tree --write-tree HEAD origin/main` is clean (tree `8bcdebb7252b683db8d327e7f4fd41abf3e5fa7e`); it is prospective, and no merge is made (no source delta, no unnecessary merge or rebase).

## Boundaries

No source, test, config, product, API or UI change. No new test source. No full gate, SQL, cloud, model, private or live credential, or global install. No evidence cleanup before coordinator verification.
