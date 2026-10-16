# RPI Plan Critique: Demo direct ingress

## Metadata

* Task ID: issue-360.
* Critique date: 2026-10-16.
* Plan: .copilot-tracking/plans/2026-10-16/demo-direct-ingress-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/demo-direct-ingress-phase-details.md
* Critique execution status: Complete.
* Assessment count: exactly one final-candidate critique.

## Inputs and Criterion Boundary

* Caller direction: offline explicit demo external ACA environment and own subnet, private backing services, direct Entra without Front Door discovery, probes and migration documentation. No Azure operations, deployment, deletion, MVP/prototype working-tree access or private datasets.
* Candidate evidence: the plan, phase details and .copilot-tracking/research/2026-10-16/demo-direct-ingress-research.md, including C1-C7. Issue #360 was read through GitHub for its scope and criteria a-f; no issue mutation occurred.
* Necessary existing context: infra/main.bicep; infra/modules/network.bicep; infra/modules/containerapps.bicep; discovery, registration and auth reconciliation in infra/scripts/setup-entra.py; smoke behavior in infra/scripts/private-cutover-proof.py; image-selection references in infra/scripts/deploy.py; relevant setup/proof test references; docs/architecture/cutover-evidence-pack.md public-browser section; docs/adrs/0006-src-layout-and-cutover.md. Required repository case-study, index and memory context was also consulted.
* Decisions and dependencies: a/b/f are offline deliverables; c is a proposed runbook awaiting owner approval; d/e remain Not run. Default/production and optional Front Door behavior must remain unchanged. The supplied research records the main integration prerequisite and separate PR #359 work; those are not live tenant or deployment evidence.
* Boundary: assess implementation-plan credibility, not implementation correctness or Azure capability/currentness. Existing source reads support the findings below; historical and live claims in the research were not independently re-executed. No external Azure research was performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| #360 a; C1-C3; P01-T01 | Covered | Separate exposure switch, workload-only naming, dedicated delegated subnet/NSG, retained subnets, private backing inputs and compiled guards are explicit. |
| #360 b; C4; P01-T02 | Partial | Branch-before-edge, ambiguity, external ingress checks and isolated extension diagnostics are explicit; inherited auth-state handling needs PC-003. |
| #360 c; P01-T03 | Partial | No-move rule, parity, rollback, cost/approval and gated retirement are explicit; concurrent consumers need PC-001. |
| #360 d; C5; P01-T02 | Partial | Live acceptance is correctly excluded; the offline probe contract needs PC-002. |
| #360 e; P01-T03 | Covered | Retirement remains separately owner-authorized after verification; no Azure action is part of this task. |
| #360 f; C5-C6; P01-T03 | Covered | Runbook, infra guide, ADR/evidence reconciliation, historical separation, KB index and append-only log are intended. |
| C7; P02-T01 | Covered | Preserve separate device-code work; offline tests, tooling failures, one review and privacy-safe non-forced PR delivery are specified. |
| Caller prohibitions; plan scope and validation | Covered | No deployment, private data, legacy working-tree edits or live acceptance is authorized. Proposed fixture/compiler work belongs to implementation, not this critique. |

## Verdict

* Verdict: Revise.
* Severity counts: 0 Critical, 1 High, 2 Medium, 0 Low.
* Rationale: the selected architecture is credible for offline implementation, but the runbook and auth/probe details leave concrete failure paths in existing code insufficiently specified. All findings are direct planner corrections within the confirmed scope.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Gate queue-scaled workers as well as scheduled jobs during coexistence

* Related IDs: #360 c; P01-T01; P01-T03; research C2-C3.
* Evidence: .copilot-tracking/details/2026-10-16/demo-direct-ingress-phase-details.md:29-33 promises staged activation and a "single active scheduled consumer." infra/modules/containerapps.bicep defines agents with an azure-queue scale rule on agent-tasks, minReplicas 0 and maxReplicas 5, independently of the scheduled orchestrator. It also defines scheduled token-renewal and ledger-publishing jobs. Both workload generations would share backing queues and identities.
* Concern: limiting scheduled consumers does not prevent both old and new agents from scaling on the same queue. Nor does it specify safe handling of already-running jobs or in-flight messages at cutover and rollback.
* Impact: replacement staging can divert or concurrently process work against different API generations; an apparently dormant zero-minimum worker is not disabled. Duplicate maintenance/publication schedules can also remain active.
* Smallest useful change: expand staged activation into an explicit producer/queue-worker/maintenance-job inventory, with a documented inactive staging mechanism, stop/drain boundary, one authoritative active generation and reverse-order rollback. Do not require implementing a new runtime switch if existing deployment controls can demonstrate that boundary.
* Action owner: planning parent for P01-T03, coordinated with the infrastructure implementer for P01-T01.
* Exact resolving evidence: revised phase details require a runbook table covering agents, orchestrator, auth-renewal, ledger-verify and any import trigger; the table names how each new trigger is kept inactive, how old work is drained or dispositioned, activation order and rollback order. If template activation controls are introduced, add compiled regressions proving staged demo resources cannot consume or schedule work. These are offline checks, not a live-drain claim.
* Decision route: direct planner correction. Owner approval of the later migration remains required; no new user decision is needed now.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Define a direct-mode probe contract without weakening private proof

* Related IDs: #360 d; P01-T02; P02-T01; research C5.
* Evidence: .copilot-tracking/details/2026-10-16/demo-direct-ingress-phase-details.md:22-25 says to extend private smoke or a shared helper, disable redirect following, require API 401 and check a browser redirect to the exact Microsoft login host. infra/scripts/private-cutover-proof.py:190-235 currently follows redirects, requires private DNS before smoke and checks malformed bearer and forged-principal denials as well as anonymous denial. .copilot-tracking/plans/2026-10-16/demo-direct-ingress-plan.md:97 explicitly retains the browser JSON API 302 gap.
* Concern: the details do not define how public direct probes bypass only the private-origin DNS requirement while retaining existing private smoke behavior. They also do not distinguish native API denial from the known browser User-Agent behavior, or specify the login initiation endpoint and permitted same-origin authentication hops. "No redirect following" and a final Microsoft host assertion alone leave these outcomes ambiguous.
* Impact: implementation can make external smoke fail on valid public DNS, accidentally relax private proof, lose the existing forged-header/malformed-token checks, or report a browser API 302 as a 401 success. An ordinary local EasyAuth login hop can also be misclassified without a bounded contract.
* Smallest useful change: specify an explicit direct probe entry/mode with unchanged private-mode defaults; enumerate paths, User-Agent profiles, exact statuses and redirect locations. Inspect redirects without automatic following. If local hops are necessary, inspect them individually with a bounded same-origin allowlist before validating the exact HTTPS Microsoft host. Retain malformed-bearer and forged-principal negative checks.
* Action owner: planning parent and auth/probe implementer for P01-T02.
* Exact resolving evidence: revised phase details define the mode/DNS boundary and per-probe expectations; fake HTTP/DNS tests exercise public direct success, private-DNS failure preservation, unexpected 200/302 denial failures, malformed credentials, forged principals, hostile or malformed Location values and safe login hops. A browser JSON API 302 is recorded as the existing gap, not acceptance. Missing real role credentials are Not run, and simulated sessions remain labelled offline evidence.
* Decision route: direct planner correction. Resolving the pre-existing browser API gap or claiming real sign-in is not added to this issue's offline scope.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Specify direct setup handling for inherited proxy and bearer-only auth

* Related IDs: #360 b; P01-T01; P01-T02; research C4.
* Evidence: .copilot-tracking/details/2026-10-16/demo-direct-ingress-phase-details.md:11-12 specifies NoProxy and unsafe-auth guards for infrastructure; lines 17-21 direct setup to reuse enforcement helpers. infra/scripts/setup-entra.py:689-719 preserves an existing Custom/Standard forwardProxy for a single direct origin and preserves an existing Return401 unauthenticatedClientAction when bearer is false. infra/tests/test_setup_entra.py:610 explicitly tests preservation of bearer mode without implicit browser activation.
* Concern: successful direct discovery and reuse of the existing auth helper do not establish direct browser-mode configuration on an already configured app. The setup path can preserve stale edge forwarding or service-smoke auth, while a blanket helper change would break existing Front Door/bearer preservation guarantees.
* Impact: setup can finish with the wrong callback-host behavior or no interactive sign-in even though the infrastructure mode is correct; alternatively, fixing it globally can regress the optional edge path.
* Smallest useful change: explicitly require mode-aware direct auth reconciliation and tests. Direct mode must select NoProxy and either validate existing browser credential/action readiness or stop with an actionable prerequisite. Do not silently convert a deliberately bearer-only deployment or manufacture credentials to conceal missing tenant authority. Preserve the current edge/default behavior.
* Action owner: planning parent and auth implementer for P01-T02.
* Exact resolving evidence: revised phase details name inherited Custom/Standard and Return401/bearer states; fake CLI/auth tests prove direct NoProxy handling, fail-closed browser prerequisites, exact app-FQDN callback addition with existing callbacks retained, and repeat-run idempotence. Existing Front Door custom-forwarding and bearer-preservation tests still pass; direct tests record no afd/cdn command or extension access.
* Decision route: direct planner correction within the already confirmed direct-browser requirement. No new user decision or tenant operation is required for planning or offline tests.

## Strengths and Residual Risk

* The plan correctly rejects broad allowPublicNetworkAccess, an in-place internal/external mutation and renaming the entire backing-resource prefix.
* It preserves the optional production edge and makes live tenant authority, owner cost/migration approval, SQL/AI proof and retirement separate gates.
* No standing Consumption environment charge is correctly distinguished in the proposed documentation from running replicas, logs, networking and retained edge overlap; no cost commitment is approved by this critique.
* Existing private dependencies, identities, private DNS and data remain protected by scope. No private dataset or legacy working-tree content was inspected.
* Real browser login, wrong-role denial, SQL persistence, model calls and deletion acceptance remain unproved. Offline tests cannot clear those gates.

## Questions or Blocking Evidence Gaps

* No user decision blocks the offline plan corrections.
* Live platform and tenant evidence is deliberately unavailable and remains a later acceptance gate, not a reason to run Azure commands during this task.

## Limitations

* This is a plan critique, not an implementation/security audit or a fresh Azure design certification. No tests, compiler, Azure CLI, deployment, identity mutation or deletion were executed.
* Research C6 history and C7 integration/lifecycle statements were treated as supplied evidence, not independently repeated.
* Existing untracked planning inputs were left untouched. Only this requested critique artifact was written.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: revise P01-T03 to gate all shared-queue consumers and maintenance triggers, then incorporate PC-002 and PC-003 into P01-T02 and its offline tests.
* User response required: no. Later owner approval remains mandatory before live migration, spend or retirement.
* Return this complete finding set to the active planning parent for direct revision and finalization without another critique.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-16/demo-direct-ingress-plan.md](.copilot-tracking/plans/2026-10-16/demo-direct-ingress-plan.md) | Final-candidate plan assessed without edits |
| [.copilot-tracking/details/2026-10-16/demo-direct-ingress-phase-details.md](.copilot-tracking/details/2026-10-16/demo-direct-ingress-phase-details.md) | Phase details assessed without edits |
| [.copilot-tracking/research/2026-10-16/demo-direct-ingress-research.md](.copilot-tracking/research/2026-10-16/demo-direct-ingress-research.md) | Supplied research pointer and C1-C7 evidence |
| [.copilot-tracking/reviews/plans/2026-10-16/demo-direct-ingress-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-16/demo-direct-ingress-plan-critique.md) | Complete single-pass finding set |

## Next Steps

The active planning parent should make the three direct corrections, record their disposition and finalize without another critique. No user action is required for those revisions. Do not implement or run Azure operations as part of this critique handoff.
