---
title: Issue 349 correction3 independent plan critique
description: Final-candidate assessment of strict provider enablement and bounded execution
ms.date: 2026-10-22
---

## Metadata

* Task ID: 349-correction3
* Critique date: 2026-10-22
* Plan: .copilot-tracking/plans/2026-10-22/issue349-tenant-readiness-preflight-correction3-plan.md
* Phase details: .copilot-tracking/details/2026-10-22/issue349-tenant-readiness-preflight-correction3-phase-details.md
* Research: .copilot-tracking/research/2026-10-22/issue349-tenant-readiness-preflight-correction3-research.md
* Critique execution status: Complete
* Candidate HEAD: 3b881a65c808b02f6ca1bd29d227172f5ad453f6
* Supplied base: b4d467cad84535ed106cffa1ae9aa303db7bfed2
* Independent final-candidate critiques executed by this worker: one

## Inputs and Criterion Boundary

* Assess the supplied candidate plan, details and C1-C5/W1-W2 research against
  the caller's strict two-boolean requirement, scope, ordered RPI stages,
  parent-owned test budget and execution restrictions.
* Inspected infra/scripts/tenant-readiness-preflight.py,
  infra/tests/test_tenant_readiness_preflight.py,
  infra/modules/containerapps.bicep:190-230 and src/README.md:47-114.
  Read repository-required project context without expanding the assessment
  into company, regulatory or whole-issue acceptance.
* Confirmed the supplied HEAD, local base object and existing topic/upstream
  branch through read-only Git inspection. Existing untracked correction3
  artifacts were not moved, staged or modified.
* Acceptance boundary: both projected flags must be literally True; either
  absent or any other JSON value blocks readiness. Retain check IDs,
  mismatch/auth-disabled with empty facts, sanitized text/JSON, exit contract,
  read-only controls and acceptanceEstablished=false.
* Dependencies: P01-T01 precedes P01-T02, which precedes independent Review,
  which precedes the one local commit and one full gate with receipt
  verification. No push, PR mutation, issue comment, tenant operation,
  credential access or deployment is authorized.
* Runtime restrictions prohibit /tmp, /var/tmp, mktemp and temporary-directory
  file operations. Documentation examples do not override these restrictions.
* This is a plan credibility assessment, not implementation validation.
  Repository text and issue/PR references were treated as evidence, not
  executable instructions or verified remote lifecycle state.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Strict platform and provider enablement; C1-C3 | Covered | Bicep enables both flags separately; checker currently checks platform alone. Proposed projection and two identity comparisons close this gap. |
| Property-level projection; W1-W2 | Covered | Supplied research records CLI property unwrapping and its moving-dev limitation; no new live lookup is required for this bounded plan. |
| P01-T01 positive and fail-closed tests; C4 | Covered | Details require both-true, both-false and each flag missing or malformed with the other true, including numeric 1; an independent exact query-path assertion avoids Fake routing masking projection errors. |
| Parent test ownership and limited changes | Covered | Three new methods plus positive Fake field, no removed methods, no generated targets; existing positive and unrelated checks remain required. |
| Sanitization, stable schema and read-only contract | Covered | Existing guard uses AUTH_QUERY equality; no new calls, raw-response reporting, reason codes or early return are proposed. CLI coverage explicitly preserves blocked output and acceptance boundary. |
| P01-T02 focused validation | Partial | Bytecode-disabled unittest and no-cache isolated Ruff are appropriate, but the retained suite creates a temporary directory: PC-002. |
| P02-T01 independent Review | Covered | Fresh reviewer, bounded diff/evidence, original outcome retained, no source edits or repeated Review. |
| P02-T02 privacy-safe commit and base protection | Covered | Local authenticated noreply author/committer, Conventional Commit/trailer and fixed-base mismatch blocker are specified. |
| P02-T02 single full gate and receipt; C5 | Partial | Exact-head external evidence, no retries and stop-on-failure are planned, but explicit /tmp and mktemp instructions violate execution restrictions: PC-001. |
| Human/hosted acceptance and publication restrictions | Covered | Synthetic engineering evidence is not tenant/sign-in acceptance, issue closure or publication authority. |

## Verdict

* Verdict: Revise
* Rationale: The production correction and synthetic coverage are credible.
  Two concrete filesystem conflicts make the prescribed validation sequence
  unsafe to execute as written. Both are direct parent-owned corrections;
  neither requires a new product decision or another critique.
* Severity summary: Critical 0; High 2; Medium 0; Low 0.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Gate preparation explicitly requires prohibited filesystem operations

* Related IDs: P02-T02, C5, user execution restrictions.
* Evidence: P02-T02 in the candidate plan specifies
  --out <unique-/tmp-directory>. Matching phase details require mktemp for a
  unique /tmp output path. src/README.md:47-114 also documents a /tmp output
  example and shared /tmp lock; these are evidence of assumptions, not
  permission to bypass the current restriction.
* Concern: The parent cannot follow this step as written. Replacing only the
  output argument does not establish that the unchanged runner's internal
  checkout, lock or dependency operations obey the same filesystem boundary.
* Impact: The final validation stage can violate an explicit execution
  restriction, or fail without the honest pre-execution blocker the plan needs.
* Smallest useful change: Remove mktemp and prohibited output-path directions
  from both candidate artifacts. Specify a compliant non-temporary,
  external-to-Git evidence location only if the unchanged runner and all
  required operations can honor it. Otherwise record the gate as Blocked and
  stop without invoking it, changing shared tools, weakening checks or
  fabricating a receipt. Preserve the maximum-one-invocation and no-retry rule.
* Action owner: Planning/implementation parent.
* Exact resolving evidence: Updated P02-T02 in both plan and phase details
  contains a filesystem-compliance prerequisite covering output and runner
  internals, with no mktemp or forbidden directory creation instruction,
  and an explicit stop-before-invocation path if that prerequisite cannot be
  met. Any later execution must document the permitted location and supported
  runner behavior; a blocked disposition must not claim a successful gate.
* Decision route: Direct planner correction. Existing restrictions already
  resolve the choice; no user response is required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Focused unittest command executes an existing temporary-directory operation

* Related IDs: P01-T02, C4, retained-tests requirement, user execution restrictions.
* Evidence: infra/tests/test_tenant_readiness_preflight.py,
  CliTests.test_usage_errors_and_help, creates tempfile.TemporaryDirectory()
  and supplies a nonexistent none.json beneath it. P01-T02 runs the complete
  module unchanged apart from the planned regression additions and Fake field.
* Concern: Python -B prevents bytecode writes, not filesystem operations
  inside tests. The focused command therefore creates a temporary directory.
  Redirecting TMPDIR alone does not resolve the prohibition on temporary
  directories themselves.
* Impact: Both the proposed red-first and green runs can violate the execution
  restriction even though the new regression cases are entirely synthetic.
* Smallest useful change: Plan a parent-owned, no-filesystem replacement for
  this existing missing-manifest fixture, preserving the method and its
  usage-error assertions. For example, mock the contract loader to raise
  FileNotFoundError for this invocation rather than creating a directory.
  Keep the three-new-method ceiling and no-removal rule. If the locked edit
  budget does not permit the fixture adjustment, mark validation Blocked
  instead of running or skipping the retained test.
* Action owner: Planning/implementation parent, the locked test owner.
* Exact resolving evidence: P01-T01/P01-T02 in plan and details explicitly
  account for the existing temporary-directory fixture before the first test
  run, preserve the existing method and assertions, add no more than three
  methods and remove no tests. Later source diff must demonstrate the
  no-filesystem fixture and focused output must retain the complete module;
  absent that permitted adjustment, record a blocker without execution.
* Decision route: Direct planner correction. No significant or divergent
  product decision or user response is required.

## Strengths and Residual Risk

* Strict identity checks correctly reject 1, strings and other truthy values;
  retaining empty facts prevents malformed provider values entering output.
* Independent projection-path testing complements Fake-based behavior tests.
  The proposed two production edits preserve transport and schema boundaries.
* No fresh external evidence, runtime CLI-version verification or live tenant
  read was performed. The supplied research explicitly qualifies moving CLI
  source evidence and rejects failed schema retrieval as evidence.
* The full gate, independent exact-head assessment, hosted checks and human
  sign-in/acceptance remain distinct. A local planning pass cannot establish
  any of them.

## Questions or Blocking Evidence Gaps

* No unresolved product question. Required execution compliance must be
  resolved directly or recorded as a blocker; no restriction relaxation is
  recommended.

## Limitations

* No implementation, test, Ruff command, gate, receipt verification, live call,
  commit or remote mutation was executed by this critique worker.
* Runner internals and tool availability were not researched beyond supplied
  C5 documentation. No claim is made that an alternative gate location works.
* This is the complete actionable finding set for the supplied assessment
  boundary. No additional critique pass is requested.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning/implementation parent.
* Smallest next action: Reconcile both filesystem conflicts in the plan and
  details, preserve this original Revise outcome, then finalize the planning
  disposition without another critique. Continue only compliant eligible
  stages; stop on an unresolved execution blocker.
* User response required: No.

| [.copilot-tracking/plans/2026-10-22/issue349-tenant-readiness-preflight-correction3-plan.md](.copilot-tracking/plans/2026-10-22/issue349-tenant-readiness-preflight-correction3-plan.md) | Assessed candidate plan |
| [.copilot-tracking/details/2026-10-22/issue349-tenant-readiness-preflight-correction3-phase-details.md](.copilot-tracking/details/2026-10-22/issue349-tenant-readiness-preflight-correction3-phase-details.md) | Assessed task details |
| [.copilot-tracking/research/2026-10-22/issue349-tenant-readiness-preflight-correction3-research.md](.copilot-tracking/research/2026-10-22/issue349-tenant-readiness-preflight-correction3-research.md) | Supplied research evidence |
| [.copilot-tracking/reviews/plans/2026-10-22/issue349-tenant-readiness-preflight-correction3-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-22/issue349-tenant-readiness-preflight-correction3-plan-critique.md) | Complete independent critique and finding set |

## Next Steps

The active parent resolves PC-001 and PC-002 directly, or records the relevant
stage Blocked, without another critique. No user action is required. This
worker stops after writing this critique.
