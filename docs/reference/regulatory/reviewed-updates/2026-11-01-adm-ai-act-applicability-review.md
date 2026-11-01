---
title: Applicability Review Pack for UK Automated-Decision Rules and the EU AI Act
description: Dated official-source check, pending Legal and DPO decision record, affected review items and non-inference rules for issue 224 and OQ-019
ms.date: 2026-11-01
ms.topic: reference
---

## Scope and Status

This pack prepares the review for open question OQ-019 and issue #224. It is
an evidence check and a decision record template. It is not legal advice and
not a Legal or DPO decision. Every decision field below reads `Pending` until
the named Legal and DPO owner records it. No jurisdiction, risk tier or
compliance position is inferred.

* Reviewer prepared by: agent-assisted repository check, 2026-11-01.
* Decision owner: Legal and DPO. The exercise Legal, Compliance and DPO owner is
  Juan Manuel Servera (owner decision, 2026-10-15). Actual company appointees
  and professional competence are unknown.
* Local snapshot checked: [UK GDPR consolidated text](./data-protection/uk-gdpr-current-text.md),
  retrieved 2026-09-19.

## Official Source Check

| Regime and provision | Official source | Source date | Retrieval date | Commencement or amendment recorded | Result |
| --- | --- | --- | --- | --- | --- |
| UK GDPR Articles 22A to 22C, inserted by Data (Use and Access) Act 2025 s.80 | [legislation.gov.uk, DUAA 2025 s.80](https://www.legislation.gov.uk/ukpga/2025/18/section/80) | Versions dated 2025-06-19 and 2026-02-05 | 2026-11-01 | In force at Royal Assent for specified purposes (s.142(1)(2)(h)); in force 2026-02-05 so far as not already in force by [S.I. 2026/82](https://www.legislation.gov.uk/uksi/2026/82/contents/made) reg. 2(j), with reg. 5 | Retrieved. Page shows no known outstanding effects. Reg. 5 transitional wording was not read; unknown |
| S.I. 2026/82, Commencement No. 6 and Transitional and Saving Provisions Regulations 2026 | [legislation.gov.uk](https://www.legislation.gov.uk/uksi/2026/82/contents/made) | Made version | 2026-11-01 | Reg. 2 brings listed provisions into force on 2026-02-05 | Retrieved; reg. 5 not analysed |
| Local snapshot against official text | Snapshot retrieved 2026-09-19 contains Articles 22A to 22D | 2026-09-19 | 2026-11-01 (existence of the articles only) | Snapshot post-dates commencement of 2026-02-05 | No line-by-line comparison done. Currentness `Unknown` until the Legal/DPO reviewer compares point-in-time text |
| ICO guidance on automated decision-making | Not retrieved | n/a | n/a | n/a | `Unknown` |
| EU AI Act, Regulation (EU) 2024/1689 | EUR-Lex (target) | n/a | 2026-11-01 attempt failed (bot challenge, empty body) | Not verified | `Unknown`. Secondary commentary mentions a Digital Omnibus delaying Annex III high-risk dates; this is unverified and must not be relied on |

Unknown does not mean unchanged. The Legal/DPO reviewer must retrieve the
EUR-Lex consolidated text and any amending acts before recording the EU
decision.

## Decision Record (Pending Legal and DPO)

| Regime | Applicability question | Decision | Decider | Date | Official source checked by decider |
| --- | --- | --- | --- | --- | --- |
| UK GDPR Articles 22A to 22C | Do any Zava Forward workflows take a significant decision about a resident based solely on automated processing (no meaningful human involvement)? Which safeguards (information, representations, human intervention, contest) apply? | Pending | Pending | Pending | Pending |
| EU AI Act | Do territorial conditions arise (EU placing on the market, EU-located persons or use of output in the EU)? If so, what is the Zava role (provider, deployer or other), and what classification and obligations follow? | Pending | Pending | Pending | Pending |

Facts available to the decider, labelled as evidence and not as conclusions:

* Case-study fact: the scenario is a UK housing association exercise.
* Repository design: agents propose, and named humans approve or decide. Where
  that is verified in operation, it bears on "meaningful human involvement"
  (Article 22A(1)(a)); that is for Legal/DPO to judge.
* Unknown: any EU establishment, EU-located residents, EU market placement,
  intended use classification and the actual hosting region of any model.

## Non-inference Rules (Criterion 4)

None of the following establishes a risk classification, role or applicability
under either regime, alone or together:

* Housing association status, or being a registered provider.
* Use of an EU-hosted model or EU data-centre region.
* Social-housing or retrofit subject matter.

Each regime needs its own decision against its own provisions and facts.

## Review Items

| ID | Affected item | Why it is affected | Proposed owner action |
| --- | --- | --- | --- |
| RI-1 | OQ-019 in [PRD](../../prds/zava-forward-retrofit-programme-demonstrator.md) | Open until a Legal/DPO decision is recorded | Record decisions in the table above, then update OQ-019 |
| RI-2 | FR-034 and RULE-021 | Traced by the `automated-decision-safeguard` card | Confirm whether the requirement wording still fits Articles 22A to 22C |
| RI-3 | Seed card `automated-decision-safeguard` (`src/core/src/zava_forward/core/rulecards.py`) | Provision cites "Article 22 (illustrative)"; Articles 22A to 22C are the in-force provisions per the 2026-11-01 check. Approver is unassigned | After DPO decision, correct the citation and name the approver through the rule-card approval workflow (#211) |
| RI-4 | Tests `src/core/tests/test_rulecards.py` and `src/agents/tests/test_ai_eval.py` | Assert the card's content and the AI evaluation | Re-run and update if the card changes; no test change before the decision |
| RI-5 | AI release records (#219) | Release records bind AI activations to dependent policies | Reference this pack and the recorded decision; do not mark legal screening complete without it |
| RI-6 | Regulatory register cadence | Local snapshot is dated 2026-09-19 | Keep monthly check cadence and recheck before release |
| RI-7 | Related #121, #127, #209 and parent #218 | Share the legal basis for agent decisions | Cross-reference the decision when recorded |

## Feed to #219 and #211

* #219: until the Legal/DPO decision is recorded, release records should show
  the legal screening as `pending decision`, citing this pack and the
  2026-11-01 check. They must not infer compliance.
* #211: the seed card stays unchanged until the DPO decides RI-3. This pack
  supplies the checked citation (Articles 22A to 22C, in force 2026-02-05) and
  the four safeguards in Article 22C(2) as inputs for the owner's edit.

## Required Human Review

Legal interpretation, applicability and activation of any control stay with
the named qualified human owner. Criterion 1 and the final feeds in criterion
5 remain open until that decision is recorded. No checkbox in issue #224 is
ticked by this pack.
