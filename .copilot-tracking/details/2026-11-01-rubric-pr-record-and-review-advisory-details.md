---
title: Rubric PR recording and Copilot review advisory details
description: Phase details for the rubric recording change (D1) and Copilot Code Review advisory policy (D2)
ms.date: 2026-11-01
ms.topic: reference
---

## Phase 2 details: workflow

File `.github/workflows/rubric-score.md` (source) and `.github/workflows/rubric-score.lock.yml` (compiled).

* Delete the record step and hook. The job keeps `contents: write` because the refresh pushes `rubric/baseline-refresh`; the step is guarded by `github.event_name` and `github.ref`.
* Refresh step guard: `(github.event_name == 'push' || (github.event_name == 'workflow_dispatch' && github.event.inputs.force != 'true')) && github.ref == 'refs/heads/main' && steps.gate.outcome == 'success'`.
* Refresh script: read `/tmp/rubric-out/decision.json` with `jq`; require `valid` and `passed` and not `calibration`; require `latest.json`; copy `latest.json` and `badge.svg` into `.github/rubric/scores/`; exit when `git diff --quiet`. Create the commit on a detached `HEAD` at the scored SHA, push `HEAD:refs/heads/rubric/baseline-refresh` with `--force-with-lease` using the remote's current value, then `gh pr list/create/edit/merge`. Merge retried up to five times with a short sleep; a blocked merge is a warning, not a failure.
* Publish verdict: PR path sets the status on `SCORED_SHA`; `moved` and `lifecycleFailed` remain; no recorded-score copy in descriptions; the review uses `commit_id` of `SCORED_SHA`. The description for a pass is `<total>/100 vs baseline <baseline>/100`.

## Phase 3 details: tooling

* `diff_args(root, base_ref, event, baseline_commit=None)`: for non-PR events, when `baseline_commit` resolves to a commit that is an ancestor of `HEAD`, return `[baseline_commit, "HEAD"]`. Otherwise keep the last-scores-commit rule and the first-parent rule for a tip that wrote scores.
* `baseline_freshness(root, base_ref, baseline, artifacts)` returns `{"commit", "known", "pending"}` where `pending` is the sorted scored paths (in scope of an active artifact) that differ between the baseline commit and `base_ref`.
* `compute_state` adds `baseline_freshness` and `recorded_scores_changed` (PR event, `latest.json` or `badge.svg` differs from base).
* `gate.render_report` gets an optional `freshness` argument; `main` passes it and adds the edit warning to `result["warnings"]`. Freshness is omitted for bootstrap and calibration.

## Phase 4 details: tests

* `test_record_workflow.py`: remove recording-push tests and hook tests; keep lifecycle, malformed-response, API-failure and non-PR tests; add publish tests (single status, review commit id, moved, failed checks); add refresh script tests with local bare remote and a fake `gh` on `PATH` (no commit when unchanged, branch commit parent is the scored SHA and touches only the two files, no run on regressed or calibration decision, merge-blocked is a warning, `main` is never updated); assert the record step is absent in source and lock; keep source and lock equality.
* `test_prepare.py`: diff base uses baseline commit when ancestor; falls back when not; freshness pending count; PR editing `latest.json` sets `recorded_scores_changed`.
* `test_gate.py`: report shows freshness and warning.
* `tools` or `.github/rubric/scripts/test_workflow_policy.py`: Copilot review is not required, no repo workflow includes `copilot-pull-request-reviewer` in a cancelling concurrency group.

## Phase 5 details: documentation

* `.github/rubric/README.md`: replace "commits latest.json to your branch" language, document the refresh PR, freshness, legacy branch handling, owner actions.
* `docs/reference/research/delivery-bottleneck-analysis-2026-10-31.md`: add an implementation status note for fixes 1 and 2 without rewriting measured evidence.
* `docs/reference/log.md`: append entry. `docs/reference/README.md`: update only if a page is added.
