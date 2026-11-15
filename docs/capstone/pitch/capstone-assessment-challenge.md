---
title: Capstone Assessment Challenge Against the Complete Guide
description: Judgement-by-judgement challenge of the 55-slide capstone deck, Slide 22 and the B25 and B27 answers against all 20 criteria of the Capstone Assessment Guide, with evidence, gaps, assumptions, section floors and individual floors
ms.date: 2026-11-13
ms.topic: reference
---

## Status And Limits

This is an AI-assisted offline preparation challenge. It is not an assessor score, a floor pass or fail, a panel outcome, an owner or mentor approval or evidence of rehearsal. It supports criterion 5 of issue #435 only (Refs #435) and closes or ticks nothing.

* Scope is the existing delivered 55-slide deck, not a rebuilt or revised one. It extends the descriptor-level read in [current-deck-assessment-2026-11-12](./current-deck-assessment-2026-11-12.md) with the 2026-11-13 [Tokenomics Q&A brief](../tokenomics-qa-brief.md) (Slide 22 stays on the main route; B25 and B27 are the prepared cards). Human review of this document is incomplete.
* No numeric score, band or section sum is given. Live criteria cannot be scored from files, and a number would imply an assessor judgement that does not exist.
* Evidence is content-only: PDF page text (`pdftotext`), speaker script and answers, repository files. No rendering, native PowerPoint, rehearsal, projector, accessibility or audience check was done. The recorded preview in [validation.json](../source/validation.json) has `human_acceptance` false and `rehearsal_performed` false.
* Receipt check: `candidate_sha256` `949e2077...7fca` equals the SHA-256 of the delivered [PPTX](../deck/zava-forward-cowork-v2-draft.pptx). No file hashed by the receipt was edited. The manifest is `slides.json`; no `content.yaml` exists in this checkout.
* Not yet performed: live held-out batch (authorised up to USD 5.00; `zava_forward.agents.heldout_batch` is implemented on main but not yet run live, awaiting owner-authorised live provider execution), billing reconciliation, mentor confirmation, thought-leadership artifact submission and masterclass attendance evidence.

## Reading Key

Read: Supported (evidence stated on the deck or notes), Partial (stated with a recorded gap), Gap (the Excellent descriptor is not evidenced), Not assessable offline (needs live or external evidence). Floor-1 risk: Low (evidence argues against a 1), Unknown (no evidence either way) or Evidenced (a stated gap that a panel could score as 1 or 2). Pages are PDF pages.

## Section A: Technical Excellence

| Criterion | Evidence | Read, gaps and assumptions | Floor-1 risk |
| --- | --- | --- | --- |
| A1 Architecture, modularity, scaling | Pages 18 to 20 (three boundaries, private endpoints, managed identities), page 13 (dashed paths need acceptance), B10 page 38 | Partial. Contracts and boundaries explicit. Failure domains and scaling path are conditional; pages 13 and 19 state declarations are not an accepted live inventory. Load and recovery unmeasured | Low |
| A2 Trade-offs and patterns | Page 9, 17, 32, B20 page 48 (alternatives and rejection reasons, ADR 0002 and 0003) | Supported on named alternatives. Quantified comparison absent: held-out quality, effort and full cost are unmeasured | Low |
| A3 Security, compliance, responsible AI | Pages 18 to 20, 35, 49, B22 page 50 | Partial. Controls and AI risks bounded. The deck does not cite a stated threat model; live role denial and private routing remain gates (page 47). Assumption: repository documents are the threat model, not shown on slides | Low |
| A4 Implementation completeness | Pages 9, 10, 17, 31 | Partial with proactive gap disclosure ("integration proved; human value still unknown"). End-to-end live function Not assessable offline. A broken demo marks A4 only if it reveals a real gap (guide overlap rule) | Unknown |
| A5 Operations, cost | Slide 22, B25, pages 33, 44 | Gap at Excellent. Cost is modelled, not measured: no accepted-outcome denominator, billing reconciliation, live alert test or measured targets. Honestly shown as Unknown, which the guide rewards less than a measured figure. B25 and B27 describe task, period and call-depth bounds as source-coded, not live | Evidenced: a qualitative-only read maps to Satisfactory, and "cost unaddressed" is not the case, but this is the weakest technical criterion |
| A6 AI design and evaluation | Pages 15, 32, 39, 54 (B26), B13 page 41 | Partial. Failure modes and method stated. Model choice is justified by fit, not measured; 6,884 tokens over five runs is an observation, not a quality metric; the 315-trajectory study is planned, not a result. Assumption: the held-out batch will supply the missing metrics | Unknown: "no evaluation" is not true, but a panel may find it anecdotal |
| A7 Agentic autonomy | Pages 9, 17, 42 | Partial. Autonomy is deliberately bounded (proposals plus human approval); the deck discloses this itself. The panel may read it as scripted flow (Satisfactory) | Low |

Section A sensitivity: no criterion is Supported at Excellent; A4 and A6 depend on live evidence. The section floor (21 of 35) is not determinable; it is most exposed if A5 and A6 are read as Satisfactory and A4 is penalised for demo failure.

## Section B: Communication And Executive Presence

| Criterion | Evidence | Read, gaps and assumptions | Floor-1 risk |
| --- | --- | --- | --- |
| B1 Narrative | Page 1 ("Decision today: scope, owners, then a costed plan"), pages 9, 20, 25, 27 | Supported on paper as problem, options, recommendation. Slide 22 sits inside a Tokenomics beat that a tour-style panel could read as feature detail | Low |
| B2 Audience calibration | Page 28 index by audience, answer-first appendix | Partial. Register switching designed, not observed; attendee list unconfirmed | Unknown |
| B3 Demo and hook | Page 26, [runbook](../demo/runbook.md), B18 page 46 (labelled fallback, never simulated live proof) | Not assessable offline. Recovery is documented, not rehearsed. A break is scored on recovery, not on the failure | Unknown |
| B4 Q&A depth | B01 to B27 pages 29 to 55; B25, B27 | Prepared depth supported and separates known from assumed. Composure and depth past the deck Not assessable | Unknown |
| B5 Delivery and time | 24:30 narration plan in a 30-minute slot; 50 s on Slide 22 | Unknown. Plan only; no timing observed. The 50 s Slide 22 script is dense (workings, labels, three controls) and may compress | Unknown, highest live risk |
| B6 Deck and documentation | Visible text pages 22, 33, 53; README, script, answers, receipt | Partial to Gap on cost slides: dense, and `#435` and E-codes appear on audience slides (pages 22, 53). Documentation navigable | Evidenced for density on cost slides, Low for documentation |
| B7 Evidence and data storytelling | Slide 22 workings, pages 6, 11, 37 | Partial. Figures are labelled assumptions, so "numbers the audience can act on" is limited. The guide caps assertion without evidence at 3; labelled assumptions are better than assertion but are not measurements | Low |

Section B sensitivity: B3 to B5 are unobserved and carry most of the exposure; no rehearsal exists, so the floor (21 of 35) is not determinable.

## Section C: Consultative And Stakeholder Skills

| Criterion | Evidence | Read, gaps and assumptions | Floor-1 risk |
| --- | --- | --- | --- |
| C1 Discovery and framing | Pages 2 to 5, 8, 11, 40 | Partial. Stakeholders and constraints named; value is modelled and conditional; cost of inaction not quantified on slides | Low |
| C2 Listening and disagreement | B-card structure only | Not assessable offline. The 30-second answer in the brief restates the three-way distinction, which fits the guide's restate-then-answer behaviour, but delivery is unobserved | Unknown |
| C3 Influence and honesty | Page 27, Slide 22 ("Accepted cost Unknown"), B25 ("no saving, payback established"), brief "Do Not Say" list | Supported on disclosure and a clear recommendation. "I don't know" behaviour unobserved | Low |

Section C sensitivity: the floor (9 of 15) is better evidenced than A or B because honesty is on the page; C2 is the exposure.

## Section D And Submission

| Item | Evidence | Read |
| --- | --- | --- |
| Artifact submission (graduation requirement) | [Coauthored paper package](../thought-leadership/everything-but-the-software/README.md) exists; no submission record is in the repository | Not assessable. A missing artifact is an incomplete, not a low score; do not infer submission |
| D1 Substance and originality | Same package: owner-confirmed OSF base, ongoing exploratory amendments, no outcome result | Not assessable. Strength and limits are both real; results are not reported |
| D2 Craft and publish-readiness | Same package | Not assessable by the deck-side audit |
| D3 Dissemination and reach | None recorded | Not assessable; publication path unknown. Evidenced risk if no path exists |

Section D floor (9 of 15) is not determinable. Slides alone are explicitly insufficient under the guide.

## Slide 22, B25 And B27 Challenge

| Challenge | Evidence | Finding |
| --- | --- | --- |
| Is this a price claim? | Slide 22 shows USD 0.44/home, USD 6,873 and USD 0.88; label "E21: assumed workload; secondary price, 23 Oct 2026, not current verified price" | Labelled and disclosed, but it is a price-derived figure. The F1 tension with the issue's no-price-claim wording is unresolved and is an owner decision. The brief tells the presenter not to say USD 0.44 as the project cost |
| Is the price basis sound? | USD 1.60 per million, GPT-4.1-mini secondary source; demo deployment recorded as gpt-4.1-nano | Unsupported until an official dated price and deployment are recorded (F2) |
| Do slide and cards agree on controls? | Slide 22 lists money budgets and call and depth limits under HELD; B25 and B27 say they are source-coded, not live-proved; brief says S18 notes cite B25 and B27 as slides 52 and 54 and S18 says controls remain proposed | Wording inconsistency (F3). Prefer the B27 wording: source-coded, live activation and reconciliation unproved. Cross-reference numbers on S18 notes are stale |
| Is the unit meaningful? | B25: accepted-outcome TCA equals attributable cost divided by human-accepted proposals above a quality floor; zero or unknown denominator is not measurable | Method supported, measurement absent. Denominator, quality floor and Finance basis remain open (OD-51) |
| Is hidden-call risk answered? | B27: one selected skill, one bounded call, serialized admission; correction of the historical answer | Supported as a source contract (README and `ai_consumption.py` cited). Not a production attestation, and retried or other inference paths still need attribution |
| Is the held-out batch evidence? | Brief: up to USD 5.00 authorised; implemented on main (`zava_forward.agents.heldout_batch`), not yet run live; awaiting owner-authorised live provider execution | No. It is a plan. Do not claim it ran, reconciled or proves saving |
| Does the 50 s slot hold? | Slide 22 script covers workings, double workload, TCA method and controls | Timing risk (B5); the brief's 30-second answer is the safe cut |

## Overlap Rules Applied

* B3 versus A4: a demo failure is scored for recovery under B3; it lowers A4 only if it exposes a real implementation gap. The documented labelled fallback is the planned recovery.
* B4 versus C2: one Q&A exchange is scored twice. B25 and B27 content supports B4; whether the question is heard and restated is C2 and is unobservable here.
* B6 versus D: this deck and the capstone documentation are B6; the thought-leadership artifact is Section D only. Nothing here substitutes for it.

## Floors Applied

| Floor | Status | Basis |
| --- | --- | --- |
| Section A at least 60 percent (21 of 35) | Not determinable | Live and measured evidence absent; A5 and A6 are the exposure |
| Section B at least 60 percent (21 of 35) | Not determinable | B3 to B5 unobserved; B6 density on cost slides |
| Section C at least 60 percent (9 of 15) | Not determinable | C2 unobserved; C3 well supported |
| Section D at least 60 percent (9 of 15) | Not determinable | No artifact review or dissemination evidence |
| No criterion scored 1 | Not determinable | No criterion is evidenced as a 1; A5, A6, B5 and D3 carry the most risk |
| Artifact submitted | Unknown | No submission record found |
| Masterclasses attended | Unknown | No attendance evidence in this scope |

A total never overrides a floor, and floors apply symmetrically: technical depth here cannot offset a weak live performance.

## Gaps And Assumptions

* Assumes the PDF, PPTX and speaker script match the receipt hashes (PPTX hash re-verified; PDF and script as recorded).
* Assumes labelled modelled figures are read as scenarios. A panel may treat them as claims.
* Assumes the brief's 2026-11-13 owner decision is current; no deck change followed it.
* Unmeasured: held-out quality, accepted-outcome cost, billing reconciliation, timing, live demo, audience reading.

## Findings Routed To Owner Or Author

* F1 price-claim tension on Slide 22, page 6 and B25 (owner decision to keep, relabel or remove).
* F2 secondary price and model mismatch.
* F3 CODED/HELD wording versus B27, and stale slide 52 and 54 references on S18 notes.
* F4 internal codes and density on audience slides 22 and 53 (B6).
* F5 50 s Slide 22 timing; rehearse the 30-second answer.
* F6 artifact submission, masterclass and rehearsal evidence are missing.

## Criterion 5 Position

Criterion 5 asks for a revised deck challenged against the complete guide with evidence per judgement, gaps and assumptions, and the floors applied. This document gives that challenge for all 20 criteria and the floors, but it is partial: it covers the existing delivered deck with the 2026-11-13 Slide 22, B25 and B27 position, not a rebuilt deck, and it relies on offline content-only evidence. It does not establish an assessor score, a floor pass, rehearsal or any human approval, and the criterion is not met until the owner reviews it.
