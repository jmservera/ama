---
title: Case Study 48
description: Agentic retrofit programme delivery for a UK housing association
ms.date: 2026-09-10
ms.topic: reference
---

## Agentic Retrofit Programme Delivery for a UK Housing Association

| Field | Details | Field | Details |
| --- | --- | --- | --- |
| Industry | Real Estate (Affordable Housing) / Decarbonisation | Headquarters | United Kingdom |
| Operating Region | United Kingdom (North of England) | Regulatory Context | UK Net Zero (EPC C by 2030 - proposed); Social Housing Regulation Act; Awaab's Law; UK GDPR; PAS 2035 retrofit standard |

## Business Challenge

A housing association with 60,000 homes is planning to bring every property to EPC C by 2030 under the proposed standard while responding to damp and mould within statutory timescales under Awaab's Law. Retrofit assessments, grant applications, contractor procurement, resident consent and quality assurance are managed by a small team with spreadsheets, and progress is far behind plan.

## Transformation Objective

Implement programme agents that prioritise homes from stock and sensor data, run PAS 2035 assessments with surveyor input, prepare grant bids, coordinate contractor agents and resident consent, and verify retrofit quality, with the asset director approving investment and residents controlling consent.

## Agentic Architecture Brief

| Agent | Owns end-to-end | Autonomy level |
| --- | --- | --- |
| Stock Prioritisation Agent | Ranks homes by energy, health risk and grant eligibility | L2 - recommend |
| Assessment Agent | Drafts PAS 2035 assessments from surveys and data | L3 - drafts, retrofit coordinator approves |
| Grant & Funding Agent | Prepares funding applications and reporting | L3 - drafts, finance submits |
| Contractor & Resident Coordination Agent | Schedules works, secures consent, communicates | L3 - acts within resident preferences |
| Quality Verification Agent | Checks evidence and post-retrofit sensor data | L4 - autonomous flags |

**Orchestration:** Programme supervisor across schemes; contractor agents via scheduling APIs; resident channel with consent management; damp-and-mould alerts routed to a dedicated response loop.

**Governance, safety and evaluation:** Resident consent and vulnerability safeguards; Awaab's Law timescales as hard constraints; grant compliance; contractor quality accountability; regulator reporting.

## Expected Outcomes

Retrofit delivery rate doubled, grant capture increased, damp-and-mould responses within statutory timescales, and lower resident energy bills.

## Why Now (2026-2028)

Awaab's Law Phase 1 came into force on 27 October 2025 (emergency and damp/mould), Phase 2 applies from 30 November 2026 and Phase 3 in 2027; EPC C by 2030 remains a consultation proposal but grant funding rounds are open now.

## Business Case

*Missing EPC C deadlines risks regulatory downgrade and lost borrowing capacity; retrofit speed is a financial survival issue.*

Value at stake: missing EPC C deadlines risks a regulatory downgrade that reduces borrowing capacity by hundreds of millions; doubling retrofit delivery captures GBP 40 million of available grants and cuts resident energy bills. Cost of inaction: Awaab's Law timescales carry enforcement, and the programme is far behind plan with no capacity to catch up manually. Executive sponsor: Executive Director of Assets, with the Chief Executive. Success measures: homes retrofitted per year, grant capture, damp-and-mould response times, and resident energy cost.
