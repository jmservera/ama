---
title: Live IoT Hub final-candidate plan critique
ms.date: 2026-10-29
---

## Metadata

* Task ID: 140-184 / iot-hub-live-140
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/iot-hub-live-140-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/iot-hub-live-140-phase-details.md
* Critique execution status: Complete
* Assessment count: One independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller direction: full ordered RPI loop; quickest safe synthetic live
  sensor exercise; existing ama/uksouth B1 hub, one unit, USD5 additional
  through October 31; no new infrastructure, private endpoints or operator
  roles; existing API data role only where already approved and applicable.
* Operational constraints: no secrets, .env or private datasets; apps remain
  min0, eight jobs remain Manual, SQL remains private; local commit only,
  no push; no cloud commands or mutations during this critique.
* Primary evidence:
  .copilot-tracking/plans/2026-10-29/iot-hub-live-140-plan.md,
  .copilot-tracking/details/2026-10-29/iot-hub-live-140-phase-details.md,
  .copilot-tracking/research/2026-10-29/iot-hub-live-140-research.md.
* Bounded corroboration: infra/modules/iothub.bicep,
  infra/tests/test_iothub_module.py,
  src/api/src/zava_forward/api/iot_stream.py,
  src/core/tests/sensor_consumer_fixture.py,
  src/core/src/zava_forward/core/mssqlstore.py,
  src/README.md and the dated authorization in
  docs/adrs/0003-journey-derived-capabilities-runtime-fit.md.
* Context read: original case study, addendum, knowledge-base index,
  owner memory and housing-association primer. Memory is not authority.
* Decisions assessed: isolated hub-only entry point; unchanged production
  module and receiver authority; device-only X.509 publisher activation;
  existing-authority registry attempt with 401/403 parking; counts-only
  private SQL inspection; constructed disposable SQL fallback.
* Acceptance boundary: all five plan acceptance criteria, P01-P03 and every
  listed task, no test removals, at most twelve added test methods and the
  stated source/file ownership. This is a credibility assessment, not
  implementation acceptance, Azure authorization verification or a fresh
  observation of cloud state.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| RPI sequence and local commit/no push; AC5; P03-T02 | Partial | Original Review and commit/gate separation are retained; validation admission needs PC-001 and PC-003. |
| Existing hub only; C1/C5; AC1/AC2; P01-T01/T02 | Partial | Isolated graph is appropriate; resource-type checks alone do not prevent replacement or unintended hub-property changes, PC-002. |
| Private network and service auth; C2/C8/W1 | Partial | No SAS workaround or new receive infrastructure; exact live property preservation needs PC-002. |
| Metrics-only diagnostics; C6; P01-T02 | Covered | Reconciliation and verification precede synthetic device creation. |
| Device activation separation; C4/C10; AC3; P02-T01 | Covered | Positive/negative compatibility and receiver-refusal tests are explicit. |
| Existing-authority X.509 attempt; P02-T02 | Partial | Absence check, no overwrite, 401/403 stop and owned cleanup are explicit; whole-action limits need PC-004. |
| SQL private, apps min0, eight Manual jobs; C7; P02-T03 | Partial | Execution-only count query preserves workload definitions; execution duration/count admission needs PC-004. |
| Actual constructed SQL; C9; AC5; P02-T03 | Covered | Dedicated labelled container, random loopback port and synthetic fixtures are appropriate, subject to PC-001 and PC-003. |
| Live versus local evidence; AC4 | Covered | Local/mock success is not described as live transport, SQL delivery or resident gauge acceptance. |
| USD5 through October 31 | Partial | Existing-hub attribution is qualified, but ancillary work needs finite admission and stop limits, PC-004. |
| Locked tests, no removals, maximum twelve additions | Covered | No proposed correction requires a new framework, production-module rewrite or expanded test ownership. |
| Documentation/history; P03-T01 | Covered | Dated authorization, ADR history, knowledge-base index/log and outstanding parent criteria are preserved. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 3 High, 1 Medium.
* Rationale: The selected architecture respects the material authorization
  boundary and correctly acknowledges that live end-to-end consumption is
  currently blocked. Four actionable execution safeguards remain: usable
  storage paths, exact deployment admission, local validation before cloud
  mutation, and finite limits for ancillary cloud activity. These are direct
  planner corrections, not reasons to request broader Azure authority.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: The validation and scratch-path instructions are not executable within the current file-operation boundary

* Related IDs: AC5, P02-T02, P02-T03, P03-T02.
* Evidence: The plan requires /tmp/mv; P03-T02 repeats that path.
  P02-T02 specifies a temporary outside-repository credential directory.
  src/README.md also documents temporary paths and a temporary shared lock
  for the complete gate. Temporary-directory file operations are unavailable
  in this execution environment.
* Concern: The implementer cannot follow those literal instructions, and
  merely selecting a different gate output directory does not establish that
  the gate's internal file operations are permitted.
* Impact: Required checks or credential preparation can fail before useful
  work, or an implementer may silently substitute an unreviewed workflow.
* Smallest useful change: Replace the hard-coded environment path with an
  existing permitted persistent tooling location addressed relative to the
  working directory. Specify a permitted owner-only credential location
  satisfying the outside-repository requirement; if none exists, park the
  live credential attempt. Inspect gate path requirements before admission;
  if they cannot be satisfied without prohibited operations, record that gate
  as blocked rather than modifying gate tooling, bypassing its lock or
  weakening receipt requirements.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P02/P03 identify permitted locations,
  secret exclusion/cleanup and the gate-path preflight; the changes record
  subsequently captures actual permitted check commands or an explicit
  environment blocker. No actual certificate or key is resolving evidence.
* Decision route: Direct planner correction. Do not seek permission to
  bypass the execution boundary.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Deployment admission constrains types but not exact identities and allowed property deltas

* Related IDs: C5, AC1/AC2, P01-T01, P01-T02.
* Evidence: P01-T01 promises existing-hub reuse and preservation of name,
  tags and network state. P01-T02 stops deletions and resources outside the
  hub/children, but does not state an explicit stop on a newly created hub
  or changes to existing auth, routing or identity. The baseline includes
  those properties. infra/modules/iothub.bicep shows that auth, routing,
  managed identity and fallback delivery are distinct hub properties.
* Concern: A type-correct isolated template can still create a differently
  named B1 hub, reset omitted hub properties, or alter existing routing/auth
  on the allowed hub. Incremental deployment and a constant private-endpoint
  count do not themselves prove property preservation. This is a gap in
  admission evidence, not a claim that the unwritten entry point is defective.
* Impact: Applying an apparently allowed graph could violate one-hub scope,
  disrupt existing delivery or weaken service authentication.
* Smallest useful change: Pin the exact existing hub resource ID and approved
  child IDs before apply. Reject hub Create/Delete/replacement, SKU/unit drift,
  and every property delta except explicitly enumerated reconciliation
  changes and the separately bounded public-access toggle. Preserve and
  compare local-auth/device-auth flags, TLS, identity, routing/fallback,
  retention/partition settings and exact existing private-endpoint attachment,
  not only endpoint count. Stop on unresolved what-if differences rather
  than assuming omitted properties survive.
* Action owner: Planning parent, implemented by the P01 owner.
* Exact resolving evidence: Revised P01 specifies the ID/property allowlist;
  compiled semantic assertions fit within the twelve-test limit; sanitized
  what-if and post-apply property comparisons show only approved deltas on
  the pinned resources. No cloud execution is requested by this critique.
* Decision route: Direct planner correction; current user direction already
  requires reuse and unchanged service auth.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Relevant local validation is scheduled after cloud mutations

* Related IDs: AC1/AC3/AC5, P01-T02, P02-T01/T02/T03, P03-T02.
* Evidence: P01-T02 performs apply; P02-T02 then performs registry/send
  activity; the required Ruff, format, mypy and unittest checks are only
  placed in P03-T02, while disposable SQL proof is P02-T03.
  src/README.md, Stabilization validation ladder step 4, admits Azure-only
  work only after relevant local checks pass.
* Concern: Listing tests to add in earlier phases does not establish a
  passing-check dependency before deployment and credential use.
* Impact: A regression in activation refusal, synthetic-only validation,
  cleanup or the isolated deployment contract could be discovered only
  after exercising a live resource.
* Smallest useful change: Add an explicit local admission gate before the
  first cloud mutation: compile/semantic infra tests, publisher/receiver
  regressions and owning-project static/unit checks must pass. Run the
  relevant constructed SQL selector locally before admitting cloud-only
  SQL inspection. Local blockers park the affected Azure activity while
  independent local work continues. Keep the complete exact-head gate
  after the implementation/original Review commit; do not move or replace it.
* Action owner: Planning parent.
* Exact resolving evidence: Revised task dependencies explicitly gate
  P01-T02 and P02-T02/T03 cloud portions; dated implementation evidence lists
  passing prerequisite commands/exits before any mutation timestamp, or
  records Azure activity as not attempted.
* Decision route: Direct planner correction. The requested ASAP delivery
  does not require skipping prerequisite checks.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: The finite send budget does not bound the other billable cloud activity

* Related IDs: USD5/time-window requirement, P01-T02, P02-T02, P02-T03.
* Evidence: Two messages, one per second and at most sixty seconds explicitly
  bound publishing. P02-T02 permits ingress-metric comparison after
  unspecified lag; P02-T03 starts a Manual initializer execution without an
  execution-count limit, wall-clock limit or overrun handling. The cost
  section reserves the remaining allowance for metrics and the job without
  quantifying those bounds.
* Concern: A Manual trigger is not a runtime limit. Client-side timeout alone
  also does not prove a started cloud job has stopped. Registry/control-plane
  retries, metric polling and job execution need their own finite bounds.
* Impact: Troubleshooting can consume the reserved allowance or leave a job
  running past the approved exercise window despite the bounded publisher.
* Smallest useful change: Set explicit maximum attempts and elapsed times
  for registry operations, apply verification and metric polling; define
  one admitted counts-only job execution with a finite query/job duration,
  no automatic rerun and an exact owned-execution stop/verification procedure.
  Check existing retry/timeout behavior without changing the job template.
  If a safe bound cannot be enforced under current authority, omit that
  cloud attempt and record the blocker. Tie these limits to a conservative
  incremental cost reservation and an explicit October 31 cutoff.
* Action owner: Planning parent, implemented by the live-exercise owner.
* Exact resolving evidence: Revised P01/P02 contain numerical limits and
  cost admission/stop conditions; execution evidence records attempt count,
  elapsed time and terminal status of the owned job, or its non-admission.
* Decision route: Direct planner correction. A new role, persistent job
  update or larger budget is not the prescribed resolution.

## Strengths and Residual Risk

* Reusing the existing B1 hub and isolating its reconciliation avoids the
  demonstrably unapproved production Event Hub/private-endpoint graph.
* Publisher-only activation is an appropriate local correction. The receiver
  must still reject it before constructing credentials or network clients;
  Python annotations alone do not enforce that boundary.
* Diagnostics reconciliation before device creation, absence checks,
  no identity overwrite, owned cleanup and explicit restore-failure reporting
  are sound safeguards.
* The supplied evidence already resolves the keyless built-in receive-path
  question. Do not repeat research, assign an ineffective receiver role,
  enable service SAS or request new infrastructure as a critique correction.
* Registry authorization and current cloud state remain uncertain. A network
  or 401/403 failure is a parked attempt, not proof that local code or the
  complete parent criteria are satisfied.
* Independent local SQL and cloud table counts cannot establish causal
  live-to-SQL delivery or resident projection freshness. AC4 correctly
  preserves those unmet outcomes.
* Preserve the original post-implementation Review, including adverse
  findings. Routing work to a later task must not relabel an unaccepted
  candidate as accepted or imply publication permission.

## Questions or Blocking Evidence Gaps

* No significant or divergent user decision is needed for PC-001 through
  PC-004. Resolve them within the existing boundary or park the affected
  action.
* A future desire to unblock actual cloud consumption, missing registry
  authority or resident-app activation would need separate authorization.
  That is an explicitly out-of-scope follow-up, not a condition for honest
  bounded delivery here.

## Limitations

* No cloud commands, external retrieval, secrets, private data, builds or
  tests were executed. Research inventory is supplied evidence, not freshly
  independently verified cloud state.
* The new entry point/profile and activation implementation do not yet
  exist. Findings address missing planning controls, not invented source
  defects.
* Issue acceptance is assessed only as represented by the supplied materials;
  this critique does not close #140, #184, OD-43 or resident-gauge criteria.
* Existing dirty/untracked planning inputs were read, not moved, staged or
  committed. Only this critique artifact was written.

## Recommended Next Action

* Highest-impact finding: PC-002.
* Action owner: Planning parent.
* Smallest next action: Add exact-resource/property deployment admission,
  then resolve the other three direct corrections in the same revision.
* User response required: No.
* Stop: This completes the one requested final-candidate critique. Return
  to the active parent without another critique pass.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/iot-hub-live-140-plan.md](.copilot-tracking/plans/2026-10-29/iot-hub-live-140-plan.md) | Assessed plan; unchanged. |
| [.copilot-tracking/details/2026-10-29/iot-hub-live-140-phase-details.md](.copilot-tracking/details/2026-10-29/iot-hub-live-140-phase-details.md) | Assessed phase details; unchanged. |
| [.copilot-tracking/research/2026-10-29/iot-hub-live-140-research.md](.copilot-tracking/research/2026-10-29/iot-hub-live-140-research.md) | Supplied evidence; unchanged. |
| [.copilot-tracking/reviews/2026-10-29/iot-hub-live-140-plan-critique.md](.copilot-tracking/reviews/2026-10-29/iot-hub-live-140-plan-critique.md) | Complete one-pass critique; Revise. |

## Next Steps

The active planning parent should resolve PC-001 through PC-004 directly,
preserve this original critique and finalize the plan without another critique.
No user action is required. No cloud action or publication is authorized by
this assessment.
