---
title: Capstone Rubric Gate
description: How the rubric-score agentic workflow scores the capstone against the FY27 AMA rubric and blocks pull requests that lower the score
ms.date: 2026-10-02
ms.topic: how-to
---

## What It Does

The [rubric-score workflow](../workflows/rubric-score.md) scores the capstone portfolio against the [FY27 capstone rubric](../../docs/reference/method/ama-capstone-assessment-guide.md) on every pull request to `main`, every push to `main` and on manual dispatch. It is a [GitHub Agentic Workflow](https://docs.github.com/en/copilot/concepts/agents/about-github-agentic-workflows) using the Copilot engine.

```text
rubric_prepare (deterministic)   fingerprints registered artifacts, compares with
                                 .github/rubric/scores/latest.json on main,
                                 skips the agent when nothing scored changed
agent (read-only, sandboxed)     reads the changed artifacts and baseline, returns one
                                 20-criterion scorecard through record_rubric_score
record-rubric-score (gate)       validates, carries forward unaffected criteria,
                                 computes totals, floors and band, compares with main,
                                 sets rubric/score, comments, reviews, commits latest.json
```

The pass or fail decision is made by [gate.py](scripts/gate.py), never by the model. A pull request passes when its total is greater than or equal to the baseline total on `main`. Criterion drops are listed as warnings. When the pull request merges, its committed `latest.json` becomes the new baseline on `main`.

A criterion can only move when an artifact that informs it changes, and every move must cite a changed file. Deleting a scored file, renaming it outside the registry globs or letting it grow past `max_file_bytes` counts as a change: the scorer can lower the affected criteria by citing the removed path, but a removed path never justifies a higher score.

Scores are readiness estimates from repository evidence. Live-scored criteria (B1 to B5 and C2) are informed only by the capstone deck and pitch artifacts. They keep their baseline until one of those changes, except in bootstrap and calibration runs, which score every criterion from scratch, and in pull requests that change the rubric, registry, prompt or scripts, which reopen every criterion (moves still need a cited changed artifact file).

## Files

| Path                                                 | Purpose                                                     |
|------------------------------------------------------|-------------------------------------------------------------|
| [rubric.json](rubric.json)                           | Criteria, sections, floors and outcome bands                |
| [artifacts.json](artifacts.json)                     | Registry of scored artifact types, globs and criteria       |
| [scores/latest.json](scores/latest.json)             | Current baseline; seeded from the manual review (61/100)    |
| [scripts/prepare.py](scripts/prepare.py)             | Fingerprints, scoring decision, agent context, PPTX text    |
| [scripts/gate.py](scripts/gate.py)                   | Deterministic validation, carry-forward and comparison      |
| [scripts/test_gate.py](scripts/test_gate.py)         | Unit tests for the gate                                     |
| [scripts/test_prepare.py](scripts/test_prepare.py)   | Change-detection tests on temporary git repositories        |

## Owner Setup

1. Create a fine-grained personal access token owned by your account with Account permissions, Copilot Requests: Read. Give it a short expiry. Store it as the repository secret `COPILOT_GITHUB_TOKEN`.
2. In Settings, Actions, General, enable "Allow GitHub Actions to create and approve pull requests". Without it the gate falls back to a comment review; the status check still works.
3. The lock file `.github/workflows/rubric-score.lock.yml` was compiled with gh-aw v0.89.21. After any edit to the workflow source, recompile and commit both files:

   ```bash
   gh extension install github/gh-aw
   gh aw compile rubric-score
   ```

   The compiler only runs the gate job when the agent called `record_rubric_score`. When the agent fails or skips the call, the `conclusion` job comments on the pull request and `rubric/score` stays pending, which keeps the pull request blocked until a rerun succeeds.
4. Merge the setup pull request. The setup pull request itself triggers a bootstrap run, and so does the first run after merge while `main` still holds the manual seed: the seed is replaced by the first workflow score without a comparison. Fixes to the gate scripts and rubric configuration take effect only after they merge, because every run loads them from `main`.
5. After one successful run, add a branch protection rule or ruleset on `main` that requires the `rubric/score` status check and requires branches to be up to date before merging. Do not make the bot review a required review.

## Day-to-Day Use

* Open a pull request. The workflow posts a sticky "Rubric score" comment, sets `rubric/score`, submits APPROVE or REQUEST_CHANGES, and commits the new `latest.json` to your branch. Pull that commit before pushing again.
* Pull requests that do not touch a scored artifact or the rubric tooling get an immediate `rubric/score` success without an agent run.
* If two pull requests both record a score, the second conflicts on `latest.json` after the first merges. Update the branch from `main` and push; the gate rescores against the new baseline.
* Pushes to `main` outside a pull request are scored for information only. A regression or an invalid scorecard on `main` opens an issue; an agent failure or timeout only shows as a failed run. Runs on other branches never open issues.
* To measure scorer variance, start the workflow manually with `force` ticked two or three times on an unchanged branch. Each forced run gets its own concurrency slot, so they do not cancel each other. Forced runs score every criterion from scratch with the baseline removed from the agent's context (the prompt also tells it not to read the scores file), report in the job summary, never update `latest.json` and never open issues.
* To recover from a stuck `pending` status, rerun the workflow from the Actions tab.

## Adding an Artifact Type

Edit [artifacts.json](artifacts.json) in its own pull request: set the entry's `status` to `active` and check its `include` globs and `criteria`. Registry and rubric changes take effect after they merge, because the gate reads them from `main`. The next pull request that touches those files scores them.

PRDs under `docs/prds/**/*.md` are active scoring artifacts. Planned entries remain for ADRs, solution code, infrastructure, the capstone deck (`docs/capstone/deck/*.pptx`), pitch transcripts (`docs/capstone/pitch/`) and the thought leadership artifact. PPTX files are converted to slide and speaker-note text before scoring.

## Limits and Risks

* A change to the rubric, the registry, the prompt or the model reopens every criterion in that pull request, but each move still needs a cited changed artifact file. Such changes therefore do not rescore untouched documents by themselves; their effect shows when the relevant artifacts next change, or in a forced calibration run. If a legitimate recalibration lowers the total, merge with an owner override and record why.
* The model is pinned in two places in [rubric-score.md](../workflows/rubric-score.md): `engine.model` and the gate's `--model` argument. Change both together and recompile.
* Pull request runs use the workflow file from the pull request. The gate scripts and rubric configuration are read from `main`, but a determined author could still edit the compiled workflow. Branch protection and review remain the control.
* Fork pull requests are blocked by the gh-aw default.
* Each scored run consumes AI credits. The scoring agent is capped at 300 per run by `max-ai-credits`; the threat-detection job has its own separate default cap.
* GitHub Agentic Workflows are in public preview and may change. Recompile deliberately after upgrading the extension.

Run the gate tests locally with `uv run --with pytest pytest .github/rubric/scripts`.
