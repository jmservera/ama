---
title: Regulatory Context Reference Documents
description: Authoritative reference documents for the Case Study 48 regulatory context
ms.date: 2026-09-25
ms.topic: reference
---

## Scope

These files support the regulatory context identified in the
[original Case Study 48](../../case_study_48_original.md). They were downloaded
from official UK government, legislation, regulator, or standards-body sources
on 19 September 2026.

This folder is the source layer of the
[Project Knowledge Base](../README.md). The snapshots are grouped by topic:

| Folder | Topic |
| --- | --- |
| [energy-efficiency/](./energy-efficiency/) | UK net zero target and social rented sector energy efficiency standards |
| [social-housing-regulation/](./social-housing-regulation/) | Social Housing (Regulation) Act, consumer standards and Awaab's Law |
| [data-protection/](./data-protection/) | UK GDPR and the Data Protection Act 2018 |
| [retrofit-standards-and-funding/](./retrofit-standards-and-funding/) | PAS 2035 and Warm Homes: Social Housing Fund delivery requirements |

Treat snapshots as immutable evidence. Record a newer retrieval as a new
snapshot or a reviewed update, never as a silent edit.

The collection distinguishes legislation already in force from consultation
material, guidance, and licensed standards. Always check the linked source for
later amendments or replacements before relying on a local copy.

Each converted reference links to its original authoritative source near the
top of the file.

## Authority and Use

Apply sources in this order when they address the same point:

1. Current consolidated legislation and commenced statutory instruments
2. Current regulatory standards and binding directions
3. Applicable grant agreements, contracts and incorporated technical standards
4. Official guidance and final government policy
5. Impact assessments and consultation material

The lower-ranked source may explain context but cannot override a higher-ranked
source. The current UK GDPR text is the working local baseline. The adopted UK
GDPR text, enacted-text Data Protection Act PDF and consultation documents are
historical or incomplete where later amendments or final decisions exist.

> [!IMPORTANT]
> A successful source check does not constitute legal advice or approval to
> activate a rule. Consequential interpretations require the named legal,
> compliance, data-protection, funding or competent professional owner.

## Change Assessment and Monitoring Register

Change likelihood describes the risk that the operational interpretation or
supporting detail will change, not the importance of the source.

| Local file | Current-use status | Change likelihood | Official monitoring cadence |
| --- | --- | --- | --- |
| `energy-efficiency/net-zero-2050-target-order-2019.md` | In-force national target; it does not itself impose an EPC C duty on the provider | Low | Check legislation.gov.uk annually and after major climate legislation |
| `energy-efficiency/social-rented-sector-mees-consultation-2025.md` | Historical consultation; superseded where the 2026 final position differs | Low relevance, high obsolescence | Retain for rationale and audit; do not encode operational rules from it |
| `energy-efficiency/social-rented-sector-mees-impact-assessment-2025.md` | Historical consultation-stage analysis | Low relevance, high obsolescence | Retain for sensitivities; compare only when final policy changes |
| `energy-efficiency/social-rented-sector-mees-government-response-2026.md` | Final policy position, not evidence by itself of a commenced landlord duty | Medium | Check MHCLG, DESNZ and RSH monthly until implementation, then quarterly |
| `energy-efficiency/social-rented-sector-mees-final-impact-assessment-2026.md` | Final policy evidence; technical metric and implementation detail remain subject to delivery work | High for EPC and exemption detail | Check EPC reform, Home Energy Model, DHS and RSH publications monthly until final specifications |
| `social-housing-regulation/social-housing-regulation-act-2023.md` | Enacted primary legislation; current commencement and amendments require consolidated-source checks | Low for framework, medium for commencement detail | Check legislation.gov.uk quarterly and before relying on a provision |
| `social-housing-regulation/social-housing-safety-and-quality-standard-2024.md` | Regulatory standard effective from 1 April 2024 | Medium | Check RSH consumer standards and regulatory publications quarterly |
| `social-housing-regulation/awaabs-law-hazards-in-social-housing-regulations-2025.md` | Phase 1 regulations in force from 27 October 2025 | Low for Phase 1, subject to amendment | Check SI 2025/1042 monthly and after MHCLG announcements |
| `social-housing-regulation/awaabs-law-phase-1-guidance-2025.md` | Official non-statutory implementation guidance | Medium | Check the GOV.UK publication monthly and after regulation changes |
| `social-housing-regulation/awaabs-law-phase-2-guidance-2026.md` | Official non-statutory guidance for planned commencement on 30 November 2026 | High until commencement | Check legislation.gov.uk and GOV.UK weekly until commencement, then monthly for six months |
| `social-housing-regulation/awaabs-law-phase-2-hazards-guidance-2026.md` | Official non-statutory guidance; the local copy contains limited introductory material | High | Check the GOV.UK publication weekly until a complete stable version is confirmed |
| `data-protection/uk-gdpr-current-text.md` | Working consolidated local baseline as retrieved on 19 September 2026 | High for automated-decision rules; lower for core principles | Check consolidated legislation and ICO guidance monthly and before each production release |
| `data-protection/uk-gdpr-adopted-text.md` | Historical comparison only; not the current operational authority | Low relevance, high obsolescence | Retain for comparison; do not use for current Article 22 rules |
| `data-protection/data-protection-act-2018.md` | Enacted-text copy; later amendments may be absent | Medium | Check revised legislation quarterly and before relying on a Schedule 1 condition |
| `retrofit-standards-and-funding/pas-2035-2023-bsi-overview.md` | Overview only; obtain the licensed standard and verify contractual incorporation | Medium | Check BSI, TrustMark and applicable scheme rules quarterly and at procurement or grant change |
| `retrofit-standards-and-funding/warm-homes-social-housing-fund-technical-annex-2025.md` | Allocation methodology, not complete eligibility rules or evidence of an award | High for provider use | Check current scheme guidance, award letter and grant agreement monthly during delivery and before claims |

Phase 3 of Awaab's Law is not represented by an implementing instrument in
this collection. Monitor MHCLG, legislation.gov.uk and GOV.UK monthly, moving
to weekly checks when draft regulations are laid.

## Managed Update Workflow

The production solution should maintain a regulatory source register separate
from the searchable document index. Each source record needs:

* Stable source identifier, official URL, jurisdiction and authority type
* Publication, retrieval, effective, review and supersession dates
* Content hash, local version, parser result and completeness status
* Change likelihood, monitoring cadence and accountable owner
* Applicability, affected requirements, operational rules, tests and user
  journeys
* Review, approval, activation and retirement history

Use official APIs, legislation data, publication metadata, feeds and alerts
where available. Scheduled retrieval may compare metadata, hashes and semantic
sections. Scraping is a fallback for discovery, not an authority signal.

The update path is:

1. Detect a new publication, amendment, metadata change or retrieval failure.
2. Preserve the previous snapshot and store the candidate with provenance.
3. Classify the difference and identify affected requirements, rules, evidence
   templates, communications and reports.
4. Route the candidate to the named legal, compliance, data-protection, funding
   or professional owner.
5. Update interpretations and deterministic rules only after approval.
6. Run regression, accessibility, timing, privacy and audit-trace tests.
7. Activate the approved version on its effective date with rollback available.
8. Notify affected employees, residents, contractors and reporting owners in
   an appropriate form.

Detection must never overwrite the last approved operational rule. If a change
may create immediate harm or illegality, an authorised owner can place a hold
while the interpretation and implementation are reviewed.

## Agent Retrieval and Answer Controls

Agents using this corpus must:

* Retrieve only sources marked current for the question and disclose historical
  material when it is used for context
* Return source, provision, status, retrieval date and effective-date context
  with each consequential answer
* Preserve uncertainty where commencement, applicability or interpretation is
  unresolved
* Refuse to convert missing evidence into compliance or to treat a policy
  announcement as commenced law
* Escalate conflicting sources, incomplete retrievals and high-impact changes
  to a named human owner
* Keep resident reports, professional findings and authorised decisions above
  inferred or generated conclusions

## UK Net Zero and social housing energy efficiency

| Local file | Status and purpose | Official source |
| --- | --- | --- |
| [net-zero-2050-target-order-2019.md](./energy-efficiency/net-zero-2050-target-order-2019.md) | Legislation that amended the Climate Change Act 2008 target to net zero by 2050, converted from PDF | [UK Statutory Instruments 2019 No. 1056](https://www.legislation.gov.uk/uksi/2019/1056/contents) |
| [social-rented-sector-mees-consultation-2025.md](./energy-efficiency/social-rented-sector-mees-consultation-2025.md) | Consultation proposal for EPC C or equivalent by 2030, converted from PDF | [Improving the energy efficiency of socially rented homes in England](https://www.gov.uk/government/consultations/improving-the-energy-efficiency-of-socially-rented-homes-in-england) |
| [social-rented-sector-mees-impact-assessment-2025.md](./energy-efficiency/social-rented-sector-mees-impact-assessment-2025.md) | Consultation-stage impact assessment converted from PDF | [Consultation attachments](https://www.gov.uk/government/consultations/improving-the-energy-efficiency-of-socially-rented-homes-in-england) |
| [social-rented-sector-mees-government-response-2026.md](./energy-efficiency/social-rented-sector-mees-government-response-2026.md) | Government response converted from the published HTML | [Government response](https://www.gov.uk/government/consultations/improving-the-energy-efficiency-of-socially-rented-homes-in-england/outcome/improving-the-energy-efficiency-of-socially-rented-homes-in-england-government-response) |
| [social-rented-sector-mees-final-impact-assessment-2026.md](./energy-efficiency/social-rented-sector-mees-final-impact-assessment-2026.md) | Final-stage impact assessment converted from PDF | [Consultation outcome](https://www.gov.uk/government/consultations/improving-the-energy-efficiency-of-socially-rented-homes-in-england) |

## Social housing regulation and Awaab's Law

| Local file | Status and purpose | Official source |
| --- | --- | --- |
| [social-housing-regulation-act-2023.md](./social-housing-regulation/social-housing-regulation-act-2023.md) | Enacted Social Housing (Regulation) Act 2023, converted from PDF | [2023 c. 36](https://www.legislation.gov.uk/ukpga/2023/36/contents) |
| [social-housing-safety-and-quality-standard-2024.md](./social-housing-regulation/social-housing-safety-and-quality-standard-2024.md) | Regulator of Social Housing consumer standard effective from 1 April 2024, converted from PDF | [Safety and Quality Standard](https://www.gov.uk/government/publications/safety-and-quality-standard) |
| [awaabs-law-hazards-in-social-housing-regulations-2025.md](./social-housing-regulation/awaabs-law-hazards-in-social-housing-regulations-2025.md) | The Hazards in Social Housing (Prescribed Requirements) (England) Regulations 2025, converted from PDF | [UK Statutory Instruments 2025 No. 1042](https://www.legislation.gov.uk/uksi/2025/1042/contents) |
| [awaabs-law-phase-1-guidance-2025.md](./social-housing-regulation/awaabs-law-phase-1-guidance-2025.md) | Phase 1 landlord guidance converted from the published HTML | [Phase 1 guidance](https://www.gov.uk/government/publications/awaabs-law-guidance-for-social-landlords) |
| [awaabs-law-phase-2-guidance-2026.md](./social-housing-regulation/awaabs-law-phase-2-guidance-2026.md) | Phase 2 landlord guidance converted from the published HTML | [Phase 2 guidance](https://www.gov.uk/government/publications/awaabs-law-phase-2-guidance-for-social-housing-landlords) |
| [awaabs-law-phase-2-hazards-guidance-2026.md](./social-housing-regulation/awaabs-law-phase-2-hazards-guidance-2026.md) | Phase 2 hazard guidance converted from the published HTML | [Phase 2 hazards guidance](https://www.gov.uk/government/publications/awaabs-law-phase-2-hazards-guidance-for-social-landlords) |

## Data protection

| Local file | Status and purpose | Official source |
| --- | --- | --- |
| [uk-gdpr-current-text.md](./data-protection/uk-gdpr-current-text.md) | Consolidated UK legislation data for Regulation (EU) 2016/679 converted from XML, including amendments recorded by legislation.gov.uk | [UK GDPR current text](https://www.legislation.gov.uk/eur/2016/679/contents) |
| [uk-gdpr-adopted-text.md](./data-protection/uk-gdpr-adopted-text.md) | Adopted EU text converted from PDF for historical comparison; use the consolidated Markdown text for the current UK text | [Regulation (EU) 2016/679](https://www.legislation.gov.uk/eur/2016/679/contents) |
| [data-protection-act-2018.md](./data-protection/data-protection-act-2018.md) | Enacted Data Protection Act 2018, converted from PDF | [2018 c. 12](https://www.legislation.gov.uk/ukpga/2018/12/contents) |

## PAS 2035 and funded retrofit delivery

| Local file | Status and purpose | Official source |
| --- | --- | --- |
| [pas-2035-2023-bsi-overview.md](./retrofit-standards-and-funding/pas-2035-2023-bsi-overview.md) | BSI overview of PAS 2035:2023 converted from the published HTML | [BSI PAS 2035 overview](https://www.bsigroup.com/en-GB/insights-and-media/insights/brochures/pas-2035-retrofitting-dwellings-for-improved-energy-efficiency/) |
| [warm-homes-social-housing-fund-technical-annex-2025.md](./retrofit-standards-and-funding/warm-homes-social-housing-fund-technical-annex-2025.md) | Government technical annex that applies retrofit requirements to funded delivery, converted from PDF | [Warm Homes: Social Housing Fund Wave 3](https://www.gov.uk/government/publications/warm-homes-social-housing-fund-wave-3) |

PAS 2035:2023 is a licensed BSI standard. The standard itself is not reproduced
in this repository. Obtain an authorised copy from BSI and verify the edition
required by the relevant funding scheme or contract.
