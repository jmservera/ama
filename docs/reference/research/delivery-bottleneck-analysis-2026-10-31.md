---
title: Delivery Bottleneck Analysis and Seven-Day Speed-Up Plan
description: Measured delivery bottlenecks for the AMA repository on 2026-10-31, ranked fixes with expected savings, separated owner decisions and a seven-day plan to a working resident and employee demo
ms.date: 2026-10-31
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

* Merged PR metrics: `/tmp/prs-bottleneck.json` (381 merged PRs, merged
  2026-09-26 to 2026-10-31; fields are open-to-merge time, files and added
  lines) and `gh pr list --state merged`.
* CI timings: `gh run list` over the latest 300 runs, which span only
  2026-10-31 13:28Z to 23:30Z (about 10 hours). They are a sample of one busy
  day, not a two-week average. Job timings come from the latest successful
  Source projects CI run.
* Review loop: `gh pr view` commits and reviews for the 40 most recently
  merged PRs.
* Gate analysis: the 2026-10-27 local gate speed analysis (serial `--all`
  gate of 23 to 26 minutes on a 4 vCPU, 15 GiB VM), `tools/rpi-checks.py`,
  `.github/workflows/src-ci.yml` and `.github/workflows/rubric-score.lock.yml`.
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
| 1 | Copilot Code Review cancels Source projects CI | 29 of 75 Source projects CI runs (39 percent) were cancelled, median 5.5 min each, about 160 runner minutes wasted in 10 h. Only 23 runs succeeded (median 10.8 min). Workflow concurrency is `cancel-in-progress: true` per PR; 87 Copilot runs (median 3.9 min) fired in the same window | Each cancel adds a full 11 min rerun to the critical path | Medium: cause per cancel not traced individually |
| 2 | Rubric bot commits `latest.json` to PR branches | Workflow step "Record score on the pull request branch" commits and pushes `latest.json` and `badge.svg`. Rubric Scorer: 12 cancelled, 12 failed, 64 succeeded runs; 12 push-event runs. 33 of the last 40 PRs carry a bot commit (55 in total). 112 of about 203 merge commits since 17 October changed `latest.json` | Every bot push makes a new head SHA, restarts CI and review, and invalidates the exact-head gate; the file is a guaranteed conflict hot spot | High for pushes; conflict mechanism inferred, not replayed |
| 3 | Copilot review raises fresh threads after each push | Last 40 PRs: 193 Copilot reviews (mean 4.8, max 14 per PR), mean 7.2 commits per PR, max 39 | Correction cycles dominate the long tail; each cycle costs a push, a CI run (11 min) and a review (4 min) | Medium: review count includes automatic re-reviews, not only distinct threads |
| 4 | Very large PRs | 191 of 381 PRs touch 16 or more files: mean open-to-merge 15.1 h against 3.8 h for the 50 PRs of 5 or fewer files (median 0.9 h against 0.3 h) | Review surface and thread count grow with size; large PRs fail more rounds | High for correlation; the cause is not isolated and the RPI artifact share is unmeasured |
| 5 | Single heavy lock serialises local full gates | `HEAVY_LOCK_PATH=/tmp/ama-rpi-heavy.lock`, default wait 600 s; one `--all` gate takes 23 to 26 min, 17 of 17 completed runs | With 8 parallel loops the last gate waits up to 7 x 26 = 182 min; more than one gate per 26 min is impossible on this VM | High for serialisation; queueing is arithmetic, not observed |
| 6 | Hosted mssql and src-api jobs are long | Latest successful run: src-api 670 s (11.2 min), mssql 358 s (6.0 min), src-namespace 267 s, src-core 187 s, others under 75 s | CI wall time is set by src-api; every cancel or correction round pays it again | High |
| 7 | Unreliable browser checks | Local browser group is only 39 s when it works; #608 recorded a Chromium SIGABRT from a long socket path and blocked the SQL group; the earlier Playwright timeouts were reported by the owner | A false browser failure invalidates a 26 min gate run | Low to Medium: failure rate not measured |
| 8 | Human-gated issues | The cutover evidence pack records #523, #524, #570 and #432 as open with human attestation or pricing inputs missing | Not reducible by tooling; blocks demo claims regardless of speed | Medium: ageing not measured |

Local gate cost structure from the 2026-10-27 analysis: tests are 75 percent
of the 26 minutes (mssql 26 percent, project-api 22 percent, infra 16
percent, project-core 11 percent). Everything runs serially and a hosted CI
run already covers the same checks, so local repetition is the largest
avoidable duplicate.

## Ranked Fixes

Savings are per PR on the critical path unless stated. Rank orders by saving
divided by effort and risk. Fixes marked "agent-ready" need no policy change;
the rest need an owner decision in the next section.

| Rank | Fix | Addresses | Expected saving (estimate) | Effort | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | Stop the rubric bot committing `latest.json` and `badge.svg` to PR branches; publish the score as a PR check or comment and refresh the file on main only | 2 | Removes about 1.4 bot commits and one CI plus review restart per PR; removes the post-merge conflict on every open PR. Estimated 15 to 25 min per PR | Small workflow change | Owner decision D1 |
| 2 | Make Copilot Code Review non-cancelling: remove it from the CI concurrency group, run it as an advisory non-required review, or stop it triggering on every push | 1, 3 | Removes the 39 percent cancel rate; about 11 min per avoided rerun. About 160 runner minutes per busy day | Small | Owner decision D2 |
| 3 | Cap PR size: split RPI artifacts into a docs PR separate from the code PR, target 10 files or fewer and about 600 added lines | 4, 3 | The 5 or fewer file PRs merge in a mean 3.8 h against 15.1 h; fewer threads per review. Estimated halving of the long tail | Process change | Owner decision D3 |
| 4 | Make the focused (`--changed`) tier the default local gate for source-only changes; docs-only changes need no heavy gate; full `--all` only for the final release candidate | 5, 7 | 26 min to 3 to 8 min per iteration (gate analysis estimate); frees the lock for other loops | Tool exists; policy change | Owner decision D4 |
| 5 | Relax the two-cycle Copilot review rule: after two cycles, further new threads become follow-up issues unless they are blocking defects | 3 | Caps correction rounds; the mean PR has 7.2 commits and 4.8 reviews. Estimated 20 to 60 min per looped PR | Policy change | Owner decision D5 |
| 6 | Split src-api hosted tests into two parallel jobs and cache pip; start mssql in parallel (already a separate job) | 6 | src-api 11 min to about 6 min; CI wall time then limited by mssql at 6 min. Estimate only | Medium; touches workflows | Agent-ready after D1 and D2 |
| 7 | Cap concurrent heavy local gates at the lock and let every loop use hosted CI as the exact-head evidence for docs-only and small PRs; schedule full gates only at merge candidates | 5 | Removes up to 182 min of queueing with 8 loops | Process | Owner decision D4 |
| 8 | Make browser checks retry once on infrastructure errors only (socket path, launch timeout), never on assertion failures, and keep the short scratch path guard from #610 | 7 | Avoids losing a 26 min run to a launch error; failure rate unknown, so saving unquantified | Small; fix #608 follow-up | Agent-ready |
| 9 | Triage the 132 open issues into demo-critical (resident and employee demo paths), human-gated and deferred; park the rest until after the demo | 8 | Removes decision load; no minutes saved but protects the week | Small | Agent-ready |

Combined, fixes 1, 2 and 4 together are expected to remove most of the
per-PR critical path waiting for small PRs: from roughly 11 min CI plus one
restart plus 4 min review per cycle, to one CI run and one review. This is an
inference and should be re-measured after the first two days.

## Owner Decisions Required

These change policy, workflow behaviour or settings. None was applied in this
PR and none should be assumed.

* D1 Rubric score recording: stop the rubric bot pushing `latest.json` and
  `badge.svg` to PR branches. Options: post the score as a PR comment or
  check only; refresh the file on main by a separate scheduled or post-merge
  job. Consequence: the committed score file lags merges; the rubric gate
  must read the check result instead of the file. Needs a decision because the
  rubric workflow is a governance control.
* D2 Copilot Code Review trigger: make it non-cancelling and advisory, or
  trigger only on ready-for-review and on request rather than every push.
  Consequence: some review comments arrive later; branch protection must not
  treat the review run as required.
* D3 PR size policy: require separate PRs for RPI artifacts and code, with a
  target size. Consequence: more PRs and links to maintain, but smaller review
  surfaces.
* D4 Gate tier default: make the focused tier the default local gate and
  reserve the complete local gate for the final merge candidate. The current
  repository instructions require the complete gate for every final RPI
  candidate, including documentation-only work, so this needs an explicit
  owner amendment. Consequence: lower local assurance per iteration, with
  hosted CI as the per-push evidence.
* D5 Two-cycle review rule: after two review correction cycles, convert new
  non-blocking threads to follow-up issues. Consequence: some edge cases ship
  and are tracked rather than fixed in place; blocking safety, privacy and
  accessibility defects still stop the PR.
* D6 Demo scope: confirm which resident and employee journeys are the
  minimum working version, and accept that human-gated items such as #523,
  #524, #570 and #432 are reported as pending, not accepted.
* D7 Review mode: confirm that human review of the final candidate remains a
  required boundary even when tiers are relaxed. This page does not remove it.

## Seven-Day Plan

The plan assumes the owner decides D1 to D6 on day 1. If a decision is not
made, the dependent step is skipped and the fix is not applied.

| Day | Work | Exit evidence |
| --- | --- | --- |
| 1 (1 Nov) | Owner decides D1 to D6. Triage the 132 open issues into demo-critical, human-gated and deferred. Freeze new scope outside the demo paths | Decision record in the issue or PR; labelled issue list |
| 2 | Apply D1 and D2 as one reviewed workflow PR. Start a daily metric: cancelled CI share, rubric bot commits per PR, merges per day | CI cancel share below 10 percent on the next 20 runs (target, to verify) |
| 3 | Apply D3 and D4 as policy text. Fix the browser launch retry (fix 8). Split src-api hosted CI (fix 6) if the owner agrees | New PRs of 10 files or fewer; mean CI wall time near 6 to 7 min |
| 4 | Resident demo path: close the demo-critical resident issues using small PRs. Run at most two parallel loops per heavy-lock slot | Resident demo journey passing in hosted CI |
| 5 | Employee demo path: same method. Do not start new human-gated work; record pending attestations | Employee demo journey passing in hosted CI; #523/#524/#570 shown as pending where unproven |
| 6 | Stabilise: fix regressions only; no new features. One complete local gate on the merge candidate | Exact-head receipt verified; hosted CI green |
| 7 | Demo-ready release candidate, owner review, remaining issues parked with rationale | Owner acceptance recorded; open-issue list reconciled |

Eight parallel loops: the 4 vCPU VM supports one full gate every 26 minutes,
so run the eight loops on source work and documentation, and let hosted CI
(not the local lock) be the per-push evidence. Queue full local gates only for
merge candidates: eight candidates then wait about three hours in total, which
fits the day-6 stabilisation window but not a daily cycle.

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
