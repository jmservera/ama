# Plan: integrate parent candidate 99814198 into the #136 child (Refs #136, #1258)

Details: `.copilot-tracking/details/2026-11-09-ranking-blob-bicep-136-c6-integration-details.md`. Research: `.copilot-tracking/research/2026-11-09-ranking-blob-bicep-136-c6-integration-research.md`.

## Scope

* Commit this prospective research/plan/details/critique first, then a normal local `git merge --no-ff 99814198079c7c8fcd641497826986c706627b0f`. No rebase, reset, force, cherry-pick, main merge, sibling #1259 import or parent mutation. No publication, PR, issue or board write.
* No source edit unless a selected check fails because of the integration; any genuine own source fix needs its own prospective plan (C2) and is not authorized here.
* Targeted DEMO checks on the integrated head only for impacted inputs. Heavy unchanged checks are not rerun to refresh metadata.

## Phases

1. Preconditions: after the prospective-records commit P (child of `fba4273a4`), HEAD is clean and `git diff fba4273a4 P --name-only` is only the four C6 prospective records; recompute `git merge-tree --write-tree P 99814198` (the pre-records prediction `0714b2bc...` applies to `fba4273a4`, not P) and expect P's tree plus the parent delta.
2. Merge locally; tree must equal the recomputed prediction for P; first parent P, second `99814198`; the child infra files must be byte-identical to `fba4273a4` (`git diff fba4273a4 HEAD -- infra` empty).
3. Checks (below), exits preserved, raw hashes of the exact inputs recorded.
4. Changes record, one Review, state, freeze, handoff.

## Checks (DEMO tier)

* `infra/`: `az bicep build --file main.bicep` (stdout), `az bicep lint --file main.bicep`, `az bicep build-params` for the four existing parameter files, `python3 -m unittest tests.test_bicep_policy tests.test_identity_rbac tests.test_secret_lifecycle tests.test_api_ingress_transport tests.test_governance`.
* Isolated `/tmp` venv with editable installs of this worktree's core, agents and api: `src/core` Blob adapter and runner tests (`test_ranking_archive_blob.py`, `test_ranking_publication_runner.py`, count and exit), `src/api` `test_ranking_publication_wiring.py` (wiring/config/imports), and an import check of `zava_forward.core.ranking_archive_blob` constants against the Bicep env names (the policy test already parses them).
* `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` and `ruff format --isolated --line-length 100 --check` on `infra/tests/test_bicep_policy.py` (changed file; local ruff 0.17.3 vs CI pin 0.17.1 recorded).
* A failing selected check is not waivable; stop and report rather than editing silently.

## Stop rules

Conflict or tree differing from the prediction, parent pin change (record refresh need), or a failing check: stop and record. Not authority to publish or merge remotely.
