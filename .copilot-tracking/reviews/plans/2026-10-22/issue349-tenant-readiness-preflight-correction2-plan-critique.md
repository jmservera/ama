---
title: Issue 349 correction2 final-candidate plan critique
description: One bounded critique of the malformed collection correction plan
ms.date: 2026-10-22
---

## Metadata

* Task identity: issue349-tenant-readiness-preflight-correction2.
* Issue: #349.
* Critique date: 2026-10-22.
* Plan: .copilot-tracking/plans/2026-10-22/issue349-tenant-readiness-preflight-correction2-plan.md.
* Phase details: .copilot-tracking/details/2026-10-22/issue349-tenant-readiness-preflight-correction2-phase-details.md.
* Critique execution status: Complete.
* Assessment count: exactly one final-candidate critique; no nested agents.
* Candidate: 4753af1edf74db7f5cf0ec1025b69d22f72f18f5.
* Requested base: b4d467cad84535ed106cffa1ae9aa303db7bfed2.

## Inputs and Criterion Boundary

* Canonical research: .copilot-tracking/research/2026-10-22/issue349-tenant-readiness-preflight-correction2-research.md, including C1-C8.
* Caller requirements: ordered research, plan, implement and review; strict
  collection-shape handling for audiences, identifierUris and web.redirectUris;
  preserved absent/null behavior; fixed unknown/malformed-response findings,
  sanitized facts and blocked results; offline coverage for every affected field.
* Supplied evidence checked: the three readers and reporting/CLI paths in
  infra/scripts/tenant-readiness-preflight.py; Fake transport, existing CLI tests
  and test inventory in infra/tests/test_tenant_readiness_preflight.py;
  local gate contract in src/README.md and shared-lock implementation in
  tools/rpi-checks.py. The correction1 review was read as historical context,
  not as the independent functional assessment of the present candidate.
* Caller-supplied independent functional outcome: NEEDS CHANGES for the
  candidate against the requested base. Its complete independent report was
  not supplied by path; no additional findings are attributed to that report.
* Repository context consulted: docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md and
  docs/reference/memory.md. No customer or regulatory acceptance is assessed.
* Publication boundary: exactly one complete gate after implementation and
  committed RPI evidence, shared-lock waiting without duplication, fresh
  exact-head/current-base receipt verification, authenticated noreply identity,
  Conventional Commit and Copilot trailer, normal push and draft non-closing PR.
* Constraints: no live tenant, Graph, Entra, Azure, credential or resource
  operations; no force push, merge, other-worktree edits or acceptance changes.
  The execution environment also prohibits file operations in temporary
  directories. This critique writes only its designated artifact.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1-C3; functional shape guards; P01-T01 | Covered | Explicit non-null list validation at all three readers; no iterable coercion or catch-all exception handling. |
| C4-C5; fixed sanitized blocked result; P01-T01 | Covered | Unknown/malformed-response, empty affected-check facts, CLI exit 1, both formats, stderr and sentinel assertions are planned. |
| C5; non-crashing false-ready shapes; P01-T01 | Covered | Matching URI dictionary keys, falsey values, integers, floats, booleans and strings are explicitly included in details. |
| C6; compatibility; P01-T01 | Covered | Missing/null/empty/valid lists, existing member filtering and callback-target dependency precedence are retained. |
| Locked test ownership; P01 | Covered | One canonical test module; no removals; at most three new methods using subtests; original 29 tests remain; no generated targets. |
| C6; focused validation; P01-T02 | Partial | Required checks are named, but the prescribed tool location and default tempfile behavior conflict with the execution constraint: PC-001. |
| Ordered RPI evidence; P02-T01 | Covered | One post-implementation Review records its actual bounded outcome and preserves previous adverse outcomes. |
| C7; one full gate and shared lock; P02-T02 | Partial | Correct one-run and lock-wait intent, but the supplied gate necessarily opens a forbidden temporary-directory lock: PC-001. |
| C8; exact head/current base; P02-T02 | Partial | Receipt verification is required, but the executable sequence fetches main only before the long gate: PC-002. |
| Identity, commit and publication boundaries; P02-T02 | Covered | gh identity/noreply, required commit conventions, committed evidence, external final receipt and no post-gate commits are planned. |
| Issue, draft PR and human acceptance boundary | Covered | Issue stays open, criteria unticked, PR draft without closing keywords; final independent PR review remains coordinator work. |

## Verdict

* Verdict: Revise.
* Severity summary: 2 High; 0 Critical, 0 Medium, 0 Low.
* Rationale: the functional correction and locked regression scope are credible.
  Validation cannot be executed literally under the supplied filesystem
  constraints, and publication freshness needs an explicit post-gate fetch.
  These are execution/publication defects, not a request to broaden the code fix.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Planned validation requires prohibited filesystem operations

* Related IDs: C6-C7, P01-T02, P02-T02; validation and publication prerequisites.
* Evidence: .copilot-tracking/details/2026-10-22/issue349-tenant-readiness-preflight-correction2-phase-details.md:26-28
  explicitly selects /tmp/ama-349-correction2-checks.
  infra/tests/test_tenant_readiness_preflight.py:449 uses
  tempfile.TemporaryDirectory() without a controlled directory.
  tools/rpi-checks.py:1676-1678 hardcodes /tmp/ama-rpi-heavy.lock and opens it
  for creation/write. The caller's environment prohibits temporary-directory
  file operations. The plan does not account for these conflicts.
* Concern: merely replacing the named Ruff environment does not resolve the
  existing test's default scratch behavior or the gate's mandatory shared
  lock. The current plan nevertheless calls the candidate implementation-ready
  and schedules publication without a blocked-prerequisite disposition.
* Impact: literal execution violates the filesystem constraint. Silently
  moving or bypassing the shared lock would undermine required serialization;
  changing the gate helper would exceed the locked correction scope.
* Smallest useful change: remove the prohibited tool path from P01-T02 and
  identify a permitted persistent tool location and controlled project-local
  scratch configuration for focused tests, with no candidate residue before
  gating. Explicitly mark the full gate/publication blocked while the
  supplied runner requires forbidden operations. Do not run it, bypass or
  relocate its shared lock, broaden source scope, claim a passing gate, or
  substitute a second/cloud gate. Preserve the exactly-one-run authorization.
* Action owner: planning parent/coordinator; implementer follows the corrected
  focused-check instructions and stops at the recorded gate prerequisite.
* Exact resolving evidence: revised P01-T02 contains executable permitted
  tool/cache/scratch instructions; revised P02-T02 and handoff explicitly
  record the hardcoded-lock blocker and fail-closed stop. Publication remains
  blocked unless a permitted execution context supporting the unchanged
  shared-lock contract is established and evidenced before the single run.
* Decision route: direct planner correction and prerequisite disposition.
  No user decision can authorize overriding the execution constraint; no
  tool or shared-lock rewrite is recommended within this task.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Current-base verification lacks an explicit final fetch

* Related IDs: C7-C8, P02-T02; exact-head/current-base receipt requirement.
* Evidence: .copilot-tracking/details/2026-10-22/issue349-tenant-readiness-preflight-correction2-phase-details.md:47-50
  fetches main before invoking the full gate and then verifies against
  origin/main. src/README.md's local RPI gate contract explicitly requires
  fetching main again immediately before verification and push.
* Concern: origin/main is a local tracking reference. A shared-lock wait and
  heavy gate can leave it stale even when receipt verification against that
  local value succeeds. The plan checklist's shorthand "fetch/verify receipt"
  does not make the detailed post-gate sequence unambiguous.
* Impact: publication can occur without checking whether the remote base
  moved during the wait or gate, invalidating the claimed current-base proof.
* Smallest useful change: explicitly fetch origin/main again after the gate,
  then verify the new receipt with --base set to that freshly fetched SHA,
  checking the unchanged exact head and clean candidate immediately before
  normal push. If the base differs from the requested/gated base, verification
  fails, or candidate inputs changed, stop publication. Do not automatically
  rebase or consume a second full gate under the exactly-one-run authorization.
* Action owner: planning parent; implementer/coordinator executes the sequence.
* Exact resolving evidence: amended P02-T02 names the second fetch, freshly
  resolved base, receipt verification and fail-closed branch. At publication,
  external evidence records the successful final fetch and exact-head/base
  verification, or records the blocker without pushing.
* Decision route: direct planner correction; existing direction resolves the
  policy. Further gate authorization, if ever needed after invalidation, is
  outside this candidate's authorized execution and is not presumed.

## Strengths and Residual Risk

* The plan addresses both crashes and false-ready iterable inputs rather than
  masking errors with broad exception handling.
* Both output formats, fixed reason/facts, absent/null compatibility and callback
  blocker priority are explicitly planned within the three-method test budget.
* Local functional success is correctly separated from full-gate evidence,
  independent exact-head PR assessment and live/human acceptance.
* The original adverse outcome remains historical. Neither this critique nor
  the correction can establish tenant readiness or complete issue #349.

## Questions or Blocking Evidence Gaps

* No unresolved functional design question requires user input.
* Full-gate execution/publication has the concrete filesystem prerequisite in
  PC-001. The planner must expose it rather than assume a permitted workaround.
* Main freshness is not established by this critique; PC-002 concerns the
  future publication sequence, not an assertion that main has already moved.

## Limitations

* This was a read-only plan credibility assessment, not implementation,
  independent functional re-review, a test run or a gate execution.
* Research-reported baseline tests and installed tools were not rerun or
  independently re-established. No remote freshness, PR state or identity
  operation was performed.
* Research, plan, details, source, tests and prior reviews were not changed.
  Only this requested critique artifact was written.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent/coordinator.
* Smallest next action: correct the validation locations and record the
  mandatory-lock publication blocker, then add PC-002's final-fetch sequence.
* User response required: no for these direct plan corrections. A blocked
  execution prerequisite is not permission to weaken the controls.
* Return this complete finding set to the active parent; no second critique,
  implementation, full gate or additional agent is invoked here.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-22/issue349-tenant-readiness-preflight-correction2-research.md](.copilot-tracking/research/2026-10-22/issue349-tenant-readiness-preflight-correction2-research.md) | Canonical research and C1-C8 evidence. |
| [.copilot-tracking/plans/2026-10-22/issue349-tenant-readiness-preflight-correction2-plan.md](.copilot-tracking/plans/2026-10-22/issue349-tenant-readiness-preflight-correction2-plan.md) | Assessed final-candidate plan. |
| [.copilot-tracking/details/2026-10-22/issue349-tenant-readiness-preflight-correction2-phase-details.md](.copilot-tracking/details/2026-10-22/issue349-tenant-readiness-preflight-correction2-phase-details.md) | Assessed executable task details. |
| [.copilot-tracking/reviews/plans/2026-10-22/issue349-tenant-readiness-preflight-correction2-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-22/issue349-tenant-readiness-preflight-correction2-plan-critique.md) | Complete single-pass finding set. |

## Next Steps

The active planning parent should resolve PC-001 and PC-002 directly and record
their dispositions without commissioning another critique. No user response is
required for those revisions. Stop publication at the documented execution
prerequisite unless it is lawfully cleared; this critique performs no next RPI
stage and no gate.
