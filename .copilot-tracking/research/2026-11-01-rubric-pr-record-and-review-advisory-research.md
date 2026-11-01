---
title: Rubric PR recording and Copilot review advisory research
description: Evidence for owner decisions D1 and D2 from the delivery bottleneck analysis, covering the rubric score recording path and the Copilot Code Review trigger
ms.date: 2026-11-01
ms.topic: reference
---

## Task

* Task id `rubric-d1-d2-2026-11-01`, slug `rubric-pr-record-and-review-advisory`.
* Branch `ci/rubric-and-review-triggers`, worktree `workflow-d1-d2`, target `main`, base `245985722` (equal to `origin/main` at fetch).
* Research disposition: `executed`. Planning Readiness: `Ready`.
* Owner approval 2026-11-01 for D1 and D2 as in the task statement and in `docs/reference/research/delivery-bottleneck-analysis-2026-10-31.md` (fixes 1 and 2, decisions D1 and D2).
* Constraints: no repository settings or branch protection change (report as owner actions), keep existing check names, `Refs` only, never push to `main`.

## Evidence

### D1 current behaviour

* `.github/workflows/rubric-score.md` (compiled to `rubric-score.lock.yml` by gh-aw v0.89.21) runs `rubric_prepare`, the agent, then the safe-output job `record-rubric-score`.
* That job runs trusted `gate.py`, then, for `pull_request` events only, the step "Record score on the pull request branch" copies `latest.json` and `badge.svg` from `/tmp/rubric-out`, commits as `github-actions[bot]`, and pushes to the PR head ref through a pre-push hook. "Publish verdict" then waits up to five attempts for the new head (`selfRecorded`, `visibilityPending`), sets the `rubric/score` status on both the scored and the new SHA, upserts the sticky comment and submits an APPROVE or REQUEST_CHANGES review at the new head.
* On `push` to `main` nothing is recorded. The step only opens an issue when the score regressed or scoring failed.
* `prepare.py` `compute_state` reads the baseline from `git show <base_ref>:.github/rubric/scores/latest.json`. It uses `fingerprints` to decide which artifacts changed and which criteria are open, `rubric_version` and `source` for bootstrap, and carries the per-criterion baseline into `tool_inputs_template`. `gate.py` `evaluate` reads `total` and per-criterion scores. A check verdict or comment cannot replace this file.
* For non-PR events `prepare.diff_args` diffs from the last commit that wrote `latest.json`. `should_score` is true whenever the artifact fingerprints differ from the baseline, so a push to `main` whose scored artifacts are not yet in `latest.json` already triggers scoring. This is the existing path a post-merge refresh can use.
* `latest.json` already records `commit`, the scored source SHA, and `fingerprints`.

### Repository protection (read-only API, 2026-11-01)

* Ruleset `mainprotect` (id 24504150, active, default branch, no bypass actors): `deletion`, `non_fast_forward`, `pull_request` (0 required approvals), `required_status_checks` with an empty list (strict policy), and `copilot_code_review` with `review_on_push: true` and `review_draft_pull_requests: false`. A second ruleset `main` (id 24682333) is disabled. Classic branch protection returns 404.
* Consequences: a direct push by `github-actions[bot]` to `main` is blocked by the `pull_request` rule, so a post-merge refresh must go through a pull request. No check is required, so `rubric/score` and the Copilot review run are not required today.
* Actions settings: `can_approve_pull_request_reviews: true` (Actions may create pull requests), `default_workflow_permissions: read`.

### D2 current behaviour

* No file under `.github` defines or references Copilot Code Review. The `Copilot` run is a dynamic workflow (`dynamic/agents/copilot-pull-request-reviewer`) started by the ruleset rule above.
* `src-ci.yml` concurrency is `src-ci-<PR number>` with `cancel-in-progress: true` and triggers on `pull_request` and `workflow_dispatch`. A Copilot review run is a different workflow and is not in that group. A new push cancels the prior CI run regardless of Copilot. `infra-plan.yml` uses `cancel-in-progress: false`, `src-deploy.yml` never cancels.
* The only trigger Copilot review shares with CI is the push itself, through `review_on_push: true`. Per the analysis, the cancellation cause is unverified; fix 2 does not shorten the CI critical path.

## Findings that shape the design

1. A bot cannot push `latest.json` to `main` under the active ruleset. The refresh must be a bot branch plus pull request, merged by the workflow only when the ruleset permits it, otherwise left open for the owner.
2. The refresh must be scored on the merged `main` commit by the existing push path, using trusted base tooling, and must only write `latest.json` and `badge.svg`.
3. Coverage must be cumulative. `diff_args` uses the last commit that wrote `latest.json`; a refresh PR merging after later commits would hide earlier merge changes. Using the baseline's recorded `commit` when it is an ancestor of `HEAD` keeps the range exact, and cancelled or skipped refreshes lose nothing.
4. PRs scored against a lagging baseline can only be told apart if the report states how far behind the baseline is. This is the freshness signal.
5. Stale PR branches that already carry a bot-committed `latest.json` can overwrite the main baseline on merge. The gate must warn when a PR changes `latest.json` or `badge.svg`.
6. Post-merge scoring re-runs the agent for each merge that changes a scored artifact. Reusing the PR scorecard is a possible later optimisation, not part of this change.
7. D2 needs no in-repo workflow change. The trigger lives in the ruleset (`review_on_push`), which the task forbids changing. In repo, add a regression test that no workflow places a Copilot review run in a cancelling group or requires it, and document the policy and the owner action.

## Rejected options

* Direct push to `main` from the workflow: blocked by the `pull_request` rule.
* Committing the score to the PR branch (current): the defect being fixed.
* Replacing the baseline by a check verdict: loses the fingerprints and per-criterion scores `prepare.py` and `gate.py` need.
* Reusing the PR scorecard post-merge without rescoring: needs artifact transport and fingerprint reconciliation that cannot be exercised locally. Deferred as a follow-up.

## Owner actions identified

* Ruleset `mainprotect` (24504150): set the `copilot_code_review` rule to `review_on_push: false` so review runs on ready-for-review and on request only. Keep `required_status_checks` free of the Copilot run.
* Confirm the bot refresh pull request may merge (0 approvals required today). If a bypass or approval rule is added later, grant `github-actions[bot]` bypass or merge the refresh PR by hand.
* Open pull requests that already carry `chore(rubric): record score` commits should merge `main` and drop `latest.json` and `badge.svg` changes.

## Validation boundary

* Local: `actionlint`, YAML parse, `gh aw compile` for the lock file, the rubric pytest suite, then the full local RPI gate (the diff is not workflow-only, so tier is full).
* Not exercisable locally: a live GitHub run of the post-merge refresh, ruleset behaviour and PR creation by `GITHUB_TOKEN`. These stay unverified until the first merge after this PR lands.
