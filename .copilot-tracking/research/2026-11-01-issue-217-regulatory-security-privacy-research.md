---
title: Issue 217 research - regulatory assistant security, privacy, audit
ms.date: 2026-11-01
---

Research disposition: executed (repository evidence only). Planning Readiness: Ready.

## Evidence

* Issue 217 comments: two of eight criteria ticked (audit logging, injection and cross-role tests); closure audit of 2026-10-31 says the rest are DPO, Legal, tenant or live-data gates that code cannot tick.
* `src/core/src/zava_forward/core/regulatory_privacy.py`: read-only retention report; chat simulated with SYNTH- reference; other record classes always `unknown`.
* `src/core/src/zava_forward/core/chat_privacy.py` `ChatPrivacy.decision`: reference-based gate for chat storage only (CHAT_DPIA_REF and others).
* `src/core/src/zava_forward/core/regulatory_usage.py`: content-free usage records (tokenomics criterion shape).
* `src/api/README.md` ~2825-2850 and `src/core/README.md` ~3841-3853: unmet boundaries recorded.

## Gap

No single, testable gate covers the whole regulatory scope (law store, rule cards, checks, alerts, chat, usage) and refuses live-data readiness until the human evidence references exist. Reviewers also lack one machine-readable per-criterion matrix separating automated proof from human gates.

## Slice

Add `regulatory_privacy.readiness_report(env)`: per-criterion status (`automated-pass`, `partial`, `human-gate-unmet`), reference-only live-data gate (DPIA, retention, Entra roles, Art 22A-22C references; SYNTH- references never permit live data), no content, no approval claim.

## Constraints

* Code cannot attest DPO or Legal approval; the report always states `dpo_reviewed` false.
* No secrets; references are identifiers only. Pip only; no mvp/ or prototype/ changes.

## Follow-ups

1. Wire the report to an API route for the staff demo (small).
2. Live Entra role assignment evidence (tenant action).
