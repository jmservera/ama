<!-- markdownlint-disable-file -->
---
title: Rubric Model Pilot Research
description: Evidence and controls for the owner-approved three-model pilot
ms.date: 2026-10-24
---

## Brief

The owner selected the cheaper-model comparison and explicitly approved a
USD 10 pilot with one assessment per model on 2026-10-24. No production model,
score, workflow, remote status or PR changes are authorized. No repeated-model
equivalence claim can follow from one sample per model.

## Findings

* The failed hosted Sonnet 5 assessment used 229.99097 credits, about USD 2.30,
  across 67 inference calls. Its D3 details omitted change_reason.
* The scorer now has executable jq preflight; 49 adapter tests pass after
  separating completed synthetic submissions from unscored baseline templates.
* Local Copilot CLI is 1.0.103; hosted workflow pins 1.0.87. A local pilot is
  not an exact hosted reproduction.
* CLI supports explicit model selection, restricted available tools, disabled
  custom instructions, final usage JSON and a session credit guardrail.
* Credit guardrails are soft. Reserve headroom within USD 10 and stop starting
  runs as the allowance is approached. Count failed billable attempts too.

## Selected Approach

Freeze registered artifact files, rubric, guide, prompt and tools from one
commit. Withhold prior scores. Use the same isolated read-only assessment
prompt and tools for Sonnet 5, Haiku 4.5 and GPT-6 Luna. Collect one result per
model; do not replace unavailable models or retry assessments without approval.
Use the production adapter and pure gate locally to validate each returned
card. Record requested/served models, elapsed time, credits, validity, full
20-score vectors and pairwise differences. Never publish pilot scores.

## Questions and Limits

* Actual model access and authentication remain unverified until invocation.
* Identical evidence does not imply identical model-selected reads.
* Baseline-hidden calibration and same-baseline incremental gate replay are
  separate measurements; pilot grades must not replace the live baseline.
* Faster/cheaper observed samples do not establish stable score equivalence.

## State

Pilot complete: one invocation each, no fallback or retry. Sonnet returned a
valid card at 61/100, 121.75 seconds and USD 0.240189 equivalent. Haiku omitted
summary and added prose/fences; adapter rejection, 113.76 seconds and USD
0.11417745 equivalent. Luna returned a valid card at 59/100, 155.89 seconds and
USD 0.03194431 equivalent. Total USD 0.38631076. All usage statuses complete;
served identities match. Frozen input hashes verified after runs.

Luna differs on A4, A7, B1 and C2: 16/20 final grades match, including three
forced D zeros. No within-model variance estimate or equivalence conclusion.
Recommendation: retain Sonnet; investigate native structured submission and
independent repeated quality checks before switching. Durable findings are in
docs/reference/resources/ai-tokenomics.md, with index and append-only log.
