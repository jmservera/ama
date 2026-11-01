---
title: Delivery Bottleneck Analysis and Seven-Day Speed-Up Plan
description: Measured delivery bottlenecks for the AMA repository on 2026-10-31, ranked fixes with expected savings, separated owner decisions and a seven-day plan to a working resident and employee demo
ms.date: 2026-11-01
ms.topic: reference
---

## Purpose and Scope

The owner needs a working version with the main functionalities (resident and
employee demo sites) within one week, with about 130 open issues and about 86
delivered in the previous two weeks. This page quantifies what slows delivery,
ranks fixes by expected saving, and keeps owner decisions separate from
changes an agent may make without new authority.

This is a research and planning page. No workflow, setting or code was
changed in the delivering PR. Every saving below is an estimate unless the
Evidence column says it was measured.

## Evidence and Limits

* Merged PR metrics: 381 merged PRs, PR numbers 1 to 621, merged 2026-09-26 to
  2026-10-31 (cutoff 2026-10-31T23:30Z). Extraction (run from the repository
  root; the working copy was `/tmp/prs-bottleneck.json`, which is not
  retained, so this command is the durable record):

  ```bash
  gh pr list --state merged --search "merged:<=2026-10-31T23:30:00Z" \
    --limit 400 \
    --json number,createdAt,mergedAt,additions,changedFiles > prs.json
  ```

  The search qualifier applies the cutoff before the limit. Dataset summary
  saved here because the file is not retained: 381 merged PRs (numbers 1 to
  621), 191 touching 16 or more files, 50 touching 5 or fewer files, merged
  2026-09-26 to 2026-10-31. Any later extraction is a point-in-time snapshot.

  Open-to-merge is `mergedAt - createdAt`; the 17 to 31 October and 27 to 31
  October rows filter on `mergedAt`. Percentiles use the nearest-rank method.
  Re-running later returns more PRs; keep the cutoff qualifier above.
* CI timings: the latest 300 workflow runs (run IDs 41207526347 to
  41253940923, 2026-10-31 13:28Z to 23:30Z, about 10 hours), of which 74 are
  Source projects CI runs in the table below:

  ```bash
  gh run list --limit 300 \
    --json databaseId,workflowName,conclusion,event,headSha,createdAt,startedAt,updatedAt
  ```

  `gh run list` has no upper time bound, so this sample is a point-in-time
  snapshot: later runs displace members of the 300-run window and the same
  command will not reproduce it. Dataset summary saved here: 300 runs, 74
  Source projects CI runs (23 succeeded, 29 cancelled), 87 Copilot runs, run
  IDs 41207526347 to 41253940923. Counts are by `workflowName` and `conclusion`; duration is
  `updatedAt - startedAt`. This is a sample of one busy day, not a two-week
  average. Job timings come from `gh run view <id> --json jobs` for the latest
  successful Source projects CI run in that window.
* Review loop: `gh pr view <n> --json commits,reviews` for the 40 PRs with the
  most recent merge times at the cutoff (PR 621 is the highest number; PRs 611
  and 618 are examples), counting reviews by author `copilot-pull-request-reviewer`
  and commits by the rubric bot author.
* Dataset summary kept in this page (sanitised, aggregate only): 381 PRs;
  median open-to-merge 1.2 h and mean 14.8 h for 17 to 31 October; median 19
  files and +2286 lines; 300 runs of which 74 Source projects CI (23 success,
  29 cancelled); 40 PRs with 193 Copilot reviews. These are the values the
  tables below use.
* Gate analysis: the 2026-10-27 local gate speed analysis (23 to 26 minutes is
  a sum of command durations, not a controlled serial wall-time baseline,
  reported on a 4 vCPU, 15 GiB VM), `tools/rpi-checks.py` (which supports
  parallel groups with `--jobs`, see #470), `.github/workflows/src-ci.yml` and
  `.github/workflows/rubric-score.lock.yml`.
* Open issues counted with `gh issue list --state open`: 132 on 2026-10-31.
* Not measured: the share of PR lines that are RPI artifacts (owner
  observation only), Playwright failure rates, the cause of the 19 to 24
  October slowdown, and human-gated issue ageing.

## Throughput Baseline

| Measure | Value | Source |
| --- | --- | --- |
| Merged PRs, whole window | 381 in 36 days, 10.6 per day | PR metrics |
| Merged PRs, 17 to 31 October | 203 in 15 days, about 14 per day | PR metrics |
| Merged PRs, 27 to 31 October | 130 in 5 days, 26 per day | PR metrics |
| Slow period | 19 to 24 October: 2 to 7 merges per day (16 in 6 days) | PR metrics, cause not diagnosed |
| Open-to-merge, 17 to 31 October | median 1.2 h, mean 14.8 h, p90 45 h | PR metrics |
| PR size, 17 to 31 October | median 19 files and +2286 lines; p90 53 files and +8321 lines | PR metrics |
| PR size, whole window | median 16 files, +1466 lines | PR metrics |

At 26 merges per day the repository is already fast for most PRs. The cost is
in the tail: the mean is twelve times the median, so a minority of large,
review-looped PRs holds most of the waiting time.

## Measured Bottleneck Table

Impact is the evidence-backed cost, not a forecast of what a fix saves.

| # | Bottleneck | Measured evidence | Impact | Confidence |
| --- | --- | --- | --- | --- |
| 1 | Source projects CI cancellations coincide with Copilot Code Review activity | 29 of 74 Source projects CI runs (39 percent) were cancelled, median 5.5 min each, about 160 minutes (29 x 5.5 median) of workflow elapsed time cancelled in 10 h, a median-based estimate and not measured runner usage. Only 23 runs succeeded (median 10.8 min). `src-ci.yml` has its own per-PR concurrency group (`src-ci-<PR number>`, `cancel-in-progress: true`), so a newer push to the same PR cancels the older run. 87 Copilot runs (median 3.9 min) fired in the same window. The sample shows cancellations and concurrent Copilot activity, not that Copilot caused them | Hypothesis: a push triggers both a review and a replacement CI run, and the replacement cancels the earlier run. Cancelling an obsolete run saves its cost, but the new head still needs a full CI run, so cancellation does not shorten the critical path by 11 min | Low: cancelled runs are not yet traced to replacement events and head SHAs |
| 2 | Rubric bot commits `latest.json` to PR branches | Workflow step "Record score on the pull request branch" commits and pushes `latest.json` and `badge.svg`. Rubric Scorer: 12 cancelled, 12 failed, 64 succeeded runs; 12 push-event runs. 33 of the last 40 PRs carry a bot commit (55 in total). 112 of about 203 merge commits since 17 October changed `latest.json` | Every bot push makes a new head SHA and invalidates exact-head evidence. Source projects CI triggers only on pull requests that touch the `paths` filter in `.github/workflows/src-ci.yml` (for example `src/**` and `infra/**`; ordinary documentation-only changes and rubric score files do not match), so a CI restart applies only to those PRs. Pushes made with `github.token` are normally suppressed from triggering new workflow runs (`.github/rubric/README.md`, recursive-trigger note), so on matching PRs CI on the new head may need a manual dispatch or a later human push; observed reruns versus automatic triggers are not yet separated. The file is a likely conflict hot spot | High for pushes and head invalidation; CI restart and conflict mechanisms are inferred, not replayed |
| 3 | Copilot review raises fresh threads after each push | Last 40 PRs: 193 Copilot reviews (mean 4.8, max 14 per PR), mean 7.2 commits per PR, max 39 | Hypothesis, unverified: that each push creates fresh threads and that correction cycles dominate the long tail. An automatic re-review can contain no new findings. Where a cycle does occur it costs a push, a CI run on PRs matching the `src-ci.yml` paths (11 min) and a review (4 min). Measurement action: count distinct new review threads per push and the time from each review to the next correction commit, before using this to justify D5 | Low: review count includes automatic re-reviews, not distinct threads |
| 4 | Very large PRs | 191 of 381 PRs touch 16 or more files: mean open-to-merge 15.1 h against 3.8 h for the 50 PRs of 5 or fewer files (median 0.9 h against 0.3 h) | Review surface and thread count grow with size; large PRs fail more rounds | High for correlation; the cause is not isolated and the RPI artifact share is unmeasured |
| 5 | Single heavy lock serialises local full gates | `HEAVY_LOCK_PATH=/tmp/ama-rpi-heavy.lock`, default wait 600 s; the 2026-10-27 analysis reports 23 to 26 min for `--all` as a historical command-duration sum, not a controlled wall-time baseline, and the runner now supports parallel groups with `--jobs` | Admission times out after 600 s and `src/README.md` requires nonqueued admission (`--lock-timeout 0`), so a long queue is not a supported mode. Current lock-held wall time is unmeasured | High for serialisation; duration is historical and unmeasured now |
| 6 | Hosted mssql and src-api jobs are long | Latest successful run: src-api 670 s (11.2 min), mssql 358 s (6.0 min), src-namespace 267 s, src-core 187 s, others under 75 s | CI wall time is set by src-api; every cancel or correction round pays it again | High |
| 7 | Unreliable browser checks | Local browser group is only 39 s when it works; #608 recorded a Chromium SIGABRT from a long socket path and blocked the SQL group; the earlier Playwright timeouts were reported by the owner | A false browser failure invalidates a 26 min gate run | Low to Medium: failure rate not measured |
| 8 | Human-gated issues | The cutover evidence pack records #523, #524, #570 and #432 as open with human attestation or pricing inputs missing | Not reducible by tooling; blocks demo claims regardless of speed | Medium: ageing not measured |

Local gate cost structure from the 2026-10-27 analysis: tests are 75 percent
of the 26 minutes (mssql 26 percent, project-api 22 percent, infra 16
percent, project-core 11 percent). The 23 to 26 minute total is a historical
command-duration sum, not a controlled baseline. Hosted CI overlaps only part
of the full local gate: `src-ci.yml` is path-filtered (it does not run for a
documentation-only PR such as this one) and builds or scans only changed
images, whereas `--all` covers all four images. Local repetition is therefore
a candidate duplicate, not a proven one; compare the checks and exact-head CI
runs actually available per PR before treating hosted CI as a replacement.
Measure serial against `--jobs` lock-held wall time (#470) before using any
gate duration in the plan.

## Ranked Fixes

Savings are per PR on the critical path unless stated. Rank orders by saving
divided by effort and risk. Fixes marked "agent-ready" need no policy change;
the rest need an owner decision in the next section.

| Rank | Fix | Addresses | Expected saving (estimate) | Effort | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | Stop the rubric bot committing `latest.json` and `badge.svg` to PR branches; publish the score as a PR check or comment and refresh the file on main only | 2 | Removes about 1.4 bot commits and head invalidations per PR, and the post-merge conflict on open PRs. CI restart saving applies only to PRs matching the `src-ci.yml` paths and is unverified (see bottleneck 2). Estimated 15 to 25 min per PR, hypothesis | Small workflow change | Owner decision D1 |
| 2 | Make Copilot Code Review non-cancelling: remove it from the CI concurrency group, run it as an advisory non-required review, or stop it triggering on every push | 1, 3 | Cancellations arise from `src-ci.yml` concurrency on new pushes, so this may not remove the 39 percent rate; cause unverified. Trace cancels first. Saves the cost of obsolete runs if the hypothesis holds; it does not by itself shorten the per-PR critical path, which depends on CI for the new head | Small | Owner decision D2; trace first |
| 3 | Cap PR size: target 10 files or fewer and about 600 added lines (superseded: owner rejected a size target on 2026-11-01, see D3; retained as the pre-decision analysis) | 4, 3 | The 5 or fewer file PRs merge in a mean 3.8 h against 15.1 h; fewer threads per review. Estimated halving of the long tail | Process change; separating RPI artifacts would fail the coordinator check unless D3 amends it | Owner decision D3 |
| 4 | Make the focused (`--changed`) tier the default local gate for source-only changes; full `--all` only for the final release candidate. A docs-only exception applies only after owner approval of D4 | 5, 7 | Historical 23 to 26 min sum versus 3 to 8 min focused (gate analysis estimate, not a controlled baseline); measure first | Tool exists; policy change | Owner decision D4 |
| 5 | Relax the two-cycle Copilot review rule: after two cycles, further new threads become follow-up issues unless they are blocking defects | 3 | Caps correction rounds if the cause in bottleneck 3 is confirmed by measurement; the mean PR has 7.2 commits and 4.8 reviews. Estimated 20 to 60 min per looped PR | Policy change | Owner decision D5 |
| 6 | Split src-api hosted tests into two parallel jobs and cache pip; start mssql in parallel (already a separate job) | 6 | src-api 11 min to about 6 min; CI wall time then limited by mssql at 6 min. Estimate only | Medium; touches workflows | Agent-ready after D1 and D2 |
| 7 | Coordinate admissions to the heavy lock (`--lock-timeout 0`, one owner at a time) and schedule full gates only at merge candidates against the current reviewed main base. Hosted CI counts as exact-head evidence only where it runs and covers the same checks | 5 | Unquantified until the lock-held wall time is measured; the earlier 182 min queue figure is withdrawn | Process | Owner decision D4 |
| 8 | Make browser checks retry once on infrastructure errors only (socket path, launch timeout), never on assertion failures, and keep the #610 guard, which rejects an overlong output path before browser launch. For #608 (a long socket path) a retry of the same path cannot succeed: use a new, admitted, shorter external scratch output, keep the original failure evidence, and reserve retries for transient launch failures | 7 | Avoids losing a long gate run to a launch error; failure rate unknown, so saving unquantified | Small; fix #608 follow-up | Agent-ready |
| 9 | Triage the 132 open issues into demo-critical (resident and employee demo paths), human-gated and deferred; park the rest until after the demo | 8 | Removes decision load; no minutes saved but protects the week | Small | Agent-ready |

Combined, fixes 1, 2 and 4 together are expected to remove most of the
per-PR critical path waiting for small PRs: from roughly 11 min CI plus one
restart plus 4 min review per cycle, to one CI run and one review. This is an
inference and should be re-measured after the first two days.

## Owner Decisions Required

These change policy, workflow behaviour or settings. The owner decided D1 to
D7 on 2026-11-01 (chat input to the agent); each outcome is recorded below as
`Decision 2026-11-01`. Workflow changes for D1 and D2 are delivered in a
separate PR and are not applied here. D4 and D5 policy text is applied in
`.github/copilot-instructions.md` and
`.github/agents/ama-backlog-delivery-coordinator.agent.md`.

* D1 Rubric score recording: stop the rubric bot pushing `latest.json` and
  `badge.svg` to PR branches. Options: post the score as a PR comment or
  check only; refresh the file on main by a separate scheduled or post-merge
  job. Consequence: the committed score file lags merges. A check verdict cannot
  replace the baseline: `prepare.py` reads artifact fingerprints and `gate.py`
  carries forward per-criterion scores from `latest.json`, and a main-only
  refresh lets concurrent PRs score against an outdated baseline. D1 must
  preserve a trusted full scorecard and define freshness handling. Needs a
  decision because the rubric workflow is a governance control.
  Decision 2026-11-01: APPROVED. The rubric score is posted as a PR check or
  comment and is not committed to PR branches. `latest.json` is refreshed on
  main by a post-merge job with freshness handling and a trusted full scorecard
  baseline. Workflow change: separate PR.
* D2 Copilot Code Review trigger: make it non-cancelling and advisory, or
  trigger only on ready-for-review and on request rather than every push.
  Consequence: some review comments arrive later; branch protection must not
  treat the review run as required.
  required by branch protection. Workflow part: separate PR.
* Implementation status, 2026-11-01: D1 is implemented on branch `ci/rubric-and-review-triggers` (PR
  pending): the rubric workflow no longer commits to PR branches, posts the
  score as `rubric/score`, a comment and a review, and refreshes `latest.json`
  and `badge.svg` on main through a bot pull request after merge, with
  freshness reported in the PR comment. D2 has no in-repo workflow change
  because the Copilot review is started by ruleset `mainprotect`; the owner
  action is to set `review_on_push` to `false` there and keep the review out of
  required checks. Neither effect is measured yet, and the measured evidence
  above is unchanged.
* D3 PR size policy: set a target size. Option for the owner: allow RPI
  evidence in a separate PR from the code. This would require amending the
  coordinator check in `.github/agents/ama-backlog-delivery-coordinator.agent.md`
  (about lines 461-466), which currently requires the issue's research, plan,
  changes and review files in that PR's diff; until amended, RPI evidence
  stays in the code PR. Consequence: more PRs and links to maintain, but
  smaller code review surfaces.
  Decision 2026-11-01: size target REJECTED (no PR size cap). Separate
  RPI-evidence PR option REJECTED: evidence stays in the code PR and the
  coordinator check is not amended.
* D4 Gate tier default: make the focused tier the default local gate and
  reserve the complete local gate for the final merge candidate. The current
  repository instructions (`.github/copilot-instructions.md`) require the
  complete exact-head gate for every final RPI candidate, including
  documentation-only work, so relaxing it, including any docs-only exception,
  needs an explicit owner amendment and applies only after that approval. Consequence: lower local assurance per iteration, with
  hosted CI as the per-push evidence.
  Decision 2026-11-01: APPROVED. The focused tier is the default local gate.
  The complete gate applies to big features, releases, infrastructure,
  deployment, SQL and security-sensitive changes. Independent exact-head
  review, hosted CI and human approvals are kept.
* D5 Two-cycle review rule: after two review correction cycles, convert new
  non-blocking threads to follow-up issues. Consequence: some edge cases ship
  and are tracked rather than fixed in place; blocking safety, privacy and
  accessibility defects still stop the PR.
  Decision 2026-11-01: APPROVED. After two correction cycles, new
  non-blocking Copilot threads become follow-up issues; blocking safety,
  privacy and accessibility defects still stop the PR.
* D6 Demo scope: confirm which resident and employee journeys are the
  minimum working version, and accept that human-gated items such as #523,
  #524, #570 and #432 are reported as pending, not accepted.
  Decision 2026-11-01: APPROVED with change. Minimum demo journeys are
  resident (sign in, own case status, grounded assistant, consent and
  appointments) and employee (sign in, capacity and work orders with paging,
  asset board, chat), plus the SENSORS LIVE VIEW. The human-gated #523, #524,
  #570 and #432 are reported pending, not accepted. Everything else is frozen
  outside these paths.
* D7 Review mode: confirm that human review of the final candidate remains a
  required boundary even when tiers are relaxed. This page does not remove it.
  Decision 2026-11-01: unchanged. Human review of the final candidate remains
  a required boundary.

### Owner-approved deferrals (2026-11-01)

These are deferrals, not met criteria.

* #466: scope is automated axe and keyboard checks only. Screen-reader and
  assistive-technology passes are deferred to before the production build.
* #163: criteria 2 and 5 (DPO and Legal) are deferred to before production.
  The demo uses synthetic data only.

## Seven-Day Plan

The plan assumes the owner decides D1 to D6 on day 1. If a decision is not
made, the dependent step is skipped and the fix is not applied.

| Day | Work | Exit evidence |
| --- | --- | --- |
| 1 (1 Nov) | Owner decides D1 to D6. Triage the 132 open issues into demo-critical, human-gated and deferred. Freeze new scope outside the demo paths. Verify live access to the selected demo, cost headroom and approvals: the resident AI authority in `infra/README.md` expires 2026-11-01T00:00Z and that page records live renewal as Pending, so obtain separate inference authority for any AI journey or mark it blocked | Decision record in the issue or PR; labelled issue list; recorded access, expiry and cost check |
| 2 | Apply D1 and D2 as one reviewed workflow PR. Start a daily metric: cancelled CI share, rubric bot commits per PR, merges per day | CI cancel share below 10 percent on the next 20 runs (target, to verify) |
| 3 | Apply D4 as policy text (D3 size target rejected 2026-11-01; ignore the pre-decision size exit evidence). Fix the browser launch retry (fix 8). Split src-api hosted CI (fix 6) if the owner agrees | Mean CI wall time near 6 to 7 min (the pre-decision 10-file PR target is superseded by D3) |
| 4 | Resident demo path: close the demo-critical resident issues using small PRs. Run at most two parallel loops per heavy-lock slot | Resident demo journey passing authorized live checks of the reviewed deployment (hosted CI is synthetic only) |
| 5 | Employee demo path: same method. Do not start new human-gated work; record pending attestations | Employee demo journey passing authorized live checks; the evidence pack records it blocked by missing independent identity expectations, so keep it blocked until those prerequisites exist; #523/#524/#570 shown as pending where unproven |
| 6 | Stabilise: fix regressions only; no new features. One complete local gate on the merge candidate | Exact-head receipt verified against the current main base; hosted CI green where it applies. Repeat the authorised live checks for each journey claimed working on the final release candidate, since day-6 fixes can change the deployment checked on days 4 and 5; a journey not rechecked is reported as unverified |
| 7 | Demo-ready release candidate (live journey checks repeated on this exact deployment), owner review, remaining issues parked with rationale | Owner acceptance recorded; open-issue list reconciled |

Eight parallel loops: the VM has one heavy lock and its current wall time is
unmeasured, so run the eight loops on source work and documentation and use
hosted CI as per-push evidence only where it runs. Admit full local gates one
at a time with `--lock-timeout 0` (admission times out after 600 s; no
queued waiting), coordinated against each current reviewed main base. Each
merge advances that base and makes the other candidates' receipts stale, so
budget revalidation per candidate; do not promise a three-hour batch. Measure
serial against `--jobs` first (#470) and size the day-6 window from that.

## Risks and Open Questions

* The 300-run CI sample covers one day. Re-run the measurement over 14 days
  before treating cancel and failure percentages as stable.
* The cause of the 19 to 24 October slowdown (2 to 7 merges per day) is not
  diagnosed. It may be a work pattern, an outage or a gate backlog.
* The RPI artifact share of PR size is an owner observation, not a measured
  result. A file-path breakdown of the last 100 merged PRs would confirm
  fix 3.
* Relaxing gates trades assurance for speed. The decision belongs to the
  owner and must not weaken accessibility, privacy, safety, resident consent
  or human approval boundaries.
* Savings are estimates. None has been trialled.

## Related

* [Source README local RPI gate](../../../src/README.md#local-rpi-gate)
* [Live evidence pack](../../architecture/cutover-evidence-pack.md)
* [Tracking retention policy](../method/tracking-retention-policy.md)
