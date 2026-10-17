<!-- markdownlint-disable-file -->

# Task Research: resident-update-remedy-controls-88

| Field | Value |
| --- | --- |
| Date | 2026-10-17 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | In progress |
| Artifact path | .copilot-tracking/research/2026-10-17/resident-update-remedy-controls-88-research.md |

## Research Brief

* What to research: actual resident commitments, complaint/remedy records, independent closure clocks and writer validation for issue #88.
* Why it matters: closure must never imply resolution of another outstanding issue.
* Audience: implementation and independent critique/review.
* Scope: committed main 1a05dfb8a4c4d9992d72a57228ce15123e9bcf2c, src core/API, directly related tests and guides.
* Non-goals: communications, real resident/legal authority, portals, paid AI, Azure, #92 held changes or other dirty worktrees.
* Criteria: explicit purpose, named current owner, due date and basis; independently owned/dated response, remedy, defect, charge-query and delivery/handover/finance states.
* Requested outputs: evidence-grounded minimal amendment recommendation and planning handoff.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | Which existing records and endpoints can satisfy the exact criteria, and where must transaction-time validation occur? |
| Codebase scope | src/core, src/api, requirement sources and related KB routes |
| External scope | GitHub issue/PR lifecycle only; no new legal claims |
| Initial internal candidate areas | workflows.py, resident_decisions.py, store.py, sqlstore.py, complaint/update tests |
| Initial external candidate areas | jmservera/ama issue 88 |
| Research posture | focused |
| Posture provenance | bounded caller scope and named source references |
| Explicit limits | one final critique, one original Review; at most two authorized correction cycles |
| Completion basis | exact scope coverage and source-grounded counter-evidence |
| Edits allowed during research | no source edits |
| Resolved evidence root | .copilot-tracking/ |
| Exclusions | other worktrees, private data/roster, unmerged #91/#92/#102 source |

## Extension Registry and Provenance

| Kind | Candidate | Provenance and scope | Disposition |
| --- | --- | --- | --- |
| Instruction | repository instructions | all source and evidence paths | selected; src-only, safe branch, privacy-safe commit, KB append-only |
| Skill | rpi-research | selected RPI wrapper and caller ordered lifecycle | selected; actual three-wave execution |
| Skill | web-design-guidelines | applicable only if web edits needed | deferred pending source discovery |
| Specialist | RPI Researcher | registered research lanes | skipped; single coupled source trace handled inline |

## User Participation and Research Decisions

Caller explicitly requests the complete ordered lifecycle and authorized commit/push/PR.
No routine phase approval is needed. State records automatic execution of this explicit
request; no additional follow-up work is authorized.

## Scope and Success Criteria

Preserve merged stock/hazard/procurement/finance/grant semantics, original event provenance,
reopen/history and rollback/post-commit outcome behavior. Missing identity and unknown legacy
provenance must remain explicit. Use small fictional data only.

## Task Research Requests

Verify PRD FR-033/049 AC-063 and BRD FR-047 AC-089 against actual implementation/tests,
not stale issue notes. Parent #81 is hierarchy, not a dependency.

## Direction Controls

| Control | Direction | Provenance | Effect |
| --- | --- | --- | --- |
| narrow | existing records/routes, minimal domain changes | caller | reject new architecture |
| exclude | #92 hold and other dirty worktrees | caller | only current committed main |
| preserve | current actor/input/date checks at writer transaction | caller | investigate save hooks and recovery |

## Research Questions

| ID | Question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | Existing commitment and independent closure shapes? | depth | High | open |
| Q2 | Exact mutation, authorization and SQL writer boundaries? | depth | High | open |
| Q3 | Smallest sufficient tests and actual isolated SQL execution? | depth | High | open |

## Prior Knowledge Gate

Original/addendum, KB index/memory and src/core/API guides read at intake.
Branch is clean, at exact supplied committed main base, with no source from other worktrees.
Issue 88 fetched fresh via REST; first GraphQL PR lookup hit rate limit and will be retried
using REST. Old issue notes remain unverified.

## Research Cycle Log

### Cycle 1

Focused inline Wider -> Deeper -> Contrarian.

### Wave 1: Wider (executed)

Actual PRD/BRD and source search finds only handoff-created resident_update
owner/due pairs, a single service request status and existing quality/procurement/
finance objects. No independent remedy status exists. Existing resident panel
already hosts service actions, so small additions there avoid another screen.
Reflection: prioritize resident_action, handoff compatibility, projections and SQL save;
do not amend parallel quality.py/assistants.py or progress.py.

### Wave 2: Deeper (executed)

Resident action validates cached staff once and saves directly; failures can mutate JSON
before validation completes. SQL has additive domain validation hooks and rowversions.
Merged hazard scope explicitly distinguishes committed errors from rollback and quarantines
audit before recovery I/O. Reuse this existing boundary instead of inventing another store.
Complaint close currently sets only request status but has no distinct remedy lifecycle.
Reflection: explicit subordinate remedy state is required; desired_outcome is insufficient.

### Wave 3: Contrarian (executed after Deeper)

Read actual quality, procurement, projection, task queue and existing handoff/service
tests. Counter-evidence: no existing package/quality/finance function currently clears
service_requests; therefore no blanket package guard or new closure architecture is
justified. Existing independent work-order and quality history already retains dates
and named actors. Reuse and assert invariance rather than duplicate those clocks.
Handoff tests demonstrate implicit owner/due-only creation, contradicting the complete
commitment criterion. Reject continued partial creation: create full commitments through
the existing resident route; handoff may preserve/reference them but cannot create one.
Legacy stored pairs remain visible with Unknown provenance, not automatically enriched.
Fresh installed-src baseline: 59 tests, OK, one existing opt-in skip. HTTP fixture
explicitly logs unavailable law-store evaluation; no legal acceptance inferred.
Reflection: scope is covered, no further research cycle needed before bounded planning.

## Evidence Log

| ID | Evidence | Finding |
| --- | --- | --- |
| C1 | docs/prds/zava-forward-retrofit-programme-demonstrator.md:868,884,1481,1509 | exact commitments and closure independence; full AC includes broader scope/lease controls beyond issue's three criteria |
| C2 | docs/brds/agentic-retrofit-programme-brd.md:1429 | BRD FR-047/AC-089 confirms response/remedy separation |
| C3 | src/core/src/zava_forward/core/workflows.py:158-202 | handoff creates owner/due only; preserves prior update but cannot explicitly manage it |
| C4 | src/core/src/zava_forward/core/resident_decisions.py:203-218,309-372 | service route supports named owners but one status; single cached identity check |
| C5 | src/core/src/zava_forward/core/sqlstore.py:540-657 | shared transaction validation, rowversions, commit marker and pre-I/O discard |
| C6 | src/core/src/zava_forward/core/hazard.py:16-112 | reusable current-subject validation and truthful post-COMMIT decision scope |
| C7 | src/api/src/zava_forward/api/web/panels.js:122-148 | existing resident panel hosts update/close requests; minimal extensions possible |
| C8 | src/core/src/zava_forward/core/quality.py:128-175; procurement.py:398-409 | independent defect and handover events; package completion updates work order only |
| C9 | src/core/src/zava_forward/core/projection.py:139-180 | contractor allowlist exists; resident-only additions must be stripped for other staff |
| C10 | src/core/tests/test_handoff_lifecycle.py:53-96; src/core/tests/test_finance_signoffs.py:289-310 | retain intentional complaint response-close and handoff history patterns |
| C11 | src/core/src/zava_forward/core/taskqueues.py:280-287 | existing independent update deadline can consume full commitment unchanged |
| W1 | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (retrieved 2026-10-17) | native labelled forms, inline live errors/focus, keyboard/manual access; repository Fluent/content rules take precedence |

## Findings Mapped to Questions and Evidence

Q1 answered by C1-C4/C8: complete commitment and distinct remedy object are missing,
while delivery/handover/provider-finance clocks already exist independently.
Q2 answered by C5/C6/C9: scope per resident action; current actor and destination
checks inside writer transaction, optimistic rowversion, truthful committed outcome.
Q3 answered by C10/C11 and baseline: extend typed resident suites and independently
exercise local SQL Server with unique loopback container/database; browser via existing panel.

## Alternatives and Decision State

Accepted: existing resident endpoint, full commitment/history and subordinate remedy
lifecycle per service request; preserve other domains byte-for-byte.
Rejected: treating desired_outcome as remedy completion; parallel closure registry;
new portal/assistant; blanket procurement hold; implying service or legal authority.
Rejected: silently manufacturing purpose/basis/identity for handoff legacy pairs.
Selected compatibility amendment: optional handoff update metadata may reference an
existing matching full commitment, not create a new incomplete pair. UI moves creation
to existing resident panel. Preserve old pairs as Unknown until explicitly confirmed.

## Open Questions, Risks, and Residual Uncertainty

Shared SQL save-hook overlap with #91/#102 must be declared, not avoided through duplicate stores.

## Planning Readiness

Ready. Research disposition: executed. All three waves completed in order.
No unresolved source prerequisite or explicit issue dependency. Full PRD AC-063 also
contains lease/scope/age-band governance outside the exact issue criteria; this task
does not claim full PRD acceptance or invent those authorities/thresholds.

## Self-check

Evidence IDs map all questions; no other worktree/private data read, no source edited
during Research. Only actual baseline execution reported. Proceed to ordered Plan.
