---
title: Zava Forward v2 - build handoff
description: Cowork-generated v2 build report retained as supplied, with repository metadata added
ms.date: 2026-10-23
---

## Zava Forward v2 build handoff

Deck: "Zava Forward - More homes ready with control intact.pptx" (OneDrive, edited in place). Version 1 (the cautious, evidence-first route) stays in the file's version history.
Status: draft for the owner's review. Zava North Homes is a fictional case organisation (AMA Case Study 48).

## Deliverables

* The deck (OneDrive, edited in place): "Zava Forward - More homes ready with control intact.pptx". It has 54 slides: the 26-page spoken story, the question index on slide 27, and appendix answers B01-B27 on slides 28-54. Speaker notes are on every slide.
* Zava Forward v2 - More homes ready with control intact.pdf: a static route of all 54 pages. It has bookmarks by section, 115 internal links that mirror the on-slide navigation, a selectable text layer and the en-GB language tag.
* Zava Forward v2 - contact sheet.png: all 54 slides at a glance.
* Zava Forward v2 - slide previews.zip: 54 JPG previews at 1600 x 900.
* uk-social-housing-retrofit-damp-stats-report.md: the statistics research behind the forecast, with every source and its date.
* The version 1 files (PDF, contact sheet, previews and the first handoff) are still in the folder for reference. They describe version 1, not the current deck.

## What changed from version 1

* **Story:** a product-manager story in five acts. The challenge, the discovery work, the product, why it can be trusted, and the plan. It replaces the 18-slide evidence route. 23 story slides on 26 pages (two build sequences for Morph), about 24 minutes.
* **Numbers:** a bold, sourced forecast for a 60,000-home landlord. Every figure is a national official statistic applied to 60,000 homes, or a fact from the AMA repository. Forecasts are labelled FORECAST and pilot numbers TARGET.
* **Architecture:** a three-step deep architecture. It shows security boundaries (identity, private network, public edge), Microsoft 365 touchpoints and the Excel/CSV import and export path, each with its delivery status.
* **Look:** full-bleed scenes, a consistent icon set, shape-built charts, and build copies for Morph animation.
* **Tone:** positive status words (next milestone, designed, measured in the pilot) on the main route and in the appendix. The 27 appendix answers are kept, renumbered (B01-B27 = slides 28-54) and re-toned.

## The forecast and how it was computed

Method: national rates from official statistics applied to 60,000 homes. Deadline arithmetic runs from 1 Nov 2026 to 1 Apr 2030 (41 months). All numbers come from forecast.py, not by hand.

| Figure | Value | Basis | Source |
| --- | --- | --- | --- |
| Homes below EPC C | 15,600 (26%) | EHS 2024-25 social stock share below band C; D 14,400 · E 1,200 · F/G 300 | EHS 2024-25 ch. 2 (MHCLG, 29 Jan 2026) |
| Required pace | 4,566 a year · 380 a month · 88 a week | 15,600 / 41 months | Government response: EPC C by 1 Apr 2030 (MHCLG/DESNZ, 1 Apr 2026) |
| Ramp (cumulative) | 5,327 end 2027 · 9,893 end 2028 · 14,459 end 2029 · 15,600 on 1 Apr 2030 | Linear at the required pace | forecast.py |
| Capital works | £95m (HA average £6,082 a home); range £88m-£107m | Average cost to reach C | SRS MEES final impact assessment (1 Apr 2026) |
| Grant potential | up to £47m | 50% co-funding of the HA average; per-home cap £7,500 | WH:SHF wave 3 guidance (DESNZ, 2026) |
| Homes with damp | 3,600 (6% HA); 3,000 serious mould (5%) | EHS housing quality | EHS 2024-25 ch. 1 |
| Households likely to report damp, condensation or mould | 22,800 (38%) | Self-reported problems, HA tenants | EHS 2024-25 perceptions report (9 Jul 2026) |
| Stage-one complaints a year | 3,210 (53.5 per 1,000 homes) | Sector median rate | RSH Tenant Satisfaction Measures 2024/25 |
| AI inference, whole programme | ≈ $6,873 | 20 AI tasks a home, each 10x the observed 1,376.8-token run, all tokens at the GPT-4.1 mini output list price ($1.60 per 1M) | Repository operator exercise; price from third-party trackers of Azure retail prices |

Reconciliation note: the repository BRD/ADD use 39% (23,400 households) and about 3,270 complaints from slightly different tables. The deck uses the verified 38% and 53.5 per 1,000.

## Story map (spoken route, about 24 minutes)

| Slide(s) | ID | Title | Answers in appendix |
| --- | --- | --- | --- |
| 1 | S01 | More homes ready. Faster. With control intact. | - |
| 2 | S02 | 15,600 homes to lift by 2030. Thousands more to keep safe. | - |
| 3 | S03 | Three clocks are already running. | B24 (slide 51) |
| 4 | S04 | Homes don't stall on ambition. They stall between teams. | B01 (slide 28) |
| 5-6 (builds) | S05 | Forecast: every Zava home at EPC C by April 2030. | B08 (slide 35) |
| 7 | S06 | Six weeks of product work sit under these slides. | - |
| 8 | S07 | We designed for the people who move a home forward. | B12 (slide 39) |
| 9 | S08 | We challenged the brief to make it shippable. | B03 (slide 30), B14 (slide 41) |
| 10 | S09 | Every prototype taught us something we kept. | - |
| 11 | S10 | We stress-tested the economics before we wrote the product. | B09 (slide 36) |
| 12 | S11 | Meet the Workbench: every home, one owner, one next step. | B02 (slide 29) |
| 13 | S12 | One home, end to end: the exception has an owner the moment it appears. | B06 (slide 33), B23 (slide 50) |
| 14 | S13 | 189 backlog items, 16 epics, one coherent product. | - |
| 15 | S14 | Start Monday with the spreadsheets you already run. | B20 (slide 47) |
| 16 | S15 | AI where it earns its place: five assistants, one workbench, people decide. | B04 (slide 31), B11 (slide 38) |
| 17-19 (builds) | S16 | Secure by design: every home record sits inside three boundaries. | B10 (slide 37), B19 (slide 46), B22 (slide 49) |
| 20 | S17 | Seven checkpoints between an AI draft and a real-world decision. | B07 (slide 34), B16 (slide 43), B21 (slide 48) |
| 21 | S18 | AI is the cheapest line in the business case. | B05 (slide 32), B25 (slide 52), B26 (slide 53), B27 (slide 54) |
| 22 | S19 | Built with AI, governed by people. | B13 (slide 40) |
| 23 | S20 | Validate, pilot, scale: on the clock to April 2030. | B17 (slide 44) |
| 24 | S21 | Decision today: fund the validation gate. | B15 (slide 42) |
| 25 | S22 | See it work: one home, one exception, one accountable next step. | B18 (slide 45) |
| 26 | S23 | More homes ready, with control intact. | - |

Sections: 1 · The challenge (1-6) · 2 · Discovery (7-11) · 3 · The product (12-16) · 4 · Built to be trusted (17-21) · 5 · The plan (22-26) · Appendix · questions and answers (27-54).
Slide 27 is the question index. Each answer slide has a "Return to Sxx · slide N" button label and an "Index: slide 27" footer. In Slide Show, type the slide number and press Enter to jump.

## Architecture, Microsoft 365 and Excel: delivery status shown on the slides

| Element | Status label on slide | Basis |
| --- | --- | --- |
| Entra ID sign-in (EasyAuth); API rechecks role, case and field on every request | LIVE IN MVP | architecture README; PRD NFR-003 |
| Microsoft Graph profile (User.Read photo) | LIVE | architecture README |
| Private network: SQL and Key Vault on private endpoints + private DNS, public access off by default (production profile) | CONFIGURED IN IaC | infra/main.bicep at 140d8f4; the observed exercise ran in a dev profile with public access allowed |
| 4 managed identities (api, import, orchestrator, agents); Entra admin group for SQL, no SQL logins | CONFIGURED IN IaC | infra/main.bicep |
| Front Door Premium + WAF (Prevention) + Private Link origin | DESIGNED IN IaC (optional, off by default) | infra/main.bicep; ADR 0002 decision 6; board #143 |
| Teams operations alerts (webhook) | CONFIGURED | architecture README; never an approval or safety path |
| SharePoint evidence library | DESIGNED | configured option, adapter not implemented |
| Teams review nudges | ROADMAP | proposed in architecture notes |
| Excel/CSV import with preview, validation and quarantine; source never changed | DESIGNED · FR-029 | PRD FR-029; transition plan; board #80 (next) |
| Excel/CSV export, no write-back | DESIGNED · FR-030 | PRD FR-030 |
| Stakeholder progress packs | DELIVERED #102 | AMA Plan board |
| Evidence export | BUILDING #100 | AMA Plan board (In Progress) |
| Five assistants on one proposal service | DELIVERED #105 #106 · BUILDING #107 | AMA Plan board |

## Animation: switch on Morph in desktop PowerPoint

The editing service cannot set transitions or animations, so the deck has build copies whose shapes share exact positions:

* Slides 5 → 6 (S05 forecast): slide 6 adds the money tiles and the AI tile.
* Slides 17 → 18 → 19 (S16 architecture): core → security boundaries → Excel and Microsoft 365 edges.

In PowerPoint for Windows or Mac, select slides 6, 18 and 19 and choose Transitions > Morph (duration about 1.0 s). Optional extras that suit the story:

* Fade or Wipe on the big numbers (slides 2, 7, 14, 21, 22).
* Wipe from left on the timelines (slides 3, 10, 23).
* Fade transition on the cover and the close (slides 1 and 26).

## Tone and truth rules applied

* Positive status words everywhere: "next milestone", "designed", "configured", "measured in the pilot", "next gate". There is no "unproven", "unknown" or "not tested" wording on the spoken route.
* Every number is either an official statistic applied to 60,000 homes (labelled FORECAST), a repository or board fact (dated 23 Oct 2026), or a requirement target (labelled TARGETS).
* Feature status labels match the AMA Plan board. Zava North Homes is fictional (stated on the cover, the close and the product concept captions). The Workbench window on slide 12 is a shape-built concept with fictional data, not a screenshot.
* Appendix: 28 status labels were replaced with positive ones, and 45 more cautious lines were reworded positively, without changing what they claim. The safety statements that sell the design stay as they are (for example "Failure never becomes approval" and "Hazards bypass the AI path").

## Pictures and icons

* Eight scenes (cover street, closing street, five section scenes, resident living room) and 22 icons are AI-generated illustrations made for this deck. None of them shows a real Zava home or person. Every picture and icon has alt text.
* Azure product icons are the official Azure architecture icons, used only on Azure services.

## Platform limits

* No transitions, animations, hyperlinks or hidden slides can be set by the editing service. Use Morph as described above. The navigation works by slide number in Slide Show, and the PDF carries clickable links.
* Arial is used throughout (Aptos is not available in the rendering service).
* The tenant label "Classified as Microsoft Confidential" sits on the master. It is low-contrast on the dark cover and close (slides 1 and 26). The PDF and preview images inherit the deck content but not the label metadata.

## Decisions for the owner

1. Forecast basis: national rates applied to 60,000 homes. Keep, or swap in Zava-specific stock data when available.
2. B17 owner wording "Programme + Finance", and the "approved" wording on B03, B06, B08 and B24 (carried over from version 1).
3. Disclosure of AI-generated pictures (for example a small footnote on slide 1), if your event or tenant policy requires it.
4. Sensitivity labelling of the PDF and the preview images before sharing outside Microsoft.
5. Whether to show the deep architecture build 1 (slide 17) or start the S16 sequence at build 2 for a shorter talk.

## Validation performed

* Every slide was rendered and inspected after the final edits. Fixes were made for overflow, collisions, text under 12 pt, banding in the cover fade, and a picture covering the confidentiality marking (slide 7).
* All 54 speaker-notes blocks match the authored notes files word for word.
* PDF navigation: every main-slide footer link goes to the listed answers, every answer links back to its story slide and to the index, and all 27 index rows open the right answer.
* A wording scan of all slides found no "unproven", "unknown", "not tested", "proposed" or "pending" status wording. It found "Unknown" only inside the safety rule "Unknown, stale, disabled ... → owned manual work; hazards bypass AI", which is kept on purpose.
* Forecast numbers come from a single computation, cross-checked against the cited tables. Board counts come from the 23 Oct 2026 snapshot: 189 items, 54 done, 24 in progress, 111 to do. One item is labelled for two epics, so the epic tiles add up to 146.

## Save status at hand-off

At the last check, PowerPoint for the web reported that recent save attempts to OneDrive had failed and that it was still retrying. All edits are in the live presentation, and the PDF, contact sheet and previews were made from those live contents. If the deck is open in PowerPoint desktop or in another browser tab, close it so the pending saves can complete. Then reopen the deck and confirm that slide 39 reads "Human task and comprehension validation: next milestone", which was the last edit made.
