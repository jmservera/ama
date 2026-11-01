---
title: Capstone Rubric Gate
description: How the rubric-score agentic workflow scores the capstone against the FY27 AMA rubric and blocks pull requests that lower the score
ms.date: 2026-10-30
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
                                 sets rubric/score, comments and reviews; on main only,
                                 refreshes latest.json through a bot pull request
```

The pass or fail decision is made by [gate.py](scripts/gate.py), never by the model. A pull request passes when its total is greater than or equal to the baseline total on `main`. Criterion drops are listed as warnings. Pull requests never write `latest.json` or `badge.svg`; the full scorecard baseline on `main` is refreshed after merge (see [Baseline refresh and freshness](#baseline-refresh-and-freshness)).

A criterion can only move when an artifact that informs it changes, and every move must cite a changed file. Deleting a scored file, renaming it outside the registry globs or letting it grow past `max_file_bytes` counts as a change: the scorer can lower the affected criteria by citing the removed path, but a removed path never justifies a higher score.

### Owner-Selected Cowork v2 Deck (2026-10-23)

The registry selects only
`docs/capstone/deck/zava-forward-cowork-v2-draft.pptx` for `capstone-deck`.
The older executive deck and the
[imported Cowork source and historical exports](../../docs/capstone/history/cowork-generated/README.md)
are not alternate scored decks. The imported source PPTX is encrypted;
the later owner-supplied public v2 export is installed at the selected path.
Local verification with the actual extractor reads 54 slides and 54
speaker-note blocks and confirms Cowork's final slide-39 save marker.
PDFs and handoff claims do not substitute for extracted notes. These local
checks are not a fresh hosted assessment or a full content/accessibility review.

`prepare.py` supports an optional artifact-level `max_file_bytes` override.
Only `capstone-deck` raises this limit to 20,000,000 bytes; other artifacts
retain the 2,000,000-byte registry default. Files above their effective limit
are still excluded, and the 200,000,000-byte PPTX decompression guard remains.
The regression checks cover the exact size boundary, unchanged non-deck
limit and exclusion of historical/protected deck paths.

These are pending branch changes, not an activated hosted score. PR scoring
loads its trusted registry and tooling from base `main`. They must reach
that trusted base before a fresh v2 assessment can use the new selection
and allowance. Do not edit `scores/latest.json`, fall back to the historical
deck, or claim a v2 pass while readable slide-and-notes evidence is missing.

### Capstone Reorganization (2026-10-29)

The [current capstone index](../../docs/capstone/README.md) separates delivery,
complete native/JSON/image sources, pitch, demo and preserved history. The
scoring PPTX stays at the same exact path with the same 20 MB allowance.
The `pitch` artifact now includes `.md`, `.txt` and `.vtt` files in both
`docs/capstone/pitch/` and `docs/capstone/demo/`. Historical packages and
the source baseline are outside those scopes; they are not current rehearsal
evidence. Thought-leadership registration and recorded scores are unchanged.

The actual supplied deck has 108 fixed slide-jump actions, not the older
review's 27 dynamic caller returns. The new builder preserves its actual
navigation and all 54 notes; original findings and counts remain dated history.
Local registry/extraction tests do not dispatch the scoring agent or establish
a fresh grade. Hosted PR preparation still uses trusted base-`main`
configuration, so the new demo-folder scope is active there only after this
registry update is integrated. Preserve the normal publication and review gates.

### PPTX Slide Citation Repair

For text, cite `path:line`. For a deck, cite its original repository `.pptx`
path, optionally followed by `:slideN` (positive slide number), not the
temporary extracted Markdown path. The legacy parser stripped line anchors
only, so PR #61's `:slide1` and `:slide17` citations were treated as different
filenames and B1/B2/B6/B7 changes were discarded. Normalising supported slide
anchors fixes the mismatch without relaxing changed-file, artifact-presence
or floor rules; unchanged decks and unsupported slide anchors remain rejected.

The regression coverage adds 12 cases. Run the 19 targeted cases with:

```bash
python -m pytest .github/rubric/scripts/test_gate.py -q -k 'evidence_reference or changed_deck or unchanged_deck or unsupported_slide or pptx_slide or no_pitch_or_thought'
```

The wider gate/prepare/adapter suites had 19 confirmed pre-existing failures
coupled to the historical 66-point seed and retired prototype registry; see
the 2026-11-01 reassessment in [Zava Forward MVP](#zava-forward-mvp).
This repair does not change those fixtures, rubric defaults or `latest.json`.
The recorded PR score was 35; replaying its saved assessment with the repaired
parser yielded 47, a reproduction rather than a fresh assessment. The separate
[report-only calibration](https://github.com/jmservera/ama/actions/runs/38177388117)
on `6a8b60a` measured revised-deck B1/B2/B6/B7 at 4 each and the full portfolio
at 43/100, Incomplete because pitch and thought leadership evidence was missing.
Calibration neither updates the baseline nor supplies an incremental comparison.

Ordinary PR runs load the trusted gate from base `main`. The owner must merge
this independent repair first, then trigger fresh scoring for presentation
PR #61's current head before deciding whether to merge it. Merge updated
`origin/main` into the presentation topic and push without rewriting history.
Rerunning an older head's run can hit the branch-moved guard; merging this
repair alone does not automatically replace PR #61's score.

Scores are readiness estimates from repository evidence. Live-scored criteria (B1 to B5 and C2) are informed only by the capstone deck and pitch artifacts. They keep their baseline until one of those changes, except in bootstrap and calibration runs, which score every criterion from scratch, and in pull requests that change the rubric, registry, prompt or scripts, which reopen every criterion (moves still need a cited changed artifact file).

## Scorecard Submission Preflight

### PR #423 invalid D1 details (2026-10-30, Refs #360)

[Run 40556907743](https://github.com/jmservera/ama/actions/runs/40556907743)
recorded no score: its actual submitted D1 object contained an extra
`evidence2` field alongside `evidence`, `rationale` and `change_reason`.
The strict adapter rejects extra keys even on unchanged, closed criteria.
This was a malformed model tool submission, not missing fields in the
transport documentation and not a measured numerical score regression.
The existing jq preflight already rejects this shape; the adapter and
actual prompt-filter regressions now cover the exact extra-key case.
Strict validation and the generated workflow are unchanged.

A diagnostic replay removing only that extra field yields 77 against the
77 baseline. It is not a new assessment or a recorded score. Only A1/A3/A5
were open, each already 5; infrastructure evidence cannot raise closed
pitch or thought-leadership criteria. The
[transport evidence map](../../infra/README.md#transport-evidence-and-integration-2026-10-30-refs-360)
distinguishes offline proof from live gaps. A fresh hosted submission after
publication remains necessary; no local test guarantees model compliance.

[Run 40025652570](https://github.com/jmservera/ama/actions/runs/40025652570)
was rejected because D3 omitted `change_reason`, not because its total fell
below the 55-point baseline. The template contained the field, but the
submitted details did not. No valid score was recorded.

The scorer prompt now requires a read-only `jq -e` preflight of the complete
final arguments before its single `record_rubric_score` call. The embedded
filter checks all 20 criterion IDs, all 22 argument keys, exact score choices,
detail keys and types, non-blank summary/rationales, and rationale length.
It emits the candidate unchanged, without filling missing fields or coercing
values. A failed preflight must be corrected before submission. Tests execute
the actual filter from the prompt, including the D3 omission and a score with
a trailing newline:

```bash
.venv/bin/python -m pytest .github/rubric/scripts/test_scorecard_adapter.py -q
```

All 49 adapter tests pass locally after a separate fixture repair. The two
earlier round-trip/carry-forward failures were reproduced from unchanged
HEAD: their submitted-card fixture reused an unfinished baseline-derived
template. Completed-card tests now use explicit synthetic grades, independent
of the recorded score. Zero/null baseline cases are covered, while unscored
bootstrap/calibration scaffolds remain rejected. Production template, adapter,
gate and recorded baseline behavior are unchanged.

This is an executable agent instruction, not a new MCP interception hook.
The pinned runtime still checks `details` only as a string before append;
the strict adapter validates its contents afterward. The preflight does not
prove evidence quality, reject duplicate outer JSON keys, or replace the
gate's comparison and exactly-one-submission rule. Duplicate keys inside
encoded details remain rejected by the adapter. No hosted rerun or score
recovery is implied by these local tests. Deck registration and size support
on trusted base `main` remain separate from this submission repair.

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

## Owner Setup

1. No repository token secret is required by this workflow. Copilot inference
   uses the automatic Actions token with `copilot-requests: write`. GitHub
   checkouts, reads and safe outputs explicitly use `secrets.GITHUB_TOKEN`; the
   post-merge baseline refresh commit uses the equivalent `github.token`. Both refer to the job-scoped token
   minted by GitHub, not a secret an operator creates. The generated lock
   must not be edited independently of the Markdown source.

   Secretless inference still requires GitHub to authorize Copilot requests
   for this repository and its billing context. The
   [official authentication reference](https://github.github.com/gh-aw/reference/auth/)
   (checked 2026-10-13) documents organization Copilot billing for this path
   and PAT-based inference for personal repositories or unavailable centralized
   billing. This repository is user-owned: compilation does not prove that
   GitHub has enabled token-based inference here. Check a real agent run;
   requesting a permission does not create a subscription or entitlement.
   No PAT fallback is configured.
2. In Settings, Actions, General, enable "Allow GitHub Actions to create and approve pull requests". Without it the gate falls back to a comment review; the status check still works.
3. The lock file `.github/workflows/rubric-score.lock.yml` was compiled with gh-aw v0.89.21. After any edit to the workflow source, recompile and commit both files:

   ```bash
   gh extension install github/gh-aw
   gh aw compile rubric-score
   ```

   The compiler only runs the gate job when the agent called `record_rubric_score`. When the agent fails or skips the call, the `conclusion` job comments on the pull request and `rubric/score` stays pending, which keeps the pull request blocked until a rerun succeeds.
4. Merge the setup pull request. The setup pull request itself triggers a bootstrap run, and so does the first run after merge while `main` still holds the manual seed: the seed is replaced by the first workflow score without a comparison. Fixes to the gate scripts and rubric configuration take effect only after they merge, because every run loads them from `main`.
5. After one successful run, add a branch protection rule or ruleset on `main` that requires the `rubric/score` status check and requires branches to be up to date before merging. Do not make the bot review a required review.

### Job-Scoped Token Permissions

The agent has `contents: read`, `issues: read`, `pull-requests: read` and
`copilot-requests: write`, but no repository write permission. The trusted
prepare job has `contents: read`, `statuses: write` and `pull-requests: write`
to publish the initial status and dismiss obsolete bot reviews. The trusted
record job has `contents: write`, `statuses: write`, `pull-requests: write` and
`issues: write` to commit score files and publish the verdict/review/comment
or a main-branch regression issue. The compiler scopes helper-job permissions;
the generated workflow defaults to `permissions: {}`.

Explicit built-in token bindings prevent optional `GH_AW_GITHUB_TOKEN` or
`GH_AW_GITHUB_MCP_SERVER_TOKEN` secrets from replacing repository-operation
credentials. Compiler-generated optional diagnostic/telemetry secret
references do not make those secrets required. The Copilot PAT secret is
not used or required. Existing repository secrets are not deleted by this
change.

GitHub normally suppresses new workflow runs caused by pushes made with
`GITHUB_TOKEN`, avoiding recursive scoring on the refresh commit. The gate
publishes `rubric/score` on the scored SHA only; the workflow no longer
commits to pull request branches. Fork pull requests
and repository policy can restrict token writes independently of requested
permissions.

## Day-to-Day Use

* Tracking-only changes under `.copilot-tracking/**` do not trigger any of
  the four repository push/PR workflows. Rubric and prototype workflows
  explicitly ignore that path; MVP workflows already include only their
  source/infrastructure/workflow paths. Mixed source/tracking changes still
  trigger applicable checks, and manual dispatch remains available.
  GitHub evaluates PR filters against the cumulative PR diff, not just the
  latest commit. Required checks on a path-filtered workflow can remain
  pending; do not require unconditional checks for tracking-only PRs while
  also expecting no workflow to run.
* Open a pull request. The workflow posts a sticky "Rubric score" comment, sets `rubric/score`, and submits APPROVE or REQUEST_CHANGES. It does not commit to your branch, so there is nothing to pull before pushing again.
* Pull requests that do not touch a scored artifact or the rubric tooling get an immediate `rubric/score` success without an agent run.
* A pull request that still carries an older bot commit editing `latest.json` or `badge.svg` gets a warning in the report. Merge `main` and drop those file changes so the merge cannot overwrite the trusted baseline. Pull requests no longer conflict with each other on `latest.json`.
* Pushes to `main` outside a pull request are scored for information only. A regression or an invalid scorecard on `main` opens an issue; an agent failure or timeout only shows as a failed run. Runs on other branches never open issues.
* To measure scorer variance, start the workflow manually with `force` ticked two or three times on an unchanged branch. Each forced run gets its own concurrency slot, so they do not cancel each other. Forced runs score every criterion from scratch with the baseline removed from the agent's context (the prompt also tells it not to read the scores file), report in the job summary, never update `latest.json` and never open issues.
* To recover from a stuck `pending` status, rerun the workflow from the Actions tab.

### Closed and Moved Pull Request Heads

The recording job checks current PR state before checkout and uses the original
event's immutable head SHA. An explicitly closed PR is an obsolete run: it
emits a notice and does not record or publish a score. A missing branch alone
is not proof of closure; PR API errors or invalid responses fail visibly.
There is no checkout fallback to `main`.

For an open PR, a moved head blocks a passing verdict. State is checked again
before publication, which requires the current PR head to equal the scored SHA.
The status, comment and review target only that SHA. PR lifecycle and API calls
are not a single transaction, and movement after the final API read is not
claimed to be atomically prevented. Closed obsolete runs are not rubric passes,
successful reruns or issue closure.

### Baseline refresh and freshness

`latest.json` and `badge.svg` on `main` are the trusted full scorecard baseline
read by `prepare.py` and `gate.py`. Only the post-merge refresh writes them:

* After a successful, non-calibration, non-forced run on `refs/heads/main`
  (push or manual dispatch), the `Refresh baseline on main` step copies the
  scorecard and badge to a commit on `rubric/baseline-refresh`, opens or
  updates one pull request and squash-merges it with `--match-head-commit`.
  The ruleset requires a pull request, so a direct push to `main` is not used.
* Publication is compare-and-swap. The step observes the refresh branch head
  first, skips when `latest.json` on `main` or the pending refresh commit
  (`Scored commit:` trailer) records a commit newer than the scored SHA, pushes
  with a lease on the observed head, and re-checks `main` before merging. An
  older dispatch therefore cannot replace a newer score, whichever run finishes
  first.
* Pull request edits to `latest.json` or `badge.svg` are detected against the
  merge-base, so a PR forked before a main-only refresh is not flagged. A
  badge-only edit triggers scoring so the warning is reported.
* A refresh is skipped when the decision is invalid, failed or calibration, the
  checkout is not the scored SHA, or nothing changed. A blocked merge is a
  warning; the next main run refreshes cumulatively.
* The refresh commit is made with `GITHUB_TOKEN`, so it triggers no workflow
  and cannot recurse.
* Freshness: the baseline records the main commit it scored. The PR report
  states how many scored paths changed on `main` since that commit. Push and
  dispatch runs diff from that commit when it is an ancestor, so changes
  accumulate until a refresh lands. A missing or non-ancestor commit (legacy
  baselines) is reported as freshness unavailable.
* Cost: a merge that changes scored artifacts is rescored once on `main`. Reusing
  the PR scorecard is a deferred follow-up.

Owner actions (not applied by this change): confirm the refresh pull request can
merge under ruleset `mainprotect`. The refresh pull request is made with
`GITHUB_TOKEN`, so it triggers no workflows and gets no `rubric/score` status;
this works only while the ruleset requires zero approvals and no status checks
(the state on 2026-11-01), or lets `github-actions[bot]` bypass. Otherwise the
merge warns and the baseline stays stale until merged by hand. Also ask open pull requests to drop old bot score
commits; and, for Copilot Code Review, set `review_on_push` to `false` in the
ruleset so it runs on ready-for-review and on request, and keep it out of
required status checks. Copilot Code Review is advisory and is not part of any
workflow concurrency group in this repository
(`test_workflow_policy.py`).

Run the local source/compiled lifecycle, publication and baseline-refresh
regressions without dispatching the scorer:

```bash
python3 -m pytest .github/rubric/scripts/test_record_workflow.py .github/rubric/scripts/test_workflow_policy.py -q
```

### Post-Push Visibility and Exact-Head Completion

PR #416's [run 39237980947](https://github.com/jmservera/ama/actions/runs/39237980947)
recorded 48/100 against baseline 48/100 and successfully appended score commit
`7e810dc9c9ac520e4e7717b4604dc08fbbc8e311` to scored commit
`e87967580520f421e6181dff546b478bf5c02f1a`. Nevertheless publication reported
branch movement. Its actual inputs show the new SHA and successful gate,
recording and lifecycle outcomes: the immediate PR API head comparison caused
the denial. The original response SHA was not logged, so old-head visibility
is a reproduced explanation, not an observed response value or proof of a race.
The workflow's successful conclusion did not make its failed status a pass.

After a successful guarded score push, publication now makes at most five
PR-head reads, waiting 1/2/4/8 seconds only while the API still returns the
original scored SHA. It still requires the exact newly pushed SHA before
publishing success. An unrelated head, prior movement, failed push, API error,
invalid response or closed PR is not eligible for this wait. Exhaustion fails
with a distinct visibility message. Diagnostics record public SHAs/attempts
only. Scoring, trusted baseline tools, push protections and review requirements
are unchanged. Movement after the last API read remains a non-atomic limitation.

A finite publication sequence separates scoring from final-head validation:

1. Obtain the required independent source/RPI/full-receipt assessment and
   publication authority for a clean frozen candidate before pushing it.
   One ordinary source push triggers legitimate scoring; do not dispatch paid
   scoring merely to diagnose this lifecycle.
2. Let that run complete its one score append and verdict. Verify live PR state,
   resulting head, score commit's parent and score-only diff. A real numeric
   regression or failed publication remains blocked. Do not edit the recorded
   score's `commit`: it names the scored source, not the metadata commit.
3. Fetch and fast-forward the clean local topic to that final remote head.
   Every earlier receipt/review is insufficient for this new exact HEAD.
   Run the [complete local gate](../../src/README.md#local-rpi-gate) in a fresh
   external directory, verify against freshly fetched main, and obtain independent
   exact-head assessment again. No new commit is needed to validate this head;
   keep its receipt external.
4. Run required hosted checks on that same final head using their existing
   supported mechanism, not a source/empty commit or a rubric rescore. For the
   existing non-deploying Source CI workflow, an authorized operator can use
   `gh workflow run src-ci.yml --ref fix/demo-private-publisher-360`, then verify
   the resulting run's `headSha` equals the frozen PR head. Dispatch selects all
   four image checks when no base is supplied. Its downstream infrastructure
   workflow requires a `pull_request` event, so a dispatch does not authorize
   or execute Azure what-if. This does not substitute for any separately
   required PR-only/protected-environment checks: if their supported exact-head
   execution is unavailable, stop for that concrete permission/mechanism blocker.
5. Update the PR's external evidence pointers only after the required assessment
   and authority. Recheck head/base before the owner's merge decision.
   Do not push again merely to refresh evidence or manually set green statuses,
   dismiss reviews, disable checks or bypass protection.

GITHUB_TOKEN's suppression of recursive workflows is intentional; the one
rubric status on both exact source/bot SHAs is not a Source CI result.
If the visibility wait is exhausted after a successful append, stop and retain
the failed run. Rerunning the original scoring event after its head moved can
legitimately hit the stale-head guard; repeated pushes/rescores are not a
recovery strategy. A further authorized repair would be needed, not an
unbounded retry loop or trust in an arbitrary candidate score file.

Local source/compiled lifecycle regressions include transient and persistent
old-head visibility, true concurrent movement/deletion before and after Git
advertisement, actual remote score-push rejection, and the real deterministic
nondecreasing comparison. These tests simulate API responses, not hosted API
latency or product acceptance. The wider rubric suite retained 21 pre-existing
failures (seed/adapter assumptions and retired trigger expectations) at the
pre-recovery head; they were not silently suppressed or repaired by this bounded
lifecycle change. The 2026-11-01 count is 17 (see
[Zava Forward MVP](#zava-forward-mvp)).

## Adding an Artifact Type

Edit [artifacts.json](artifacts.json) in its own pull request: set the entry's `status` to `active` and check its `include` globs and `criteria`. Registry and rubric changes take effect after they merge, because the gate reads them from `main`. The next pull request that touches those files scores them.

BRDs, PRDs, solution code, infrastructure, ADRs, the capstone deck
(`docs/capstone/deck/*.pptx`), pitch transcripts (`docs/capstone/pitch/`) and
the thought leadership artifact (`docs/capstone/thought-leadership/`) are active
artifacts. [docs/capstone/README.md](../../docs/capstone/README.md) is the
storage map for every capstone asset. PPTX files are converted to slide and
speaker-note text before scoring.

### Score badge

Whenever the gate records `latest.json` it also renders `badge.svg` (rubric score out of 100, coloured by outcome) and the post-merge baseline refresh commits both together on `main`. The root README embeds it with a relative link, so it renders for anyone who can read the repository. The gate script that renders it loads from `main`, so the first badge update follows the first run after this change merges.

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

### Zava Forward MVP

On 2026-10-08 the owner directed that the MVP replaces the earlier prototype as
the scored solution code. `solution-code` now includes `mvp/zavaforward_mvp/`,
`mvp/web/` (without `vendor/`), `mvp/tests/`, `mvp/Dockerfile`, `mvp/README.md`
and the data generator scripts under `support/synthetic-data/`. The private
`mvp/data/` is excluded. The registry no longer reads `prototype/`. The prototype
was removed in #202 step 1, together with its validation workflow and the dead
`prototype/deploy/**/*.bicep` infrastructure glob; the registry edit takes
effect only after that pull request merges.

On 2026-10-15 (#198, ADR 0006) `solution-code` also excludes
`src/**/web/vendor/**`, `src/**/data/**`, `**/*.egg-info/**` and `**/build/**`,
so third-party, private and generated files under `src/` are not scored.
`src/**/*` already counts tests, `pyproject.toml` and Dockerfiles. The `mvp/`
globs stay until the cut-over registry pull request. A registry change takes
effect only after it merges; `rubric_version` is not bumped.

On 2026-10-15 (#199 M5) the moved code, web assets, tests and Dockerfile are
counted through `src/**/*`, so the `mvp/zavaforward_mvp`, `mvp/web`, `mvp/tests`
and `mvp/Dockerfile` globs were removed; only `mvp/README.md` remains.

On 2026-10-15 (#199 M6) `mvp/README.md` was split into the per-project READMEs
(`src/api`, `src/core`, `src/agents`, `src/orchestrator`, `src/importer`), which
`src/**/*` already counts, so the `mvp/README.md` glob was removed. The dated
evidence sections moved unchanged; only the `mvp/` pointer README is left, and
it is not scored.

On 2026-11-01 (#198) the registry state was re-checked. `artifacts.json` has no
`mvp/` include glob and no `prototype/` or `prototype/deploy/**/*.bicep` glob;
only the defensive `mvp/data/**` and `mvp/web/vendor/**` excludes remain, and
`rubric_version` is still 2. The migration baseline was 47 of 100 (commit
9261c5c); `scores/latest.json` now records 77 (A34, B23, C11, D9) at commit
051f6a3. The recovery came through later per-criterion re-evidencing from
`src/**/*`, not through a registry or version change. The historical per-pull-
request dip records and cut-over sequence are documented in
`docs/architecture/cutover-evidence-pack.md` and are not reconstructed here.

The same day the 19 recorded pre-existing test failures were re-assessed by
running `python -m pytest .github/rubric/scripts -q`: 17 failed, 358 passed, 7
skipped. Seven failures assert the retired 66-point seed (six in `test_gate.py`,
one in `test_prepare.py`) and ten are tracking-only trigger cases for
`infra-plan`, `mvp-ci`, `mvp-validation`, `src-ci` and `src-deploy`. None
touches the registry or `src/` counting, and they remain unrepaired follow-up
work.

### Solution code and infrastructure

The `solution-code` entry covers `src/**/*` and the registered synthetic-data
generator scripts. There are no legacy-directory include globs. Archive
`v0.21.0` marks the owner-approved 2026-10-27 pointer retirement; the dated
migration notes above remain historical. Legacy data/vendor exclusions remain
defensive and do not add scored inputs.
It informs A1, A3, A4, A5, A6 and A7, plus B6: the README is capstone
documentation, whose completeness and navigability are explicitly assessed by
B6 in the [assessment guide](../../docs/reference/method/ama-capstone-assessment-guide.md).
Criteria are mapped per artifact, not per file, so any solution-code change
reopens those seven criteria; a score move still needs relevant changed-file
evidence. This mapping does not establish implementation completeness or AI
quality, and does not map the code to Section D thought leadership.

The `infrastructure` entry covers `infra/**/*`, informing A1, A3 and A5. Bicep
is not included in `solution-code`.

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
