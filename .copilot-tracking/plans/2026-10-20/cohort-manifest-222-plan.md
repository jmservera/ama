<!-- markdownlint-disable-file -->
# RPI Plan: Cohort and missing-data evaluation manifest preparation (#222)

## Task Metadata

* Task ID: 222
* Task slug: cohort-manifest-222
* Planning status: ready (single critique executed, all findings dispositioned below)
* Plan date: 2026-10-20
* Research: .copilot-tracking/research/2026-10-20/cohort-manifest-222-research.md
* Phase details: .copilot-tracking/details/2026-10-20/cohort-manifest-222-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-10-20/cohort-manifest-222-plan-critique.md
* Changes record: .copilot-tracking/changes/2026-10-20/cohort-manifest-222-changes.md
* Review: .copilot-tracking/reviews/logs/2026-10-20/cohort-manifest-222-review.md

## Executive Summary

This plan prepares, for owner review only, a versioned and wholly synthetic
paired-scenario and expected-outcome manifest, and a proposed human evaluation
protocol, for issue #222. It adds one registered JSON draft beside the existing
#108 golden files, one review-pack Markdown page, a small structural test that
proves the draft stays unapproved and internally consistent, and the index and
log updates. It adds no evaluator, runtime, API or UI behaviour, runs no model
and uses no private data. Every artifact is labelled DRAFT, UNAPPROVED and NOT
EXECUTED. All six #222 acceptance criteria stay unticked.

### User Decisions and Requirements Highlights

* Preparation only, for owner review before implementation; no approval, fairness result, threshold or activation is inferred.
* Agent-authored expected outcomes and labels are proposals, never an approved or held-out oracle.

### What You May Not Know

* The existing deterministic ranking sorts a resident with Unknown support together with one with No support (research C6). The draft seeds this as a candidate defect for owner decision, not a confirmed production finding.
* The ranking policy v1.0.0 is itself an unsigned draft, so a manifest cannot be approved against an approved policy yet.
* Adding a JSON file under `src/agents/evals/` triggers the registry test, so registration is required and intended.

### Unresolved Decisions or Blockers

* Owner: cohort set and lawful fields (OQ-018), sufficiency rule, thresholds, named labeller, reviewer, adjudicator and custodian, and the C6 disposition. These are listed in the review pack checklist and are not decided here.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements).

## User Decisions and Requirements

* Issue #222 owner decision 2026-10-20: prepare the versioned synthetic scenario and expected-outcome manifest for review before implementation; prepare held-out label, critical-error, cohort and reviewer protocol and quality-threshold proposals; prepare the human protocol only, no participants or study.
* Build on the existing #108 offline harness and the delivered #174 fixture and registry; no new service. #108 whole issue stays open; #174 is closed.
* Manifest must be explicitly DRAFT, UNAPPROVED and NOT EXECUTED with stable scenario IDs, paired factors, expected justification, source and policy versions, missingness and insufficient outcomes, exclusions, critical error seeds, denominators and reconciliation expectations; numeric values only as labelled proposals with rationale and approval requirement.
* Pin minimal artifact locations and deliverable criteria before implementation; add deterministic local checks only where warranted.
* No participants, studies, model batches, paid calls, deployment, live or private data, threshold approval or whole-issue claim. Update the KB index and append-only log. Publication is local-first; commit only reviewed issue files and RPI artifacts; PR later uses "Refs #222" only.

## Goals

* G1 Provide a reviewable, versioned synthetic manifest integrated with the existing eval registry.
* G2 Provide a human review pack: held-out custody, independent reviewer, leakage boundary, adjudication, small-sample, disaggregated critical error, review-burden and uncertainty plan, AC traceability, owner checklist.
* G3 Keep every claim bounded: nothing approved, executed or fairness evidence.

## Scope and Non-Goals

### In Scope

* P01 manifest JSON, registry entry, structural test.
* P02 review-pack Markdown page under the KB.
* P03 pointer, index and log updates; agents README pointer.
* P04 validation and the single post-implementation Review.

### Non-Goals

* Evaluator, runner, API, UI, SQL, model or paid execution; changes to ranking or policy files; participants; live or private data; threshold approval; ticking any acceptance criterion; editing the original case study or `docs/reference/memory.md`.

## Functional Requirements

* FR-1 Manifest file `src/agents/evals/cohort_manifest_draft.json`, `version` "cohort-manifest-draft-v0.1.0", with top-level `status` "DRAFT", `approval` "UNAPPROVED", `execution` "NOT EXECUTED", `dataset_role` stating it is a development draft that is never a held-out set, `is_synthetic` true, `fairness_evidence` false, and source, ranking policy (1.0.0), registry and fixture version pointers.
* FR-2 Stable scenario IDs `CM-P01`... each with a pair (`baseline` and `variant`), the single varied factor from the set sensor-or-source completeness, accessibility-or-contact need, appointment history, expected deterministic outcome (invariant, or an explicit proposed difference with justification), expected AI-task outcome marked `unlabelled` until an independent labeller supplies it, neutral placeholder arms ARM-A and ARM-B (not proposed cohorts, OQ-018 stays open), missingness treatment, expected insufficient state, and critical error seeds.
* FR-3 Seeded defects `SD-xx` (unjustified exclusion or deprioritisation), each linked to a scenario, with detection expectation; includes the support-Unknown candidate (C6) as an unconfirmed seed with two proposal expectations (current behaviour and a candidate correction) and no pass or fail until the policy owner decides, plus labelled adverse/negative controls. Minimum inventory: at least one invariance pair per factor family, one C6 pair, one small-sample, one zero-denominator, one missing-cohort-label, one open-safety critical seed and one threshold-averaging seed.
* FR-4 Denominators and reconciliation expectations per arm, an illustrative template (counts that add up, errors, review burden, uncertainty) with no producer; the test checks internal consistency only. Plus small and missing sample cases that must report insufficient.
* FR-5 Every numeric target is in a `proposals` block whose entries have `value`, `rationale`, `basis`, `requires_approval` true and `approver_role`; scenario counts are structural, not targets.
* FR-6 Registry entry in `src/agents/evals/registry.json` (id, path, version, owner "Unassigned", purpose containing DRAFT/UNAPPROVED and not-held-out, used_by only the new test, contains_real_data false). The review pack links to the registry, not the reverse.
* FR-7 Review pack `docs/reference/research/evaluation/cohort-evaluation-review-pack.md` with YAML frontmatter, no H1, `*` bullets, ASCII, covering G2 plus an AC1-AC6 traceability table showing each as Not met, the owner checklist and unresolved decisions; adverse evidence retained.
* FR-9a Manifest `acceptance_trace` maps AC1 to AC6 to manifest keys, each with status "Not met" and what would meet it.
* FR-8 Test `src/agents/tests/test_cohort_manifest_draft.py` checks only the draft: status/flag literals, unique stable IDs, pair completeness and one varied factor, seed-to-scenario links, reconciliation arithmetic, proposals labelled, the registry purpose agrees with the manifest status literals, JSON-only assertions that reject the words oracle, gold and ground truth and any status other than DRAFT, UNAPPROVED, NOT EXECUTED, ASCII, no personal-data patterns, and every AC mapped to Not met. It is an internal-consistency check, not an evaluation, and does not read docs/. It reads no private data and calls no model.
* FR-9 KB `docs/reference/README.md` index row and an appended `docs/reference/log.md` entry; one pointer in `src/agents/README.md`.

## Non-Functional Requirements

* NFR-1 Wholly fictional identifiers; no name, email, address, roster, secret or real postcode.
* NFR-2 Deterministic and offline; ASCII punctuation; no em dashes.
* NFR-3 Existing tests, `test_eval_registry` and the complete local gate pass.
* NFR-4 No change outside the listed files and RPI artifacts.

## Acceptance Criteria

* AC-P1 All FR-1 to FR-9 files exist and satisfy their criteria; the new test and the registry test pass; Ruff passes for the new test.
* AC-P2 No #222 criterion is claimed met; the pack and manifest say DRAFT/UNAPPROVED/NOT EXECUTED.
* AC-P3 Changes record, single Review and local gate receipt exist; candidate is clean and committed with the privacy-safe identity; no push or PR.

## Phase Checklist

* [x] P01 Manifest, registry entry and structural test
* [x] P02 Review pack
* [x] P03 Index, log and README pointers
* [x] P04 Validate, changes record, single Review

## Follow-Up Items

* Owner review and approval of cohorts, fields, thresholds, labeller and manifest before any evaluator work (#222, #108, #223).
* Per-cohort reporting in the offline harness and fail-closed unapproved thresholds, only after manifest approval.
* Decide whether support Unknown deserves a ranking-policy change (policy owner).

## Critique Disposition

Critique executed once: Revise (3 High, 5 Medium, 2 Low). All ten were direct planner corrections; none needed a user decision. No second critique runs.

| Finding | Disposition |
| --- | --- |
| PC-001 | Applied: `dataset_role` field, registry wording, banned oracle words, pack states the held-out set is separate and created after approval |
| PC-002 | Applied: two proposal expectations, unconfirmed seed, no pass or fail |
| PC-003 | Applied: test cross-checks registry purpose with manifest literals; used_by lists only the test |
| PC-004 | Applied: FR-9a acceptance_trace and minimum inventory |
| PC-005 | Applied: neutral ARM-A/ARM-B, AI expectations unlabelled, invariance noted |
| PC-006 | Applied: illustrative template, internal-consistency test only |
| PC-007 | Applied: exact commands in details P04; test does not read docs/ |
| PC-008 | Applied: assertions scoped to the JSON |
| PC-009 | Applied: new folder justified in details; status wording corrected |
| PC-010 | Applied: required proposal keys in FR-5 |

## Handoff

Implement P01 to P04 in order; the changes record is .copilot-tracking/changes/2026-10-20/cohort-manifest-222-changes.md.

## Correction Continuation (2026-10-20, appended; original plan and critique unchanged)

Owner decisions 2026-10-20 (issue comment 6295248053; PR comment 6295248627) authorised correction only, returned for owner approval before any evaluator work. This is an ordinary later `rpi-implement` invocation, not a second critique or Review.

* <!-- rpi:phase id=P05 --> P05 Correction scope (declared: full P05)
  * <!-- rpi:task id=P05-T01 --> [x] P05-T01 Split confounded pairs, bind expectations to unchanged `rank()`, add Unknown-support policy proposal (PP-01), fresh held-out ID rule with unfilled roles
  * <!-- rpi:task id=P05-T02 --> [x] P05-T02 Replace arbitrary sample and error values with justified options and uncertainty methods; define review burden over eligible; restrict test support exemption with regression
  * <!-- rpi:task id=P05-T03 --> [ ] P05-T03 Reconcile PR inline findings and RV-001/002/004/006 dispositions; full local gate; frozen local handoff

### P06 Independent exact-head assessment correction (2026-10-21, appended)

Assessor f9636e1f returned Defects on 93cb2bba (original Review verdict and earlier gate history unchanged). Ordinary later `rpi-implement`; no second Review or critique.

* <!-- rpi:phase id=P06 --> P06 Correct assessor findings 1 and 2 (declared: full P06)
  * <!-- rpi:task id=P06-T01 --> [x] P06-T01 Preserve sensor_data, source_record, appointment_history in the test case conversion; assert converted pairs differ in the declared factor; add regression where a missing-data exclusion or appointment penalty fails the binding check
  * <!-- rpi:task id=P06-T02 --> [x] P06-T02 Correct the open-safety ordering wording (open safety first; within it support, waiting days, stage, case id) in manifest and review pack; add supported open-safety neighbour test showing rank 2 is fixture-specific
  * <!-- rpi:task id=P06-T03 --> [ ] P06-T03 Focused tests, ruff, mypy; KB index/log; commit and freeze clean (full gate is coordinator-owned)
