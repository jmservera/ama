---
title: DPIA scope drift guard research (issue 217)
description: Re-research of issue 217 delivery state and the smallest remaining locally provable slice
ms.date: 2026-11-01
---

## Identity and disposition

Task 217 / regulatory-security-privacy-217-dpia-scope. Research disposition: executed
(direct inspection) and reuses [the 2026-10-16 research](../../2026-10-16/regulatory-security-privacy-217-research.md).
Planning Readiness: Ready.

## Evidence

* PR 353 (synthetic security, privacy, audit) and PR 506 (content-free usage) are merged
  ancestors. `core/regulatory_privacy.py`, `regulatory_usage.py`, `regulatory_chat.py` and their tests exist.
* The 2026-10-31 closure audit keeps criteria 1 to 4, 7 and 8 unmet only on human/platform
  evidence: DPO sign-off, DPO-set periods, live Entra assignment, provider terms.
* `docs/reference/research/chat-memory-dpia.md` lines 177-188 list every record class and the
  usage metadata, but no test ties `regulatory_privacy.CLASSES` to the DPIA draft, so the
  tokenomics criterion (usage records inside the DPIA scope) can silently drift.

## Gap and slice

Add a drift guard test: every retention class and the chat/usage storage appear in the DPIA
draft, and the report keeps usage content-free with no DPO approval. No new runtime code,
no invented retention periods.

## Boundaries

DPIA completion, DPO periods, tenant roles and provider evidence cannot be proven locally.
