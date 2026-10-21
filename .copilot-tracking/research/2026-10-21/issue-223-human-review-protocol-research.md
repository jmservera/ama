<!-- markdownlint-disable-file -->

# Task Research: issue-223-human-review-protocol

| Field | Value |
|---|---|
| Date | 2026-10-21 |
| Researcher / agent | rpi-research skill (native loop, inline waves) |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-21/issue-223-human-review-protocol-research.md |

## Research Brief

* What to research: where and how to place a PROPOSED meaningful-human-review protocol (seeded critical-error case definitions, effort and comparator definitions, OQ-017 competence evidence, automation-bias controls) for issue #223.
* Why it matters: owner comment on #126 (2026-10-20, issuecomment-6290697705) authorises preparation of reviewer protocol and thresholds for #108/#222/#223 only; no participants or execution.
* Scope: docs/prds AC-070/FR-026/FR-027/NFR-009, addendum RAI position, src/agents and src/core READMEs, existing harness. Non-goals: runtime/evaluator code, models, humans, #222 manifest, memory, case study original.
* Output mode: convergence (placement recommendation).

## Research Parameters

| Field | Value |
|---|---|
| Posture | focused (caller-specified bounded preparation task, named sources) |
| Limits | no participants, model calls, Azure, private data; USD500 monthly budget untouched |
| Evidence root | .copilot-tracking/ |

## Extension Registry

| Kind | Candidate | Disposition |
|---|---|---|
| Instruction | AMA repository instructions (applyTo **) | selected: KB index/log, evidence labelling, ASCII, no em dashes |
| Skill | rpi-research | selected |
| Skill | web-design-guidelines, design skills | skipped: no web changes |
| Specialist | RPI Researcher | skipped: bounded, tightly coupled, inline |

No interactive question needed; inputs sufficient (non-interactive run).

## Evidence (C# codebase)

* C1 docs/prds/zava-forward-retrofit-programme-demonstrator.md:1536 AC-070 (Not run): seeded plausible wrong/stale/unsupported/incomplete critical proposals plus correct controls; detection, corrections, total review effort versus same workflow-only scenarios; default acceptance and citation validity alone cannot pass.
* C2 same file:861-862 FR-026/FR-027; :950-965 NFR-009 (workflow-only comparator, error taxonomy, review-effort capture, owner thresholds first; valid-citation materially incorrect recommendations block release).
* C3 same file:1079-1170 RAI Oversight Contract: reviewers explain source-based disposition; review unflagged critical fields; preparation-plus-review effort versus workflow-only.
* C4 same file:2038 OQ-017: authority/competent-review holders and evidence making oversight meaningful remain unanswered.
* C5 same file:1023-1078 evaluation harness method: pair AI-assisted and workflow-only runs; zero undetected critical failures as release condition; Finance approval of financial fields.
* C6 src/agents/README.md:253-330 offline harness and #108 accounting: scripted provider only, "not evaluated" for actual-model/human; reviewer accept/edit/reject counts with reasons; this section is the existing evaluation-protocol placement.
* C7 src/core/src/zava_forward/core/ai_tasks.py:175,307 existing review record fields: reviewer_action, reviewer_reason, override text, source hashes, prompt version (delivered part of #106).
* C8 src/agents/README.md:67 and :195 #216/#214 evaluation gates: citation validity is lexical/structural, claim-level grounding unproven; chat eval keeps unsupported-claim-with-valid-citation as an open critical gap.
* C9 src/api/README.md:2607 "Staff comprehension protocol (Not run; unmet)": precedent for an in-README protocol section with predeclared thresholds, frozen key, two independent scorers, consent preconditions.
* C10 docs/adrs/0002-pilot-readiness-architecture.md:355 mandatory RAI tests include plausible wrong answers and reviewer automation bias.
* C11 docs/reference/README.md index lists src READMEs; docs/reference/log.md append-only; no existing standalone human-review protocol page.
* C12 src/core/README.md:2711 governance records protocol freeze with different approver, never decides; precedent for separation of recorder and approver.

## Evidence (W# external)

None required: the task is internal preparation from owner comment and repository sources. GitHub issue evidence (gh, retrieved 2026-10-21): #223 open, whole criteria unticked, "Not run"; #106 CLOSED; #108 OPEN with all criteria unticked and PR #405 merged as offline accounting only; #222 OPEN, "Not evidenced", its manifest is an unapproved external prerequisite (no published manifest on origin/main 993a7b88).

## Wave Record (cycle 1)

* Wider: enumerated PRD, addendum, ADR, READMEs, issues #106/#108/#126 comment/#222/#223.
* Deeper: read AC-070, NFR-009, RAI contract, harness evidence block, review record fields, comprehension-protocol precedent.
* Contrarian: tested alternatives. (a) New standalone docs page: rejected, duplicates harness placement and adds a governance surface; (b) PRD edit: rejected, owner-approved requirements text would be rewritten, out of scope; (c) code/evaluator fixture: prohibited. (d) Risk: a proposal reading as approval; mitigation: every threshold/sample/role labelled PROPOSED/UNFILLED, outcomes NOT RUN. Counter-evidence: #108 harness only has scripted accept/edit/reject; no human field for effort exists, so effort capture is a protocol definition, not a built metric.

## Parent Synthesis

* Accepted: add one section "Meaningful human-review protocol (#223; proposed, Not run)" to src/agents/README.md directly after "Priority repetition accounting (#108)", plus index row and appended log entry. Rationale: C6, C9, C11.
* Rejected: new page, PRD/ADR/addendum edits, code.
* Deferred: #222 cohort labels/manifest (unapproved external prerequisite); real thresholds, samples, named reviewers, OQ-017 holders; #108 dependency remains open.

## Decisions and Disposition

* Research disposition: executed.
* Planning Readiness: Ready.
* Unresolved: owner-approved thresholds, reviewer panel, consent/accessibility/privacy authorisation, #108 closure, #222 manifest, Finance validation, approved finite costed plan.
* Issue criteria: none ticked by this work.

## Next Steps

Plan phase: author plan, details and independent critique.
