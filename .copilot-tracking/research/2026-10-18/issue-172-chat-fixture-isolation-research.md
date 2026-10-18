<!-- markdownlint-disable-file -->
# Task Research: issue-172-chat-fixture-isolation

| Field | Value |
| --- | --- |
| Date | 2026-10-18 |
| Researcher | RPI parent, inline |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-18/issue-172-chat-fixture-isolation-research.md |

## Research Brief

Investigate the claimed mismatch between eleven persona perspectives and eligible
same-role thread owners, then identify any missing contractor-as-actor denial
coverage. Intended use: bounded offline fixture correction, not issue closure.
Output mode: convergence. Research is read-only except evidence and required state.

## Research Parameters

Focused posture selected from explicit caller scope. Candidate internal sources:
`src/agents/tests/chat_fixture.py`, its fixture/provenance tests, API role tests,
component guides, public data dictionary and SN-08 inventory. External sources:
current GitHub #172, #158, #167 and linked delivery #283/#279 only.
Resolved evidence root: `.copilot-tracking/`. No private inputs, runtime edits,
UI, paid inference, live cloud, policy approval or invented volume acceptance.

## Extension Registry and Provenance

Repository instructions selected for privacy, branch, validation and KB rules.
`rpi-research` selected for ordered waves and evidence. RPI Plan, Implement and
Review reserved for later actual phases. No domain research worker: this is one
tightly coupled trace. Independent critique and original Review will be delegated
once each as explicitly requested.

## User Participation and Research Decisions

Caller explicitly requested the full ordered loop and publication on this branch;
no interactive clarification is needed or available. Preserve adverse verdicts,
route later defects to coordinator (at most two corrections), no second Review.

## Scope and Success Criteria

Preserve 22 personas/11 perspectives and role/task mappings; zero contractor-owned
threads. Verify baseline before prescribing a correction. Derived owner coverage,
explicit read/list/search denial probes with real eligible targets, mutation
sensitivity, lifecycle null content and metadata-only withdrawal ledger, nine
synthetic payloads, canaries and seed determinism are the acceptance boundaries.

## Task Research Requests and Direction Controls

Only fixture helper/tests and directly coupled provenance/roles tests may change,
plus necessary documentation and provenance coupling. SN-08 remains partial.
Do not resume #122/draft #398, change runtime, access private data, or close #172.

## Research Questions

| ID | Question | Status |
| --- | --- | --- |
| Q1 | Does the claimed perspective/eligible-owner contradiction exist? | Open |
| Q2 | Are contractor actor denial probes missing and how can loss be detected? | Open |
| Q3 | Which local commands and public provenance coupling apply? | Open |

## Prior Knowledge Gate

Clean worktree on caller branch `test/chat-fixture-isolation-172` at exact base
`3104bb69ddc26c81e0e9d2f57000dac1d99a419a`; no matching prior PR.
Current #172 has no comments and API blocked_by is empty. Its body is stale:
#158 is CLOSED, owner accepted ADR 0004 as written on October 15, merged #279.
OD-45 to OD-49 remain open. #167 is hierarchy, not a new ordering prerequisite.
Merged #283 already delivered synthetic fixtures; its evidence must be inspected
without replaying private-data commands or treating historical delivery as acceptance.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Started: current issue/dependency/delivery and component evidence discovery.
Reflection: existing delivery disproves "Missing"; owner acceptance disproves
"proposed" as current ADR status. Neither establishes runtime or scope approval.

#### Wave 2: Deeper

Read the helper, fixture/provenance/role tests, component README/pyproject and
source CI. Initial system-Python baseline failed with three missing-package
imports. Installed editable core[dev], agents[dev], API with pip in `.venv`;
the same focused command then ran 11 tests successfully.
Reflection: no failing-test contradiction exists. The test counts thread AND
memory cases, so ineligible thread owners can contribute memory coverage.

#### Wave 3: Contrarian

Executed a read-only build/count probe to challenge the hypothesis. There are
22 personas, 42 threads, 80 turns, 63 ledger events, 22 memory states, 48 memory
items, 55 exclusion probes, 121 isolation cases and 53 deletion cases. Seven
perspectives have eligible thread owners; eleven have sampled memory owner
probes. Contractor tasks are empty and contractor-owned threads are zero.
One contractor already acts in an incidental cross-role read denial; the second
does not, and neither has explicit list/search denial coverage.
Reflection: reject the alleged baseline failure; accept the narrower missing
resource-specific owner and contractor actor coverage. Do not invent eligibility
for support/safety/contractor roles or remove their existing memory fixtures.

#### Parent Synthesis and Disposition

Accept C1-C5 and W1-W5. Reject unconditional eleven thread-owner perspectives:
eleven is persona coverage, not assistant eligibility. Select explicit per-
contractor read/list/search probes against an active eligible staff-owned thread,
and exact eligible-owner checks split from memory coverage. Reject runtime or
role-map changes and frozen snapshot rewrites. No second cycle needed: questions
are answered with direct code, executed baseline and counter-evidence.

## Evidence Log

| ID | Claim | Source | Retrieved |
| --- | --- | --- | --- |
| W1 | #172 stale body, no comments, blocked_by empty | https://github.com/jmservera/ama/issues/172 and dependencies API | 2026-10-18 |
| W2 | #158 closed; accepted as written, OD-45 to OD-49 open | https://github.com/jmservera/ama/issues/158 | 2026-10-18 |
| W3 | Acceptance merged October 15 | https://github.com/jmservera/ama/pull/279 | 2026-10-18 |
| W4 | Prior synthetic fixture delivery merged | https://github.com/jmservera/ama/pull/283 | 2026-10-18 |
| W5 | #167 parent generator hierarchy | https://github.com/jmservera/ama/issues/167 | 2026-10-18 |
| C1 | Empty task users skipped when creating threads | src/agents/tests/chat_fixture.py:86,105-112 | Read/build probe |
| C2 | Existing isolation samples first thread and memory independently; incidental contractor read only | src/agents/tests/chat_fixture.py:173-213 | Read/build probe |
| C3 | Eleven-perspective test mixes memory and thread resources | src/agents/tests/test_chat_fixture.py:84-102 | Read and baseline 11 tests OK |
| C4 | Nine-payload rehashed synthetic-label/email mutation checks | src/agents/tests/test_chat_provenance.py:15-43 | Read and baseline |
| C5 | SN-08 partial, scope/volume open; generator metadata has no source digest | docs/reference/research/retrofit-synthetic-data/needs-inventory.json:183-205; provenance-register.json DS-CHAT-MEMORY-FIXTURE; src/core/src/zava_forward/core/synthetic/scenario_manifest.py source set | Read/search |

## Findings Mapped to Questions and Evidence

Q1 answered C1-C3: hypothesis disproved as a baseline failure; actual thread
owner coverage is seven perspectives. Q2 answered C2-C4: meaningful gap is
explicit both-contractor read/list/search targeting and resource-specific
coverage, protected by removal mutations. Q3 answered C4-C5 and source CI:
focused tests, agents discovery, Ruff lint/format and mypy; public provenance/
scenario tests where coupled. No tracked chat payload or source digest exists
to refresh. `write()` computes the generated manifest aggregate from current
bytes, and existing mutation tests rehash independently. Frozen unrelated
scenario sources and evaluation fingerprints must remain unchanged.

## Alternatives and Decision State

Selected bounded coverage correction after baseline verification (C1-C5).
Evidence-only rejected because incidental one-actor read cannot detect removal
of required both-actor list/search probes. Approval and runtime work deferred.

## Open Questions, Risks, and Residual Uncertainty

SN-08 actual scope/volume approval is unverified; no authority to infer it.
Declarative expected fixture results cannot establish runtime enforcement.

## Planning Readiness

Ready. Research disposition: executed. All three waves completed in order.
Self-check: questions answered, claims traceable, contrary baseline preserved,
privacy/authority boundaries retained. Handoff: parent advances to Plan with
C1-C5; scope/volume approval remains outside this bounded task.
