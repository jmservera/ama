---
title: Issue 108 demo model evidence research
description: Research for a documentation-only record of configured model, version and rate-limit facts for the existing demo deployment, against origin/main 0f420dc95
ms.date: 2026-11-07
---

## Disposition

Research executed (issue body and comments, knowledge-base index and synthesis, owned native evidence, one fresh read-only Azure readback, three official Microsoft Learn pages). Planning Readiness: Ready.

## Evidence

* Issue #108 (open): criterion "Model names, versions and quotas are confirmed in the chosen region" is unticked. The 2026-10-31 closure audit says chosen-region actual serving names, versions and quotas are unconfirmed; the 2026-11-04 audit leaves regional model/quota confirmation open. Held-out, human, benefit and actual-serving criteria are separate and unticked.
* Knowledge base: `docs/reference/README.md` points #108 and cost evidence to `docs/reference/resources/ai-tokenomics.md` (its Gaps table already names #108). `infra/README.md` records the 2026-10-28 nano deployment at capacity 1, Legacy lifecycle, inference retirement 2027-04-14.
* Native #891 evidence `/mnt/ama-gates/live-891-capacity-1107` (before/after deployment JSON, account, model SKUs, model capacities; owner comment 6705173727 at 2026-11-07T09:40:56Z): capacity 1 to 10, rate limits 1/1,000 to 10/10,000 per 60 s, nano 2025-04-14, `NoAutoUpgrade`, `Microsoft.DefaultV2`. `usage.json` and `location-usages.json` are empty lists. `availableCapacity` for nano `GlobalStandard` uksouth was 4,999 before the change.
* Fresh read-only readback 2026-11-07 (`az cognitiveservices account deployment show`, `account show`, `account list-models`, this resource only) matches the coordinator readback. No token or key was printed.
* Official sources (retrieved 2026-11-07): deployment types (Global may process in any Azure region; page 2026-08-06), working with models (`NoAutoUpgrade` semantics), quota (TPM per subscription/region/model/type; RPM ratio varies by model; page 2026-05-04).
* Live app environment, provider responses and any other candidate model were not read; no regional evidence exists for other candidates.

## Decisions

* Integrate into the existing AI Tokenomics synthesis; no new page.
* Record configuration facts only; state explicitly what each does not prove.
* Do not tick or relax any criterion; keep the original log append-only.
