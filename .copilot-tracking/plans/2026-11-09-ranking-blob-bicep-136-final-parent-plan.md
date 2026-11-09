# Plan: integrate frozen #1258 parent 9b1e2567 into #136 and validate (Refs #136, #1258)

Details: `.copilot-tracking/details/2026-11-09-ranking-blob-bicep-136-final-parent-details.md`. Research: `.copilot-tracking/research/2026-11-09-ranking-blob-bicep-136-final-parent-research.md`. Prospective: research, plan, details, critique and state are COMMITTED before the merge, any edit or any check.

## Scope

* Ordinary `git merge --no-ff 9b1e2567c2d0a2173b562103cd27508f75181526`; keep both the #136 Bicep and API wiring and the parent's Blob and main-8d behaviour. No rebase, reset, force or stash.
* No parent source fix (parent C5 budget zero; API wiring-test lint needs separate owner authorization). A conflict, if any, is resolved only to keep both intents; an unresolved intent conflict is reported, not forced.
* Owner demo-targeted tier: targeted checks only. No `rpi-checks`, full gate, SQL, browser, deployment, role grant, WORM/retention activation, model call or spend.
* Productive child review cycles stay 1 of 5; this task adds none.

## Phases

1. Commit these prospective records (author and committer `8036360+jmservera@users.noreply.github.com`, Copilot trailer).
2. Merge the parent. Record merge commit, tree, conflict state, and `git diff` classes (paths from parent versus from #136).
3. Capture identities, install and import paths in an owned external directory under the coordinator session files (`logs-136-final-parent/run-XXXXXX` via `mktemp -d`); nothing deleted.
4. Run the checks below, one log per command with command, cwd, stdout, stderr and `EXIT=`; `exits.tsv`; `SHA256SUMS` after the last check.
5. Commit changes and review records (hashes, outcomes, adverse items), run one Review, write the state, then the coordinator handoff `handoff-136-final-parent.md`.

## Checks (all in an owned venv with editable installs of this worktree; `PYTHONDONTWRITEBYTECODE=1`)

* `infra/`: `az bicep build --file main.bicep` and `lint`; `build-params` for `main.test`, `main`, `main.pilot.example`, `iot-hub-live`, each separately; plus CI-form loop over `infra/*.bicep` and `infra/modules/*.bicep` build and lint.
* `infra/`: unit tests for policy, identity, secret lifecycle, API ingress transport and governance with `REQUIRE_AZ_BICEP=1` (expect 100 before the merge; the post-merge count is recorded as measured).
* `src/core`: `PYTHONPATH=tests python -m unittest test_ranking_archive_blob test_ranking_publication test_ranking_publication_runner test_documents` (parent baseline 137), after printing the imported `zava_forward.core` path. Opt-in SQL and Azure tests stay skipped; counts of skips recorded.
* `src/api`: `PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest test_ranking_publication_wiring test_case_journey` (parent baseline 66 plus the #136 wiring tests), discover form, with import paths printed.
* Priority-order and resident-decision core modules, because the merge overlaps `store.py`: `PYTHONPATH=tests python -m unittest test_priority_order test_resident_decisions` (parent baseline 398 OK, 158 skipped), nonselected skips disclosed.
* Ruff 0.17.1 isolated (`pip install 'ruff==0.17.1'` into the owned venv): `--isolated --select E,F,I,B,UP --target-version py312 --line-length 100` check and `format --check` on the three-file infra CI form and on the changed infra test file. Also the same isolated form on `src/api/tests/test_ranking_publication_wiring.py`, expected to fail as inherited from the parent: recorded as adverse, not fixed. Plain default-88 and host-ruff runs, if any, are labelled nonselected baselines.
* Source qualification: `git diff` of every non-`.copilot-tracking` path against the parent for parent-owned files and against `95fcaf561` for #136-owned files; report paths changed by the merge.

## Stop rules

A failing selected check is not waivable and is reported with its actual output; the freeze is then marked not clean-passing. No source edit, no invalid-path result counted as a pass, no deletion of logs, no claim that lost captures survive.
