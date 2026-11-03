# Research: issue 124 Phase 0 retrofit-flow discovery (r1)

Research disposition: executed (delta). Planning Readiness: Ready for slice 1.

## Prior delivery check

* No merged PR delivers #124. PR searches for "Refs #124" returned only unrelated hits (#292, #403, #407, #683, #723, #816 mention 124 as a count or number).
* `git log --all --grep '#124'` and a source search for "discovery owner" found only `docs/brds/retrofit-flow-discovery-brief.md`.
* `governance.py` (#126) holds a BG-011 benefits register and a protocol `event_dictionary` text field, but no owner nomination, validated dictionary or constraint register.

## Source evidence

* Brief, Discovery Outcomes 1 and 4, Minimum Evidence Specification, Readiness Before Writing the Agent (nominated owner, agreed endpoint, validated dictionary).
* Brief: accepted handover is the endpoint; candidate selection, release, appointment, installation, practical completion, invoice and documentary completion stay separate events.
* Brief: no ranked constraint becomes a company finding until the operational owner validates data and interpretation; unknown or disputed causes stay visible.

## Acceptance criteria assessment

| Criterion | Needs | Slice 1 |
| --- | --- | --- |
| Owner nominated, endpoint agreed | Sponsor decision | Record shape and status only; unmet |
| Dictionary validated | Operational owners | Gap check and owner-role validation; unmet |
| Constraint register with supporting and contradicting evidence | Data plus analyst | Rule layer; no real evidence; unmet |
| Not company findings until owners validate | Rule | Enforced in code; met as a rule |

## Constraints

* Dependency: sponsor decision and the twelve-month population are not available; no company data is read.
* Manual path: the module is deterministic and has no AI. AI-unavailable behaviour is the same.
* Validation tier: focused (no security, infrastructure, SQL or deployment change).
