# Plan: integrate frozen #1258 C5 parent and correct changed-file formatting (Refs #136, #1258)

Details: `.copilot-tracking/details/2026-11-09-ranking-blob-bicep-136-c5-integration-details.md`. Research: `.copilot-tracking/research/2026-11-09-ranking-blob-bicep-136-c5-integration-research.md`.

## Scope

* Normal local `git merge --no-ff` of the exact commit `52f9b61bb22c5ceaaed0f9bf6a55dab7a7a59cb8` into `feat/ranking-blob-bicep-136-1109`. No rebase, reset, force, cherry-pick, main merge, sibling import or moving-parent propagation.
* Format only the lines this child added to `infra/tests/test_bicep_policy.py` with the CI command; no sweep, no suppression.
* Rerun the modified and impacted checks on the integrated source (DEMO tier). No blanket gate, SQL, browser, scanner or deployment.

## Phases

1. Pre-merge: verify tracked files clean (only this task's untracked records and the critique-driven wording edits below are present, and neither is touched by the parent delta) and the pinned SHA and tree; record baseline checks (format FAIL retained).
2. Merge locally; verify tree equals the predicted clean merge tree and both README intents survive.
3. Critique PC-1 wording correction: `infra/README.md` and the `containerapps.bicep` `rankingArchiveContainer` description no longer say flag-off makes the API refuse publication; the store then selects the local folder adapter (`store.py` `_ranking_archive`), and only the runner `--blob` CLI refuses. Then the format fix as a separate commit; confirm `git diff` shows no existing-line change.
4. Checks on the integrated head (below), preserving each exit code.
5. Records (changes, state), one critique before implementation, one Review after; commit; freeze.

## Checks

From `infra/`: `az bicep build --file main.bicep`; `az bicep lint --file main.bicep`; `az bicep build-params` for `main.test.bicepparam` and the other existing parameter files; `python3 -m unittest tests.test_bicep_policy tests.test_identity_rbac tests.test_secret_lifecycle`; the `main.test` build. Also `tests.test_api_ingress_transport` and `tests.test_governance` (they read changed Bicep or parameter files). From `src/api`: `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest tests.test_ranking_publication_wiring -q`. From `src/core`: `test_ranking_publication_runner.py` and `PYTHONPATH=src python3 -m unittest discover -s tests -p test_ranking_archive_blob.py` on the new C5 adapter. From the root: CI `ruff check` and `ruff format --check` on `infra/tests/test_bicep_policy.py`. A failing selected check is not waivable.

## Stop rules

Merge conflict that needs an intent decision, a tree different from the prediction, or a failing check: stop and report. Not an authorization for publication, PR, issue or board changes.
