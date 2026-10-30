---
title: "RPI Plan Critique: live-acceptance-1030c"
description: Independent final-candidate assessment of the bounded live acceptance plan
ms.date: 2026-10-30
---

## Metadata

* Task ID: live-acceptance-1030c-2026-10-30.
* Critique date: 2026-10-30.
* Plan: .copilot-tracking/plans/2026-10-30/live-acceptance-1030c-plan.md.
* Phase details: .copilot-tracking/details/2026-10-30/live-acceptance-1030c-phase-details.md.
* Critique execution status: Complete.
* Assessment: the one independent final-candidate plan critique requested by the caller. No additional agents or critique passes.

## Inputs and Criterion Boundary

* Caller requirements: fresh resident and employee acceptance; Refs #550/#551/#552/#563 only; at most two sign-in attempts per site; at least 120-second warming timeouts with retries; slow callback allowance; no credential output or captures; no Azure mutation; local commit only; disabled-AI fallback expected without an AI label; no AT claim.
* Primary evidence: the plan and phase details above and .copilot-tracking/research/2026-10-30/live-acceptance-1030c-research.md.
* Bounded evidence checks: the four supplied issue bodies retrieved read-only with gh issue view; research pointer C7's source binding projection; the /api/me handler; shared chat widget and resident consent implementation; supplied map/case browser-check pointers and src/README.md local-gate instructions. Historical changes records were consulted for the already documented adverse-evidence boundary.
* Project context: docs/case_study_48_original.md, docs/case_study_48_addendum.md, docs/reference/README.md and docs/reference/memory.md.
* Decisions and dependencies: tracking-only implementation, no product repair, no enabled-model run, no baseline improvement claim without a trusted deployed-before baseline, one independent Review, local commit followed by a complete local-gate attempt. Browser/runtime availability, successful authentication and actual deployed behavior are implementation dependencies, not established results.
* Assessment boundary: planning credibility, concrete safety, test/output ownership and strength of the proposed evidence for all 24 issue entries. This critique does not execute the runner, authenticate, inspect credentials, visit live sites, approve accessibility conformance or establish live acceptance.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Caller runtime and file-operation constraints; P01-T01 | Partial | Explicit /tmp runtime instruction conflicts with the current prohibition; PC-001. |
| Credential/capture exclusion; P01-T01/P01-T02 | Partial | Strong output intent but missing process-level diagnostic and failure-path controls; PC-002. |
| Attempt cap, warming and callback; P01-T01/P01-T02 | Covered with test gap | Durable launch count, three 120-second warmup tries, one submission per attempt, no retry after uncertain delivery and 180-second settling are explicit; PC-004 covers executable verification. |
| Employee authoritative admission; research C7; P01-T02 | Covered | Strict schema, expected identity, trusted-proxy provider, programme-manager role and literal false view-only field. Redirect success alone is rejected. |
| Resident actual login and consent ordering; P01-T02 | Covered with evidence limit | Real form login and no assistant POST before consent are planned. This is not server/model non-use proof. |
| 550-01..09; P01-T02/P02-T01 | Partial | Real shared-widget evidence and chat interactions are planned, but compound predicate ownership is incomplete; PC-003. |
| 551-01..04; P01-T02/P02-T01 | Partial | Marker/API agreement and narrow widths are planned; keyboard/non-colour predicates and test ownership need explicit mapping; PC-003/PC-004. |
| 552-01..06; P01-T02/P02-T01 | Partial | Icons, disclosure and geometry are planned; baseline/presentation provenance and compound evidence boundaries need mapping; PC-003. |
| 563-01..05; P01-T02/P02-T01 | Covered with explicit limits | Disabled-AI fallback can be observed; enabled AI and its label cannot be proven. Client consent blocking does not prove every server/model path. |
| Output budget and offline semantic tests | Partial | Named categories exist, but exact generated/test paths, commands and crash-path coverage are not yet fixed; PC-004. |
| P02-T02 local commit, original Review and gate | Covered with runtime dependency | No push, issue mutation, Azure change or second Review is planned. Gate feasibility must respect current file-operation constraints; PC-001. |

## Verdict

* Verdict: Revise.
* Severity counts: 0 Critical, 2 High, 2 Medium, 0 Low.
* Rationale: the acceptance boundaries are appropriately conservative, but the explicit forbidden runtime path and incompletely specified capture-free execution envelope need correction before implementation. Atomic checklist and safety-test ownership should be fixed in the same direct planner revision. No supplied evidence gap blocks this planning assessment itself.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: The planned runtime violates the current file-operation boundary

* Related IDs: P01-T01, P02-T02; research Deeper cycle.
* Evidence: .copilot-tracking/details/2026-10-30/live-acceptance-1030c-phase-details.md directs use of the existing /tmp/mv runtime. Current caller-environment instructions prohibit /tmp and temporary-directory file operations. src/README.md also documents external gate working directories and a shared /tmp lock, so the complete gate cannot simply be presumed compatible.
* Concern: the plan carries forward a historical runtime location that is not authorized in this execution environment. Relocating only the final JSON does not resolve runtime/cache/lock operations.
* Impact: implementing the plan literally violates a hard execution constraint; an attempted gate could do the same.
* Smallest useful change: select an available permitted runtime and explicitly configure permitted working/cache/output paths. Inspect the gate's path requirements before executing it; if its mandatory operations cannot comply, record that gate as blocked without bypassing it or changing product/tooling scope. Do not copy, read or execute the forbidden runtime as a workaround.
* Action owner: planning parent, then parent implementation.
* Exact resolving evidence: revised P01-T01/P02-T02 naming permitted runtime and output strategy; a safe dependency/import probe with no credential access; documented gate path feasibility or an explicit blocked-gate disposition. No claim of a passing complete gate without its actual receipt.
* Decision route: direct planner correction. The current constraint already resolves the policy choice; no user decision is needed to remove the conflicting instruction.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Capture exclusion is not yet a complete execution and failure-path contract

* Related IDs: functional credential requirements, non-functional output exclusions, P01-T01/P01-T02.
* Evidence: .copilot-tracking/plans/2026-10-30/live-acceptance-1030c-plan.md prohibits raw exceptions, URLs, identities and private payloads. Phase details say to mask fields and disable captures, but do not define the process diagnostic environment, browser launch logging, unexpected-exception handling or trust checks before credential filling.
* Concern: field masking and aggregate JSON alone do not prevent Playwright/API debug logs, inherited diagnostic settings, uncaught tracebacks or provider redirects from exposing sensitive inputs or sending them to an unintended origin. These are execution hazards, not allegations that a leak has occurred.
* Impact: one failure during sign-in can violate the no-output/no-capture requirement despite a clean final JSON.
* Smallest useful change: specify a diagnostic-disabled process/browser configuration; no tracing, HAR, video, screenshot, console or network-payload capture; fixed safe error codes for every failure path; and an exact authorized application/provider origin check immediately before each credential fill/submission. Stop on unknown origins without printing their URLs. Retain actual authorized redirects and the single-submission cap.
* Action owner: planning parent defines the envelope; parent implementation owns enforcement.
* Exact resolving evidence: revised safety steps plus offline tests using synthetic canary secrets and credential-bearing fake URLs/errors, covering JSON and stdout/stderr, unexpected failure cleanup, diagnostic-setting rejection/removal and denial before credential fill on an unauthorized origin. Tests must not use real credentials.
* Decision route: direct planner correction; no new permissions or user decision required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: The 24-row output does not yet have a complete atomic observation map

* Related IDs: P01-T02/P02-T01; 550-04/05/09, 551-03, 552-01/05, 563-03/05.
* Evidence: the plan promises rendered controls and all 24 decisions, but phase details only say "actual widget/skill" for employee chat and do not assign explicit live predicates for changing the active skill, disabled-tool reasons, delayed loading/error behavior, reduced motion or map non-colour keyboard state. The supplied shared widget source contains a 200 ms timer and explicit error/status semantics; issue 552 also requires presentation-icon provenance and preservation of the Fluent/WCAG baselines.
* Concern: generic inspection language leaves the implementer to discover required subchecks after execution. Merely producing 24 rows can conceal untested subparts, particularly 550-09 and 552-05. A consent-blocked client request cannot establish all of 563-03.
* Impact: limited sign-in opportunities can be spent before essential observations are scheduled, or a broad row can accidentally overstate what boolean evidence proves.
* Smallest useful change: before the live run, assign each checklist row its atomic predicates, site/action, safe evidence fields and blocked/not-observed disposition. Explicitly schedule the missing safe interactions. For unavailable natural slow/error responses, record that subpart Unproven rather than fabricating a response. Keep source-only provenance distinct from deployed evidence and scoped browser semantics distinct from AT or whole-baseline acceptance.
* Action owner: planning parent defines the map; parent implementation records each result.
* Exact resolving evidence: revised details or a planned evidence schema mapping all 24 IDs to their subpredicates, including explicit disabled-AI, server/model, no-baseline and no-AT limits. Every compound row must have a rule that prevents whole-row Proven when a required subpart is unobserved.
* Decision route: direct planner correction; no expanded live authorization, AI activation or user decision required.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Safety tests and generated-output ownership need exact executable boundaries

* Related IDs: Test Ownership and Output Budget, P01-T01, P02-T01/P02-T02.
* Evidence: .copilot-tracking/plans/2026-10-30/live-acceptance-1030c-plan.md names one runner, offline module, manifest and aggregate JSON without exact locations or test invocation. .copilot-tracking/details/2026-10-30/live-acceptance-1030c-phase-details.md requires exclusive invocation and durable submission intent but does not state the restart/crash tests. Tracking-local tests are not shown to be discovered by the repository gate.
* Concern: "validate syntax/tests" does not establish that the new safety module will run. Basic count-admission tests alone do not prove that a crash between admission and password submission, concurrent invocation or uncertain delivery cannot permit an extra sign-in. It is also unclear which exact files are generated versus safe to stage.
* Impact: the central two-attempt guarantee can remain unverified, and a passing general gate can be mistaken for coverage of this runner. Broad task-directory staging could include unintended diagnostic output.
* Smallest useful change: specify exact runner/test/manifest/evidence paths, a narrow offline test command and explicit stage allowlist. Add offline state-transition tests for durable admission before browser work, repeated/concurrent invocation denial, submission intent before password action, uncertain-delivery stop, exhausted caps across restart and context cleanup. Use injectable fake browser/persistence adapters, never live credentials or fixture substitutions for live acceptance.
* Action owner: planning parent fixes ownership/commands; parent implementation supplies tests and command results.
* Exact resolving evidence: revised executable validation commands; passing offline results covering those transitions; explicit output-schema/hash validation and a final staged-file list limited to the approved artifacts. The full local gate remains a separate requirement, not proof that undiscovered tracking tests ran.
* Decision route: direct planner correction; no user decision required.

## Strengths and Residual Risk

* Authentication is authoritative rather than inferred from a callback or app-origin redirect.
* Warming and callback budgets are concrete. Unknown password delivery stops the site instead of spending another submission.
* No backend response fabrication, application repair, Azure mutation, issue update or remote publication is authorized.
* Historical adverse evidence is preserved. Disabled-AI fallback, absent baseline and unperformed AT acceptance remain explicit limits rather than manufactured passes.
* Matching public widget hashes plus both rendered uses support component reuse only, not whole-site acceptance or source/deployment parity.
* A live site or external gate may remain unavailable. A truthful Partial/Unproven row or blocked gate is an acceptable evidence outcome, not permission to repair or bypass.

## Questions or Blocking Evidence Gaps

* No user question is required for these revisions. Live authentication, runtime availability and gate feasibility are implementation evidence dependencies; none should be invented or resolved by expanding authorization.

## Limitations

* No credential file or live site was accessed. No browser, login attempt or application request was executed.
* No product changes, tests or complete local gate were run for this read-only critique.
* Only the critique artifact was written. Plan, phase details, research, historical records and session state were not modified.
* This is the complete actionable finding set for the supplied boundary. The planning parent should dispose of it directly without another critique pass.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: replace the forbidden runtime instruction and document gate feasibility, then resolve PC-002 through PC-004 in one plan/details revision before implementation.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-30/live-acceptance-1030c-plan.md](.copilot-tracking/plans/2026-10-30/live-acceptance-1030c-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-30/live-acceptance-1030c-phase-details.md](.copilot-tracking/details/2026-10-30/live-acceptance-1030c-phase-details.md) | Assessed execution details |
| [.copilot-tracking/research/2026-10-30/live-acceptance-1030c-research.md](.copilot-tracking/research/2026-10-30/live-acceptance-1030c-research.md) | Supplied research boundary |
| [.copilot-tracking/plans/2026-10-30/live-acceptance-1030c-critique.md](.copilot-tracking/plans/2026-10-30/live-acceptance-1030c-critique.md) | This independent critique |

## Next Steps

Active planning parent: directly resolve and record dispositions for PC-001 through PC-004, finalize the plan without another critique, and continue only after the safety conditions are satisfied. No user action is required.
