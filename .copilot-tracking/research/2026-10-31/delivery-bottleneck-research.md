---
title: Delivery bottleneck research
description: RPI research record for the delivery bottleneck analysis
ms.date: 2026-10-31
---

## Disposition

* Research disposition: executed. Planning Readiness: Ready.
* Task slug: delivery-bottleneck-plan. Mode: automatic (user requested the full loop).

## Evidence gathered

* `/tmp/prs-bottleneck.json`: 381 merged PRs. 203 merged 17-31 October (about 14 per day); 130 in 27-31 October. Open-to-merge median 1.2 h, mean 14.8 h, p90 45 h. PRs of 16 or more files: 191, mean 15.1 h; PRs of 5 or fewer files: 50, mean 3.8 h.
* `gh run list` (latest 300 runs, 2026-10-31 13:28Z to 23:30Z): Source projects CI 29 cancelled, 21 failed, 23 succeeded (median 10.8 min); Copilot 87 runs, median 3.9 min; Rubric Scorer 12 cancelled, 12 failed, 64 succeeded.
* Latest successful CI run job times: src-api 670 s, mssql 358 s, src-namespace 267 s, src-core 187 s.
* Last 40 merged PRs via `gh pr view`: mean 7.2 commits, 193 Copilot reviews, 55 rubric bot commits.
* `git log origin/main -- .github/rubric/scores/latest.json`: 112 commits since 17 October.
* `rubric-score.lock.yml` step "Record score on the pull request branch" commits and pushes latest.json and badge.svg; `src-ci.yml` concurrency is `cancel-in-progress: true`.
* `tools/rpi-checks.py`: `/tmp/ama-rpi-heavy.lock`, 600 s default wait, `--changed` mode exists.
* 2026-10-27 gate analysis: serial gate 23-26 min; tests 75 percent.
* 132 open issues.

## Lane coverage (eight bottleneck lanes)

The eight requested parallel loops were run as eight analysis lanes by one agent, one per bottleneck, not as eight sub-agents, to keep a docs-only task cheap. Lanes: CI cancel, rubric bot, review loop, PR size, heavy lock, hosted CI time, browser reliability, human gates.

## Gaps

* CI sample is one day. RPI artifact share of PR size, Playwright failure rate and the 19-24 October slowdown cause are unmeasured.
