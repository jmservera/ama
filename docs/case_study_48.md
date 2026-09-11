---
title: Case Study 48
description: Agentic retrofit programme delivery for a UK housing association
ms.date: 2026-09-11
ms.topic: reference
---

## Proper Warm at Proper North Homes

| Field | Details | Field | Details |
| --- | --- | --- | --- |
| Industry | Real Estate (Affordable Housing) / Decarbonisation | Headquarters | United Kingdom |
| Operating Region | United Kingdom (North of England) | Regulatory Context | UK Net Zero (EPC C by 2030 - proposed); Social Housing Regulation Act; Awaab's Law; UK GDPR; PAS 2035 retrofit standard |
| Fictional Association | Proper North Homes | Programme | Proper Warm |

The working presentation line is "Ready, steady, retrofit." The name is not
cleared for legal, trademark, domain or resident-facing use. It must not be used
for hazard, complaint, safeguarding or consent communications.

## Business Challenge

Proper North Homes is a fictional housing association with 60,000 homes. It
is planning to bring every property toward EPC C by 2030 under the proposed
standard while responding to damp and mould within statutory timescales under
Awaab's Law. Retrofit assessments, grant applications, contractor procurement,
resident consent and quality assurance are managed by a small team with
spreadsheets, and progress is far behind plan.

## Provisional Sector Baseline

Research completed on 11 September 2026 provides an initial planning benchmark,
not company facts:

| Measure | Provisional benchmark | Evidence status |
| --- | --- | --- |
| Homes at EPC C or above | 74%, or 44,400 homes | England social-rented estimate |
| Homes below EPC C | 26%, or 15,600 homes | Derived planning benchmark |
| Four-year accepted-completion trajectory | 3,900 homes per year | Derived scenario |
| Surveyor-assessed damp | 6% HA benchmark, or 3,600 homes | Stock-prevalence estimate |
| Resident-reported damp, mould or condensation | 39% HA benchmark, or 23,400 households | Lived-experience estimate |
| Repairs satisfaction | 73.6% | RSH landlord median |
| Complaint-handling satisfaction | 35.5% | RSH landlord median |
| Stage-one complaints | 54.5 per 1,000 homes, or about 3,270 per year | RSH landlord median translated to stock |
| Ordinary WH:SHF Wave 3 grant cap | GBP 7,500 per home with normally at least 50% co-funding | Scheme limit, not an award |
| First-appointment no-access | 10% central; 5% to 15% sensitivity | Planning assumption only |
| Discretionary retrofit refusal or withdrawal | 5% to 10% | Planning assumption only |

The initial below-C scenario implies 3,900 accepted completions per year. A
GBP 20,000 fully loaded planning assumption gives a GBP 312 million gross
programme, with a maximum GBP 117 million ordinary grant ceiling before
eligibility and award constraints. The stated GBP 40 million remains an
unsecured opportunity and would support at most about 5,333 homes at the
GBP 7,500 cap.

Full sources, limitations and alternative sensitivities are recorded in
[UK Social Housing Baseline Research](../support/uk-social-housing-baseline-research.md).

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
