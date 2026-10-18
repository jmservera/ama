<!-- markdownlint-disable-file -->
# Issue 87 appointment controls research

## Research Brief

* Task: #87, parent #81; full ordered RPI requested on 2026-10-18.
* Purpose: prepare implementation of offer-versus-commitment, household
  constraints and configurable missed-appointment human investigation.
* Audience: implementation, independent critique/Review and repository owner.
* Scope: existing src core/API/operations UI, relevant tests and component
  documentation; existing #90 capacity and #88 commitments remain authoritative.
* Non-goals: real scheduling/sending, new crew allocation, invented competence,
  legal approval, consultation hold from unmerged #92, unrelated issue delivery.
* Criteria: user's four exact acceptance criteria and stated bypass,
  concurrency, recovery, privacy and evidence boundaries.
* Requested output: source-grounded findings and a planning-ready handoff.
* Output mode: convergence.

## Research Parameters

* Posture: focused, selected from explicit bounded caller scope.
* Evidence root: `.copilot-tracking/research/2026-10-18/`.
* Initial source head and origin/main: `99056cae7bc679d2ace3e42c75f28577cfce8887`.
* Prior-knowledge gate: supplied backlog-manager gaps are hypotheses pending
  actual readers/writers/tests verification, not fresh validation evidence.
* No interaction needed: detailed explicit user direction resolves intake.

## Direction Controls

Retain works consent separately from appointment agreement; appointment-specific
representative authority must be explicit and bounded. Historical Booked is not
verified commitment. Confirmation provenance must bind actual home/work scope/
order/period/current capacity; material change affects only dependencies.
Strict greater-than threshold and reset must first be checked against sources.
Only a human-investigation task may follow eligible missed access. Urgent safety
must not wait on bundles, routine appointments or investigation.

## Extension Registry and Provenance

* Selected: repository instructions, `rpi-research`, explicit issue and caller
  constraints. They govern evidence placement, authority and source boundaries.
* Research specialist: bounded current-code inventory lane may be delegated to
  the registered RPI Researcher, evidence only, no source implementation.
* Web design and redesign skills: deferred until before any web edit; current
  guidelines retrieval and refresh required for original Review.
* Regulatory register: required before any regulatory evidence use; no new
  legal interpretation is requested.
* Memory is context only and remains unchanged.

## Initial Questions and Candidate Areas

1. What do PRD/BRD/addendum actually authorize for confirmations, no-access
   eligibility, threshold and human reset?
2. Which current source readers/writers and transition paths trust Booked?
3. How can bounded appointment agreement preserve capacity, consent, safety,
   resident commitments and durable post-COMMIT truth?
4. Which existing tests and local SQL/browser/container workflows prove changes?

Internal candidates: named PRD/BRD, addendum, knowledge-base index, resident
journey synthesis, src component READMEs, procurement/resident/capacity/event
contracts, current operation controls and persistence tests.
External candidates: GitHub merged appointment provenance and issue dependencies;
current web interface guidelines when relevant. No private datasets.

## Research Cycle Log

Cycle 1 completed in order on 2026-10-18:

1. Wider: verified merged appointment search and requirement families; delegated
   the substantial current-code inventory to one RPI Researcher. Search returned
   #14, #20, #13, #15 and merged #384, not delivery of #87. Parent #81 is open;
   #389/#92 remains open and is excluded. Origin/main equals pinned base.
2. Deeper: parent verified exact PRD/BRD/addendum wording below. Source lane
   verified actual Booked writer, direct advance reader, capacity validation,
   consent/authority, SQL revalidation, audit, UI and existing test seams.
   Reflection: reuse these seams; new appointment-specific agreement is required.
3. Contrarian: verified that a works decision or attendance authority cannot
   substitute for appointment agreement; legacy Booked has insufficient
   provenance; current capacity is a home-work-order quota, not a visit-slot
   allocation. Bundles cannot establish competence or couple urgency. The source
   authorizes human case closure reset, not arbitrary counter reset.
   Reflection: reject automatic migration/confirmation, new allocation, generic
   no-access counting and imported blanket consultation holds.

Lane evidence: `.copilot-tracking/research/2026-10-18/subagents/issue-87-current-code-evidence.md`.
The parent accepts the cited source inventory and rejects its suggested possible
reuse of Works decision authority for appointment confirmation: explicit bounded
appointment-specific authority is required by the caller.

## Evidence Log

| ID | Evidence retrieved 2026-10-18 | Finding |
| --- | --- | --- |
| C1 | docs/prds/zava-forward-retrofit-programme-demonstrator.md:883,1508,1511 | FR-048/AC-062/065 require three confirmations, bundle agreement and competence, non-digital route, no sending, household constraints/options/pause/owner, cause counts; preference-breach reporting threshold Unknown. |
| C2 | docs/prds/zava-forward-retrofit-programme-demonstrator.md:436,866,1479 | DD-006/FR-031/AC-033: exercise-only default five, strict greater-than, confirmed verified no-access active-case only, exclusions, version history, human closure reset. |
| C3 | docs/brds/agentic-retrofit-programme-brd.md:1420,1430,1436 | FR-046/AC-088, RULE-006/007 distinguish offers, tri-party confirmation, committed package/location/volume/period, owned investigation and next update; no consequence or hazard delay. |
| C4 | docs/case_study_48_addendum.md:128,394-428 | EXA-014 and missed-appointment evidence explicitly authorize sixth-event investigation and human-case-closure reset preserving history; threshold is not sector policy. |
| C5 | src/core/src/zava_forward/core/procurement.py:375-396,504-531; src/core/src/zava_forward/core/store.py:504-527 | Booked currently accepts date and moves Issued to Appointed; direct advance consumes Booked without appointment-specific resident agreement. |
| C6 | src/core/src/zava_forward/core/procurement.py:53-70,82-111,162-235; src/core/src/zava_forward/core/sqlstore.py:546-568 | Retain quota, source, delegated authority, scope, coverage, period and transaction-time dependency validation. |
| C7 | src/core/src/zava_forward/core/resident_decisions.py:25-30,123-218,283-330,469-496,638-707 | Works decision/attendance are separate; measure-bound decisions, update/remedy ownership and committed-response recovery must remain intact. |
| C8 | src/api/src/zava_forward/api/server.py:144-148,728-746; src/api/src/zava_forward/api/web/ops.js:124-207 | Actual API/UI appointment controls require extension; source inventory found no hidden tri-party appointment feature. |
| C9 | src/core/tests/test_quality_procurement.py:790-980; src/api/checks/procurement_browser_check.py:1-194 | Existing actual SQL race/recovery seams and local synthetic browser setup can be reused; no fresh test result is claimed. |
| C10 | src/api/Dockerfile:1-28; src/core/pyproject.toml:15-41; src/api/pyproject.toml:13-57 | Source-context nonroot runtime and configured ruff/mypy/Playwright validation are present. |
| W1 | https://github.com/jmservera/ama/pull/384, retrieved 2026-10-18 with gh | Merged b5d4c8402692758bd929a7ff9bf1832770738346; committed capacity dependency delivered, not appointment agreement. |
| W2 | https://github.com/jmservera/ama/pull/389, retrieved 2026-10-18 with gh | Open consultation proposal; do not import. |
| W3 | https://github.com/jmservera/ama/issues/87 and /issues/81, retrieved 2026-10-18 with gh | Exact four AC and parent hierarchy confirmed; issue remains open. |

## Findings, Alternatives and Decisions

Accepted recommendation: extend existing procurement/domain/API/UI control seams
with explicit scoped offer/agreement records, separate appointment authority,
server-derived current commitment and append-only outcome/configuration history.
Reuse current committed capacity as bounded evidence, not a new visit allocator.

Reject: client-supplied status, retroactive Booked confirmation, using attendance/
works authority as appointment agreement, counting unknown/provider causes,
automatic refusal/sanction, invented breach thresholds or consultation clearance.

Counter reset is authorized only by a named human closing the same underlying
home case whose appointments accumulate, not by disposing an investigation task.
Retain all prior events and configuration versions. Investigation task disposition,
appointment/order completion, pause and remedy/update closure do not close that
case or reset its count. Reopening is not itself a new reset; consumed event IDs
must never become eligible again. Critique PC-001 corrected the earlier unsupported
investigation-case equivalence; exact source C2-C4 governs.

Provider projection contains only necessary safe-contact/adjustment instructions,
never household diagnoses or sensitive reasons. Existing resident-update owner
contracts are reused without silently closing or clearing remedies.

No new material legal claim is needed: the regulatory register was read for the
evidence hierarchy; no snapshot is promoted to new operational clearance.

## Risks and Residual Uncertainty

Operational Housing/Repairs/Resident Engagement ratification, real representative
evidence, competence and supplier commitments remain human prerequisites for live
use, not blockers to synthetic engineering. Local SQL/browser/container evidence
is mandatory before correctness acceptance; currently unexecuted. Further research
is unnecessary because exact source semantics and existing integration seams are
verified. Re-enter only if implementation exposes a material source contradiction.

## Artifact Self-Check and Participation

One focused complete cycle, one bounded source-evidence worker, parent-owned
canonical findings and recommendation. No source changed during Research.
Required internal/external provenance and caller exclusions are explicit.
No private data, external AI, spend or operational action occurred.

## Planning Readiness

Ready. Research disposition: executed. All four issue criteria have source-backed
semantics; implementation and actual validation remain future work.
Next action: parent transitions to Plan, creates plan/details, then runs exactly
one independent final-candidate critique before implementation.
