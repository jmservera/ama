---
title: Setup Entra expiry issue 358 final-candidate plan critique
description: One independent assessment of the bounded offline reassessment plan
ms.date: 2026-10-30
---

## Metadata

* Task ID: 358.
* Critique date: 2026-10-30.
* Plan: .copilot-tracking/plans/2026-10-30/setup-entra-expiry-358-plan.md.
* Phase details: .copilot-tracking/details/2026-10-30/setup-entra-expiry-358-phase-details.md.
* Critique execution status: Complete.
* Assessment count: exactly one independent final-candidate critique.
* Observed branch: fix/setup-entra-expiry-358.
* Observed HEAD and supplied base: 9ee48592a2e80e3a9f9e3c90ef039b9fa1987d19.

## Inputs and Criterion Boundary

* Caller requests the ordered Research, Plan, Implement and independent Review
  loop, followed by a local commit only. This critique stops after writing this
  artifact. No push, PR, Azure, deployment, sign-in, secrets or credential-file
  operation is authorized.
* Supplied research:
  .copilot-tracking/research/2026-10-30/setup-entra-expiry-358-research.md,
  including C1-C9 and W1-W3. Current issue/PR statements are supplied evidence;
  no additional GitHub or cloud query was performed.
* Directly inspected evidence: infra/tests/test_setup_entra.py:1435-1553
  and :2235-2274; infra/scripts/initialize-api-auth.py:170-179;
  infra/README.md:1876-1960;
  .copilot-tracking/reviews/logs/2026-10-19/live-keyvault-preservation-358-review.md;
  .copilot-tracking/changes/2026-10-19/live-keyvault-preservation-358-synthetic-summary.json.
  src/api/pyproject.toml and src/README.md supplied bounded validation and
  publication context. Mandatory project context was consulted without changing it.
* Decisions assessed: documentation/evidence-only implementation; zero source
  and test additions/removals; canonical infra/scripts production ownership and
  infra/tests regression ownership; no generated source/test targets; no
  duplicate preservation helper or tests.
* Dependencies assessed: critique disposition, Python 3.12, existing distribution
  installation after observed missing dependencies, serialized heavy execution,
  separate command-result recording, one independent Review and local identity/
  commit handoff.
* Acceptance boundary: AC1 and AC3 can receive fresh offline evidence; AC2
  remains blocked and cannot be replaced by FakeAzure, mutation tests or the
  historical real temporary synthetic roundtrip. AC4 is prospective and requires
  actual implementation evidence and a local commit.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Q1, FR1, AC1 | Covered | Frozen 2030 clock exercises expired, equal-now, missing and future expiry for generated and legacy names, including check/dry-run/write behavior. Existing mutation test requires assertion failures for both bypasses. Fresh execution remains pending. |
| Q2, FR2 | Covered | Mixed inventory test checks exact KV URL/identity, ordinary and empty values, environment reference and token-store binding across five response shapes. Seven mutations include metadata/value loss and retry/readback guards. |
| Q3, FR3, AC3 | Covered | Legacy main delegates through runpy to setup-entra.py. Existing regression execution is planned; merged lineage is reported by research, not independently re-fetched here. |
| Q4, FR4, AC2 | Covered | Both plan and details retain originally populated deployed-app/full-setup acceptance as unmet. Historical Partial / Residual Review and synthetic exclusions remain unchanged. |
| Scope and ownership | Covered | Zero production/test additions or removals, infra ownership retained, no generated targets, no frontend changes or speculative defect correction. |
| P01-T01, requested checks | Partial | Exact API unittest command, Ruff lint, Ruff format check, mypy and both infra test selectors are retained with separate outcomes. Runtime file locations need PC-001 correction. |
| P01-T01, heavy admission | Partial | flock -w 600 is explicitly retained, but its proposed lock location conflicts with the active filesystem boundary; PC-001. |
| P01-T02, AC4 | Covered | Dated runbook reassessment and current RPI records are justified; historical records and source/tests remain byte-preserved. Execution and commit are not yet proven. |
| P01-T03, independent Review | Covered | One fresh reviewer receives exact candidate diff/base and all evidence pointers. Findings are routed without a repeat Review or silent repair loop. |
| P01-T03, local handoff | Covered | Privacy-safe authenticated identity resolution and coauthor trailer are required. No push, PR, full receipt or hosted/human approval is claimed. |
| FU1, dependencies and residual risk | Covered | Authorized populated-target evidence belongs to a separately scoped operator/coordinator plan; no safe offline substitute is invented. |

## Verdict

* Verdict: Revise.
* Severity counts: Critical 0; High 0; Medium 1; Low 0.
* Rationale: The bounded reassessment is evidence-backed and preserves literal
  issue acceptance. One execution-location conflict must be corrected before
  implementation. It does not justify adding source/tests, weakening validation,
  changing acceptance or requesting cloud authority.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Resolve runtime file locations before executing the retained checks

* Related IDs: P01-T01; plan User Decisions and Requirements, Non-Functional
  Requirements and Dependencies; phase-details P01-T01.
* Evidence: The plan and details prescribe
  `flock -w 600 /tmp/ama-rpi-heavy.lock`; details also place the writable pip
  environment under an external session folder, and the plan calls for captured
  external logs. The active execution boundary prohibits temporary-directory
  file operations and requires created files to remain within the project.
* Concern: The proposed commands cannot be followed verbatim within that
  boundary. A flock lock file is still a file operation. Quietly choosing a
  different lock would also risk losing serialization with concurrent heavy
  work.
* Impact: Implementation could violate the filesystem boundary or report
  validation performed without the requested shared admission control. This is
  an execution prerequisite, not a reason to count checks as passed or skipped.
* Smallest useful change: Retain `flock -w 600`, every requested API/infra check,
  separate exit-status capture and the no-cloud boundary. Have the coordinator
  identify a permitted project-local lock location that actually coordinates
  the relevant heavy workers, and permitted run-owned environment/log paths.
  If shared coordination cannot be established, record admission as blocked;
  do not use an isolated replacement lock, remove flock or perform forbidden
  writes. Keep runtime files out of the committed documentation/evidence delta.
* Action owner: Planning parent/coordinator.
* Exact resolving evidence: Revised plan/details name compliant writable paths
  and the common-lock coordination basis, or explicitly record P01-T01 blocked
  before execution. Subsequent changes evidence records the exact
  `flock -w 600` invocation/admission outcome and separate requested command
  outcomes without claiming a substituted lock provides serialization.
* Decision route: Direct planner correction within existing constraints. No
  significant or divergent user decision and no new cloud/credential permission
  are required. Do not waive the filesystem boundary to preserve a literal path.

## Strengths and Residual Risk

* No demonstrated source defect or missing regression supports duplicate code
  or test work. The proposed runbook reassessment is a legitimate bounded
  implementation, not evidence that the whole issue is delivered.
* Expiry assertions are behavioral and mutation-sensitive, not merely textual.
  Preservation assertions include both exact metadata and application bindings.
* The earlier real synthetic roundtrip is not mislabelled as mock execution;
  equally, it is not promoted into full secret_reference, token-store/auth
  consumption or originally populated target acceptance.
* AC2 is explicitly accepted as residual blocked work under caller limits.
  Completing P01 must not check AC2, close #358 or use a closing keyword.
* Explicit API checks and flock -w 600 remain required. Recording an unrelated
  baseline failure honestly is appropriate; it is not passing acceptance.
* Independent Review can assess the bounded result with unresolved findings
  recorded. Local commit is not publication approval. Any later publication
  still requires the repository gate and independent exact-head assessment.

## Questions or Blocking Evidence Gaps

* No user question is required for the supplied acceptance boundary.
* PC-001 requires coordinator resolution before heavy execution. If compliant
  shared-lock admission is unavailable, preserve the blocked result rather than
  invent successful validation.
* Fresh test results, implementation delta, independent Review and local commit
  do not yet exist as completed evidence in this candidate.

## Limitations

* This is a plan credibility assessment, not an implementation Review or test
  run. No dependencies were installed and no application/setup CLI was invoked.
* Historical cloud observations and merged-PR metadata are assessed only through
  supplied research and committed sanitized evidence. No current provider,
  deployed-resource or credential state was inspected.
* Direct inspection confirms the cited regression logic and delegation, not
  runtime success. No original historical Review outcome is upgraded.
* The critique writes only its designated artifact; plan, details, research,
  source, tests and earlier evidence remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent/coordinator.
* Smallest next action: Correct execution paths/shared-lock admission or record
  the prerequisite blocked, disposition this one critique, then continue the
  ordered bounded loop only within the resolved constraints.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/setup-entra-expiry-358-research.md](.copilot-tracking/research/2026-10-30/setup-entra-expiry-358-research.md) | Supplied focused research |
| [.copilot-tracking/plans/2026-10-30/setup-entra-expiry-358-plan.md](.copilot-tracking/plans/2026-10-30/setup-entra-expiry-358-plan.md) | Final-candidate plan assessed |
| [.copilot-tracking/details/2026-10-30/setup-entra-expiry-358-phase-details.md](.copilot-tracking/details/2026-10-30/setup-entra-expiry-358-phase-details.md) | Execution details assessed |
| [.copilot-tracking/reviews/plans/2026-10-30/setup-entra-expiry-358-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/setup-entra-expiry-358-plan-critique.md) | This original independent critique |

## Next Steps

The active planning parent should directly disposition PC-001 and finalize
without another critique. Preserve AC2 blocked, the requested checks and
flock -w 600. No user action is required. This reviewer stops after writing
this artifact; it does not invoke implementation, Review, commit or publication.
