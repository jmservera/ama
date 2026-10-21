---
title: Cohort and Missing-Data Evaluation Review Pack (DRAFT, issue 222)
description: Owner review pack for a synthetic paired-scenario manifest and a proposed human evaluation protocol; draft, unapproved and not executed
ms.date: 2026-10-20
ms.topic: reference
---

> [!WARNING]
> DRAFT, UNAPPROVED, NOT EXECUTED. Revision v0.2.0 (owner-authorised correction,
> 2026-10-20) is returned for owner approval BEFORE any evaluator work. Everything
> here is an agent-authored proposal under issue #222. Nothing is an
> approved label, a held-out set, a measured result, an operational threshold or
> fairness evidence. No participant, study, model run or live data is authorised.
> The independent reviewer, second reviewer, adjudicator and custodian are
> UNFILLED. All six #222 acceptance criteria remain unmet.

## Revision v0.2.0 (correction, not a new Review)

Owner decisions 2026-10-20 retained the three factor families (sensor or source
completeness, accessibility or contact need, appointment history).

| Change | Effect |
| --- | --- |
| CM-A03 split | CM-A03 now varies only a separate contact field and is `representation_pending` (ranking has no contact input); CM-A04 covers an accessibility adjustment recorded as text, which feeds support status (RV-002) |
| CM-C01 split | CM-C01 varies sensor data only; new CM-C02 varies the source record only |
| Ranking binding | Each deterministic expectation names a `ranking_binding` that the structural test checks against the unchanged `rank()` (RV-001); the comparison basis is the same case id ranked twice in a fixed neighbour set |
| Open safety wording | An open safety case ranks ahead of every case without one. Inside open safety the order is support, then waiting days, then stage, then case id, so a supported case waiting 1 day outranks an unsupported one waiting 10 days (RV-004; corrected 2026-10-21 after independent assessment). Rank 2 in the CM-C01 test is specific to its fixed neighbours; the AI top-k exception of `ai_eval.py` is stated |
| Unknown support | PP-01 is a POLICY PROPOSAL with three options; ranking is not changed |
| Sample and error options | SO-1 to SO-3, ED-1 to ED-3 and uncertainty methods replace the arbitrary 30 and 10 percent |
| Review burden | Defined over eligible cases, with zero eligible not computable |
| Held-out | Fresh, unexposed scenarios with new IDs; none drafted; all roles UNFILLED |
| Structural test | The support exemption applies to `support_state` pairs only, with a regression proving an unrelated support change is rejected |

RV-006 (claims without persisted output) stays a note: the fresh gate receipt
is the persisted evidence. The original Review findings are not rewritten; see
the correction record under `.copilot-tracking/changes/`.

## Purpose and boundaries

The owner asked for a versioned synthetic manifest and a human evaluation
protocol to be prepared for review before any implementation. This pack
describes the [draft manifest](../../../../src/agents/evals/cohort_manifest_draft.json)
(`cohort-manifest-draft-v0.2.0`, registered in the
[eval registry](../../../../src/agents/evals/registry.json)) and proposes how a
later, separately authorised evaluation could use it.

* Builds on the #108 offline harness (`src/agents/evals/ai_priority_golden.json`, `ai_eval.py`) and the delivered #174 registry and fixture. No new service, evaluator, API or UI.
* Requirements: PRD FR-054, FR-012, NFR-014, AC-073 and OQ-018 in the
  [PRD](../../../prds/zava-forward-retrofit-programme-demonstrator.md); the
  Measure gate in the [addendum](../../../case_study_48_addendum.md#responsible-ai-release-position-2026-10-14).
* Not covered: cohort selection, lawful analysis fields, live thresholds, legal
  or DPO acceptance, participants, recruitment, costs or any model or paid call.

## What the draft contains

| Part | Content |
| --- | --- |
| Status | `DRAFT`, `UNAPPROVED`, `NOT EXECUTED`, synthetic, `fairness_evidence` false, `dataset_role` development draft, never held-out |
| Source versions | PRD 0.17.0, ranking policy 1.0.0 (unsigned draft), registry 2026-10-16, golden set 2026-10-09, fixture 1.2.0 seed 174; no model or prompt run |
| Scenarios | 14 stable IDs (CM-S01 to CM-T01) across the three factor families; 10 pairs differing in one factor (CM-A03 representation pending) and 4 sample or aggregation cases |
| Defect seeds | SD-01 to SD-06, including one critical seed (open safety case dropped, CM-C01 and CM-C02) and one unconfirmed candidate (SD-01) |
| Reconciliation | Four illustrative arm templates with an arithmetic identity per arm |
| Proposals | Sample-size, error-rule and uncertainty options, a proposed zero critical-miss tolerance and one Unknown-support policy proposal, each needing named approval |
| Acceptance trace | AC1 to AC6 each marked Not met with what would meet it |

Arms are neutral placeholders (ARM-A, ARM-B). They do not propose cohorts.
Expected AI-task outcomes are `unlabelled` until an independent labeller supplies
them. The deterministic expectations follow what ranking policy 1.0.0 reads
(open safety, support status, days in stage, stage order, case id) and does not
read (sensor data, source completeness, appointment history, contact
preference), so most pairs can only test invariance.

## Adverse and limiting evidence retained

* Ranking policy 1.0.0 is "Draft rule order, not yet signed off by an owner"; a manifest cannot be approved against an approved policy yet.
* Candidate defect SD-01: `support_status` can return Unknown, but the ranking
  `support` key treats only Yes as priority, so Unknown sorts with No while the
  case carries a human-review reason code. This is an observation of current
  code, not a verified production finding. The test now asserts this current
  behaviour; any change is the separate policy proposal PP-01 and is not made here.
* The #108 harness has no cohort field and lists "no independently labelled
  held-out split, approved thresholds or cohort sample sizes" as open.
* The draft is committed in the open and written by an agent, so it cannot be a
  held-out set or an independent oracle. The earlier multi-factor pairs were
  split (see Revision v0.2.0).
* The 60,000-home fixture carries tenancy and consent states but no cohort
  labels, so counts from it would not reconcile to approved labels.
* The earlier illustrative values (30, 0.10) had no statistical basis and are
  replaced by the options below. Zero critical misses is retained as a
  proposal, not an activated threshold.

## Sample-size, error-rule and uncertainty options

Proposal only; the owner chooses. With zero errors in n evaluated cases the exact
one-sided 95 percent upper bound on the error rate is 1 - 0.05^(1/n), so the
smallest n reaching a target t is ceil(ln 0.05 / ln(1 - t)).

| Option | Target upper bound | Minimum evaluated | Note |
| --- | --- | --- | --- |
| SO-1 | 10 percent | 29 | Cheapest; weak assurance |
| SO-2 | 5 percent | 59 | Middle |
| SO-3 | 2 percent | 149 | Strictest; small arms stay insufficient |

* Error rules: ED-1 breach on observed rate above target; ED-2 breach only when the exact lower bound exceeds target; ED-3 block when the exact upper bound exceeds target (precautionary).
* Uncertainty methods: UM-1 Clopper-Pearson exact (proposed default for small n), UM-2 Wilson score, UM-3 rule of three (quick check only).
* Cases from one scenario are not independent, so these are lower bounds on evidence, not a representativeness claim.
* Zero critical misses stays PROPOSED. Zero observed in n does not prove a zero rate (upper bound about 3/n), so reports state n and the bound. The existing harness exception applies: not critical when open safety cases outnumber k and every pick is one.
* The reconciliation templates use SO-1 and ED-1 only for arithmetic, not as a recommendation.

## Unknown-support policy proposal (PP-01)

POLICY PROPOSAL ONLY; no ranking change. Options: A keep current behaviour (Unknown
ties with No); B add an extra review priority for Unknown through a new signed-off
policy version; C leave order alone and add a separate review-queue flag. Needs a named
policy owner, Resident Engagement and DPO, and a separate authorisation.

## Proposed held-out split and custody

Proposal only. A held-out split does not exist (`held_out_split.status` is
`NOT CREATED`).

* Create the split only after the owner approves cohorts, fields and the
  manifest structure. A named custodian who does not write prompts, rules or
  tuning data holds it.
* The custodian, not the implementer, selects which fresh scenarios are held out,
  fixed before any model or rule change is tested against them. Held-out
  scenarios must be newly authored from a separate, unexposed source with NEW IDs
  and NEW inputs. No CM- ID, input or proposed answer in this manifest may be
  moved, relabelled or reused as held-out, because its exposure cannot be
  undone. None is drafted here, and all roles (independent reviewer, second
  reviewer, adjudicator, custodian) are UNFILLED.
* Held-out inputs and expected outcomes are stored outside the repository and
  outside prompt, retrieval and tuning paths. Only IDs and content hashes are
  recorded in the evaluation record.
* A held-out answer never enters a prompt, example, fine-tune, rule change or
  test fixture. A leaked item is retired and replaced, and the leak is recorded.
* This draft manifest is the development set. Using it for tuning is allowed
  and expected; passing it proves nothing about held-out behaviour.

## Proposed independent reviewer protocol

* Labels are produced by an independent competent reviewer named by the owner,
  who did not author the scenarios or the system under test. The agent-authored
  expectations here are proposals for that person to confirm, change or reject.
* Each held-out item is labelled by two reviewers working separately from the
  source facts, with the system output hidden; reviewers record outcome,
  justification and the policy or source version relied on.
* Disagreement goes to a named adjudicator who is a third competent person. The
  adjudicator records the decision and rationale. Unresolved items stay
  unlabelled and are excluded from scoring with a count, not forced to a label.
* Reviewers see only synthetic material. No resident, staff or personal data is
  used and no participant is recruited under this pack; any human study needs a
  separate owner authorisation, consent, accessibility and privacy design.
* Reviewer notes are retained. Agent proposals are never counted as a reviewer.

## Small-sample, unknown and critical-error handling

* An arm below the approved minimum denominator is reported `insufficient` with
  its counts and no rate presented as a result. A zero denominator is reported
  not computable, never 0 percent.
* Missing or unlabelled cohort records form an explicit unassigned bucket so
  totals reconcile. Unknown is a distinct state, not a negative.
* Critical errors (for example an open safety case missing from the recommended
  set) are counted per arm and per scenario, fail the run on a single
  occurrence under the proposed zero tolerance, and are never pooled away.
* A per-arm breach blocks activation pending named human disposition. A pooled
  rate under the threshold is not a clearance (scenario CM-T01).
* Unapproved or absent thresholds block; they are never defaulted to pass.

## Review burden and uncertainty reporting plan

* Per arm report eligible, evaluated, excluded with reason, not evaluable,
  errors and review required, with the identity
  eligible = evaluated + excluded + not evaluable.
* Review burden is review required divided by eligible, because review required
  includes eligible cases that were not evaluated (for example the unassigned
  bucket in RC-M03, 5 of 5). Counts stay visible. Zero eligible is
  not computable, never 0 percent; an unmeasured burden is Not run, not green.
  A separate evaluated-only review count may be added but never shares the
  eligible numerator.
* Report an interval for every rate or state insufficient. The method is an
  owner decision from the options above; none is computed in this draft.

## Traceability to issue acceptance criteria

| AC | Criterion (short) | Status | Draft coverage | What would meet it |
| --- | --- | --- | --- | --- |
| AC1 | Paired cohorts evaluated against an approved manifest | Not met | Scenarios and factor families | Owner approval of the manifest and an executed evaluation |
| AC2 | All seeded exclusion or deprioritisation defects detected | Not met | SD-01 to SD-06 | A run detecting each seed and the SD-01 decision |
| AC3 | Counts, errors, review burden and uncertainty reconcile | Not met | Reconciliation templates and reporting plan | Real-run counts that reconcile |
| AC4 | Small or missing samples remain insufficient | Not met | CM-M01 to CM-M03 | A run reporting these insufficient |
| AC5 | Exceeded or unapproved thresholds block, not averaged | Not met | CM-T01 and proposals | Approved thresholds and a run that blocks |
| AC6 | Owner approval before live use; synthetic is not fairness evidence | Not met | Status literals | Owner and DPO approval under OQ-018 |

## Owner review checklist

* [ ] Confirm or replace the factor families and the neutral arms; decide the cohort set and lawful analysis fields (OQ-018, with DPO and Resident Engagement).
* [ ] Decide whether SD-01 (Unknown support treated as No) is a defect or accepted policy behaviour, and whether the ranking policy is to be approved first.
* [ ] Confirm the revised scenario inventory (CM-A03 and CM-C01 now split into CM-A03, CM-A04, CM-C01, CM-C02) or ask for further splits, and decide the contact-field representation for CM-A03.
* [ ] Choose among PR-01 to PR-03 options (SO, ED, uncertainty methods, zero critical misses as proposed), with the named approver role, and decide PP-01.
* [ ] Name the independent labeller, second reviewer, adjudicator and held-out custodian.
* [ ] Approve or change the held-out custody, leakage and adjudication rules above.
* [ ] Choose the uncertainty method and the observation window.
* [ ] Decide whether implementation of per-cohort reporting in the offline harness may start, and under which separate authorisation (#108 and a separate owner authorisation).

## Unresolved decisions

* Cohort set, lawful fields, sufficiency rule and every numeric threshold.
* Named human roles and independence rules.
* Status of ranking policy 1.0.0 and of candidate defect SD-01.
* Whether any human study is ever authorised, and its consent and accessibility design.
* Whole-issue acceptance, #108 actual-model and human results, and live use stay open.

## Evidence and validation

The structural test `src/agents/tests/test_cohort_manifest_draft.py` checks only
that the draft stays labelled unapproved, seed-to-scenario links and pair isolation
are consistent (the support exemption is limited to `support_state` pairs), the
ranking-bound expectations (the sensor, source and appointment fields are carried on each case and a missing-data exclusion or appointment penalty is shown to fail the check) still hold against the unchanged `zava_forward.core`
`rank()`, the sample arithmetic and review-burden fractions are consistent, all
held-out roles stay UNFILLED and each AC is Not met. It is not an
evaluation and does not read this page.
