---
title: Startup probe plan for issue 691
description: Plan for probes and client cold-start tolerance
ms.date: 2026-11-02
---

## Phases

* [x] Phase 1: Bicep probes for api (8088) and resident-demo (8089, Host header).
* [x] Phase 2: Client bounded read retry, photo retry, script retry budget of 3.
* [x] Phase 3: Tests (Bicep probe contract, Node VM retry test) and `az bicep build/lint`.
* [x] Phase 4: Focused gate, commit, PR with `Refs #691`; no deploy, no merge.

## Critique (one pass, executed)

Verdict: proceed. Findings applied directly: do not retry JSON application errors or POSTs (mutations stay non-retried); keep min replicas unchanged; resident probe needs Host header.
