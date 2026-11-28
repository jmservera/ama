---
title: Privacy, UK Residency and Responsible AI Presentation Review
description: Dated official-source checks and proposed presentation interpretations, with legal and operational acceptance pending
ms.date: 2026-11-28
ms.topic: reference
---

## Status and scope

This reviewed update supports the capstone presentation. It preserves the
September snapshots and the [1 November applicability review](./2026-11-01-adm-ai-act-applicability-review.md).
Legal and DPO applicability, lawful-basis and real-data acceptance remain
pending. No live control or deployment changes follow from this document.

The [company profile](../../research/company/company-profile-research.md)
records owner-confirmed not-for-profit status. Exact legal form, charity status
and registration remain unknown. RSH duties depend on registered-provider and
jurisdictional applicability, not simply on being not-for-profit.

## Sources checked on 28 November 2026

| Source | Classification, section and source date | Current reading and limits |
| --- | --- | --- |
| [UK GDPR](https://www.legislation.gov.uk/eur/2016/679/contents), [Article 5](https://www.legislation.gov.uk/eur/2016/679/article/5), [6](https://www.legislation.gov.uk/eur/2016/679/article/6), [9](https://www.legislation.gov.uk/eur/2016/679/article/9), [25](https://www.legislation.gov.uk/eur/2016/679/article/25), [35](https://www.legislation.gov.uk/eur/2016/679/article/35), [22A](https://www.legislation.gov.uk/eur/2016/679/article/22A) and [22C](https://www.legislation.gov.uk/eur/2016/679/article/22C) | Consolidated legislation; Regulation 2016/679 as amended, checked 2026-11-28. The earlier review records ADM commencement on 2026-02-05 | Principles, lawful basis, special-category conditions, protection by design and likely-high-risk DPIAs apply. Current ADM provisions distinguish solely automated significant decisions from meaningful human involvement and provide covered-decision safeguards. No approval of Zava's processing follows |
| [RSH Transparency, Influence and Accountability Standard](https://www.gov.uk/government/publications/transparency-influence-and-accountability-standard) | Regulatory standard for relevant registered providers in England; publication updated 2026-10-01, including STAIRs | Accessible service/decision information and tenant accountability do not mean unrestricted resident-record disclosure. Zava's exact applicability remains unconfirmed |
| [ICO international-transfer guide](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/a-guide-to-international-transfers/) and its restricted-transfer compliance chapter | Official guidance; updated 2026-01-15 | Restricted transfers may use adequacy, appropriate safeguards with the required data protection test/TRA, or an applicable derogation. UK GDPR is not a blanket UK-only storage/processing rule |
| [ICO automated-decision guidance](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/automated-decision-making/) | Draft consultation at retrieval; publication date not established in this check | Useful review context, not final guidance or a replacement for current legislation. Earlier failure/unknown-guidance evidence remains historical |
| [Microsoft deployment types](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/deployment-types) and [regional model catalog](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure-region-availability) | Provider technical documentation; current pages checked 2026-11-28, not a contract or quota receipt | Standard and regional provisioned inference process within the selected geography. The Standard/Regional Europe table lists gpt-4.1-mini for UK South; subscription quota and activation were not established. Global Standard is separate; EU DataZone is not UK |
| [Microsoft model data privacy](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy) | Provider processing/monitoring documentation; current page checked 2026-11-28 | Model training restrictions, inference location and provider access are separate assurances. The stated reviewer-location guarantee covers EEA resources, not UK. Modified Abuse Monitoring has a future-change notice for models made available on/after 2026-11-01, with at least 30 days notice; do not promise permanent coverage |

Source and retrieval dates are distinct. Dynamic consolidated legislation and
provider pages do not establish the publication date of every displayed change.
The original checks and table-context evidence are retained in the
[research record](../../../../.copilot-tracking/research/2026-11-28/capstone-privacy-residency-rai-research.md).

## Presentation interpretation

Useful transparency means that residents can understand the service, who owns
the next action and how to challenge a decision. Own-case access must protect
other households. Not-for-profit status alone creates neither unrestricted
disclosure nor a universal Article 9 condition.

The proposed customer policy is UK application/storage and UK Standard-model
inference. Standard is public-Azure regional processing, potentially across
regions within the selected geography; it is not on-premises Foundry Local.
The [architecture analysis](../../../architecture/environment-region-quota-strategy.md)
retains the GlobalStandard default, independently selectable SQL/AI locations
and Sweden Central option. No current UK-only deployment was attested.
Identity, support/remote access, logs, backups, abuse monitoring and the control
plane need separate data maps and contract checks.

UK hosting does not establish lawful processing. A real service needs a
documented lawful basis, data minimisation, approved retention and rights
handling, with a DPIA where likely high risk requires it. Health information
can be special category; not every vulnerability datum is. Works consent and
monitoring choice are distinct from the lawful basis for data use. The
[draft DPIA](../../research/chat-memory-dpia.md) does not approve real data.

AI prepares suggestions, drafts and review flags. A competent, authorised
human needs relevant evidence, time and discretion to correct or reject before
applying a consequential decision, with reasons and applicable challenge
routes. An accept button or later spot check alone is insufficient. Resident
consent, professional/safety judgement, funding approval and independent
quality acceptance remain separate. The suggestion-only product policy is a
stronger design choice, not a claim that UK GDPR prohibits all automation.
The [RAI review](../../research/rai/project-rai-review.md) is partial engineering
evidence, not operational fairness, safety or privacy acceptance.

## Review and activation gates

Change likelihood is High for ADM guidance, model availability/lifecycle and
provider monitoring; Medium for transfer guidance and RSH interpretation.
Check monthly and before real-data deployment or external assurance. Increase
to weekly around announced changes or consultation deadlines.

Legal and the DPO must confirm jurisdiction, processing purpose/basis,
special-category conditions, transfers, rights and DPIA outcomes. Digital must
attest the actual service/model locations and provider terms; Programme,
Engagement, Safety, Finance and Quality must accept the human review and
resident routes within their decision rights. Until then, presentation
wording is a proposal and the demo remains constructed-data evidence.
