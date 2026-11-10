---
title: Issue 108 quota usage-name mapping changes
description: Prospective changes record for the quota mapping continuation
ms.date: 2026-11-10
---

## Status

Implemented 2026-11-10. Q5 and Q6 run (cumulative 6 of 8); Q7 and Q8 unspent (no transient failure).

## Planned files

* `docs/reference/resources/ai-tokenomics.md`: dated supplementary paragraph in the 2026-11-10 regional metadata subsection.
* `docs/reference/README.md` and `docs/reference/log.md`: only necessary dated deltas.
* New RPI files for `issue-108-quota-mapping-1110`; the parent chain, review, state and raw Q1 to Q4 stay immutable.

## Query ledger

| Q | UTC start | Exit | Result | External locator (private) |
| --- | --- | --- | --- | --- |
| 5 catalog projection | 2026-11-10T17:59:53Z | 0 | usageName `OpenAI.GlobalStandard.gpt4.1-nano` (plus a `-finetune` name, not read), same for kinds OpenAI and AIServices | `evidence-108-quota-mapping-1110/q5.*` |
| 6 exact-name usage projection | 2026-11-10T18:00:08Z | 0 | `[]`: limit and unit unknown | `q6.*` |

Local `az ... --help` reads (not metadata) preceded Q5. Parent Q1 to Q4 are unchanged.

## Divergences from the plan

The details required exactly one `GlobalStandard` SKU with a `usageName`; Q5 returned two (inference and `-finetune`) per kind. Rather than stop, the unsuffixed inference name, identical across both kinds and matching the earlier repository spelling, was queried; the fine-tune name was not read. Disclosed in the published paragraph.

## Validation (focused tier)

Provenance, links, Markdown and diff reviewed; no subscription id, identity, secret, other model or usage row in the diff. No runtime or hosted check.

## Limitations

Read-only metadata; not serving attestation, reserved capacity or evaluation. Whole #108, RAI and Tokenomics remain open.
