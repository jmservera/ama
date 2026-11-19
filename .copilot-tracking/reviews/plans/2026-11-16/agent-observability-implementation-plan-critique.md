<!-- markdownlint-disable-file -->
---
description: Standard critique of the agent observability implementation plan
ms.date: 2026-11-16
---

# RPI Plan Critique: Agent observability implementation

## Metadata

* Task ID: agent-observability-implementation
* Critique date: 2026-11-16
* Plan: .copilot-tracking/plans/2026-11-16/agent-observability-implementation-plan.md
* Critique execution: Complete
* Critique depth: standard, first-task default
* Critique type: initial; no earlier critique

## Inputs and Criterion Boundary

* User requested OTel instrumentation, applied recommendations and Agent 365
  future proposals in the capstone executive deck, with end-to-end progression.
* Evidence: supplied plan and its explicit source references, plus
  .copilot-tracking/research/2026-11-16/agent-observability-agent365-research.md.
* Boundary: implementation credibility, requirements, dependencies, packaging,
  privacy and publication. No live tenant/operational acceptance is inferred.

## Lens Assessments

| Lens | Scope | Reasoning effort and source | Status | Candidates |
|---|---|---|---|---|
| Coverage | All tasks and FR/NFR | Host default | Complete | Adopted PC-001/002; rejected restatement-only and speculative candidates |
| Evidence | Research-to-plan fit | Host default | Complete | Adopted PC-003; deck/status/metadata concerns checked against parent reads |
| Executability | Dependencies, tools and gates | Host default | Complete | Adopted PC-004; ancestry allegation disproved |
| Risk | Privacy, authority and shared environment | Host default | Complete | Adopted PC-005/006; rejected already-prohibited bypasses |

## Coverage Assessment

* FR-001/002/003 and NFR-001/002: covered by P01/P02, with explicit test
  contract refinements in PC-001.
* FR-004 and the wider PRD measurement contract: bounded scope needs PC-002.
* FR-005/NFR-003: P04 explicitly blocks publication on missing exact-head evidence.

## Verdict

* Verdict: Revise.
* Severity counts: 0 Critical, 0 High, 6 Medium, 0 Low.
* Execution is complete; planning parent must dispose the six refinements.

## Findings

### PC-001 [Medium]: Make privacy/configuration/timeout test cases explicit

* Related IDs: P01-T01, P02-T01, P02-T02, NFR-001/002.
* Evidence: plan names real SDK exported-shape tests and existing slot/timeout
  tests, but does not enumerate every configuration, metric-cardinality and
  carrier assertion.
* Concern and impact: implicit test coverage could omit a required edge case.
* Smallest useful change: name default-off/invalid/duplicate configuration,
  metric/carrier canaries, sampling and timeout/late-thread/slot assertions
  within existing addition budgets.
* Action owner: planning parent.
* Exact resolving evidence: updated P01/P02 test details and named owning suites.
* Decision route: direct planner correction.
 
### PC-003 [Medium]: Record the package-selection evidence and current tool state

* Related IDs: P01-T01, Sources, Executive Summary.
* Evidence: parent directly queried dated PyPI metadata and verified Python
  3.12.15 in its external task directory; the plan records these outcomes but
  omits the exact metadata URLs and leaves the initial missing-tool summary stale.
* Concern and impact: insufficient provenance and an internal summary inconsistency.
* Smallest useful change: cite PyPI URLs and compatible constraints, record the
  isolated interpreter path, refresh the summary and justify direct SDK versus distro.
* Action owner: planning parent.
* Exact resolving evidence: current summary and package decision/source record.
* Decision route: direct planner correction.
* Rejected candidates: the supplied capstone source guide, already read by the
  parent, explicitly establishes 55 slides, protected pages and jump counts.
  Lack of that evidence in older research does not invalidate newer plan evidence.
  BRD NFR-004/012/014 and ADR 0001 status were verified directly; ADR 0006's
  Status says Accepted on 2026-10-15. No mutation of completed research is needed.

### PC-004 [Medium]: Make restoration, export bounds and final-deck dependencies explicit

* Related IDs: P01-T01, P03-T02, P04-T01.
* Evidence: Python 3.12.15 restored; other named tools remain absent. Export
  bounds and final deck dependence on runtime evidence are currently qualitative.
* Concern and impact: avoidable rework and ambiguous measurable acceptance.
* Smallest useful change: state batch/queue/export/shutdown defaults, final deck
  dependency on P02, isolated prerequisite route and resolver/install/image
  verification commands.
* Action owner: planning parent.
* Exact resolving evidence: task details and prerequisite decision table.
* Decision route: direct planner correction.
* Rejected High ancestry finding: direct git verification shows HEAD and the
  local/remote research parent at 723d502687ee148c7cbd869cad2ec3036e71a8a2;
  that SHA is an ancestor and is their merge-base. PR 1823 is OPEN at that head.
  The critic's bfed6c99 assertion has no matching evidence and must not trigger
  an unauthorized rebase.
* Tool absence is an explicitly retained publication blocker, not proof that
  implementation is impossible. Node 26.13.0 and Docker were observed; local
  SQL/browser prerequisites remain for the canonical gate to verify/provision.

### PC-005 [Medium]: Use random trace IDs rather than business-derived export references

* Related IDs: P02-T01, FR-002, NFR-001.
* Evidence: plan proposes SHA-256 task references, while raw case identifiers are
  forbidden and existing production task IDs are already content-derived digests.
* Concern and impact: generic hashing does not anonymize low-entropy identifiers;
  no business-derived exported identifier is necessary for the required audit join.
* Smallest useful change: use randomly generated OTel trace/span IDs for exports
  and record those IDs in the protected JSON audit; retain task/meter/source
  identifiers exclusively in existing protected records. No schema migration.
* Action owner: planning parent.
* Exact resolving evidence: revised P02 contract; no case/task hashes in exports.
* Decision route: direct planner correction; no new HMAC key or authority required.
* Rejected High redaction finding: P02-T02 already requires retaining every
  redaction behavior and explicitly rejecting extras/exception content. JSON
  formatting is downstream of the same process-wide guarded LogRecord path;
  tests will assert final serialized output, not just logger calls.

### PC-006 [Medium]: Specify configuration secrets, failure behavior and proposal privacy conflict

* Related IDs: P01-T01, P03-T01/02.
* Evidence: F6's mandatory Agent 365 fields conflict with content-free diagnostics;
  export secrets/failures need precise operating guidance.
* Concern and impact: enabling telemetry must not expose credentials, stall
  controlled work or imply Agent 365's privacy compatibility is established.
* Smallest useful change: fail fast on invalid enabled configuration, export
  asynchronously with finite bounds and content-free failure reporting, keep
  destinations/credentials out of errors, and explicitly describe Agent 365's
  unresolved payload conflict in roadmap/notes/Q&A.
* Action owner: planning parent.
* Exact resolving evidence: configuration/failure contract and P03 proposal text.
* Decision route: direct planner correction.
* Rejected optional-package restriction: the SDK/exporters are already an
  optional core extra and deployment export is opt-in. The user authorized
  package selection; audited pinned installation is not tenant activation.

## Strengths and Residual Risk

* Core authority, default-off export, full gate, no paid inference and future-only
  Agent 365 are consistently bounded. Tool and tenant acceptance remain separate.
* All candidates were checked against the supplied boundary and parent evidence;
  speculative restatement requests were not promoted to requirements.

## Questions or Blocking Evidence Gaps

* No significant or divergent owner decision needed.
* Missing tool/live acceptance evidence remains a later validation/publication
  gate, not a basis to fabricate success.
* Rejected candidates: timeout was already required in the task and risk table,
  so lack of a named method is not High. Mandatory new file/method names are not
  needed for every already-explicit behavior. Metric canaries are already
  required by NFR-001; this refinement does not add scope.

### PC-002 [Medium]: Separate this slice from the full proposed measurement system

* Related IDs: P02-T01, P03-T01, FR-004.
* Evidence: the PRD scenario-completion method is wider than invocation metrics;
  research F1-F3 retain unproved job, harm and operational coverage.
* Concern and impact: citing the complete contract could overstate delivery.
* Smallest useful change: explicitly defer broader business-scenario SLOs,
  importer/orchestrator/IoT tracing, resident adapter inventory and billing;
  document started/failed/retried/incomplete invocation denominators and an
  evidence matrix without calling them accepted scenario SLOs.
* Action owner: planning parent.
* Exact resolving evidence: non-goals and P03-T01 coverage matrix requirements.
* Decision route: direct planner correction.

## Limitations

* Source-based assessment only; does not execute validation or authorize export.

## Recommended Next Action

* Planning parent resolves PC-001 through PC-006 directly, then implements.
* No second critique required or authorized. User response required: no.
