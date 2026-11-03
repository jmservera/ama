---
title: Issue 126 round 1 research
ms.date: 2026-11-03
---

Research disposition: executed. Planning Readiness: Ready.

## Already delivered (merged PRs)

* #261 frozen protocol, benefits register, release decisions, guardrail pause (criteria 2, 3, 4 ticked).
* #409 constructed RAI evidence claims (RAI registers ticked; closure items unmet).
* #422, #439 cost and demo plans (docs only); #433 tokenomics requirements.

## Unmet and why

* Protocol, DPIA, lawful basis approved before capture: needs real named approvers and OD-36; code gate exists, approval is human. Unmet.
* RAI closure items: need fresh assessment, DPO, Legal and owner decisions. Unmet.
* Tokenomics 1: no AI running-cost line in the register. Code slice available.
* Tokenomics 2: no booked-destination value claims. Code slice available.
* Tokenomics 3: release decisions carry no AI economics report. Needs metering (NFR-012, AC-100), not yet built; deferred to a later stacked slice.

## Chosen slice 1

Tokenomics criteria 1 and 2 in `governance.py`: AI running-cost line required for the capture gate; value claims that stay capacity until a different person records one booked destination and the budget owner's confirmation reference. No price, budget or target is set (OD-51 open); a missing price source means Unknown.

Sources: BRD NFR-012, FR-052, AC-100 to AC-103, OD-51; `docs/reference/resources/ai-tokenomics.md`.
