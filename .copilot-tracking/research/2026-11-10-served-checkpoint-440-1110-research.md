<!-- markdownlint-disable-file -->
# Served import-refusal checkpoint 440 research (2026-11-10)

Task `440-served-checkpoint-1110`. Research disposition: executed. Stub persisted at 2026-11-10T06:59Z (tool `date -u`) before the witness `research-open` boundary and before any observation run or document edit; the findings below are appended after that boundary and the file is a non-guarded, evolving artifact.

## Intent and boundaries (from the owner brief)

* NEW due bounded post-integration checkpoint after PR 1361 reached main. It is not a repair or reset of the previous Discovery checkpoint (#440 ledger C4 of five spent there, one correction remaining; no source fix and no new corrective budget is granted here).
* Pin: `origin/main` `1ee56da3a27ad39eb53eaede0b66dc4905f0d820`, tree `b56e2bc2165149f23a2ec31e31d4d648e04da4de`; branch `docs/demo-served-checkpoint-440-1110`.
* Focused documentation and evidence tier. No blanket full or `--changed` gate, no source edit, no push, PR, GitHub or board write.

## Findings (appended after research-open)

Read after `research-open` (witness seq 2, 06:58:45Z). Sources: owner brief, issue #440 admission artifact (criteria 1 to 6 ticked, 7 and 8 open), the `1361-final-merge-guard-1110.json` guard, the parent 73 handoffs, live `gh` reads and local `git` at the pin.

* Fresh `origin/main` at start (`git fetch`): `1ee56da3a27ad39eb53eaede0b66dc4905f0d820`, equal to HEAD; tree `b56e2bc2165149f23a2ec31e31d4d648e04da4de`. Subtrees: `src` `4d7dc17fad54`, `src/core` `973b78bacab3`, `src/api` `1dc8eb03b13f`, `src/importer` `c6e324d1c3a0`, `tools` `432a4e8f7d74`, `infra` and `.github/workflows` unchanged from the earlier checkpoint.
* Contribution chain: PR 1357 (`feat/demo-served-import-refusal-135-1110`) merged 2026-11-10T05:17:41Z into the declared parent branch `feat/demo-served-exceptions-73-1110` (merge `b0af68a3`), not into main. PR 1361 (that parent branch to main) merged 06:51:12Z as squash `1ee56da3a`. Main acceptance is therefore the 1361 merge; 1357 is contributing history only. Its hosted Importer run failed on mypy (`mssql_python` import-not-found, 2026-11-10T04:34Z log kept in the Root folder) and was corrected inside the 1361 history (`pyproject.toml` override).
* The squash tree `b56e2bc2` equals the tree of the 1361 PR head `1fab5d04`; `git diff` of `src`, `infra`, `tools` and `.github` between `af7b20a3` (independently reviewed product head) and the pin is empty. Byte-identical code is not fresh execution: the historical af7b, 27dab and 1fab observations keep their dates and sources and this checkpoint re-executes only what its own commands show.
* Hosted state: the guard shows 19 reported checks SUCCESS on the PR head `1fab5d04` (base 736561ba). For the merge commit `1ee56da3a` itself the commit-scoped runs read at 2026-11-10T07:0xZ show only a Dependabot graph run and a queued rubric scorer push run; no Source projects CI is claimed for the exact main commit.
* 1361 changed 13 source files against `736561ba`: Core `exception_register.py` (+67), `import_refusals.py` (+109, new), `sqlstore.py`, `store.py`; Importer `__main__.py`, `exceptions.py`, `pyproject.toml`, README; API `role-screens.js` (empty-state wording) and two test files; Core and Importer tests (249 and 173 lines).
* Open owners compared (live state 2026-11-10): #1360 OPEN Medium non-blocking, static, unreproduced, unfixed, location `src/importer/src/zava_forward/importer/__main__.py:160-161`; #144 container hosting, #185 IoT identity, #111 sensor analysis and #132 contractor pack are unrelated to the served exception path and are named only as exclusions (111, 132 unmerged; 185 independent). #73, #135, #440 OPEN. Lanes #230, #231 and #153 are independent and remain allowed.
* Documents at the pin: BRD 0.21.0 `draft` blob `34d88395de86`; PRD 0.21.0 `in-review` blob `c788b917bafa` with FR-066 and AC-120 (owned staff exception queue; AC-120 "Not run") and NFR-019 and AC-135 (denial and privacy); addendum `28c1924285ee`; original `0aec2d807011`; ADR-0006 source layout (no ADR changes the exception contract); evidence pack blob `abdecf2ee74f`. Draft and in-review are not approval.
* Environment: no zava distribution is installed from this worktree and the importer discovery run fails with an import error first (kept as `E0`), so one owned environment is created externally (`/tmp/i440-served-1110/venv`, editable installs of this worktree `core[dev]`, `agents`, `api[dev]`, `importer[dev]`). The shared checkout `/home/azureuser/source/ama` installs are not used. The heavy lock `/tmp/ama-rpi-heavy.lock` was probed free with a non-blocking `flock -n`, but no exact maintained served-browser harness for the register exists (the 73 browser story was an ad hoc Root script), so browser and MSSQL runs are not attempted and stay deferred.

## Planning Readiness

Ready. Observation selection: Core `test_import_refusals` and `test_dependency_rule`, full Importer discover, API `test_exception_register*` and `test_role_screens*`, `node --check` of `role-screens.js`, ruff and mypy on the Importer, plus one constructed served-story run (explicit owned `ZF_DATA`, SQLite store) through the real importer CLI and the API read path. Static check of #1360 location only; reproduction is not attempted because the owner states no repair or budget and the issue proposes its own reproduction.
