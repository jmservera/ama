---
title: Issue 1397 rubric scoring failure research
ms.date: 2026-11-17
---

## Status

Research disposition: executed (supplements the merged 2026-11-10 record in `.github/rubric/README.md`). Planning Readiness: Ready.

## Measurements (2026-11-17, base eb51af5c)

* The failing run 42838857558 (2026-11-10, commit 6cc59776) is already diagnosed in `.github/rubric/README.md`: an empty-details placeholder call reached `scorecard_adapter.from_inputs`, which raised `details must contain exactly the 20 rubric criterion IDs`. Source is byte-identical to the #1383 failing commit; the rejection is designed fail-closed behaviour.
* `gh run list --workflow "Capstone Rubric Scorer" --branch main -L 40` shows 40 runs: the newest 17 all succeeded (2026-11-15 onward to 2026-11-17T20:09Z). Baseline `scores/latest.json` is total 79 at commit 915788b6, run 44156510325.
* The 8 non-success runs on 2026-11-14/15 were cancelled (concurrency) or failed in the `activation` job (runs 43664409796: daily AI Credits `Server Error`; 43613413504: `Daily AIC inspection stopped to preserve GitHub API quota`). None is a scoring-details rejection.
* The key-set rule for an empty `{}` object is not pinned by a test: `test_malformed_details_fail_without_defaults` covers one deleted ID but not an empty object.

## Conclusions

* Cause: producer submitted a placeholder `details: {}` as the judged call. Smallest fix inside authority: pin the rejection with a regression test and record current recovery evidence. Refusing placeholders before append, retaining accepted-item/decision artifacts, or reconciling the quota statement need workflow or prompt changes and are owner/full-tier items.
* Recovery: successor baseline publication proven (PR #1398 and later 17 successes); recovery of 6cc59776 itself remains unproved. Issue criteria 2 and 4 stay partly unmet.
