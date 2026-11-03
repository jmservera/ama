---
title: Issue 164 chat outcome rates research
ms.date: 2026-11-03
---

## Prior delivery (merged PRs, not redone)

* #307 chat_eval harness, golden multi-turn scenarios, refusals, non-AI comparison, failure recording.
* #663 chat task registration and explicit enablement gates (disabled, accountable function).
* #728 and #737 claim-level grounding check; critical gap closed; enablement `insufficient`.
* Per-turn, per-scenario and total scripted calls, tokens (Unknown) and cost (Unknown) already reported by `consumption_summary`.

## Evidence for the remaining gap

Tokenomics criterion 1 asks for consumption "beside grounding, abstention and critical-error rates". The report had pass counts by category but no outcome rates and the CLI did not print consumption. Research disposition: executed. Planning Readiness: Ready.

## Unmet and owner-gated (not in this slice)

Approved thresholds and named accountable individual; independent held-out set; actual-model and human exercises; memory-poisoning/injection assurance before enablement on a real model; authorised spend, prices and review effort.
