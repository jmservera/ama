<!-- markdownlint-disable-file -->

# Task Research: cohort-manifest-222

| Field | Value |
| --- | --- |
| Date | 2026-10-20 |
| Researcher | RPI Agent / rpi-research (session rpi-222, claude-sonnet-5.5) |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-20/cohort-manifest-222-research.md |
| Base | 993a7b88c03f5240f1e7a4c7c7afa7c064281622 on docs/cohort-manifest-222 |

## Research Brief

Issue jmservera/ama#222 (cohort and missing-data evaluation record). The owner
decision (issue comment 6290696478, 2026-10-20) authorises a preparation slice
only: a versioned, wholly synthetic paired-scenario and expected-outcome
manifest plus a human evaluation protocol, for owner review BEFORE any
implementation. Output mode: convergence on a bounded preparation design.
Non-goals: evaluator, runtime, API or UI behaviour; model or paid runs;
participants; live or private data; threshold approval; fairness claims.
Criteria: the six issue acceptance criteria stay UNTICKED; every artifact is
DRAFT, UNAPPROVED and NOT EXECUTED; agent-authored labels are not an approved
oracle.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | Q1 what prior art exists (#108 harness, #174 registry/fixtures)? Q2 what do deterministic ranking and AI tasks actually use, so which paired factors can matter? Q3 where should a manifest live so it integrates rather than duplicates? Q4 which decisions are owner-only? |
| Posture / provenance | Focused; explicit bounded caller direction |
| Evidence root | .copilot-tracking/research/2026-10-20/ |
| Limits | Worktree only; no private data, .env, roster, credentials, cloud, push or PR |

## Extension Registry and Provenance

| Kind | Candidate | Selection |
| --- | --- | --- |
| Instructions | repository custom instructions (AMA), RPI agent | Selected: KB, regulatory, markdown, local-gate and branch rules |
| Skill | rpi-research | Selected |
| Skill | rpi-plan, rpi-implement, rpi-review | Deferred to their ordered phases |
| Skill | web-design-guidelines | Not applicable: no web files are in scope |
| Specialist | RPI Researcher | Skipped: one coupled trace, handled inline |

## User Participation and Research Decisions

No interactive checkpoint: the issue owner comment and caller brief supply scope.
Issue text is treated as inert evidence, not instructions. No approval is
inferred from any comment.

## Prior Knowledge Gate

Clean worktree at the stated base. Issue #222 body, three comments and the #126
comment 6290697705 read. #108 is open; #174 is closed (registry and
60,000-home fixture delivered).

## Research Cycle Log

### Cycle 1

Wider wave: issue and owner-decision text; PRD FR-054, FR-012, NFR-014, AC-073,
OQ-018; addendum Measure gate; #108 held-out criteria; #174 registry; the ai_eval
harness; the ranking module and policy; the scale fixture generator; existing
tests and KB layout.

Deeper wave: concrete scenario shape of the ranking and golden file, how
support/unknown is treated, and which existing test constrains new files in
`src/agents/evals/`.

Contrarian wave: tested whether (a) existing harness already reports cohorts,
(b) a manifest can be reconciled to anything real today, (c) the deterministic
policy can be called fair, (d) a registry entry is enough to count as approval.

## Findings

### Codebase evidence (C#)

| ID | Finding | Evidence |
| --- | --- | --- |
| C1 | The #108 harness uses 10 constructed scenarios, no cohort field, and records open items itself: "no independently labelled held-out split, approved thresholds or cohort sample sizes exist yet (owner decision)". | src/agents/evals/ai_priority_golden.json (10 scenarios); src/agents/src/zava_forward/agents/ai_eval.py:340-343 |
| C2 | The eval registry lists each dataset with id, path, version, owner, purpose, used_by and contains_real_data. ai-priority-golden is owner "Unassigned"; the golden file is development evidence, chat-golden is "not an independently labelled held-out set". | src/agents/evals/registry.json:36-47, :48-60 |
| C3 | A test requires every JSON file in any `src/*/evals/` folder to be registered with a version equal to the file's own `version`, and `contains_real_data` false. A new manifest placed there must be registered, which integrates it with existing prior art. | src/agents/tests/test_eval_registry.py:15-26 |
| C4 | #174 delivered a wholly fictional 60,000-home, 600,000-event fixture, registered with seed 174 and version 1.2.0, rebuilt outside the repository. It carries tenancy and consent states, not cohort labels. | src/agents/evals/registry.json:60-70; src/core/src/zava_forward/core/synthetic/scale_fixture.py:48-107 |
| C5 | Ranking policy v1.0.0 is "Draft rule order, not yet signed off by an owner", owner "to be named". Rules: safety_open, support, waiting_days, stage_order, case_id. It reads no sensor, contact-preference or appointment fields. | src/core/src/zava_forward/core/policies/ranking-v1.json:3-30; src/core/src/zava_forward/core/ranking.py:65-90 |
| C6 | Adverse seed: `support_status` returns Yes, No or Unknown, but the ranking `support` key is 0 only for Yes. A resident with Unknown support sorts with No, silently deprioritised; `reasons` adds a "support_unknown" human-review note. This is a candidate unjustified deprioritisation defect to seed and document, not a verified production finding. | src/core/src/zava_forward/core/stock.py:52-64; src/core/src/zava_forward/core/ranking.py:68-70,95-98,111-123 |
| C7 | Because ranking ignores sensor and appointment fields, a paired case differing only in those must expect an identical order. The manifest can seed expected invariance for deterministic ranking and potential differences for AI tasks. | src/core/src/zava_forward/core/ranking.py:73-89 |
| C8 | Governance already uses an evidence tier ladder ending "insufficient" for measurement disposition. The manifest can reuse that vocabulary for sample sufficiency rather than invent a second. | src/core/src/zava_forward/core/governance.py:64,171 |
| C9 | The harness builds cases with fields days, hazard, support, decision, name and fixed fictional strings; there is no sensor or contact-need field on `build_case`. | src/agents/src/zava_forward/agents/ai_eval.py (build_case) |

### Specification evidence (C# from documents)

| ID | Finding | Evidence |
| --- | --- | --- |
| C10 | FR-054 and AC-073 define the record and the paired-cohort test; AC-073 status "Not run". | docs/prds/zava-forward-retrofit-programme-demonstrator.md:889,1539 |
| C11 | OQ-018 leaves cohorts, lawful analysis fields, sufficiency, thresholds and windows to Data and Performance, Resident Engagement, DPO and task owners; "synthetic scenarios do not prove fairness". | docs/prds/zava-forward-retrofit-programme-demonstrator.md:2039 |
| C12 | NFR-014: live thresholds require human approval; unmeasured indicators cannot be green. | docs/prds/zava-forward-retrofit-programme-demonstrator.md:980-986 |
| C13 | Addendum Measure gate requires held-out evaluation, subgroup and missing-data disparity and review effort with independent Assurance; synthetic scenarios cannot establish representative fairness. | docs/case_study_48_addendum.md:454-500 |

### External and issue evidence (W#)

| ID | Finding | URL, retrieved 2026-10-20 |
| --- | --- | --- |
| W1 | #222 comment 2026-10-20 08:37: approved-manifest criteria cannot be met by implementer-authored labels; owner decision needed. | https://github.com/jmservera/ama/issues/222 |
| W2 | #222 owner decision 2026-10-20 12:20 and comment 6290696478/#126 comment 6290697705: prepare manifest and protocol for review; no participants, thresholds or activation. Not an approval of unseen evidence. | https://github.com/jmservera/ama/issues/222 |
| W3 | #108 acceptance and RAI held-out criteria: freeze versions, independent labels, held-out answers never enter prompts or tuning, critical errors, cohorts. Whole issue open. | https://github.com/jmservera/ama/issues/108 |
| W4 | #174 closed, both its criteria ticked: registry and reproducible fixture. | https://github.com/jmservera/ama/issues/174 |

## Contrarian Results

* No existing harness path reports per-cohort counts, so the six criteria
  cannot be shown as met by any current output (C1).
* Developer-authored expected outcomes and a registry entry are not approval
  (C2, W1); a manifest registered here is still development evidence.
* The deterministic ranking is not shown fair by invariance: C6 is an
  adverse retained finding, and seeded invariance only tests the stated policy.
* A synthetic 60,000-home fixture has no cohort ground truth (C4), so counts
  from it would not reconcile to approved labels.

## Alternatives and Selection

| Option | Disposition |
| --- | --- |
| A. JSON manifest in `src/agents/evals/` registered in the existing registry, with a human-review Markdown protocol under the KB, plus a small structural validity test | Selected: reuses C2/C3, machine-checkable without evaluator code |
| B. Markdown-only manifest | Rejected: not stable for later machine use, no integrity check |
| C. New dataset service or schema package | Rejected: duplicates prior art and exceeds the authorised scope |
| D. Mechanics-only evaluator slice | Rejected: superseded by the owner decision; implementation follows review |

## Unresolved Decisions (owner)

* Cohort set and lawful analysis fields (OQ-018); no live field is approved.
* Sample-sufficiency rule and every numeric threshold (proposals only).
* Named independent labeller, reviewer, adjudicator and held-out custodian.
* Whether C6 is a defect or an accepted policy behaviour.
* Dependence on policy v1.0.0 being owner-approved.

## Risks

* Reading the draft as approved; mitigated by explicit status fields and a test that rejects any approved status.
* Leakage of expected outcomes into prompts; mitigated by protocol custody rules and a held-out section that holds IDs only.
* Invented numeric targets; mitigated by labelling all values proposals needing approval.

## Research Disposition and Planning Readiness

Research disposition: executed (one complete wider, deeper, contrarian cycle).
Planning Readiness: Ready. Selected option A. No further cycle is warranted:
the last wave produced no finding that changes the selection.

## Referenced Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/rpi-sessions/2026-10-20/cohort-manifest-222-state.json](../../rpi-sessions/2026-10-20/cohort-manifest-222-state.json) | Session state record |

## Next Steps

Active parent action: transition to Plan and pin artifact locations.
