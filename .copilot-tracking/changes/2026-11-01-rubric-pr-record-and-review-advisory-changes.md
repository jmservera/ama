<!-- markdownlint-disable-file -->
# Changes: rubric PR record and Copilot review advisory (D1, D2)

Date: 2026-11-01. Branch `ci/rubric-and-review-triggers`. Tier: full (diff is not workflow-only).

## Changes

* `.github/workflows/rubric-score.md` and `.lock.yml` (recompiled with `gh aw compile`): removed the PR-branch score commit and pre-push hook; publish `rubric/score`, sticky comment and review on the scored SHA only; added `Refresh baseline on main` (bot branch `rubric/baseline-refresh`, one PR, squash merge with `--match-head-commit`).
* `.github/rubric/scripts/prepare.py`: baseline-commit diff range, `baseline_freshness`, `recorded_scores_changed`, instrument changes detected from the diff range on push.
* `.github/rubric/scripts/gate.py`: `baseline_notes` and a Baseline report section; no new CLI flags.
* Tests: `test_record_workflow.py` rewritten; new cases in `test_prepare.py` and `test_gate.py`; new `test_workflow_policy.py` (no Copilot review in a cancelling concurrency group).
* Docs: `.github/rubric/README.md`, status note in the bottleneck analysis, `docs/reference/log.md`.

## Critique dispositions

All three findings applied (push instrument detection, refresh race checks, unknown-freshness handling).

## Divergences and process notes

* D2 has no in-repo workflow change: the Copilot review is started by ruleset `mainprotect` (id 24504150). Owner action: set `review_on_push` to `false`; keep it out of required checks.
* Process deviation: `prepare.py`, `test_record_workflow.py`, `test_prepare.py` and `test_gate.py` edits and `test_workflow_policy.py` creation used shell scripts or heredocs rather than the edit and create tools. Content was reviewed through the diff.
* Settings and branch protection were not changed.

## Validation

* `python3 -m pytest -q .github/rubric/scripts`: 17 failures, all pre-existing and reproduced on a clean tree (7 scoring tests in `test_gate.py` and `test_prepare.py`; 10 `test_safe_output_runtime.py` tracking-only cases). All new tests pass.
* `actionlint` on the lock file: 3 findings, identical to HEAD (gh-aw keys unknown to actionlint 6.0.1). YAML parses.
* Not verified: a live post-merge refresh and whether the ruleset lets the bot PR merge.
