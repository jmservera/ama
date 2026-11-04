---
title: Journey learning-test bundles with non-AI comparators
description: Experiment protocol for the five candidate journey learning-test bundles, with comparators, net-effort measures, stop rules, boundaries and scope exclusions (issue #129, first slice)
ms.date: 2026-11-04
ms.topic: reference
---

## Scope and evidence label

First slice of [#129](https://github.com/jmservera/ama/issues/129) under #123.
This page is a **protocol**: a test design for hypotheses from the desk-based
[customer journey atlas](./customer-journeys/customer-journey-atlas.md). It
records no experiment run, no measured result, no user validation and no
approval. Sources are
[ADR 0003](../../../adrs/0003-journey-derived-capabilities-runtime-fit.md)
decisions 1 to 5 and the PRD section "Candidate journey learning tests"
(`docs/prds/zava-forward-retrofit-programme-demonstrator.md`).

Atlas opportunity IDs O01 to O24 are test-design candidates, not approved
features. The bundle to opportunity mapping below is the PRD author's mapping
and is **not yet confirmed by the atlas owner**.

## Bundles

| Bundle | Atlas IDs | Linked requirements | Non-AI comparator | Stop rule |
| --- | --- | --- | --- | --- |
| Story once and promise ownership | O01, O02, O03, O15 | FR-045, FR-048, AC-062, AC-064, GOAL-004 | Manual re-asking and chase log | Stop if representative or consent boundaries blur |
| Pre-visit pack and readiness rehearsal | O06, O08, O09 | FR-048, FR-049, AC-062, AC-063, AC-065 | Current visit preparation | Stop if an offer reads as a commitment |
| Change impact and evidence reuse | O07, O16 | FR-008, FR-043, AC-011, AC-013, AC-051 | Manual dependency check | Stop if reuse transfers an approval |
| Accessible handover and aftercare | O13, O14 | FR-049, FR-014, AC-063 | Paper handover | Stop if handover closes an open remedy |
| Review-ready funding evidence | O16, O17 | FR-019, FR-042, AC-050 | Manual evidence pack | Stop if a submission or award is inferred |

O16 appears in two bundles in the PRD. The atlas owner should confirm whether
that is intended or whether one bundle owns it; until then each run must say
which bundle it counts O16 under, so effort is not counted twice.

## Out of scope

Opportunities O10, O18, O19 and O20 stay out of the next accepted application
exercise build (ADR 0003 decision 4). No run, comparator or measure in this
protocol covers them. Other opportunities (for example O04, O05, O11, O12 and
O21 to O24) are not in any of the five bundles and are not covered here.

## Common design rules

* Each bundle runs as an experiment with two arms on the same constructed
  cases: the deterministic non-AI comparator above, and the same workflow with
  deterministic records and state transitions in the existing schema (ADR 0003
  decisions 1 and 2). Assistance, where used, is an arm of the experiment, not
  a precondition of it.
* The non-AI arm is first-class. A result that favours the comparator, or no
  difference, is a valid learning outcome.
* Any AI use is registered under FR-036 and reaches only the existing five
  assistants, proposal-only, with independent human review and proactive scans
  off by default. A new assistant or wider authority is a registry change, not
  part of a bundle. A non-AI comparator never waives CON-009.
* AI-unavailable behaviour: with assistance off or failing, every step stays
  completable by the manual path and shows plain text "assistance not
  available"; nothing blocks viewing a case or finishing the manual task.
* Human approval, resident consent and representative authority stay
  server-side decisions. Offers are never commitments, reuse is never approval,
  and a handover or funding step never closes a remedy or infers a submission.
* Cases are constructed or fictional. Representative data follows the
  permitted-field matrix (NFR-003); its retention stays Unknown until the DPO
  decides, so runs retain no representative data beyond the run.
* Any screen used keeps the Fluent 2 design system, the WCAG baseline, the
  plain-language content standard, non-colour status signals, keyboard
  operation and reduced motion. Participants may use the manual path at any
  time without detriment.

## Net-effort comparison (NFR-009)

For each bundle and arm, record per case, in minutes unless stated:

| Component | What is counted |
| --- | --- |
| Preparation | Time to assemble inputs before the task |
| Checking | Time verifying the work, including any AI proposal |
| Correction | Time fixing errors found at checking or later |
| Coordination | Handoffs, chases and waiting-for-reply effort by staff |
| Resident effort | Repeat explanations, extra contacts and forms for the resident or representative |
| Support cost | Help-desk or officer time resolving problems the arm caused |

Net effort is the sum of all six components. An arm that moves effort from staff
to the resident is not a saving. Report the median and the range, state the
number of cases, and label every figure as constructed-case evidence.

Saved minutes are **capacity** until Finance validates them (ADR 0003 decision
5). No run may report them as cash, headcount or benefit realised.

## Per-bundle learning questions

| Bundle | Question the experiment answers | Measures beyond net effort |
| --- | --- | --- |
| Story once and promise ownership | Does a scoped, corrected account cut repeat explanations without blurring authority? | Repeat-ask count; promises without an owner; authority or consent breaches (target zero) |
| Pre-visit pack and readiness rehearsal | Does a cited pre-visit pack reduce missing facts and abortive visits? | Missing-fact count at visit; offers misread as commitments (target zero) |
| Change impact and evidence reuse | Does a dependency check catch stale evidence that a manual check misses? | Stale items escaped; approvals wrongly carried over (target zero) |
| Accessible handover and aftercare | Can the resident use the handover material, and are open remedies still visible after it? | Accessibility defects found; open remedies hidden by handover (target zero) |
| Review-ready funding evidence | Does the pack reduce reviewer return requests without implying submission or award? | Reviewer returns; unsupported statements; inferred submissions (target zero) |

A nonzero count on a "target zero" measure triggers the stop rule for that
bundle and is reported, not averaged away.

## Acceptance criteria status for issue #129

| Criterion | Status after this slice |
| --- | --- |
| Bundles: story once, pre-visit pack, change impact and evidence reuse, accessible handover and aftercare, review-ready funding evidence | Unmet. All five are specified as a protocol and a net-effort helper exists; none has been run as an experiment, and no measured comparison exists |
| Opportunities O10 and O18 to O20 stay out of scope | Met for this protocol (see Out of scope). Not a delivered-build property, so it is not independent evidence for the experiments |
| Atlas owner confirms bundle to opportunity mapping | Unmet. Needs the atlas owner; the O16 overlap is the specific question |

Open dependencies from ADR 0003: owner acceptance of the BRD and PRD versions
it names, and the DPO decision on representative data retention. Neither is
decided here.

## Next slices (proposed)

* Atlas-owner confirmation of the mapping, including O16.
* Delivered (second slice, 2026-11-04): `learning_test_bundles.py` in
  `src/core` sums the six effort components per arm, reports median and range,
  applies each bundle's "target zero" stop rule, rejects out-of-scope
  opportunities and labels saved minutes as capacity. It is a pure helper
  tested on synthetic numbers only; it holds no representative data, calls no
  AI and records no run. Wiring it to a screen or storing run records waits for
  the owner mapping and the DPO retention decision.
* A first bundle run with its stop rule checked, then the other four.
