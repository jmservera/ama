<!-- markdownlint-disable-file -->

# Task Research: operator-suspension-221

| Field | Value |
| --- | --- |
| Date | 2026-10-20 |
| Researcher | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-20/operator-suspension-221-research.md |

## Research Brief

Investigate issue #221 for the coordinator's bounded synthetic engineering
delivery. Verify actual #219 release primitives, incident-to-dispatch and
proposal-reliance enforcement, trusted authority, evidence and durable storage
before planning. Output mode: convergence, preparing planning only when Ready.
Scope: core/API release, governance, identity, stores and their tests.
Non-goals: live activation, cohort evaluation (#222), invented OD-35 authority,
cloud operations, private data, new UI or operational acceptance.
Criteria: the six issue ACs, including negative controls, independent tasks,
manual/hazard continuity, distinct authorized restart and persistence.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | What is already enforced? Where are genuine integration gaps? What authority can safely be constructed and what remains human-blocked? |
| Internal candidates | src/core/src/zava_forward/core/{assistant_release,governance,release}.py; API server/auth/tests; SQL/JSON stores; PRD/BRD/ADR index |
| External candidates | GitHub issue #221 and dependency #219 metadata only |
| Posture / provenance | Focused; explicit bounded caller direction |
| Completion basis | Actual in-scope contract coverage and materiality |
| Evidence root | .copilot-tracking/research/2026-10-20/ |
| Research edits | Evidence and required workflow state only |
| Limits | Worktree only; no private datasets/credentials, cloud, push, PR, authority invention or cohort evaluation |

## Extension Registry and Provenance

| Kind | Candidate | Selection and scoped contract |
| --- | --- | --- |
| Instructions | .github/copilot-instructions.md; supplied repository and RPI instructions | Selected: worktree, original evidence, local gate and source authority boundaries |
| Skill | rpi-research | Selected: ordered wider/deeper/contrarian research |
| Skill | rpi-plan / rpi-implement / rpi-review | Deferred to explicit caller-authorized subsequent phases |
| Specialist | RPI Researcher | Skipped: one continuous tightly coupled trace handled inline |
| Web skills | web-design-guidelines | Not applicable unless research proves essential web edits |

## User Participation and Research Decisions

Caller explicitly authorizes the complete ordered loop and bounded synthetic
delivery. No routine phase questions are needed. Missing significant authority
decisions must remain human blockers, never default approvals.

## Direction Controls

Preserve failed attempts and adverse findings; no retrospective phases.
Use existing contracts, trusted capabilities and transactions. Distinct identity
alone is not authority. Stop before publication after committed candidate and
full gate, or report concrete unresolved blockers.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | Which #219 primitives actually merged and how do dispatch/reliance consume them? | depth | Open |
| Q2 | Can the existing incident/authority/evidence contracts safely serve task-specific restart? | depth | Open |
| Q3 | Which persistence, race, rollback, denial audit and manual/hazard tests cover the interface? | depth | Open |
| Q4 | Which acceptance remains blocked by actual human authority? | straightforward | Open |

## Prior Knowledge Gate

Read original case, reference index opening, owner memory and addendum opening.
Clean worktree on supplied branch at supplied base verified. No open PR.
GitHub #219 is still OPEN despite caller's statement that bounded primitives
merged; distinguish merged code from whole-issue acceptance in investigation.
Supplied code pointers remain hypotheses until read.

## Research Cycle Log

### Cycle 1

Focused scope; all three waves will run inline in order.

#### Wave 1: Wider

Verified source inventory and prior #219 original adverse Review and later
bounded correction Review. PRD/BRD/ADR folders have no README; ADR 0002 and
the source README are the applicable routing documents.
Reflection: dispatch and reliance already consume continuity and release
records; duplicating an incident/release table is unnecessary.

#### Wave 2: Deeper

Traced continuity.suspend/restart through API, SQL meta document optimistic
writer, independent assistant connection and ordinary legacy review/export.
Existing suspension captures truncated assistant metadata supplied before the
write, but no evidence/resident impact/remediation/restart authority. Restart
accepts a different manager plus arbitrary authority_ref and corrective text.
The global epoch invalidates unrelated tasks. Current staff identity helper
and trusted-proxy separately provisioned capability mapping are reusable.
Reflection: strengthen continuity itself, not a new parallel control. Existing
restart behavior is not sufficient authority/evidence.

#### Wave 3: Contrarian

Challenged "new release fixes everything": a suspended release can be replaced,
but continuity must remain independently held until a qualified restart.
Challenged role/different-email authority: current restart accepts arbitrary
reference and does not validate a provisioned restart capability or versioned
corrective result. Challenged task isolation: even unrelated ready output is
invalidated by the shared global epoch. Existing tests only prove all-scope
cycles. JSON has no release authority and must remain manual/fail-closed for AI.
Reflection: these are bounded mechanism defects, not evidence that OD-35 is
appointed. A separately provisioned trusted restart capability is an engineering
permission, not approval of an actual authority holder. Actual OD-35 remains
blocked; fixtures must be explicit and non-operational.

#### Parent Synthesis and Disposition

Accept reuse of existing continuity document, audit ledger and rowversion writer
(C2-C5). Reject a duplicate incident table or automatic release renewal. Accept
task-bound history fencing and trusted distinct restart permission checks;
retain unknown actual authority and live acceptance as blockers (C1/C6).
One cycle sufficient: every material in-scope seam is located. No external
regulatory claim/currentness check or cohort evaluation is needed.

## Evidence Log

| ID | Source | Evidence |
| --- | --- | --- |
| C1 | docs/prds/zava-forward-retrofit-programme-demonstrator.md:888,980,1538,2038; docs/brds/agentic-retrofit-programme-brd.md RULE-024/OD-35; docs/case_study_48_addendum.md:454-527 | Six ACs require suspension/reliance/restart, actual authority remains open |
| C2 | src/core/src/zava_forward/core/assistant_release.py:61-150; rai_release.py:20-24,109-139 | Extended #219 records exist, active replacement cannot substitute for incident restart |
| C3 | src/core/src/zava_forward/core/continuity.py:73-75,131-218 | Shared epoch, incomplete incident, arbitrary-reference restart |
| C4 | src/core/src/zava_forward/core/assistants.py:423-436,478-521,680-685,796-803,868-889 | Transactions and dispatch/detail/review/completion gates already wired |
| C5 | src/core/src/zava_forward/core/change_provenance.py:17-44; sqlstore.py:94-130,568-670,711 | Current identity, SQL transaction revalidation, optimistic continuity document persistence |
| C6 | src/api/src/zava_forward/api/auth.py:97-157; server.py:853-856 | Trusted-proxy bound claims carry separate capabilities; API already exposes continuity actions |
| C7 | src/api/tests/test_continuity.py:1-145; test_continuity_epoch_export.py:53-168 | Existing all-scope/late/replay tests, no unrelated task survival or qualified restart evidence |
| C8 | .copilot-tracking/reviews/logs/2026-10-15/src-rai-release-record-219-review.md:100-155; rai-reliance-review-fixes-219-review.md:100-115 | Original adverse findings retained; later corrections do not establish actual human acceptance |

## Findings Mapped to Questions and Evidence

Q1 answered C2/C4/C8: bounded primitives merged, whole #219 still open.
Q2 answered C3/C5/C6: reuse continuity, harden identity and distinct permission,
bind corrective result to exact scope/version/epoch; do not accept a text claim
alone. Q3 answered C4/C5/C7: native SQL integration and adverse transaction
tests required; existing rowversion document reused. Q4 C1/C8: actual OD-35,
approved monitoring thresholds, human witnessed drill, live acceptance open.

## Alternatives and Decision State

Select strengthening existing continuity and its consumers. New capability
must use the existing trusted-proxy OID-bound mapping, never caller body or
email fallback. No default grant, no seeded application approval. Constructed
fixtures may exercise that permission boundary but must remain labelled.
Corrective results are human-recorded structured evidence, not executed by
the server or proof of actual evaluation. Actual authority is not selected.

## Open Questions, Risks and Residual Uncertainty

OD-35 actual restart authority is explicitly unknown. No seeded actor or test
record can constitute actual human approval.

## Planning Readiness

Ready for bounded engineering Plan only. Research disposition: executed,
complete. Actual authority/live acceptance remains blocked and must be
distinguished from synthetic mechanism tests throughout the loop.
