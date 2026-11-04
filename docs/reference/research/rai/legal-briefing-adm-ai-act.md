---
title: Legal Briefing on UK Automated-Decision Rules and EU AI Act Applicability
description: Briefing for the Legal contact with main points, open questions and recommendations for issue 224 and OQ-019; it prepares a decision and does not make one
ms.date: 2026-11-04
ms.topic: reference
---

## Purpose and Status

This briefing helps the Legal contact decide two questions for the Zava
Forward demonstrator (open question OQ-019, issue #224):

* Do the UK GDPR automated-decision rules (Articles 22A to 22C) apply to any
  workflow, and if so which safeguards must exist?
* Do any conditions arise that make the EU AI Act relevant, and if so what
  role, classification and obligations follow?

It is not legal advice. It does not decide either question, infer a
jurisdiction, risk tier or compliance position, or approve any control.
Legal interpretation stays with the named human Legal and DPO owner. The
exercise Legal, Compliance and DPO owner is Juan Manuel Servera (owner
decision, 2026-10-15); real company appointees are unknown. Decisions are
recorded in the
[applicability review pack](../../regulatory/reviewed-updates/2026-11-01-adm-ai-act-applicability-review.md),
where every decision field reads `Pending`.

Evidence labels used below: `Official` (read from the official source on the
stated date), `Repository` (a design fact in this repository), `Unknown`
(not verified).

## Main Points

### UK GDPR Articles 22A to 22C

* Official, retrieved 2026-11-04: the Data (Use and Access) Act 2025 s.80
  replaced the old Article 22 with Articles 22A to 22D. Commencement
  Regulations S.I. 2026/82, reg. 2(j), bring s.80 into force on 2026-02-05.
* Official, retrieved 2026-11-04: reg. 5 says the s.80 amendments do not apply
  to a decision taken before 2026-02-05 that was subject to the old Article
  22(3). This closes the transitional point left unread on 2026-11-01. Zava
  Forward has no live decisions, so it is unlikely to matter, but Legal should
  confirm.
* Article 22A(1): a decision is "solely automated" when there is no
  meaningful human involvement, and is "significant" when it has a legal or
  similarly significant effect on the person. Article 22A(2) says profiling
  counts when judging human involvement.
* Article 22B: a significant solely-automated decision using special-category
  data is barred unless explicit consent, or a contract or legal
  authorisation plus the Article 9(2)(g) substantial public interest
  condition, applies. A solely-automated significant decision that relies on
  recognised legitimate interests (Article 6(1)(ea)) is barred outright.
* Article 22C: where a significant decision is solely automated and based on
  personal data, the controller must provide safeguards that give the
  person information, let them make representations, let them obtain human
  intervention, and let them contest the decision. Article 22D lets the
  Secretary of State add detail by regulations; none were checked.
* Repository: agents recommend, draft and flag, and named humans approve or
  decide ([release position](../../../case_study_48_addendum.md#responsible-ai-release-position-2026-10-14)).
  Whether that amounts to "meaningful human involvement" in operation is a
  fact-and-judgement question for Legal and DPO, not settled here.
* Repository: the seed rule card `automated-decision-safeguard` cites
  "Article 22 (illustrative)", which no longer matches the in-force
  provisions.

### EU AI Act (Regulation (EU) 2024/1689)

* Unknown: the EUR-Lex retrieval failed again on 2026-11-04 (bot challenge,
  no body), so no text, commencement date or amendment was read from the
  official source. Secondary mention of a delay to high-risk dates is
  unverified and must not be relied on.
* The Act's reach depends on facts the repository does not hold: whether any
  system is placed on the EU market or put into service in the EU, whether
  the output is used in the EU, and the Zava role (provider, deployer or
  other).
* Classification depends on the intended use and the Act's own lists, not on
  sector. The questions Legal needs to answer from the Act itself are scope
  (Article 2), prohibited practices, high-risk classification (Article 6 and
  Annex III), general-purpose model duties and transparency duties.
* Housing association status, an EU-hosted model or social-housing subject
  matter does not by itself establish a role, a risk tier or applicability
  (issue #224 criterion 4, addendum release position).

## Recommendations

Each is a proposal for the Legal and DPO owner to accept, change or reject.

| # | Recommendation | Why | Evidence status |
| --- | --- | --- | --- |
| 1 | Decide the two regimes separately and date each decision, naming the official source read | Each regime has its own provisions and facts; no inference across them | Pack decision table is `Pending` |
| 2 | For Articles 22A to 22C, list each workflow that could be a significant decision about a resident (prioritisation, offer, scheduling, contact, eligibility, access) and record whether a named human takes the decision with meaningful involvement | The test turns on actual human involvement, not on the design intent | Repository design only; no operational evidence |
| 3 | Record the 22B position for special-category data (for example health, vulnerability or disability markers) and whether Article 6(1)(ea) is relied on anywhere | These are the cases the Act restricts outright | Unknown; no lawful-basis map checked |
| 4 | If any workflow is solely automated and significant, require the four Article 22C safeguards (information, representations, human intervention, contest) with a manual path and plain-language notice | Matches the repository's manual-path and resident-consent boundaries | Not built as a legal control |
| 5 | Retrieve the EUR-Lex consolidated text and any amending acts by a method that works for a person (browser or official download), then record the EU decision | Automated retrieval is blocked; the EU position is `Unknown` until then | Failed 2026-11-01 and 2026-11-04 |
| 6 | State the territorial facts before classifying: EU establishment, EU-located residents, EU market placement, model hosting region and intended use | Legal cannot decide scope without them | `Unknown` |
| 7 | Check the ICO automated decision-making guidance and any Article 22D regulations, and compare the 2026-09-19 local snapshot with the point-in-time official text | Not retrieved; snapshot currentness is `Unknown` | Not done |
| 8 | After the decision, correct the seed card citation to Articles 22A to 22C and name its approver through the rule-card approval workflow (#211) | Card still cites Article 22 and has no approver | Not changed; awaits decision |
| 9 | Make AI release records (#219) show legal screening as `pending decision` until the decision is recorded, then cite the dated decision | Avoids implying compliance | Release records not edited here |
| 10 | Keep the monthly source check cadence and recheck before any release or external submission | Consequential change risk is high near commencement dates | Cadence in regulatory README |

## What Legal Is Asked to Decide

* UK GDPR: applicability per workflow, the 22B position and the safeguards
  needed, with the date and sources read.
* EU AI Act: whether territorial conditions arise, the Zava role, any
  classification and the obligations that follow, with the date and sources
  read.
* Whether the AI-unavailable and manual paths described in the design are
  adequate for the contest and human-intervention safeguards.

## Gaps Not Closed by This Briefing

* No Legal or DPO decision is recorded; criteria 1 and 5 of #224 stay open.
* EU AI Act text, commencement and amendments are unverified.
* The local UK GDPR snapshot was not compared line by line with the official
  text; ICO guidance and Article 22D regulations were not read.
* Real appointees, lawful-basis records and operational evidence of human
  involvement are unknown.
