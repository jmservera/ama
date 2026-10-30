<!-- markdownlint-disable-file -->

# Task Research: finance-96-98-99

| Field | Value |
| --- | --- |
| Date | 2026-10-27 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-27/finance-96-98-99-research.md |

## Research Brief

* Research issues #96, #98 and #99, their schema prerequisite #97, and Finance authority boundaries.
* Purpose/audience: an evidence-based, single draft PR for the owner and Finance reviewers.
* Scope: existing src/core forms, finance, persistence and src/api form routes; linked PRD, BRD and ADR 0006.
* Non-goals: invented company figures, template/rule approval, submission, cash, new AI authority, deployment, private datasets.
* Criteria: prove each claimed acceptance criterion; keep actual human approvals held and ledgered.
* Output: dated research, plan/details/critique, implementation evidence and independent Review.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | What is already delivered; what can be built independently; which decisions must remain held? |
| Internal candidates | docs/reference/README.md; PRD FR-038..043; BRD RULE-011/012; core forms/finance and API adapters |
| External candidates | Named GitHub issues and prerequisite issue #97 only |
| Posture / provenance | Focused, bounded caller scope |
| Limits | Local tests only; no full --all gate; at most one locked scoped --changed for large changes; no Azure/private data/secrets/uv |
| Edits during research | Evidence and workflow tracking only |
| Evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Selection |
| --- | --- | --- |
| Instruction | Repository instructions, all paths | Selected: src layout, human authority, evidence and branch controls |
| Skill | rpi-research | Selected: three-wave research |
| Specialist | Housing Finance and Grants Lead | Skipped: a role simulation cannot resolve actual Finance or Board authority |
| Specialist | RPI researcher | Skipped: one tightly coupled evidence trace handled inline |
| Skill | Web design skills | Not applicable unless web files are changed; no UI overhaul planned |

## User Participation and Research Decisions

The caller explicitly requests the full ordered loop and a draft PR. No routine phase prompt is needed in this non-interactive execution. Any missing Finance/Board decision blocks only dependent functionality; implement independent work and report the decision in the PR.

## Scope and Success Criteria

Preserve issue checkboxes; do not close issues without complete proof. No source-policy approval, Board envelope or tolerance can be inferred from a fixture, role agent or existing proposed schema.

## Task Research Requests and Direction Controls

One existing clean topic branch, docs/finance-96, has no PR. Reuse it for one PR to main. #96 has #97 (closed engineering slice) and #98; #99 is a sibling under #93, included by explicit owner scope. Do not expand to other #93 children.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What schema and lineage foundation exists? | depth | Answered provisionally |
| Q2 | Which field review, validation, pack and stale functions are independent of approval? | depth | Investigating |
| Q3 | Is an actual investment envelope/tolerance authority available? | straightforward | Blocked: no such evidence supplied |

## Prior Knowledge Gate

Read original/addendum, reference index and owner memory. Memory is context, not evidence. GitHub #96 comment explicitly says approved schema authority remains missing after #377/#97. Verified against immutable unapproved registry rows in forms.py.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Named issues, parent/dependency, PRD and BRD confirm separate form-draft and controlled-financial authority. ADR 0006 requires core domain code with external tests. Reflection: do not interpret closed #97 as an approved template.

#### Wave 2: Deeper

The existing /api/form-schemas and case form-candidates endpoints delegate to forms.py, which enforces current Finance/resident/reason-view rights. Case JSON bodies persist automatically through SqlStore; new per-case histories need no new SQL table. change_provenance.controlled provides rollback and current-actor writer-transaction rechecks. Ordinary case detail deliberately excludes form staging. Reflection: reuse these guards and isolate review data from ordinary case/detail/export projections.

#### Wave 3: Contrarian

Read #97 comments, grants.require_authority and the actual registry. Closed #97 explicitly does not establish approval; previous fictional Finance decision pack FD-01..14 remains unresolved. Existing financial designation is constructed-exercise-only and production-denied, not general template or Board authority. Reject adding a generic approve endpoint or rule/limit defaults. Unknown rules must not become a successful validation. A held diagnostic manifest can be useful but cannot be called a reviewed pack. Unknown Board limits must produce a pause for human decision, never a zero limit, invented breach or successful affordability check.

#### Parent Synthesis and Disposition

Accept an independent engineering slice: isolated field-review notes on supplied unapproved schemas, deterministic draft diagnostics, source-bound diagnostic manifests, and a durable held-decision ledger. Defer approved-schema/rule binding, calculations, reviewed application/claim export and downstream approval invalidation until actual Finance decisions. Defer approved-envelope/breach/restart processing until Board inputs. No new AI, UI or workflow/check rename.

#### Cycle Re-entry Evaluation

No further research cycle: missing evidence is named human authority, not a discoverable implementation fact. The bounded independent slice is adequately supported. Another cycle cannot ratify missing decisions.

## Evidence Log

| ID | Claim | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Registry records Unapproved schemas; supplied policy is not approved authority | src/core/src/zava_forward/core/forms.py:250 | High |
| C2 | Candidate staging retains exact hash/version, locator and parser/OCR history | src/core/src/zava_forward/core/forms.py:380 | High |
| C3 | Field draft acceptance must not satisfy an approval | docs/prds/zava-forward-retrofit-programme-demonstrator.md, FR-040 (located by identifier) | High |
| C4 | Reviewed pack needs approved rules and inputs; changes invalidate only dependents | docs/prds/zava-forward-retrofit-programme-demonstrator.md, FR-041..043 (located by identifier) | High |
| C5 | Actual capital envelope and downside tolerances require Finance/Board evidence | docs/brds/agentic-retrofit-programme-brd.md, RULE-011/012 and OD-12/15 (located by identifier) | High |
| C6 | Authenticated bounded form routes | src/api/src/zava_forward/api/server.py:734 | High |
| C7 | Controlled writer provides current actor recheck and rollback | src/core/src/zava_forward/core/change_provenance.py:108 | High |
| C8 | Existing designation is synthetic and cannot establish actual Board/template approval | src/core/src/zava_forward/core/grants.py:28 | High |
| C9 | Ordinary detail excludes private staging | src/core/src/zava_forward/core/store.py:376 | High |
| W1 | Approved schema authority remains unmet despite closed engineering prerequisite | https://github.com/jmservera/ama/issues/96 ; retrieved 2026-10-27 with gh issue view 96 --comments | High |
| W2 | #99 needs human-approved limits, not invented figures | https://github.com/jmservera/ama/issues/99 ; retrieved 2026-10-27 | High |

## Findings, Alternatives and Decision State

Selected: bounded independent draft review and held ledger (C1..C9, W1/W2). Reject whole-issue success or fictional approvals. Reject total stop because independent review/history/diagnostic controls are feasible and explicitly requested. All acceptance beyond the independent boundary remains unproven.

## Open Questions, Risks and Residual Uncertainty

Finance/template/rule authority and Board OD-12/15 remain unavailable. A software approval endpoint alone would not satisfy them.

## Planning Readiness

Ready for independent engineering only; approval-dependent issue acceptance Blocked. Research disposition: executed.

## Artifact Self-check

Complete Wider, Deeper and Contrarian inline; no delegated research or legal-currentness claims. Evidence gaps and independent boundary are explicit. Source references use exact requirement identifiers for tables and path:line for code.
