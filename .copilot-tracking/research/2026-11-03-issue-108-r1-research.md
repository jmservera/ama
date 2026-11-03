---
title: Issue 108 round 1 research
ms.date: 2026-11-03
---

Research disposition: executed (repository and merged-PR review). Planning Readiness: Ready.

## Already delivered (merged PRs)

* #258 offline AI eval harness evidence gate; #405 priority run accounting; #636 and #821 cohort/missing-data record and manifest-bound approval; #817 and #428 human-review intake and protocol; #684 owner-authorised limit guard; #697 cohort ranking eval; #307 chat evaluation.
* Existing cost-per-accepted logic exists only for the paired chat trial (`paired_trial.cost_per_accepted_check`); no candidate comparison exists.

## Gap

Tokenomics criteria (cost per accepted proposal, cheaper-but-worse is failure, one lever at a time on same cases, tokens per proposal and spread) have no grader. Regional model/version/quota, held-out split, live calls, human trials and Finance validation need owner, Azure or participant input and stay out of scope.

## Chosen slice

Pure offline `candidate_comparison` grader in `src/agents` with synthetic tests. No SQL, security, infrastructure or deployment change; focused tier.
