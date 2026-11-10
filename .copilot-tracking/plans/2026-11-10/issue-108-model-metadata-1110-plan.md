---
title: Issue 108 regional model metadata observation plan
description: Plan for one bounded read-only Azure metadata observation and a concise dated synthesis update
ms.date: 2026-11-10
---

## Task

`issue-108-model-metadata-1110`, base `main` `4d8443d442fa8f1c47fa0749e5b8ba7c2bdd23ff`. Research: [research](../../research/2026-11-10/issue-108-model-metadata-1110-research.md).

## Objective

Record dated, minimized read-only metadata for the demo app's configured model endpoint and deployment, the matching account and deployment in `ama`, and the regional quota limit and unit for that one model and SKU. Partially evidences the unticked #108 criterion only; it does not tick it.

## Phases

1. Run up to four projected read-only `az` queries (budget eight in total), saving raw minimal output under the external root `evidence-108-model-metadata-1110`, with stop rules from the research.
2. Sanitize and extend the existing [AI Tokenomics](../../../docs/reference/resources/ai-tokenomics.md) configured-demo-model section with one dated subsection; add an index sentence and an append-only log entry.
3. Validate provenance, scope, links, Markdown and the Git diff, then Review once.

## Success criteria

* Each query's exit, timestamp and redacted output locator is recorded; failures are preserved, not retried beyond one transient read failure.
* Published text names only the project model, region, version, SKU, capacity and quota limit and unit; no subscription identifier, identity, other resource, secret, full environment or shared aggregate usage.
* Unknown or blocked fields are marked unknown or blocked, never zero.
* If the first query blocks (absent, secret reference or denied), the lane stops and a scoped blocked record is written without inventing an acceptance criterion.
* #108, RAI and Tokenomics criteria stay unticked and open.

## Validation tier

Focused documentation tier: provenance and scope review, relative links, Markdown and Git diff only. No runtime tests, providers, SQL, browser or gate. Hosted CI is unobserved and stays so.

## Human and authority limits

Existing project-scoped ARM read metadata only. No new cloud write, paid inference, activation, quota or budget authority. No push, PR, issue or board write; the coordinator performs an independent exact-head check before any publication.

## Review plan

One Review after implementation with its outcome and routing recorded separately; no second Review in this task.
