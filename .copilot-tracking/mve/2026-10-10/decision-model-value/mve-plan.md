<!-- markdownlint-disable-file -->
---
title: Proper Warm Decision Model Value Experiment
description: Consolidated MVE proposal for task replacement and agent complementarity
ms.date: 2026-10-10
status: proposed
---

## Phase 5: Plan for Owner Review

Determine whether Microsoft Decision 1 improves the Proper Warm solution,
whether it should replace a narrow generative-agent task, or whether it adds
value as a tool within that agent. This is a ten-working-day learning
experiment, not another MVP rebuild. No results or execution approval are
implied by this proposal.

## Context and Business Decision

The continuing AMA MVP already demonstrates real Decision 1 inference and
generative assistance. Technical feasibility is observed; incremental value
is unknown. The primary customer task is preparing a fictional retrofit
funding application with sourced fields, narrative and reviewed export.
Use the existing generator and retained stock/programme context, with new
independent evaluation families. Do not use generated history as gold truth
or invent real company outcomes.

The owner chooses placement after evidence. Compare four arms on the same
inputs, schema, permissions, validators, calculations and human authority:

| Arm | Semantic treatment |
| --- | --- |
| R | Rules/parsers, templates and manual review; no semantic model |
| D | Decision 1 selects candidates/screens support; templates draft |
| A | Generative agent selects, assesses support and drafts |
| H | Agent delegates selection and draft-support screening to Decision 1 |

A versus D tests replacement of a bounded semantic component. H versus A
tests complementarity; H versus R tests whether AI is worth the overhead.
Selection-only and screening-only automated ablations explain any hybrid
gain. Decision 1 never replaces agent orchestration or human accountability.

## Prioritized Hypotheses and Success/Failure

| Hypothesis | Proposed decision gate |
| --- | --- |
| H1: safe candidate selection | >=95% correct dispositions, >=98% selected accuracy, >=50% answerable semantic coverage, 100% source binding, zero critical unsupported selections/prohibited actions |
| H2: economical bounded replacement | H1 passes; D-A accuracy difference 95% lower bound >=-2 points; >=20% lower cost/correct item OR p95 machine latency; no human-effort regression |
| H3: complementary net effort, primary value hypothesis | H passes quality; median paired complete-pack active effort reduction >=15% versus A and R; no final-quality regression or critical miss. Positive lower uncertainty bound supports robust rather than merely provisional value. |
| H4: selective semantic placement | Ambiguous tasks meet value gates while clear structured fields favor quality-equivalent cheaper/no-more-effort rules |
| H5: useful support screening | Support macro-F1>=0.90 when genuinely three-class; zero critical misses; >=50% fewer noncritical unsupported draft claims reaching review and <=2-point supported-recall loss versus A |

PRD quality, integrity and 15% effort targets remain intact. H2/H5 comparative
margins are additional proposed targets requiring freeze before execution.
Failure of a quality/safety gate blocks that task regardless of savings.
Missing data/participants or wide uncertainty yields Inconclusive.

## Dataset, Controls and Analysis

120 independent case/building/document families: 30 tuning, 30 calibration,
60 held-out. Keep variants together. The 60 held-out packs have 12 declared
dispositions each (720 total): semantic fields plus deterministic/human-only
controls. Four primary difficulty categories have 15 families each. Support
probes balance supported/contradicted/insufficient labels with at least 20
held-out families per class.

Two independent human adjudicators freeze gold labels before testing. Script/
role-agent labels are provisional, not accepted human truth. All arms receive
the same authorized candidates/sources. Human-only and calculated controls
are excluded from semantic coverage and must not be filled by a model.

Tune on tuning families only; calibrate thresholds on calibration only.
Initial candidate p>=0.90/margin>=0.20; support p>=0.95/margin>=0.20.
Freeze hashes, versions, prompts, assignments and configuration before test.
Run three repeated machine trials per held-out family/arm in randomized time
blocks. Retain every failure, retry and manual fallback, not just successes.

Measure correctness, coverage, critical errors, calibration, provenance/export,
machine/elapsed latency, tokens/charges and cost per correctly completed item.
Compute paired family-cluster bootstrap 95% intervals with 10,000 resamples.
Fields/repeated trials are correlated, not independent samples. Report every
task/slice denominator and adverse outcome.

The deployed support adapter is binary: its collapsed-label metrics cannot
stand in for three-class macro-F1. A separately frozen, shadow-only three-option
choice test may evaluate that gate. Otherwise report it Not evaluated.

## Human Trial and Responsible AI

Twelve preselected independent pack blocks, three per difficulty category;
all four arms per pack: 48 preparation sessions plus independent final reviews.
Six preparers handle eight sessions each, balanced across arms. At least two
separate final reviewers inspect anonymous normalized results. Nobody sees
the same family twice or reviews their own preparation. Rotate order and
difficulty with a frozen schedule; training uses separate families.

Record gathering, preparation, validation, review, correction and re-review
person-minutes; report provider wait/elapsed time separately. For each pack,
calculate (comparator effort - hybrid effort)/comparator effort; take the median
of twelve ratios and publish every block. Include unfinished sessions at a
45-minute ceiling as failures, not speedy completion.

No company staff or booked participants are assumed. Real representative
engineers can provide exercise-effort evidence, not company productivity
claims. Until available, only engineering findings can be reported.

All work is read-only/shadow outside the deployed ledger. No sending, award,
payment, consent, legal judgement or operational rule activation. Stop a task
on restricted leakage, critical unsupported fill, prohibited action or silent
failure. Positive finite test results do not prove zero population risk.

## Vetting, Resources and Schedule

Business alignment, problem clarity and next decisions pass for the exercise.
RAI and user-value evidence are conditional on controls and real participants.
The experiment avoids demo/mini-MVP scope; no company/partner validation is
invented. The missing-user red flag limits conclusions, not protocol design.

One engineering operator, two independent adjudicators, six preparers and two
final reviewers; actual Foundry deployments, isolated evaluation state and
protected evidence. Costs are measured despite the current budget override.

| Working days | Deliverable |
| --- | --- |
| 1-2 | Source/split manifest, gold labels, hypotheses and schedule frozen |
| 3-4 | Minimal harness/adapters, contract validation, tuning/calibration |
| 5 | Locked all-arm machine runs and ablations |
| 6-8 | Human effort and independent review sessions |
| 9-10 | All-arm analysis, failure report, replay and placement decision |

Timeline starts when people are available. If unavailable, produce a machine
report with human value Inconclusive rather than simulated timings.
Out of scope: new MVP deployment, full workflow acceptance, fine-tuning,
actual funding success, real resident contact and production readiness.

## Outcomes, Iteration and Enablement

| Observation | Action |
| --- | --- |
| Rules suffice / AI adds no value | Retain simpler task path; report negative learning |
| D passes replacement but H lacks benefit | Replace narrow generative task only |
| H passes net-effort and quality | Add Decision 1 as agent tool for evidenced tasks |
| Both pass | Select per-task whole-life cost, quality and effort |
| Quality passes but benefit unclear | Continue shadow; preregister additional independent blocks |
| Critical failure | Do not activate; fix on development data and retest on new held-out families |

Deliver protected attempt/session evidence, sanitized all-arm metrics with
intervals, rejected alternatives and a task-placement table. Preserve old
failures; no threshold tuning on held-out results. This experiment may reach
a useful negative finding without proving that every agent is unnecessary.

Owner or second engineer replays a frozen batch and reproduces calculations
without the original author. A real partner engagement would add progressive
joint ownership; none is claimed here.

## Authoritative Protocol and Supporting Artifacts

The [detailed execution protocol](./experiment-design.md) specifies assignment,
denominators, ablations, fallback, metric calculations and stop rules.
[Context](./context.md), [hypotheses](./hypotheses.md) and
[vetting](./vetting.md) record Phases 1-3. The
[accepted PRD](../../../../docs/prds/proper-warm-retrofit-programme-demonstrator.md)
and [research synthesis](../../../../docs/ideas/typesafe-system-one-agent-fit.md)
are the evidence basis. This proposed plan does not change PRD acceptance.

Owner review is requested before execution. No backlog bridge is produced.

Design delivery: all five phase artifacts and knowledge-base links were
published on draft PR #58 as source `79de566`. Owner review was requested but
unavailable on 2026-10-10; no acceptance is inferred. The requested design
deliverable is authored and published. Execution, participant recruitment and
findings are separate future stages, not completed by this delivery.
