<!-- markdownlint-disable-file -->
---
title: Decision Model Value - Experiment Design
description: Frozen-input four-arm model ablation and paired human-effort protocol
ms.date: 2026-10-10
---

## Phase 4: Approach

LLM task-quality/performance experiment followed by an exercise user-effort
trial. Ten working days once reviewers and participants are available. No
experiment run or outcome is claimed in this design.

## Arms and What the Comparison Means

Every arm uses identical permission-filtered inputs, approved schema, parsers,
deterministic calculations/validation, human sign-offs and read-only tools.
Only semantic selection/support/drafting placement varies.

| Arm | Treatment | Question answered |
| --- | --- | --- |
| R: rules and templates | Deterministic candidate extraction; explicit conflict/unknown; manual selection and templated narrative. No semantic model. | Is AI needed at all for this task? |
| D: Decision-assisted | Same parsers; Decision 1 candidate selection and support screening; template narrative. No generative drafting. | Can narrow typed tasks replace a generative call? |
| A: generative agent | Same retrieved inputs/tools; GPT-4.1-mini selects candidates, proposes support assessments and drafts cited narrative. No Decision 1. | Current agent-design comparator. |
| H: hybrid agent | A with candidate selection delegated to Decision 1 and Decision 1 screening of drafted claims. GPT-4.1-mini still drafts and the agent still orchestrates. | Does Decision 1 improve the agent rather than replace it? |

Candidate and support microbenchmarks bypass orchestration and supply the
exact same frozen inputs/options to D/A/H. Pack runs include retrieval, tools,
drafting, failure recovery and human review. A/H use the same generative model,
prompt, tool limits and settings apart from the specified intervention.

H versus A changes two components. On held-out automated runs also replay two
ablations: A+selection-only and A+screen-only. They attribute any hybrid gain;
they do not create extra human arms or a post-hoc winner selection. H5 screening
uses the same frozen A drafts for A+screen-only to isolate screening effects.
Full H runs separately measure end-to-end compounded outcomes.

An agent is a workflow, not a competing model. A D win supports replacing a
bounded component, never retrieval, coordination, narrative generation or
human decision ownership. Document if A is only an experimental realization
of a designed task rather than an already shipped agent.

## Task Scope

Primary: a fictional competitive retrofit-funding application with staged
extraction, semantic candidate choice, supported narrative, deterministic
validation and independent reviewed export. Use EXA-015 simulated funding
rules, not a current real award scheme.

Twelve evaluated dispositions per pack: four semantic fields (EPC band,
measure, invoice description, funding narrative) and eight deterministic or
human-only controls (home identity, route/version, eligible cost, currency,
match contribution, grant calculation, declaration, signature). Bind each to
the applicable source/schema mapping; fields not present in a chosen template
are scored through a declared control probe, never silently added to a live
schema. Semantic fields test FR-039; controls test that AI cannot fill or
approve protected values. Coverage excludes human-only/calculated fields.

Transfer probes: technical/invoice evidence support and case-handoff note
support. No new resident triage, legal eligibility or safety-classification
task activation. Summaries/drafts remain proposals.

## Dataset and Gold Labels

Reuse generator conventions and source hashes from the retained programme,
not its historical stages as correctness labels. Construct 120 new independent
case/building/document families: 30 tuning, 30 calibration, 60 held-out.
All variants of a family remain in one split. Seed and hash the split manifest;
do not expose the held-out labels to prompt authors.

Allocate the 60 held-out packs in advance to 15 clear structured, 15 ambiguous
but resolvable, 15 contradictory/insufficient, and 15 adverse/stale/restricted
families. Primary class varies but controlled secondary defects may overlap.
Report overlapping slice denominators explicitly. Include shuffled options,
negation, stale versions, wrong home, wrong units, unreadable input, injected
instructions and missing evidence. All variants retain family grouping.

Two independent human engineering adjudicators review raw sources, permitted
candidate IDs, correct answer or required no-match, authority constraints,
claim support class and critical-error category before test execution.
Disagreements are adjudicated and recorded before unblinding. Unresolved rows
are quarantined with reasons and replacement families restore the planned
sample before any acceptance claim. Script/agent-generated labels alone
support provisional debugging, not accepted task quality.

The 60 packs yield 720 dispositions; do not treat correlated fields as 720
independent samples. Define critical categories and count each separately.
For claim screening construct supported/contradicted/insufficient labels,
balanced across families, with a minimum 20 held-out families per class.

The current evidence_support adapter is binary. Score its binary supported/
not-supported result against the collapsed gold labels and report this
separately. It cannot satisfy the PRD three-class macro-F1 by relabelling
abstentions as contradiction. A shadow-only registered three-option choice
experiment may test that distinction; freeze its prompt/threshold on calibration
data and validate the real provider contract before the held-out run. If not
implemented, mark the three-class gate Not evaluated, not passed.

## Freeze and Execution

1. Record dataset/source hashes, code commit, schemas/registry, role filters,
   models/deployment versions, prompts, limits and experimental assignments.
2. Tune only on 30 tuning families; calibrate only on 30 calibration families.
   Starting thresholds are selection p>=0.90, margin>=0.20 and support p>=0.95,
   margin>=0.20. Threshold changes apply to experimental configuration only.
3. Lock all configurations and labels. Run all arms against all 60 held-out
   packs, randomized within time blocks to reduce provider-load confounding.
   Use three repeated machine trials per family/arm; report all, not best-of.
4. Run option-order variants and ablations in grouped batches. Keep production
   state untouched. Failure trials are logged with input/version and route.
5. Run the 12-block human trial only after task safety gates pass. Do not select
   the twelve easiest packs or only cases where a model succeeded.

Share source limits and retrieval opportunities. Set and record a common
per-task wall-clock/retry ceiling before the run; exceeding it routes to
manual handling. Invalid model outputs, retries, throttle, fallback and
abstention remain in intention-to-treat denominators.

## Human-Effort Trial

Select twelve independent packs before testing: three from each primary
input category, disjoint from tuning/calibration. Each pack is run in all four
arms: 48 preparation sessions and 48 independent final-review sessions.
Recruit six representative preparers and at least two separate final reviewers;
label expertise and onboarding. No person handles the same pack/family twice,
prepares and finally reviews the same pack, or sees another arm's output.
Balance each preparer's eight sessions across the four arms; rotate arm order
and pack difficulty using a frozen assignment schedule.

Use a common workspace and training tasks outside the evaluation families.
Final reviewers see normalized, randomly coded outputs without model names.
Preparers cannot be fully blinded to assistance; record this limitation.
Measure active gathering, preparation, validation, review, correction and
re-review separately; sum preparer/reviewer person-minutes. Record provider
wait and elapsed completion time separately so faster tokens cannot masquerade
as staff savings. Include failures and manual fallback to completion.

For pack i and comparator C, reduction is (effort_C_i-effort_H_i)/effort_C_i.
Report the median of twelve ratios, not ratio of aggregate medians. Report
every block, range, assignment, completion failures and reviewer quality.
Set a 45-minute session ceiling with unfinished items counted as failures,
time-to-ceiling and separate remaining-work assessment, never as fast success.
Zero comparator effort is invalid measurement and must be investigated.

## Measurements and Analysis

* Selection: correct dispositions including required no-match; selected-value
  accuracy; coverage of predeclared answerable semantic fields; confusion
  matrix and critical errors by field/task/slice.
* Support: binary metrics and, only when truly produced, three-class macro-F1;
  missed unsupported claims, false alarms and supported-claim recall.
* Calibration: Brier score, reliability bins with counts and expected calibration
  error on selection/support probabilities separately. Generative self-reported
  confidence is not comparable provider calibration.
* Integrity: candidate/source ID/hash/locator binding, restricted leakage,
  unchanged source/control state and reviewed-export fidelity.
* Efficiency: p50/p95 machine and elapsed latency, active person-minutes,
  requests/tokens/retries, recorded charges and cost per correctly resolved
  item/complete quality-passing pack. Failures still contribute costs.
* Whole-life cost: report one-time harness/integration and ongoing review/
  maintenance separately. A sensitivity scenario with assumed volumes/wages
  must be labelled illustrative; do not invent actual staff wages or prices.

Use paired family-cluster bootstrap 95% intervals (10,000 resamples, fixed
seed) for accuracy differences, effort reduction and cost differences.
Repeated trials and fields travel with their family. Twelve effort blocks
give directional evidence, not a powered company-wide causal estimate.
Report uncertainty and intervals crossing the decision boundary as Inconclusive.
H3 meeting the point target only is a provisional exercise result; robust
value evidence additionally requires the lower interval bound above zero.
Report all comparisons; H3 is primary, others secondary, with no omnibus
"best model" claim or multiple-slice significance fishing.

## Gates and Architectural Decisions

Retain PRD selection accuracy/disposition/coverage, support macro-F1>=0.90,
zero critical misses/actions, 100% binding/export and 15% net-effort targets.
Additional H2/H5 margins are proposals to ratify before execution. Neither
720 dispositions nor 60 families proves zero future risk.

| Result | Next decision |
| --- | --- |
| R matches quality and AI fails incremental value | Retain rules/manual handling for that task; keep useful AI in other evidenced tasks. Negative findings satisfy learning, not an AI activation gate. |
| D passes H1/H2; H fails H3 | Replace only narrow generative selection with Decision 1; keep orchestration/drafting/review. |
| H passes H1/H3 and ablations explain benefit | Adopt Decision 1 as agent tool for proven tasks; preserve source review and calibrate each new task separately. |
| Both D and H pass | Choose per task using quality-passing whole-life cost and effort, not a single overall winner. |
| Accuracy passes, effort/value inconclusive | Retain shadow mode; enlarge independently sampled human blocks only under a newly frozen extension. |
| Critical gate fails | Do not activate failing task. Analyze errors on old test data; fix on development data and use new held-out families for retest. |

## Resources, Timeline and Out of Scope

Days 1-2: freeze dataset, task contracts, gold labels and assignment.
Days 3-4: implement isolated adapters/logging; tune/calibrate; verify real
provider responses and shadow-only permissions. Day 5: locked machine runs.
Days 6-8: human sessions and adjudication. Days 9-10: analysis, reproducibility
replay and tribunal evidence. If participants are unavailable, publish only
engineering results and explicitly leave human value Inconclusive.

Resources: one engineering operator, two independent label adjudicators,
six preparers and two independent final reviewers (adjudicators may review
outputs but remain blind to arms), real Foundry deployments, isolated local
evaluation state and protected evidence storage. Participant availability and
actual charge metadata are unresolved resources, not fabricated assumptions.

Out of scope: MVP redesign/deployment, all nine workflow acceptance, real
funding awards, resident contact, real retrofit outcomes, production legal
approval, autonomous control changes and training/fine-tuning.

## Evidence Deliverables and Enablement

Protected manifest/labels, append-only per-attempt results, session timing/
correction records, quality adjudication, all-arm metrics with intervals,
failure taxonomy and task-placement decision table. Commit only sanitized
aggregates and protocol; private geography/source payloads stay out of Git.

Independent replay must reproduce metrics from frozen logged outputs and one
new small batch within declared stochastic tolerance. Owner explains why each
task uses rules, Decision 1, generative agents or a hybrid, including rejected
alternatives. No partner-team or company outcome is claimed.
