---
title: RPI Plan Critique - Issue 118 implementation plan
description: Single final-candidate critique and actionable findings
ms.date: 2026-10-16
---

## Metadata

* Task ID: 118
* Critique date: 2026-10-16
* Plan: .copilot-tracking/plans/2026-10-16/issue-118-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/issue-118-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: implement issue 118 hardened four src
  Dockerfiles, unsuppressed scan and CI tests, full Bicep app evidence, default-off
  production-gated Front Door Premium/WAF/Private Link with no public deployment,
  and explicit Policy/Defender code rationale. No Azure execution, no private
  data, no mvp/prototype changes. Candidate locks <=25 new infra unittest
  methods and one Docker runtime harness, no removals, no generated templates.
* Research and evidence considered: .copilot-tracking/research/2026-10-16/issue-118-research.md;
  direct repository reads of .github/workflows/src-ci.yml, .github/workflows/mvp-ci.yml,
  src/importer/Dockerfile, src/api/Dockerfile, src/agents/Dockerfile,
  src/orchestrator/Dockerfile, infra/modules/containerapps.bicep,
  infra/modules/edge.bicep, infra/governance.bicep, infra/README.md,
  infra/tests/test_governance.py, infra/tests/test_bicep_policy.py; one web
  search and one Microsoft Learn fetch on Azure Container Apps `command`/`args`
  semantics (2026-10-16).
* Decisions, dependencies, and acceptance criteria considered: P01→P02→P03
  phase dependency chain in the phase-details; the plan's NFR banning any
  bypass switch, scan baseline, or ignore list; the <=25 new test method and
  single-harness locks; the existing default-off Front Door Premium/WAF/Private
  Link gating already present in infra/modules/edge.bicep.
* Assessment boundary: this critique can confirm structural/textual accuracy of
  the plan against the current repository state and flag unresolved technical
  ambiguities it surfaces. It cannot execute the entrypoint guard, run Trivy
  against the four images, or deploy to Azure to confirm live Container Apps
  `command`/`args` runtime behavior; those remain implementation-time
  validations the plan itself defers.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|---|---|---|
| P01-T01 (shared guard + harness) | Covered | No existing `src/check-container.py` or guard module found; stdlib-only in-container kernel checks (UID/GID, read-only root, capabilities, NoNewPrivs) are feasible via `/proc/self/status` and are consistent with the research boundary note that Dockerfile cannot set host flags. |
| P01-T02 (wire four Dockerfiles, remove scan suppression) | Partial | `ignore-unfixed: true` in src-ci.yml confirmed as the suppression to remove, consistent with plan; feasibility of the resulting image passing HIGH/CRITICAL-with-unfixed is unverified (PC-002). |
| P02-T01 (job args, compiled proof across six consumers) | Partial | `command:` overrides confirmed in containerapps.bicep (token_store, digest_blob jobs), correctly identified as entrypoint-bypassing; the args-only replacement's correctness in Azure Container Apps is not verified (PC-001). |
| P02-T02 (Defender/Policy non-mutating rationale) | Covered | governance.bicep currently submits a `Microsoft.Security/pricings` resource unconditionally (Free/Standard toggle), confirming the exact downgrade risk the research flagged; Bicep `for ... if` conditional-resource syntax is valid, so the "submit no pricing resource when disabled" fix is technically feasible. |
| NFR: no bypass switch/scan baseline/ignore list | Partial | Locks out a `.trivyignore` or severity exception even for unfixed, no-patch-available CVEs, with no documented fallback if the four pinned base images or their dependencies carry such a finding (PC-002). |
| Lock: <=25 new infra unittest methods | Partial | Plausible but unbudgeted; P02-T01 alone implies proof obligations across six image consumers, replica/probe config, three-way Front Door gating, and Defender/Policy rationale, with no stated consolidation technique (PC-003). |

## Verdict

* Verdict: Revise
* Rationale: The plan's core intent and most decisions are evidence-backed and
  consistent with the current repository state (Defender downgrade risk, job
  command-override bypass risk, Front Door gating already present). However,
  two decision-critical technical assumptions remain unverified and could
  make specific acceptance criteria unattainable as currently worded: (1)
  whether Azure Container Apps actually honors `args` without `command` to
  reach the Dockerfile ENTRYPOINT, which the P02-T01 fix depends on, and (2)
  whether the four pinned images can pass an unsuppressed HIGH/CRITICAL scan
  given the NFR's explicit ban on any ignore list or bypass. Both are
  resolvable by targeted research/spike before or during P01-T02/P02-T01
  rather than requiring a full re-plan.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Unverified ACA `args`-only ENTRYPOINT semantics for job command overrides

* Related IDs: P02-T01, phase-details P02, research "Job command overrides
  would bypass a new image entrypoint."
* Evidence: infra/modules/containerapps.bicep lines ~243 and ~382 confirm two
  jobs set `command: [...]` with no `args`. A 2026-10-16 web search and
  Microsoft Learn ARM reference check found documented community reports
  (microsoft/azure-container-apps#926, a related Stack Overflow thread) that
  Azure Container Apps' `args` field may be ignored or behave inconsistently
  unless `command` is also set, which differs from plain Docker/Kubernetes
  semantics where `args` alone overrides CMD while ENTRYPOINT is preserved.
  The research document only checked Container Apps schema for
  `securityContext`/`readOnlyRootFilesystem`/capabilities fields; it never
  checked `command`/`args` runtime semantics.
* Concern: P02-T01's fix ("convert maintenance command overrides to args")
  assumes `args`-only will route job execution through the new Dockerfile
  ENTRYPOINT guard. If ACA's actual behavior diverges (as community reports
  suggest), the compiled-template proof can only assert Bicep structure
  (`args` present, `command` absent), not that the guard actually executes
  for these jobs — silently defeating the goal the task is meant to
  guarantee for the two maintenance jobs.
* Impact: Acceptance criterion "Keep job arguments through entrypoint" could
  be met on paper (compiled template) while being false at runtime in any
  future hosted deployment, which is exactly the class of unearned claim the
  plan says it must avoid ("Hosted controls and scans without successful
  execution remain unmet and are reported honestly").
* Smallest useful change: Before or during P02-T01, add one explicit research
  step (Microsoft Learn ARM reference confirmation or a local `az containerapp`
  schema/validate check, no live deployment required) confirming whether
  `args` without `command` is honored against the Dockerfile ENTRYPOINT for
  Container Apps Jobs at API version 2025-07-01. If confirmed unreliable,
  revise P02-T01 to keep `command` for these jobs but have `command` itself
  invoke the shared guard module explicitly (e.g.
  `command: ['python', '-m', 'zava_forward.core.guard', 'python', '-m', 'zava_forward.orchestrator.token_store']`),
  and document that this is not identical to Docker ENTRYPOINT preservation.
* Action owner: Planning parent (direct correction to P02-T01 task wording)
  with a bounded research addendum; escalate to user only if Microsoft Learn
  documentation is itself ambiguous after the check.
* Exact resolving evidence: an updated phase-details P02 entry naming the
  confirmed ACA `command`/`args` behavior and the exact Bicep field(s) the
  implementation will set for each of the two maintenance jobs.
* Decision route: direct planner correction (research/documentation check),
  escalating to a user decision only if official sources remain ambiguous.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: No feasibility check for unsuppressed scan against the "no ignore list" NFR

* Related IDs: P01-T02, Non-Functional Requirements ("No third-party runtime
  dependencies, bypass switch, scan baseline or ignore list"), Acceptance
  Criteria ("HIGH/CRITICAL scan include unfixed findings").
* Evidence: .github/workflows/src-ci.yml currently sets `ignore-unfixed: true`
  for all four images; the research document records this as the suppression
  to remove but does not record any trial scan (locally or in a prior branch)
  confirming the four pinned `python@sha256:...` images and their installed
  dependencies pass HIGH/CRITICAL scanning once unfixed findings are included.
  Trivy is not installed in this environment, so this critique could not
  independently verify it either.
* Concern: the plan simultaneously (a) requires the scan to include unfixed
  findings and pass, and (b) bans any bypass switch, scan baseline, or ignore
  list as a way to handle a true no-vendor-patch-available finding. If such a
  finding exists today in any of the four images (common for `slim` base
  images), there is no planned escape valve, and the acceptance criterion
  becomes unattainable without either bumping the pinned digest (which does
  not help for genuinely unfixed CVEs) or relaxing the NFR.
* Impact: this could block P01-T02/P03-T01 completion entirely, or force an
  un-planned relaxation of a stated non-functional requirement late in
  implementation, with no documented fallback for the user to approve in
  advance.
* Smallest useful change: run one bounded local validation (`docker build` +
  `trivy image --ignore-unfixed=false --severity HIGH,CRITICAL` for each of
  the four images, as P03-T01 already plans to do with "Trivy if available")
  earlier, as part of P01-T02 rather than only at P03-T01, so a real failure
  is discovered while the fix is still scoped, not after P02 work is built on
  top of it. If a genuine unfixed finding appears, bring it to the user as a
  named decision (accept residual risk and document it vs. relax the NFR)
  before declaring P01-T02 done.
* Action owner: Planning parent for sequencing (move the Trivy check earlier);
  user decision only if a real unfixed finding surfaces with no available fix.
* Exact resolving evidence: a recorded Trivy run (pass, or a named/approved
  residual finding) referenced from P01-T02's phase-details before P02 begins.
* Decision route: direct planner correction (resequence) now; a significant
  user decision only if an actual unfixed, unpatchable finding is found.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: 25-new-test-method lock has no stated consolidation technique for P02-T01's breadth

* Related IDs: P02-T01, Critique Disposition ("Maximum 25 added test methods").
* Evidence: infra/modules/containerapps.bicep shows at least six image
  consumers (api, agents, orchestrator, import job, token-maintenance job,
  ledger-verify job) each needing image-wiring proof; infra/modules/edge.bicep
  shows three gated properties (Premium SKU, WAF policy, Private Link origin)
  each needing default-off and production-only proof; infra/governance.bicep
  needs a non-mutation proof for Defender. Existing infra/tests files average
  ~8-28 `def test_` methods each, with no `subTest`/table-driven pattern
  currently used for per-resource iteration in test_bicep_policy.py or
  test_governance.py (both use direct assertions, not parametrized loops).
* Concern: without an explicit instruction to parametrize (e.g., one method
  with `subTest` iterating the six consumers, rather than six separate
  `test_*` methods), a straightforward implementation could approach or
  exceed the 25-method budget before covering Defender, Policy, and edge
  gating, forcing either an uncomfortable late consolidation pass or a
  renegotiation of the lock.
* Impact: Medium — the work is very likely achievable within budget with
  deliberate parametrization, but the phase-details do not say so, leaving
  this to implementation-time judgment on a hard-locked number.
* Smallest useful change: add one sentence to phase-details P02 directing
  that consumer/property iteration use `subTest` within one or two test
  methods (consistent with the existing `test_every_deployed_resource_waits_for_the_guard`
  pattern in test_bicep_policy.py, which already iterates all resources in a
  single method), reserving the remaining budget for Defender/Policy and
  P01-related infra tests.
* Action owner: Planning parent (direct addition to phase-details).
* Exact resolving evidence: phase-details P02 entry naming the consolidation
  technique, or an explicit acceptance that the lock may be exceeded with
  user sign-off.
* Decision route: direct planner correction.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Low]: Harness file identity ("src/check-container.py") not confirmed as new vs. existing

* Related IDs: Critique Disposition ("src/check-container.py for Docker
  semantics"), P01-T01.
* Evidence: no file matching `check-container*`/`check_container*` exists
  anywhere under `src/` in the current repository.
* Concern: the plan's Critique Disposition states test ownership as if
  `src/check-container.py` already exists or is an agreed filename, but
  phase-details P01 only says "Docker harness" without naming or locating it.
  An implementer could reasonably place the harness elsewhere (e.g., under
  `infra/tests` or a project-level `tests/` directory), which would not
  violate any stated requirement but would make the Critique Disposition's
  ownership statement inaccurate after implementation.
* Impact: Low — cosmetic/traceability risk only; does not affect correctness
  of the harness itself.
* Smallest useful change: confirm in phase-details P01 that
  `src/check-container.py` is the intended new path for the one locked
  Docker runtime harness, or adjust the Critique Disposition wording to say
  "a new harness under src/" without asserting a specific existing path.
* Action owner: Planning parent.
* Exact resolving evidence: phase-details P01 naming the harness path
  explicitly.
* Decision route: direct planner correction.

## Strengths and Residual Risk

* The plan correctly identifies, and the repository confirms, two real latent
  risks: (1) `infra/governance.bicep` currently submits a `Microsoft.Security/pricings`
  resource unconditionally, which could downgrade an existing Standard plan to
  Free on any redeploy with `enableDefenderPlans=false`; (2) the two
  maintenance jobs' `command:` overrides bypass any new Dockerfile entrypoint.
  Both are accurately scoped for a fix.
* Front Door Premium/WAF/Private Link default-off, production-gated behavior
  is already implemented in infra/modules/edge.bicep; P02-T01's task to
  "prove" (not build) this coverage is appropriately scoped and does not risk
  inventing unsupported Bicep properties.
* The plan's explicit refusal to claim hosted kernel enforcement (no
  `securityContext`/`readOnlyRootFilesystem` in the Container Apps schema,
  confirmed by the research's Microsoft Learn check) is accurate and avoids
  an unearned acceptance claim.
* Residual risk accepted by this critique: the exact in-container technique
  for reading capability/NoNewPrivs state (e.g., `/proc/self/status` parsing)
  is left to implementation and not specified in phase-details; this is
  reasonable detail to leave at that level given the stdlib-only NFR is
  already stated and the technique is standard.

## Questions or Blocking Evidence Gaps

* Does Azure Container Apps (API 2025-07-01, used in containerapps.bicep)
  honor `args` without `command` to preserve a Dockerfile ENTRYPOINT for
  Container Apps Jobs, or does `command` need to remain set for the guard to
  execute? (PC-001; decision-critical for P02-T01's fix design, resolvable by
  documentation/schema check, not by live deployment.)
* Do any of the four pinned base images, once Trivy is run with
  `ignore-unfixed=false`, currently report a HIGH/CRITICAL finding with no
  vendor fix, and if so, what does the user want to do given the NFR bans any
  ignore list? (PC-002; decision-critical only if such a finding actually
  exists — recommend checking before the user is asked.)

## Limitations

* This critique did not execute Trivy, build the four images, or deploy any
  Bicep template; all repository-state evidence is from static reads and a
  compiled-template understanding of existing behavior, not a live run. The
  ACA `command`/`args` semantics conclusion rests on a 2026-10-16 web search
  and a partial Microsoft Learn ARM reference fetch rather than an exhaustive
  reading of the full schema or a live Container Apps Jobs test.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: Planning parent
* Smallest next action: confirm Azure Container Apps `command`/`args`-to-
  Dockerfile-ENTRYPOINT/CMD semantics for Container Apps Jobs at API
  2025-07-01 (documentation/schema check, no live deployment) and update
  P02-T01's phase-details with the confirmed design before implementation
  starts; resequence the Trivy unsuppressed-scan validation (PC-002) into
  P01-T02; add one consolidation sentence to phase-details P02 for the test
  budget (PC-003).
* User response required: no — all four findings are resolvable by the
  planning parent through direct research/documentation checks and
  phase-details edits; escalate to the user only if the ACA documentation
  check (PC-001) remains ambiguous or a genuine unfixed/unpatchable
  HIGH/CRITICAL finding is confirmed (PC-002).

## Related Artifacts

| Path | Description |
|---|---|
| .copilot-tracking/plans/2026-10-16/issue-118-plan.md | Plan under critique |
| .copilot-tracking/details/2026-10-16/issue-118-phase-details.md | Phase details under critique |
| .copilot-tracking/research/2026-10-16/issue-118-research.md | Supporting research reviewed |
| infra/modules/containerapps.bicep | Confirms job `command:` overrides and six image consumers |
| infra/modules/edge.bicep | Confirms existing Front Door Premium/WAF/Private Link gating |
| infra/governance.bicep | Confirms unconditional Defender pricing resource submission |
| infra/tests/test_governance.py | Confirms current Defender/Policy test assertions |
| infra/tests/test_bicep_policy.py | Confirms existing subTest-free, resource-iterating test pattern |
| .github/workflows/src-ci.yml | Confirms current `ignore-unfixed: true` suppression and existing runtime/scan steps |

## Next Steps

No user action is required now. The planning parent should resolve PC-001
through PC-004 directly (documentation checks and phase-details edits) before
implementation begins; escalate to the user only if PC-001's ACA semantics
check or PC-002's Trivy check surfaces a genuine, unresolvable ambiguity or
unpatchable finding.
