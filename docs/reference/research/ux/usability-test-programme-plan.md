---
title: Usability testing programme plan with representative users (issue 155)
description: Draft moderated usability test plan, task scripts derived from the profile checks and learning-test bundles, aggregate-only measures, findings log and results templates, all unexecuted
ms.date: 2026-11-04
ms.topic: reference
---

## Purpose and evidence label

Issue [#155](https://github.com/jmservera/ama/issues/155), under #149, covers
PRD SA-009, SA-010, OQ-004, OQ-005 and OQ-011 and BRD NFR-009. This page is a
**draft plan with blank records**. At 2026-11-04 no participant has been
recruited, no session has run, no measure exists and no owner or staff
agreement is recorded. Nothing here is user validation, a conformance claim or
a usability result.

All thresholds are PRD proposals used as hypotheses, not pass marks. Real
customer access is not available; a proxy participant result must be labelled
as a proxy.

Related pages: [equity and user research protocol draft](./equity-journey-test-plan.md)
(#128), [journey learning-test bundles](./journey-learning-test-bundles.md)
(#129), [prototype profile review](./zava-forward-prototype-profile-review.md)
(checks UX-01 to UX-08), [resident journeys](./customer-journeys/residents.md)
(J1 to J6, R1 scripts), [supplier journeys](./customer-journeys/suppliers.md)
and [frontline journeys](./customer-journeys/frontline.md).

## Hypotheses and thresholds (proposals)

| Id | Hypothesis | Source | Status |
| --- | --- | --- | --- |
| H1 | At least 80 percent of 5 to 8 Excel users per role find their case and say the next step and owner, unaided, in under 5 minutes | SA-009 | Proposal, untested |
| H2 | SUS of at least 70 per role | SA-009 | Proposal, untested |
| H3 | A participant can complete each manual or non-digital alternative without detriment | NFR-009, AC-071 | Untested |
| H4 | No task step implies consent, approval, a commitment or a submission that has not happened | Bundle stop rules, UX-04, UX-05 | Untested |

With 5 to 8 participants per role a percentage is coarse (4 of 5 is 80 percent).
Report counts, not only percentages, and state that the sample cannot support
statistical claims. A participant who fails a task is a finding, not an error.

## Participants per role

| Role group | Roles | Target per role | Recruitment source | Status |
| --- | --- | --- | --- | --- |
| Staff | Neighbourhood housing officer, contact-centre or assisted-intake staff, complaint or redress handler, programme coordinator, technical or quality reviewer, finance or grants officer, data steward | 5 to 8 Excel users each (SA-009) | Zava North Homes sponsor, or proxy staff from a comparable landlord | Not started |
| Residents and representatives | Resident, including non-digital, language, literacy and adjustment needs; representative or advocate | Not set; SA-009 does not size it. Owner decision needed | Voluntary, via Resident Engagement, never from live case lists without a lawful basis | Not started |
| Contractors | Contractor scheduler or supervisor, installer field worker, procurement or contracts manager | 5 to 8 each if access exists | Procurement and Contracts, supplier invitation | Not started |

Roles with no reachable participants are reported as "not tested", not filled
by role agents or colleagues acting as residents. Real workbook shapes, owners
and contents are unknown (OQ-005, OQ-012); sessions begin with observation of
the participant's current workaround before the task.

## Accessibility and support during sessions

* Offer every participant, before scheduling, the choice of in-person, phone
  or remote; their own device and assistive technology; a plain-language
  briefing in advance; an interpreter, language support or an assisted
  session with a trusted person; and extra time. Needs are recorded only when
  volunteered.
* Include participants who use a screen reader, keyboard only or magnification
  where recruitable. If none is reached, record "assistive technology not
  tested" and do not claim accessibility.
* Breaks, stopping at any moment and switching to the manual or non-digital
  route are always allowed, with no effect on service, tenancy, contract or
  employment.
* The moderator reads tasks aloud on request and never rushes. The five minute
  limit is measured but not announced as a test of the person.
* Screens under test keep the Fluent 2 design system, the WCAG baseline, the
  plain-language content standard, non-colour status signals and reduced
  motion. Engineering checks do not substitute for these sessions.

## Consent, data handling and the audit-use statement

* Participation is voluntary and written or recorded consent is separate from
  any case or service consent. Declining or withdrawing has no consequence and
  withdrawal removes the person's data.
* Only constructed or fictional cases are used. No real resident, contractor
  or case data is shown, and participants are asked not to use their own.
* No audio, video or screen recording unless a participant agrees to it
  separately and the DPO approves purpose, storage and deletion. The default
  is moderator notes without names.
* The repository, reports and manager views hold aggregate results only
  (SA-010): counts, medians and ranges per role, plus anonymised, paraphrased
  finding text. No individual score, time, quote or identity. Where a role has
  fewer than 5 participants, merge it into a wider group or report "too few to
  report".
* Audit-use statement for staff, to be agreed before any measure is reported:
  "Results describe how well the screens work for people in a role. They are
  not used to assess, rank or discipline any person, and are not used in
  audit of individual staff."
* Lawful basis, minimum fields, retention and ethics review are decisions for
  the DPO and the programme sponsor and are not made here. Retention stays
  Unknown until the DPO decides.

Agreement record (blank):

| Item | Named agreeing person | Date | Status |
| --- | --- | --- | --- |
| Test plan, tasks and thresholds as hypotheses | | | Not agreed |
| Audit-use statement agreed with staff first (SA-010) | | | Not agreed |
| Lawful basis, minimum fields, retention (DPO) | | | Not agreed |
| Recruitment and ethics route | | | Not agreed |
| Task-script wording reviewed by the owner | | | Not reviewed |

## Task scripts

Each script gives the participant a goal, not a path. The moderator records
what the participant does, where they hesitate, and whether they reach the
manual route when they need it. Scripts are derived, not invented: staff and
contractor tasks from the eight profile checks, resident tasks from the
resident scripts, and bundle tasks from the learning-test protocol.

### Core task for every staff role (SA-009)

| Task | Goal given to the participant | Success | Source |
| --- | --- | --- | --- |
| T0 | "Find case X and tell me the next step and who owns it" | Correct next step and owner, unaided, within 5 minutes; also record time and assists | SA-009 |

### Staff and contractor tasks (from the profile checks)

| Task | Derived from | Observe | Failure cases to include |
| --- | --- | --- | --- |
| T1 Orientation | UX-01, UX-02 | Does the participant notice the current role, workflow and filters, and understand why an action is unavailable | Filter retained across a changed role |
| T2 Honest state | UX-03 | Can they tell loading, no matches and load failure from success | A failed load shown as zero work |
| T3 Readiness | UX-04 | Name the stage, next task, evidence and unmet prerequisite | Ready-for-review read as approved |
| T4 Ownership at handoff | UX-05 | Name the current owner, receiver and chase owner; say whether receipt is acceptance | Returned case with no follow-up |
| T5 Agent contribution | UX-06 | Say what a draft or recommendation used, who reviews it and what it cannot do; finish the task with AI off | AI unavailable: plain text "assistance not available", manual path completes |
| T6 Full-screen case | UX-07 | Open, work and return; focus and filter context restored; narrow and 200 percent zoom | Hover-only action |
| T7 Contact context | UX-08 | Find the safe contact route; say what is unknown | Missing field shown as invented value |
| T8 Contractor submission | Contractor design contract in [suppliers](./customer-journeys/suppliers.md) | Submit, correct, and see acknowledgement versus acceptance | Rejected submission with no stated reason |

### Resident and representative tasks (from the resident scripts)

| Task | Derived from | Observe |
| --- | --- | --- |
| R-J1/J2 | Two measures, change one choice | Explain scope, find independent help, withdraw one; no consent inferred |
| R-J3 | Offer, response, three confirmations, provider cancellation | Distinguish offered, responded and confirmed; find non-digital route |
| R-J4 | Overdue update, changed unsafe number | Find owner, due date and basis; no old-route disclosure |
| R-J5 | Controls practice, reopened defect | Use instructions without a score; find the urgent route |
| R-J6 | Closed response, open remedy or charge query | Explain separate statuses; use the formal route without detriment |

Resident tasks run only with direct, voluntary participants or an
Engagement-approved proxy, and are never simulated by role agents.

### Learning-test bundle tasks (from the bundle protocol)

Bundles run as two-arm experiments on constructed cases with a non-AI
comparator; their net-effort measure, stop rules and "target zero" counts are
defined in the [bundle protocol](./journey-learning-test-bundles.md) and are not
restated here. In a usability session each bundle contributes one task: story
once and promise ownership (R-J4 and T4), pre-visit pack (T3), change impact
(T3 with a changed assessment), accessible handover (R-J5 and R-J6), and
review-ready funding evidence (T3 for a finance or grants officer). Any stop
rule firing ends that task and is logged as a finding.

## Measures (aggregate only)

| Measure | Per role report | Notes |
| --- | --- | --- |
| T0 completion unaided under 5 minutes | Count of n and percent | H1 hypothesis |
| SUS | Median and range | H2; SUS is not accessible to every participant, so offer a read-aloud or plain-language alternative and report how many used it |
| Task success and assists | Count per task | An assist is a prompt from the moderator |
| Manual route used | Count per task | Using it is not a failure |
| Stop-rule or consent-blur events | Count | Target zero; any nonzero is reported, not averaged away |
| Accessibility barriers found | Count with severity | Only for participants who volunteered AT use |

## Findings log

Every finding is logged without participant identity.

| Field | Content |
| --- | --- |
| Id | UF-001 and up |
| Task and role | For example T4, programme coordinator |
| Observation | Plain-language, paraphrased |
| Severity | 4 Blocker: task cannot be completed or a boundary is crossed; 3 Major: completed with an assist or a serious workaround; 2 Minor: hesitation or recovery; 1 Note |
| Evidence class | Moderated participant, proxy participant, or synthetic walkthrough (not user validation) |
| Backlog link | Issue number, or "no issue yet" with the reason |
| Status | Open, linked, fixed and retested, accepted risk (named owner) |

A severity 4 finding opens a backlog issue before the session report is
closed. A finding is closed only by a retest with a participant, not by a
code change alone.

Log (blank):

| Id | Task and role | Observation | Severity | Evidence class | Backlog link | Status |
| --- | --- | --- | --- | --- | --- | --- |
| None recorded | | | | | | |

## Results record (blank)

| Role | Evidence class | n | T0 unaided under 5 minutes | SUS median and range | Outcome |
| --- | --- | --- | --- | --- | --- |
| All roles | None | 0 | Not run | Not run | Not run |

Outcome vocabulary: Supported, Not supported, Inconclusive (too few
participants, mixed result or sessions not completed), Not run. Negative and
inconclusive outcomes are reported in full with the same prominence as
positive ones. A synthetic walkthrough, an agent review or an engineering test
is labelled "not user validation" wherever it appears and never fills a
participant row.

## Acceptance criteria status for issue #155

| Criterion | Status after this slice |
| --- | --- |
| Test plan names tasks, participants per role, accessibility support, consent and data handling | Draft written on this page; the owner has not reviewed or agreed it, and no recruitment route exists. Not proven as an agreed plan |
| Task scripts derive from the profile journey contract and learning-test bundles | Drafted with traceable sources (UX-01 to UX-08, J1 to J6, bundles); wording not reviewed by the owner, and none run |
| Measures are aggregate only and the audit-use statement is agreed with staff first | Unmet. Rules and statement are drafted; no staff agreement is recorded |
| Findings are logged with severity and linked to backlog issues | Unmet. Log format defined; no finding exists |
| Results record negative and inconclusive outcomes; synthetic walkthroughs labelled | Unmet. Template and labelling rule only; no results exist |

Dependencies #150 and #151 and the relation to #128 are not resolved by this
page. A real customer or proxy participants, a DPO decision and staff
agreement are still needed before any session.

## Next slices (proposed)

* Owner review and agreement of this plan and the audit-use statement with
  staff representatives.
* DPO and ethics decision on lawful basis, recording and retention.
* A pilot with 2 to 3 proxy participants to test the scripts themselves,
  labelled as a pilot and not as validation.

## Delivery status record (2026-11-04, #155)

Merged engineering evidence is limited to this plan (#1004): drafted tasks,
participants per role, accessibility support, consent and data handling,
aggregate-only measures, findings and results templates. No participant,
session, staff agreement, finding or result exists, and the plan is not
reviewed by the owner.

All five acceptance criteria remain unmet: the plan is not agreed, the scripts
are unreviewed and unrun, the audit-use statement has no staff agreement
(SA-010), no findings are logged, and no results (including negative and
inconclusive outcomes) exist. What remains is human work: owner review, a
DPO and ethics decision, staff representative agreement, recruitment of real
or proxy participants, a labelled pilot, and moderated sessions with
assistive-technology users. No code slice can advance these. Dependencies #150
and #151 stay open for the WCAG and assistive-technology evidence. Nothing was
ticked or closed.
