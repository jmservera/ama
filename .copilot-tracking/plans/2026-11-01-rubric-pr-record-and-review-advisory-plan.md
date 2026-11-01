---
title: Rubric PR recording and Copilot review advisory plan
description: Plan for owner decisions D1 and D2 covering the rubric score recording path, baseline freshness and the Copilot Code Review trigger
ms.date: 2026-11-01
ms.topic: reference
---

## Task

Task `rubric-d1-d2-2026-11-01` on branch `ci/rubric-and-review-triggers`, target `main`. Research: [research](../research/2026-11-01-rubric-pr-record-and-review-advisory-research.md). Details: [details](../details/2026-11-01-rubric-pr-record-and-review-advisory-details.md).

## Tier

Full. The diff changes the governance workflow, its Python tooling, tests and documentation, so it is not workflow-only. Run `python3 tools/rpi-checks.py --all` at the committed final candidate, plus `actionlint`, YAML parse, `gh aw compile` and the rubric pytest suite.

## Phases

* [x] Phase 1: Research (executed, Ready).
* [x] Phase 2: Remove branch recording from the workflow source and regenerate the lock file.
  * Remove step "Record score on the pull request branch" and the pre-push hook.
  * Simplify "Publish verdict": no `NEW_SHA`, `PUSH_FAILED`, `RECORD_OUTCOME`, self-commit visibility wait. One `rubric/score` status on the scored SHA, one sticky comment, one review on the scored SHA. Keep the check name `rubric/score`.
  * Rename the head recheck step to "Recheck pull request before publishing".
  * Add step "Refresh baseline on main" for `push` to `main` and non-forced `workflow_dispatch` on `main`: valid and passing decision only, commit `latest.json` and `badge.svg` on a bot branch `rubric/baseline-refresh` whose parent is the scored SHA, force-with-lease push, create or update one pull request, then attempt a squash merge and warn if the ruleset blocks it.
  * Recompile with `gh aw compile` (v0.89.21) and commit both files.
* [x] Phase 3: Baseline trust and freshness in the tooling.
  * `prepare.diff_args`: for non-PR events use the baseline's recorded `commit` when it is an ancestor of `HEAD`, else the previous rule.
  * `prepare.compute_state`: add `baseline_freshness` (commit, pending scored paths on the base ref since that commit, known flag) and `recorded_scores_changed` for PRs.
  * `gate.render_report`: freshness line and a warning when a PR edits the recorded score files. No new CLI flags.
* [x] Phase 4: Tests.
  * Rewrite `test_record_workflow.py` for the new publish step, absence of branch recording, the refresh step against a local bare remote with a fake `gh`, and source and lock equality.
  * Add `test_prepare.py` and `test_gate.py` cases for diff base, freshness and the scores-edit warning.
  * Add a regression test that no workflow places a Copilot review run in a cancelling concurrency group.
* [x] Phase 5: Documentation.
  * Update `.github/rubric/README.md` (flow, freshness, refresh PR, owner actions) and the bottleneck analysis (status of fixes 1 and 2, owner actions).
  * Add a Copilot review policy section (advisory, not required, trigger ruleset change as owner action).
  * Add a log entry in `docs/reference/log.md` and keep the index current.
* [x] Phase 6: Validate, commit, review.
  * `actionlint`, YAML parse, `gh aw compile` clean diff, pytest, full local gate with external receipt.
  * One critique before implementation and one Review after.

## Decisions and constraints

* No repository settings, ruleset or branch protection change. Owner actions are reported in the PR and the README.
* Existing check names are kept: `rubric/score`, Capstone Rubric Scorer, Source projects CI.
* The `pull_request` ruleset rule blocks direct bot pushes to `main`; the refresh uses a pull request.
* PR uses `Refs` only; never push to `main`.
* Known trade-off: post-merge scoring re-runs the agent. Scorecard reuse is a follow-up.
