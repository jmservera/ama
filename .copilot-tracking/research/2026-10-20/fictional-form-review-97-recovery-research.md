<!-- markdownlint-disable-file -->

# Task Research: fictional-form-review-97-recovery

| Field | Value |
| --- | --- |
| Date | 2026-10-20 |
| Researcher / agent | rpi-research skill, actually invoked 2026-10-20T21:2x Z after the coordinator intervention |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-20/fictional-form-review-97-recovery-research.md |

## Recovery Disclosure

An earlier pass in this worktree wrote a research note, plan, details, critique, a pack fixture, a test and a provenance entry by direct authoring without invoking the rpi-research, rpi-plan, rpi-implement or rpi-review skills. The coordinator's execution audit found this. Those files are preserved unchanged as UNVERIFIED pre-RPI draft material and are not an executed RPI loop; the earlier "critique" was a read-only subagent call, not an rpi-plan critique. This artifact is the first genuinely skill-executed phase. Verified facts below were re-derived from source with fresh line anchors; draft files are treated as claims to verify, not evidence.

Preserved pre-RPI draft (unverified): .copilot-tracking/research/2026-10-20/fictional-form-review-97-research.md, plans/2026-10-20/fictional-form-review-97-plan.md, details/2026-10-20/fictional-form-review-97-phase-details.md, reviews/2026-10-20/fictional-form-review-97-plan-critique.md, src/core/evals/fictional_form_review_pack.json, src/core/tests/test_form_review_pack.py, and the DS-FICT-FORM-REVIEW-PACK register entry (uncommitted).

## Research Brief

* What to research: How to deliver, within existing contracts, a concrete fictional versioned form/template and Finance authority/binding review pack for #97, and whether the uncommitted draft is compatible, safe and sufficient.
* Why it matters: Owner comment on #126 (2026-10-20) permits a fictional pack for actual review, not an approved template. Issue #97 criterion 1 needs actual authority/binding and must stay unmet.
* Audience or intended use: The planning phase, then independent coordinator assessment.
* Scope: src/core forms contract, provenance registry and privacy checker, existing form fixtures, PRD FR-038/039/AC-046/047, KB index/log, the draft files.
* Non-goals: new schema engine/service/runtime, rebuilding PR #377, #98 runtime, approvals/signatures/real grant terms, infra runbook, budget/benefits synthesis, map, cohort docs, cloud, push.
* Criteria: Exact compatibility with `forms._schema`; public-fixture registration; every authority field unresolved; no implied approval.
* Requested outputs: Evidence-backed convergence on one approach and readiness.
* Output mode: convergence

## Research Parameters

| Field | Value |
| --- | --- |
| Research question(s) | See Research Questions |
| Codebase scope | src/core, src/importer/evals, docs/reference, docs/prds, .copilot-tracking draft |
| External scope | none |
| Initial internal candidate areas | forms.py, core README #97 section, privacy.py, provenance-register.json, document_form_fixtures.json, PRD |
| Initial external candidate areas | none |
| Research posture | focused |
| Posture provenance | default: bounded internal task with named source targets and caller exclusions |
| Explicit limits / deadline | Caller: no new runtime, no edits to listed docs, no push; budget deadline irrelevant (no paid work) |
| Posture-specific completion basis | scope and materiality |
| Edits allowed during research? | no, research-only (artifact only) |
| Resolved evidence root | .copilot-tracking/ default |
| Known constraints / excluded sources | private ZF_DATA not read; no web |

## Extension Registry and Provenance

* Precedence applied per skill.

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
| --- | --- | --- | --- | --- |
| Instruction | AMA repository instructions (applyTo **) | Supplied custom instructions | KB, regulatory-evidence, branch, markdown rules | Selected |
| Instruction | Web development guidance | Not matched: no web files | n/a | Skipped, backend/data-only |
| Skill | rpi-research | Invoked this phase | Primary artifact contract | Selected |
| Skill | web-design-guidelines, design skills | No UI in scope | n/a | Skipped |
| Research specialist | RPI Researcher | Not dispatched | Lane artifact | Skipped: coupled, low-volume internal trace; ran inline |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision |
| --- | --- | --- | --- |
| Intake | Non-interactive session; owner comment and coordinator contract give sufficient direction | n/a | Proceed focused |
| Direction change | Coordinator intervention 2026-10-20: run genuine skills, treat draft as unverified | Confirmed by coordinator | Recovery artifacts with new slug; preserve draft and append clarification |
| Convergence | Not needed; evidence converged | n/a | none |

## Scope and Success Criteria

* Assumptions to verify: draft pack registers through existing contract; draft needs no runtime change; draft is privacy-check clean.
* Success: each question answered with `path:line` evidence; one recommendation; readiness recorded.

## Task Research Requests

* Explicit: the fictional versioned form/template and Finance authority/binding pack; field types, units, required/conditional, source authority, evidence, version/freshness, parser/OCR lineage, preparer/reviewer separation, stale propagation, unresolved Finance decision fields, not-approved/no-submission/no-payment labels; provenance registration; focused tests only for introduced fixture behavior.
* Inferred: whether stale propagation and role separation can be represented as data only.

## Direction Controls

| Control type | Direction or boundary | Source | Effect |
| --- | --- | --- | --- |
| exclude | No new engine/service/runtime; no edits to infra runbook, budget/benefits, map, cohort docs | Caller | Data fixture plus KB note only |
| narrow | Criterion 1 stays unmet | Owner/caller | No approval, no closing keyword |
| change | Genuine skills required; draft is unverified | Coordinator 2026-10-20 | Recovery cycle below |

## Research Questions

| # | Sub-question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | What exact contract must a registrable schema satisfy, and what status does registration give? | straightforward | H | answered |
| Q2 | What already exists for lineage, human-only fields, units and conditionals? | breadth | H | answered |
| Q3 | What must a new public fixture satisfy (registry, privacy, dictionary)? | straightforward | H | answered |
| Q4 | Does an existing form fixture or Finance synthesis already hold what is needed? | breadth | M | answered |
| Q5 | Which requested elements are not runtime-enforced and must be labelled proposed data? | depth | H | answered |
| Q6 | Is the unverified draft compatible, and what must the plan correct? | depth | H | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: the preserved draft files and PR #377 documentation.
* Reused (verified): draft pack shape re-verified against source in Waves 1 to 3.
* Superseded / stale: draft claims of a "critique" and "Research executed" are not skill-executed; superseded by this record.

## Research Cycle Log

### Cycle 1

* Active direction controls: all above.
* Posture and completion basis: focused; scope and materiality.
* Explicit limits: none beyond caller exclusions.

#### Wave 1: Wider

* Plan: inline survey of contract, docs, fixtures, PRD, registry and index. Delegation unnecessary: one tightly coupled internal trace.
* Evidence relationships: Q1 C1-C3; Q2 C4-C6; Q3 C7-C9; Q4 C10-C11; Q5 C12-C13.
* Reflection: all questions have candidate evidence; the generator fixture has a different shape; stale/role separation absent from runtime.

#### Wave 2: Deeper

* Prioritized: exact schema key sets, reviewer registration requirement, status stamp, public-payload rules, existing placeholder fixture shape.
* Evidence: C1-C3, C7-C9, C10.
* Reflection: `reviewer` must be a registered staff email while the privacy checker rejects emails in public JSON, so a public pack cannot be registered verbatim; a derived request differing only in reviewer is required, and the unsubstituted rejection is itself testable. Core stores seed only two staff, so an existing test dataset actor is usable.

#### Wave 3: Contrarian

* Challenge targets: (a) just reuse or extend the 120-family generator fixture; (b) Markdown-only pack; (c) add a loader/validator; (d) claim stale propagation/role separation as tested behavior; (e) write the pack under docs/ rather than src/core/evals.
* Evidence: C10, C11, C12, C13, C14.
* Findings: (a) weakens: generator-owned, hash-stamped, different non-contract shape, 120 families, edits would break its determinism tests. (b) weakens: no mechanical proof of contract compatibility. (c) rejected by caller. (d) contradicted: runtime has no propagation or separation logic, so any claim must be labelled proposed. (e) viable but docs/ files still need registry entry; src/core/evals matches the existing control-fixture precedent (DS-DOC-CONTROL-FIXTURES) and keeps tests beside the core contract.
* Reflection: no counter-evidence overturns the data-fixture-plus-one-test approach.

#### Parent Synthesis and Disposition

| Material / claim | Evidence | Disposition | Rationale | Treatment |
| --- | --- | --- | --- | --- |
| Pack as JSON fixture over existing contract in src/core/evals | C1-C3, C7-C9, C14 | accepted | smallest concrete, mechanically checkable, precedent exists | Recommendation |
| Derived registration request with reviewer substituted | C2, C7 | accepted | contract and privacy rules conflict for a verbatim public file | Test design |
| Edit generator fixture | C10 | rejected | different shape, generator-owned | Alternative |
| Loader/validator/API/engine | C12 | rejected | caller exclusion, runtime out of scope | Alternative |
| Markdown only | C13 | rejected | no compatibility proof | Alternative |
| Stale propagation/role separation as data, labelled proposed | C12 | accepted | not runtime-enforced | Labelling decision |
| Draft pack and test as starting point | C1-C9 | deferred to plan | structurally sound but unverified; needs critique and plan-owned corrections | Plan input |

#### Cycle Re-entry Evaluation

* Another complete cycle needed: no
* Basis: all material questions answered with line evidence; contrarian wave produced no new material question; further sources redundant under focused posture.
* Readiness effect: Ready

## Evidence Log

* Delegation: inline: tightly coupled internal trace, no independent lane warranted.

### Codebase Evidence

| ID | Claim / finding | Location | Tool | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| C1 | Schema is a closed key set; fields have exactly id, section_id, type, unit, options, required, required_when, source_authority, evidence_required, calculation_ref, category; types come from TYPES | src/core/src/zava_forward/core/forms.py:120 | read | high | `_schema`; TYPES at :23 |
| C2 | Reviewer must resolve to a registered staff member; registration records no approval | src/core/src/zava_forward/core/forms.py:120 | read | high | `_registered` lookup inside `_schema` |
| C3 | Every registration is stamped `Unapproved` with null approval evidence; no approval input accepted | src/core/src/zava_forward/core/forms.py:258 | read | high | `register_schema` at :247 |
| C4 | Human-only categories are declaration, signature, attestation, consent, approval and cannot receive candidates | src/core/src/zava_forward/core/forms.py:22 | read | high | refusal at :398 |
| C5 | Processing lineage (kind text/csv/ocr, parser, version, model version, route evidence, error record) is staged as `Supplied, unverified`; OCR needs route evidence and error record | src/core/src/zava_forward/core/forms.py:301 | read | high | `_processing` |
| C6 | Funding forms cannot be Not applicable; Unknown funding requires null scheme/route/evidence | src/core/src/zava_forward/core/forms.py:146 | read | high | within `_schema` |
| C7 | Public fixtures are scanned only if registered; unregistered `src/*/evals` JSON is reported | src/core/src/zava_forward/core/synthetic/privacy.py:203 | read | high | `public_issues` at :137; emails/phones/postcodes rejected by pattern_issues |
| C8 | Register entries need visibility, location under docs/ or src/<project>/evals/, a validation contract and dictionary anchor | docs/reference/research/retrofit-synthetic-data/provenance-register.json:140 | read | high | precedent DS-DOC-FORM-FIXTURES; root_label contract at :85 |
| C9 | Core README states real authority and binding remain unmet and fixtures show mechanics only | src/core/README.md:928 | read | high | section starts :906 |
| C10 | Existing placeholder form schema SYN-FUND-FORM-1.0 uses a different non-contract shape and is generator-owned | src/importer/evals/document_form_fixtures.json:152 | read | high | no authority, versions or lineage |
| C11 | No existing Finance form-template synthesis exists in docs/reference/research besides OQ-015 mentions | docs/prds/zava-forward-retrofit-programme-demonstrator.md:2036 | grep | medium | OQ-015 names the unresolved Finance inputs |
| C12 | Conditions and calculation references are data only; the module runs no validation, calculation, stale propagation or role separation | src/core/README.md:922 | read | high | field review/staleness is #98 (README:980) |
| C13 | FR-038 requires approved versioned schema; AC-046 blocks preparation for unapproved schemas or unknown routes | docs/prds/zava-forward-retrofit-programme-demonstrator.md:873 | read | high | AC-046 at :1512 |
| C14 | A control-fixture precedent already lives in src/core/evals as a registered public payload | src/core/evals/document_control_fixtures.json:1 | read | high | DS-DOC-CONTROL-FIXTURES in register |

### External Evidence

No external sources used.

### Contradictions / Conflicts

* Public-file reviewer vs contract: C2 requires a registered email; C7 rejects emails in public payloads; resolved by a derived registration request (consistency of both constraints).

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Implication |
| --- | --- | --- | --- | --- |
| Q1 | Contract is closed and registration is always Unapproved | C1, C2, C3 | high | Pack cannot create approval; compatibility is testable |
| Q2 | Lineage, human-only fields, units, conditionals already exist | C4, C5, C6 | high | Pack restates, does not rebuild |
| Q3 | New public fixture needs register entry, label contract, dictionary anchor | C7, C8, C14 | high | Register in provenance; reuse existing dictionary anchor |
| Q4 | No existing Finance template pack; generator fixture unsuitable | C10, C11 | medium | New fixture justified |
| Q5 | Stale propagation, separation, validation are not runtime | C12 | high | Label as proposed #98 data |
| Q6 | Draft is structurally compatible; unverified, needs plan critique and focused-test re-verification | C1-C8 | medium | Plan input |

## Key Discoveries

* Verbatim public registration is impossible by design; a derived request is the honest compatibility proof.
* Stale propagation and role separation must be labelled proposed controls.
* The Finance authority/binding fields must all be null/unresolved; criterion 1 stays unmet.

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: One public JSON fixture in src/core/evals over the existing schema contract, registered in the provenance register under the existing document-and-form dictionary anchor, one focused data-integrity test that registers a reviewer-substituted derived request on JSON and SQL stores, a short KB review note, and mechanical index/log/README pointers. No runtime change.
* Rationale: smallest concrete reviewable object with mechanical compatibility proof.
* Evidence refs: C1-C3, C7, C8, C12, C14.
* Implementation impact: src/core/evals, src/core/tests, provenance register, data dictionary, KB note, index/log, core README pointer.
* Confidence: high; raised by actual test run.

### Alternative: extend generator fixture
* Rejection rationale: C10, generator-owned and wrong shape.

### Alternative: loader/validator/API
* Rejection rationale: caller exclusion; C12.

### Alternative: Markdown only
* Rejection rationale: no mechanical proof.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none for the fictional pack. Actual authority/binding is a human blocker for criterion 1.
* Important: the earlier draft contains one subagent read-only review labelled critique; the plan phase must run its own required critique.
* Risk: pack mistaken for approved template; mitigate with labels at root, template, every decision and note.
* Residual: fictional max-age values and field policies are proposals with no scheme basis.

## Current Decisions

| Decision | Status | Owner | Rationale | Evidence | Implications |
| --- | --- | --- | --- | --- | --- |
| Fictional data-only pack over existing contract | proposed | evidence | smallest approach | C1-C3, C12 | no runtime |
| Draft treated as unverified | confirmed | user (coordinator) | process defect | n/a | recovery artifacts |
| Criterion 1 remains unmet | confirmed | user/constraint | no actual authority | C9, C13 | no closing keyword |

## Unresolved Decisions

| Decision | Smallest evidence needed | Owner | Impact | Blocker status |
| --- | --- | --- | --- | --- |
| Actual Finance authority, template source/version, binding | Named human authority's version-specific source, version and binding | Finance and Grants / Legal | Closes criterion 1 | blocking for criterion only |

## Potential Next Research

| Priority | Item | Expected value | Trigger | Selected? | Related |
| --- | --- | --- | --- | --- | --- |
| M | Real funder template and OQ-015 inputs | Replace fictional template | Finance supplies sources | deferred | Q4; C11 |

## Planning Readiness

* Status: Ready
* Decision state: convergence selected (above)
* Evidence basis: C1-C14
* Preconditions met: all questions answered, contrarian wave complete
* Blockers: none for planning
* Smallest action to change readiness: none

## Closeout Record

| Field | Record |
| --- | --- |
| Research execution status | Complete |
| Completed waves | Wider, Deeper, Contrarian (cycle 1) |
| Lane evidence or inline fallback | Inline; no worker ran; limitation: single-reader synthesis |
| Research disposition | executed |
| Planning Readiness | Ready, C1-C14 |
| Blockers | none |
| Continuation owner and state | manual: advisory /rpi-plan; coordinator directed continuation to genuine rpi-plan |

## Advisory Next Step

| Field | Record |
| --- | --- |
| Research disposition | executed |
| Planning Readiness | Ready |
| Output mode and planning support | convergence; yes |
| Acting owner | user/coordinator |
| Required gates | none pending |
| Continuation result | advisory /rpi-plan |
| Primary evidence file | .copilot-tracking/research/2026-10-20/fictional-form-review-97-recovery-research.md |

* Advisory only: rpi-research does not invoke `/rpi-plan`.

## Sources

No external sources used.

## Artifact Self-Check

* [x] Questions answered; waves ordered; posture recorded; C# with path:line; Sources "No external sources used"; extension registry, participation, direction controls, synthesis, re-entry, decisions, readiness recorded; no secrets; draft treated as data.
* Checked sections: all template sections.
* Missing or limited sections: no delegated lane (inline fallback).
