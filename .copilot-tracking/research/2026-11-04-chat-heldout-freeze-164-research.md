<!-- markdownlint-disable-file -->
---
title: Issue 164 held-out freeze gate research
description: What merged PRs delivered and the smallest unmet engineering slice
ms.date: 2026-11-04
---

## Research

* Disposition: executed; Planning Readiness: Ready.
* Delivered by merged PRs: #307, #503 (golden multi-turn, refusals, non-AI comparison), #663 (task registered, disabled), #737 and #728 (grounding and status-claim checks), #837 (rates beside consumption), #923 (approved thresholds bound to versions), #999 (actual calls blocked without finite authorisation).
* Unmet and needing a human, Legal, owner or live step: independently labelled held-out set, actual-model evaluation, human exercises, owner-authorised calls, approved thresholds and reviewer decisions.
* Unmet but partly engineering: the held-out freeze and no-leak rule. `chat_eval.py` records held-out as not produced and has no mechanism to decide whether a supplied set is frozen, independent and unleaked.
* Finding: a paraphrased consent request ("the tenant has agreed") is not refused by the lexical check; this is the known open item and is left unchanged here.
* Slice chosen: a freeze and leak gate that scores a supplied set only when it is pinned, independently labelled and clear of development wording.
