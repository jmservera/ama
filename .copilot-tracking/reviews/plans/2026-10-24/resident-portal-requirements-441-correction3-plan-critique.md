---
title: Resident validator correction3 independent plan critique
description: One bounded pre-implementation assessment for issue 441
ms.date: 2026-10-24
---

## Metadata

* Task: jmservera/ama#441, correction3.
* Native session: 59f31558-980b-475c-b2e2-3b8d68279ed9.
* Critique execution: Complete.
* Verdict: Pass, for the supplied pre-implementation boundary only.
* Assessment: One independent final-candidate critique; no additional cycle.

## Inputs and Criterion Boundary

The assessed planning inputs are:

* .copilot-tracking/research/2026-10-24/resident-portal-requirements-441-correction3-research.md
* .copilot-tracking/plans/2026-10-24/resident-portal-requirements-441-correction3-plan.md
* .copilot-tracking/details/2026-10-24/resident-portal-requirements-441-correction3-phase-details.md

Actual source and tests were read under
.copilot-tracking/changes/2026-10-23/resident-portal-requirements-441:

* validate-integration.py, including lint(), main(), counter subtraction,
  report construction and the final report write.
* validate-refinement.py, including its shared helper import and both lint
  comparison and direct clean-result checks.
* test_validate_integration.py and test_validate_refinement.py.
* markdownlint.json.

The three supplied external logs were read from the native session's files
directory: 441-correction3-reproduction.log,
441-correction3-contract-probe.log and 441-correction3-main-before.log.
These are supplied external evidence, not committed-test dependencies.

Project context was read in docs/case_study_48_original.md,
docs/case_study_48_addendum.md, docs/reference/README.md,
docs/reference/memory.md and the housing-association primer.
No product or regulatory reassessment was undertaken.

The criterion is whether this exact bounded plan credibly prevents tool
failure from cancelling as inherited lint diagnostics while retaining genuine
diagnostic comparison. It includes test ownership, phase order, ancestry
guards, preservation requirements, committed-candidate Review and stop rules.
It excludes implementation acceptance, publication approval and live gates.

## Coverage Assessment

* AC1 and research C1: Covered. The supplied reproduction records identical
  missing-module outputs and an empty introduced Counter. The actual-main
  log records PASS with 22 hashes. The research explicitly identifies that
  report as an adverse false positive, not valid validation.
* Research C4: Covered. The contract probe supplies clean exit 0, genuine
  exit 1 diagnostics with and without columns, malformed-config failure and
  missing-config output mixed with a genuine MD012 diagnostic at exit 1.
  The unsuccessful initial genuine fixture is honestly retained.
* AC2 and P01-T01: Covered. Research precedes the prospective plan; one
  critique precedes both the guarded bot fast-forward and source edits.
  The recorded b06ca0b4 score-only child of 2b364 must be rechecked before
  integration. Unexpected ref or owned-file movement requires a stop.
* AC3 and P01-T02: Covered. The allowlisted status/output combinations
  exclude empty exit 1, noisy exit 0, unexpected statuses, startup stacks
  and mixed configuration errors. Validation precedes normalization and
  subtraction. Explicit errors replace the current permissive assertion;
  missing executable errors are not defaulted or broadly caught.
* AC4: Covered. Optional columns, complete diagnostic text, duplicate
  counts and shifted-line baseline equivalence are explicit requirements.
  Neither rejecting all exit 1 results nor filtering unknown lines is
  permitted. The current command/config and return triple remain intact.
* AC5 and P01-T03: Covered. The actual files contain eight integration and
  seven refinement test methods. All 15 remain; at most four methods are
  added to the existing integration test file. Planned public-helper and
  actual-main tests cover the defect, not a detached parser surrogate.
  The main test must assert explicit failure and no newly written report.
* Research C2 and shared callers: Covered. Refinement imports this exact
  helper and compares its Counters. A single helper correction reaches
  both callers without changing refinement source or report contracts.
* Validation portability: Covered. Committed tests use local absent-module
  execution and subprocess-result fixtures, not the private installed CLI.
  Separate installed-CLI probes supply real clean, genuine, missing-config
  and malformed-config behavior. Both actual validators are required.
* AC6 and P02: Covered. Implementation and original pre-Review evidence are
  committed before the single Review of that committed candidate. Only
  new Review evidence is committed afterward. The final handoff records
  both identities without claiming exact-head publication approval.
* AC7 and owner preservation: Covered. The plan preserves 52 archival
  whitespace failures, including 12 refinement failures, separately from
  correction-only checks. It retains all seven PRD FAIL/BLOCKED findings,
  30 Not run criteria, automation OFF, unregistered id null, OD/OQ items,
  A5/B6 and live gates. It forbids manual score edits and publication work.

## Verdict

Pass. No substantive planning correction is required by the supplied
evidence. The proposed shared-helper contract addresses both demonstrated
failure modes without changing the genuine baseline comparison or expanding
scope. The test and execution plan is specific enough for implementation.

This is not approval of unimplemented code. Its credibility depends on the
specified checks and later committed-candidate Review actually succeeding.

## Findings

The complete actionable PC finding set is empty.

* Critical: 0.
* High: 0.
* Medium: 0.
* Low: 0.
* Highest-impact PC finding: None.
* Finding action owner: None.
* Resolving evidence for findings: Not applicable.
* Direct planner corrections: None.
* Significant or divergent user decisions: None.

No discoverable concern is withheld for a later critique. The existing owner
directions resolve scope, cycle count, bot ordering and publication authority.

## Strengths and Residual Risk

* The mixed config-error case invalidates presence-of-diagnostic and
  exit-code-only shortcuts; the plan explicitly excludes both.
* The new contract is intentionally limited to the actual built-in-rule
  stdin text emitter. Future incompatible CLI output must fail closed,
  not be silently accepted. No broader format support is needed here.
* Main performs substantial custody checks before lint. The plan restores
  the real repository ROOT/BASE around the main regression so the fixture
  does not fail prematurely on unrelated setup. Review must confirm that
  the observed exception actually originates in lint validity checking.
* Implementation proof is deliberately split between portable committed
  fixtures and external installed-tool probes. Neither alone establishes
  the complete planned behavior.
* The owner accepts preserved archival failures as unresolved evidence,
  not waived acceptance. Later exact-head gate and retained publication
  reviewer admission remain separate coordinator responsibilities.

## Questions or Blocking Evidence Gaps

None within this pre-implementation boundary. No user response is required.

## Limitations

Only supplied materials and the named actual callers/tests were assessed.
No commands, tests, bytecode generation, Git operations, heavy gate, paid
service, cloud operation or PR mutation were performed. Recorded timestamps,
refs and installed version are supplied evidence, not freshly executed
identity or environment checks. Their fresh verification belongs to P01-T01.
No implementation, Review result, requirements quality improvement or
independent publication approval is inferred.

## Recommended Next Action

* Highest-impact finding: None.
* Action owner: Planning parent.
* Smallest next action: Record this Pass, then execute P01-T01's fresh
  exact-ref/path guard and the authorized normal bot fast-forward before
  the bounded source/test edits.
* User response required: No.
* Failure rule: Stop and report if this authorized cycle fails or scope
  becomes unclear. Do not start another correction or critique cycle.

## Next Steps

The active parent may continue the existing correction3 plan only, through
implementation commit, one actual committed-candidate Review and a separate
Review-only evidence commit if successful. Do not run the heavy gate or
publish here. No user command or additional approval is needed to return
this critique; publication and live approvals remain outside its authority.
