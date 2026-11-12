---
title: Current Capstone Deck Assessment and Tokenomics Statement Audit
description: Offline, content-only challenge of the delivered 55-slide capstone deck and notes against the complete assessment guide, with a Tokenomics claim, source and label register
ms.date: 2026-11-12
ms.topic: reference
---

## Status And Limits

This is an offline preparation assessment by an AI-assisted author. It is not an assessor score, a floor pass, a panel outcome, an owner or mentor approval, or evidence of any rehearsal. It is initial, partial progress on issue #435 criteria 5 and 6 only (Refs #435). It does not satisfy "rebuilt deck" or owner conjunction wording and closes nothing.

* The issue text describing a 24-slide deck, a 795-second route and slide 16 is stale. The delivered deck is 55 slides (main route pages 1-27, question index page 28, answers B01-B27 on pages 29-55), with a 24:30 narration plan inside a 30-minute slot and a separate 10-minute demo. Both are plans, not observed timings.
* Evidence is content-only: slide text and speaker notes read from the PPTX by standard-library XML parsing, and PDF page 22 read with `pdftotext`. No rendering, native PowerPoint, projector, accessibility or audience check was performed. Visual statements rely on the recorded Linux preview in [validation.json](../source/validation.json) (LibreOffice 24.2.7.2, `human_acceptance` false, native validation not run, `rehearsal_performed` false), whose page images sit outside the repository.
* Prior non-equivalent coverage, preserved unchanged: the criterion-level summaries in [review-2026-11-08](../source/review-2026-11-08.md) and [review-2026-11-08-cxo](../source/review-2026-11-08-cxo.md), the [placement draft](./tokenomics-placement-draft.md) (written for 54 slides; S18 is now page 22 and B25 page 53), and the adverse 2026-11-03 finding on the S18 modelled figure.

## Artifact Identity At Main cd81888e4

| Artifact | Git blob | Agreement |
| --- | --- | --- |
| [Delivered PPTX](../deck/zava-forward-cowork-v2-draft.pptx) | `3da73fd2dd480fbbde48326174a834a27e8e87e2` (SHA-256 `949e2077...7fca`) | Equals `validation.json` `candidate_sha256` and the hash in the generated script |
| [Delivered PDF](../deck/zava-forward-cowork-v2-draft.pdf) | `5bd67ab6b145fd50beca57060b0e3b9ee192c840` | Equals the recorded preview PDF hash; 55 pages |
| [Source manifest](../source/slides.json) | `20ac61d5908ae6c74758141d28cebf7b3c4a947f` | Equals `manifest_sha256` |
| Native baseline `baseline.pptx` | `a2a9c528fd77ee5b7d18d8bea169f37428ee1dd4` | Equals `baseline_sha256` |
| [Generated script](./speaker-script.md) | `be548021c57900bbb3c7058ee4617f439c1022cb` | Equals recorded hash; matches delivered notes for 54 of 55 pages (page 28 index not generated) |
| [Generated answers](./questions-and-answers.md) | `09dca60c49ec67d2f7891710eaeb55fdb040ff14` | Equals recorded hash |

Source and delivered deck agree through the receipt hashes. Raw manifest `notes` fields are not the delivered text: the builder (`tools/capstone/Invoke-Capstone.ps1`, hash equals `builder_sha256`) adds page-reference rewrites, owner-approved cost status edits and `CURRENT ROUTE TIMING` lines, and revised notes exist for some pages. Source-to-deck differences on pages 6, 11, 22, 33, 37 and 53 are documented builder deltas, not mismatches. Page 28 notes still say "All 54 page numbers" (stale count) and original `TIMING` lines on the 23:45 clock are retained beside the operative 24:30 lines.

## How To Read The Judgement Table

Reads are descriptor-level and offline: Supported (deck and notes state it with evidence), Partial (stated, with a recorded gap), Gap, or Not assessable offline. They are not points and do not imply a band.

## Section A: Technical Excellence

| Criterion | Deck and notes evidence | Offline read, gaps and assumptions |
| --- | --- | --- |
| A1 Architecture, modularity, scaling | Pages 18-20 (architecture, private endpoints, managed identities, three boundaries; notes: "No new deployment or spending is authorized"), page 13 (dashed paths need acceptance), page 38 B10 | Partial. Contracts and boundaries explicit; scaling and failure domains are stated as gated or conditional, and the page 13 and 19 notes say declarations are not an accepted live inventory. Load, scale and recovery are unmeasured |
| A2 Trade-offs and patterns | Page 9 (rules-only comparator versus bounded AI versus wider automation, with ADR 0002 and 0003), page 17 (constrained selection "not a proven saving"), page 32 (model fit "not a proven cost or latency advantage"), page 48 B20 (SQL versus Fabric) | Supported for named alternatives and rejection reasons. Quantified comparison is absent by design (held-out quality, effort and complete cost unmeasured) |
| A3 Security, compliance, responsible AI | Pages 18-20 (identity, role denial, three boundaries), page 35, 49 (grounding and injection answers), page 50 B22 (UK-only inference is a deployment choice to verify; no contractual assurance) | Partial. Controls and AI risks named and bounded. No stated threat model document is cited on the slides, live role denial and approved private routing are listed as remaining gates (page 47) |
| A4 Implementation completeness | Page 9 (five L2 evidence proposals; fuller scope remains), page 17, page 31, page 10 ("integration proved; human value still unknown") | Partial with proactive disclosure of gaps (L3/L4 scope, live acceptance). Whether the live demo works end to end is Not assessable offline |
| A5 Operations and cost | Pages 22, 33, 44, 53-55 (usage metering, finite call and token allowance, Azure budget alerts, budget alerts warn and hard stops are designed or coded), page 6 and 22 forecast, page 33 USD 242.36 partial accrual | Gap at the Excellent descriptor: cost per unit of business value is modelled (assumed), not measured; no accepted-outcome denominator, billing reconciliation or live alert test. Cost and operations are honestly Unknown rather than hidden. Observability targets measured: not evidenced in the deck |
| A6 AI design and evaluation | Pages 15, 32 (model fit), 39 (6,884 tokens/five runs is a historical observation, not a quality result), 54 (cheaper tokens do not imply cheaper accepted outcome), page 41 B13 (planned study, 315 trajectories, unregistered amendment) | Partial. Evaluation design and failure modes stated; no held-out quality metrics are reported, and a planned study is not a result |
| A7 Agentic autonomy | Page 9 (L2-L4 levels), page 17, page 42 | Partial. Autonomy is deliberately bounded (proposals, human approval); the deck itself discloses limited autonomy, which may read as Satisfactory against the descriptor |

## Section B: Communication And Executive Presence

Section B is scored live. Only the prepared materials can be read here.

| Criterion | Deck and notes evidence | Offline read, gaps and assumptions |
| --- | --- | --- |
| B1 Narrative | Page 1 "Decision today: scope, owners, then a costed plan", acts on pages 9, 20, 25, 27 ("Agree the validation gate, name the owners, review a costed plan") | Supported as an argument arc on paper; delivery is Not assessable |
| B2 Audience calibration | Page 28 question index by audience (CEO/CFO, CIO/CTO, DPO/CISO), per-page "SAY" and appendix "answer first" structure | Partial. Register switching is designed through the appendix; actual room reading is unobserved. The attendee list is unconfirmed |
| B3 Demo and hook | Page 26 and [demo runbook](../demo/runbook.md) (not re-read here); page 46 B18 (preauthorised, reversible scope, labelled fallback, never simulated live proof) | Not assessable offline. Recovery plan is documented; no demo was run |
| B4 Q&A depth | Pages 29-55 B01-B27 with answer-first and limit structure; separates known from assumed (for example pages 22, 39, 53) | Prepared depth supported; composure and depth past the deck Not assessable |
| B5 Delivery craft and time | 24:30 narration in a 30-minute slot, 5:30 reserve; [speaker script](./speaker-script.md) timing lines | Unknown. Plan only; rehearsal timing is unavailable and not simulated |
| B6 Deck and documentation | Slides carry source lines and S/B codes; several slides are dense (pages 22, 33, 53 carry 16 to 24 cost-term hits on visible text); internal tracker and E-codes appear on audience slides (pages 22, 53 `#435`, E21/E19/E05) | Partial to Gap on standalone readability for the cost slides; documentation navigable (README, script, answers, validation receipt). Visual density was not rendered here |
| B7 Evidence and data storytelling | Page 6 and 22 cost build, page 11 and 37 GBP what-if (labelled fictional exercise arithmetic), page 25 | Partial. Numbers are labelled and conditional; the figures are assumed scenarios, so "numbers the audience can act on" is limited |

## Section C: Consultative And Stakeholder Skills

| Criterion | Deck and notes evidence | Offline read, gaps and assumptions |
| --- | --- | --- |
| C1 Discovery and framing | Pages 2-4, 8 and 40 (stakeholders, constraints, brief versus built); page 5 and 11 (value at stake, GBP separate from USD technology) | Partial. Value is stated as modelled and conditional; cost of inaction is not quantified on the slides |
| C2 Listening and disagreement | Appendix structure anticipates challenges; live behaviour unobservable | Not assessable offline |
| C3 Influence and honesty | Recommendation page 27; "Accepted cost Unknown" (page 22), "no saving, payback or full-project price established" (page 53), risk disclosed unprompted on pages 17, 22, 39 | Supported on disclosure and a clear next-step recommendation; "I don't know" behaviour is unobserved |

## Section D And Floors

* D1-D3: Not assessed. The thought-leadership artifact is a separate deliverable outside the deck (the guide scores it only in Section D and B6 excludes it). Submission, review, dissemination and any publication path are unknown here.
* Floors (A 21 of 35, B 21 of 35, C 9 of 15, D 9 of 15, no criterion at 1, artifact submitted, masterclass attendance): not determinable. No numeric score exists, so no floor is claimed passed or failed. Floor risk areas to check live: A5 and A6 (unmeasured cost and evaluation), B3 to B5 and C2 (unobserved).
* Overlap rules: the demo (B3 versus A4) and Q&A (B4 versus C2) overlaps are unscorable offline; B6 covers the deck and capstone documentation only.

## Tokenomics Statement Register

Inventory method: a case-insensitive scan for token, USD, price, cost, saving, payback, TCA, budget, billing, spend and denominator terms over visible text and notes of all 55 pages, reconciled below. Pages with hits that are not Tokenomics are listed after the register. Evidence labels are those the deck prints; "unlabelled" means none is printed on that statement.

| ID | Page and field | Statement | Printed label and source | Class | Finding |
| --- | --- | --- | --- | --- | --- |
| T1 | 6 visible and notes | USD 6,873 whole-cohort inference scenario | E21 assumed workload plus secondary price (23 Oct 2026) | Forecast or scenario | Modelled; not a real cost. Notes say no percentage without Finance FX |
| T2 | 22 visible | USD 0.44/home = USD 6,873 / 15,600 homes; 20 tasks x 13,768 tokens x USD 1.60/million; doubled USD 0.88 | E21 "not current verified price" | Forecast or scenario from an assumed price | Price-derived per-home figure on the main route (see F1) |
| T3 | 22 visible | Accepted cost Unknown; no accepted-outcome unit cost established | E19 usage only; E05 controls coded, #435 not accepted | Missing denominator and billing | Correctly states unknown |
| T4 | 22 visible | CODED finite calls, tokens, expiry, usage capture, budget alerts; HELD money budgets per task and period, call and depth limits | E05 | Source-coded control, not live acceptance | Differs from page 55 wording (F3) |
| T5 | 22 and 53 notes | TCA = hosting, review, correction, assurance and support divided by human-accepted work above a quality floor | Working method with Finance; no external standard cited on the slide | Method | Not measured; zero or unknown denominator means not measurable |
| T6 | 53 visible | USD 0.440576/home inference; USD 0.881152 doubled; accepted-outcome TCA unknown; no saving, payback or full-project price | E21 | Scenario with explicit negations | Same figure and gap as T2 |
| T7 | 10, 22, 39, 53 | 6,884 tokens over five runs (mean 1,376.8), SQL restart, integration proved, human value unknown | E19 in footers (page 10 line lists PR sources, no E19 on that statement) | Observation | Historical, no acceptance, not a price or denominator. Observed model gpt-4.1-mini; configured demo deployment recorded as gpt-4.1-nano |
| T8 | 6, 22, 53 | 20 tasks per home, 10x task size, 15,600 homes | E21 | Assumption | Not measured |
| T9 | 33 visible | USD 700 owner-set October all-in ceiling (authority expired 2026-10-25T16:02Z), USD 242.36 partial accrued, USD 535.33 pre-change forecast, USD 450/month historical, "P + USD 6,872.9856" with P unpriced | E11, E05, E21 | Owner-set limit, partial real accrual, forecasts and historical figure | Mixed classes on one slide; the ceiling is an expired authority, not a spend decision; no post-change saving measured |
| T10 | 45 notes | Same USD 700, USD 535.33 and USD 450/month guardrails | Source lines for E11 and cost options | Same as T9 | Notes state not a production price or current bill |
| T11 | 35, 39, 49 | 6,884 tokens is not a price, quality result or denominator; token allowances are not currency caps; no accepted-outcome saving claim | E19 | Negation of a claim | Supported |
| T12 | 44 | Finite allowance; budget alerts warn, hard stops designed | E06, E07, E13 (page 44 visible source line and notes; no E05 is cited there) | Designed control, not live | Wording differs from pages 22 and 55 (F3) |
| T13 | 54 | Cache or cheapest model; cheaper tokens do not imply cheaper accepted outcome | E19, E04, E09 (page 54 source line; none in notes) | Method reasoning | Not a measured claim |
| T14 | 55 | Bounded one-call chat; money, call and depth bounds source-coded; live activation, billing reconciliation and per-journey cost unproved | No E-code on page 55; source line names the API bounded-skills and core consumption guides (8 Nov 2026) | Source-coded control, not live | Supported as a source-contract statement; not an E05 requirement citation |
| T15 | 36, 48, 17, 32, 25 | "No saving established", "not a proven saving", full-cost comparison to be made | Various | Negation or method | No saving, payback or price figure asserted |
| T16 | 1, 18-20, 27 | No spending authority is granted; no deployment or spending authorised | none required | Boundary statement | Supported |

Non-Tokenomics cost-term hits: GBP works benchmark, conditional grant and fictional what-if figures (pages 5, 11, 37; E02, E21 historical benchmark, not a quote), Fabric F2 USD 262.80/month (page 48, a public view with no selected region and not a quote or saving), and "full cost" prose on pages 24, 25, 32 and 43. Page 5 notes explicitly state no AI saving, TCO or accepted-outcome unit cost is established.

Provenance checks against the sources: E21 is a recovered 2026-10-23 planning arithmetic using unverified secondary-source pricing ([ai-cost-evidence](../history/cowork-main-presentation/evidence/ai-cost-evidence.md)). The 2026-10-31 official price retrieval in [AI Tokenomics](../../reference/resources/ai-tokenomics.md) recorded numerical rates unavailable and cost Unknown, and its pitch insert says fixture prices must not appear as financial evidence. The "mentor meaning" of Tokenomics remains owner-reported and unconfirmed.

## Findings Routed To Later Owner Or Author Decisions

None is applied here; no deck, source or placement change was made.

* F1 Criterion 6 tension (unresolved, owner decision): the issue asks for no price claim, and the [Tokenomics pitch brief](../history/tokenomics-pitch-brief.md) lists any price or cost-per-home figure under claims to keep out. Pages 6, 22 and 53 show a labelled, price-derived scenario (USD 0.44/home) from an unverified secondary rate. It is disclosed as an assumption, so it is not a hidden claim, but it is a price figure. Whether to keep, relabel or remove it is the owner's choice.
* F2 Price and model basis: USD 1.60/million is a secondary-source GPT-4.1 mini output rate that predates the official retrieval, while the configured demo deployment is recorded as gpt-4.1-nano. The comparison basis is unsupported until a dated official price and deployment are recorded.
* F3 Control wording consistency: page 22 visible lists money budgets and call and depth limits as HELD, page 44 says hard stops are designed, and page 55 notes say they are source-coded with live activation unproved. These are consistent only if "source-coded, not live" is stated everywhere.
* F4 Audience-slide internal codes: `#435` and E-codes appear on pages 22 and 53, and dense cost slides reduce standalone reading (B6).
* F5 Stale page-count text on page 28 notes ("54 page numbers") and the placement draft's old mappings.
* F6 Unperformed evidence: rehearsal, timings, participants, native PowerPoint check, mentor confirmation, spend and batch authority, placement decision and the thought-leadership artifact status.

## Criterion Position For Issue 435

* Criterion 5 (complete judgement-by-judgement challenge): a complete current-deck, offline, content-only challenge exists here; it is partial because it covers the existing delivered deck, not a rebuilt or revised one, and no live or human evidence exists.
* Criterion 6 (every statement audited, sourced, labelled, no price claim): the statement audit exists here; the "no price claim" condition is not met by the current deck (F1).
* Criteria 1 to 4 (placement and rebuild, mentor confirmation, rehearsal and timing, batch and spend decision) are untouched and unmet. No issue tick or closure is recorded; human review of this document is incomplete.
