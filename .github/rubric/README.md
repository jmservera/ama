---
title: Capstone Rubric Gate
description: How the rubric-score agentic workflow scores the capstone against the FY27 AMA rubric and blocks pull requests that lower the score
ms.date: 2026-10-05
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

For text, cite `path:line`. For a deck, cite its original repository `.pptx`
path, optionally followed by `:slideN` (positive slide number), not the
temporary extracted Markdown path. The gate resolves supported anchors to the
file before checking that it changed. PR #61's deck was detected and assessed,
but its `:slide1` and `:slide17` citations were previously treated as filenames,
so genuine deck score changes were discarded. Slide-anchor support repairs
that mismatch without relaxing changed-file, artifact-presence or floor rules.
As with other gate repairs, ordinary PR runs use the base-branch script until
the owner merges this change. Replaying a saved scorecard verifies the fix;
it is not a new independent assessment of a revised deck.

Validation of the slide-anchor repair passed all 19 targeted citation and
required-artifact tests. The wider gate/prepare/adapter run had 100 passes,
one skip and 19 failures. A snapshot of the unchanged pre-repair commit
reproduced those 19 failures: old tests assume a 66-point seed and active
prototype paths although the recorded score and solution registry have
changed. The snapshot's initially omitted workflow fixture caused one extra
failure; restoring that fixture made its prompt-example test pass. No new
failure is attributed to the slide-anchor change, and this repair does not
modify unrelated historical test expectations.

The fresh report-only calibration of the revised deck completed successfully
in [run 38177388117](https://github.com/jmservera/ama/actions/runs/38177388117),
on commit `6a8b60a`. It assessed B1, B2, B6 and B7 at 4 each and the full
portfolio at 43/100 (A=23, B=16, C=4, D=0). The gate recorded missing pitch and
thought-leadership criteria at zero, leaving the outcome Incomplete. This
forced run used the repaired branch scripts and withheld the baseline; it
measures the revised artifact but neither overwrites `latest.json` nor supplies
an incremental comparison. Its full-portfolio total must not be compared as
a deck regression against the earlier saved-card replay.

Scores are readiness estimates from repository evidence. Live-scored criteria (B1 to B5 and C2) are informed only by the capstone deck and pitch artifacts. They keep their baseline until one of those changes, except in bootstrap and calibration runs, which score every criterion from scratch, and in pull requests that change the rubric, registry, prompt or scripts, which reopen every criterion (moves still need a cited changed artifact file).

## Files

| Path                                                 | Purpose                                                     |
|------------------------------------------------------|-------------------------------------------------------------|
| [rubric.json](rubric.json)                           | Criteria, sections, floors and outcome bands                |
| [artifacts.json](artifacts.json)                     | Registry of scored artifact types, globs and criteria       |
| [scores/latest.json](scores/latest.json)             | Current rubric baseline loaded from the base branch         |
| [scores/badge.svg](scores/badge.svg)                 | Score badge generated with latest.json, linked from the root README |
| [scripts/prepare.py](scripts/prepare.py)             | Fingerprints, scoring decision, agent context, PPTX text    |
| [scripts/gate.py](scripts/gate.py)                   | Deterministic validation, carry-forward and comparison      |
| [scripts/scorecard_adapter.py](scripts/scorecard_adapter.py) | Strict score-choice and details reconstruction |
| [scripts/test_scorecard_adapter.py](scripts/test_scorecard_adapter.py) | Adapter, canonical gate and unscored scaffold tests |
| [scripts/test_safe_output_runtime.py](scripts/test_safe_output_runtime.py) | Generated-schema and pinned real MCP runtime tests |
| [scripts/test_gate.py](scripts/test_gate.py)         | Unit tests for the gate                                     |
| [scripts/test_prepare.py](scripts/test_prepare.py)   | Change-detection tests on temporary git repositories        |
| [prototype-validation.yml](../workflows/prototype-validation.yml) | Separate, secretless validation for the local prototype |

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

BRDs, PRDs, solution code, infrastructure, ADRs, the capstone deck
(`docs/capstone/deck/*.pptx`), pitch transcripts (`docs/capstone/pitch/`) and
the thought leadership artifact (`docs/capstone/thought-leadership/`) are active
artifacts. [docs/capstone/README.md](../../docs/capstone/README.md) is the
storage map for every capstone asset. PPTX files are converted to slide and
speaker-note text before scoring.

### Score badge

Whenever the gate records `latest.json` it also renders `badge.svg` (rubric score out of 100, coloured by outcome) and the workflow commits both together. The root README embeds it with a relative link, so it renders for anyone who can read the repository. The gate script that renders it loads from `main`, so the first badge update follows the first run after this change merges.

### Required evidence

A criterion can only score what is committed. [rubric.json](rubric.json) gives
criteria a `requires_any` list of artifact ids. When none of them holds a file,
the gate records 0 whatever the model submitted (the model is told to submit 1),
lists the override as a warning and counts the criterion as failing its floor.
`cap_without` caps a score instead: B6 is capped at 3 without a deck.
The Section D artifact must also be submitted; without it the outcome is
"Incomplete" even if the totals clear the floors. BRDs, PRDs and code never
count toward B1 to B5, B7, C2, C3 or Section D, because the guide scores those
on the live session and on a separate artifact.

Changing `rubric_version` makes the next run rescore from scratch without a
comparison with the previous baseline, so a stricter rubric does not fail as a
regression. The gate stamps the version into `latest.json`.

### Proper Warm MVP

On 2026-10-08 the owner directed that the MVP replaces the earlier prototype as
the scored solution code. `solution-code` now includes `mvp/properwarm_mvp/`,
`mvp/web/` (without `vendor/`), `mvp/tests/`, `mvp/Dockerfile`, `mvp/README.md`
and the data generator scripts under `support/synthetic-data/`. The private
`mvp/data/` is excluded. The prototype description below is retained for
history; the registry no longer reads `prototype/`. The Prototype validation
workflow still checks only `prototype/`, so MVP tests are not yet run in CI.

### Proper Warm Prototype

The existing `solution-code` entry preserves `src/**/*` and also includes the
prototype's Python implementation (`prototype/properwarm/`), web UI, Python
tests and build scripts, `Dockerfile`, `requirements.txt`, `README.md` and
Excalidraw architecture diagram. It informs A1, A3, A4, A5, A6 and A7, plus B6:
the README is capstone documentation, whose completeness and navigability are
explicitly assessed by B6 in the [assessment guide](../../docs/reference/method/ama-capstone-assessment-guide.md).
Criteria are mapped per artifact, not per file, so any solution-code change
reopens those seven criteria; a score move still needs relevant changed-file
evidence. This mapping does not establish implementation completeness or AI
quality, and does not map the prototype to Section D thought leadership.

The existing `infrastructure` entry preserves `infra/**/*` and includes
`prototype/deploy/**/*.bicep`, informing A1, A3 and A5. Bicep is not included
in `solution-code`. Generated fixtures and the import workbook under
`prototype/seed/` are excluded; their generator scripts remain implementation
evidence.

Pull request preparation and gating load `artifacts.json` from the base branch
(`origin/main`), not the proposed registry in the pull request. The registry
activation PR therefore cannot use its newly activated entries to score the
prototype. A registry edit reopens all criteria under the existing scoring
instrument rules, but does not by itself produce a prototype score.

After the owner merges the registry activation PR, the owner must rerun the
rubric workflow for prototype PR #15 or synchronize that PR with `main` and
push to trigger a new run. The run then uses the merged active registry to
assess prototype evidence against the current baseline. An earlier
`rubric/score` success reporting "No scored artifact changed" is a skipped
assessment, not a prototype score. Neither PR should be merged automatically.

### Scorer execution and complete scorecards

The scoring agent is a read-only reviewer, not a test runner. It receives no
application secrets and must inspect JSON and repository content with the
provided `jq` and read/search tools. It must not install packages, run Python
or pip, execute candidate code or tests, attempt live Azure inference, or
repeatedly retry a denied command. The trusted prepare and gate jobs run their
own scripts outside the agent. Python and pip remain outside the agent's
allowlist.

Trusted context generation adds `scorecard_template` to
`/tmp/gh-aw/agent/rubric/context.json`. In an incremental run it contains all
20 rubric IDs and copies each known baseline score, evidence and rationale;
`change_reason` starts empty. The agent preserves closed criteria and assesses
open criteria from the evidence. Bootstrap and calibration templates instead
show `score: null` and an `UNSCORED` rationale for every criterion, so no grade
is fabricated or carried forward; calibration also withholds baseline scores.
Context also contains `tool_inputs_template`: twenty required score choices
(`A1_score` through `D3_score`), `details` and `summary`. The choices are
strings `"1"` through `"5"`, not numbers. `details` is a JSON string with
exactly all twenty IDs, each containing only `evidence` (array of strings),
`rationale` and `change_reason` (strings). An unchanged criterion supplies an
empty `change_reason`; this does not introduce a new grading rule. The adapter
rejects missing, unknown, duplicate or mistyped detail fields, explicitly
maps exact choice strings to integers, and never invents scores or details.
The canonical template remains available; bootstrap/calibration tool-input
templates retain null scores and unscored rationales, not submittable grades.

The owner selected this 22-input contract after the pinned v0.89.21 compiler
rejected the original 81-input design with `maxProperties: got 81, want 25`.
MCP required/type/choice checks protect score completeness and allowed values
before append. The pinned custom-job MCP handler does not enforce a
one-call quota; multiple schema-valid items can be appended. The trusted gate
accepts exactly one item and rejects multiple submissions. Details syntax and
semantic shape validation happen only in the trusted adapter downstream, so
malformed details fail scoring and a second corrected call creates a
multiple-item submission that the gate rejects. Do not describe details as a
nested MCP schema or claim the adapter can trigger a protected pre-append
retry.

The output must replace every placeholder and contain exactly A1-A7, B1-B7,
C1-C3 and D1-D3. `gate.py` remains strict: missing IDs, unknown IDs, invalid
scores and malformed scorecards fail closed before any carry-forward.
Previously recorded canonical `scorecard` items remain readable for
compatibility; the new tool no longer advertises that string argument.
The adapter is loaded with the prepare and gate scripts from the base branch
and is part of scoring-instrument change detection. Merge this repair to main
only after owner approval, then synchronize prototype PR #15: before that,
its trusted base scripts cannot consume the new input contract.

`test_safe_output_runtime.py` exercises the compiled tool schema and the real
stdio and HTTP MCP servers. It verifies required/type/choice/unknown-key
rejections do not append, a corrected retry is accepted, a second valid call
is appended but rejected by `gate.parse_scorecard`, and malformed details
JSON reaches the adapter only downstream. The test pins runtime source blobs
from github/gh-aw-actions commit
`924af5fdc64061cfbf66fb584c8b07e2ac230c60`; set `GH_AW_RUNTIME_DIR` to that
checkout's `setup/js` directory to run it. It skips if the runtime is absent.
This confirms single-item acceptance at the trusted gate, not a transport
quota.

### Separate prototype validation

The ordinary
[Prototype validation workflow](../workflows/prototype-validation.yml) runs
after checkout with `contents: read`, no OIDC permissions, no persisted
checkout credentials and no Azure or application secrets. Dependency
installation and test execution happen only in this isolated job, not in the
scoring agent. When `prototype/` is present it installs the declared
requirements through pip with normal TLS, compiles the Python package, runs
the standard-library unittest suite, executes `evaluate_agent.py` without
`--live` and checks browser JavaScript syntax. It does not deploy Bicep or
contact Azure. When the directory is absent, the job summary explicitly says
that no prototype checks or test evidence were produced; detection occurs
after checkout so the check activates when prototype files arrive.

On this repair branch, `prototype/` is absent. Merge the scorer repair to
`main` first, then synchronize prototype PR #15 with `main` and push to trigger
the base-branch workflow against its checked-out prototype. The resulting
validation is independent of rubric scoring and is not deployment approval.

## Limits and Risks

* A change to the rubric, the registry, the prompt or the model reopens every criterion in that pull request, but each move still needs a cited changed artifact file. Such changes therefore do not rescore untouched documents by themselves; their effect shows when the relevant artifacts next change, or in a forced calibration run. If a legitimate recalibration lowers the total, merge with an owner override and record why.
* The model is pinned in two places in [rubric-score.md](../workflows/rubric-score.md): `engine.model` and the gate's `--model` argument. Change both together and recompile.
* Pull request runs use the workflow file from the pull request. The gate scripts and rubric configuration are read from `main`, but a determined author could still edit the compiled workflow. Branch protection and review remain the control.
* Fork pull requests are blocked by the gh-aw default.
* Each scored run consumes AI credits. The scoring agent is capped at 300 per run by `max-ai-credits`; the threat-detection job has its own separate default cap.
* GitHub Agentic Workflows are in public preview and may change. Recompile deliberately after upgrading the extension.

Run the gate tests locally in a Python virtual environment with
`python -m pip install pytest`, then
`python -m pytest .github/rubric/scripts`. Use the configured company proxy
for package retrieval; do not bypass proxy or TLS controls.
