---
title: Public browser access final-candidate critique
description: Bounded independent assessment of the issue 344 implementation plan
ms.date: 2026-10-16
---

## Metadata

* Task ID: 344
* Critique date: 2026-10-16
* Plan: .copilot-tracking/plans/2026-10-16/public-browser-access-344-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/public-browser-access-344-phase-details.md
* Critique execution status: Complete
* Execution boundary: Exactly one final-candidate critique; no implementation, external research, agent dispatch, deployment or tenant queries.

## Inputs and Criterion Boundary

* Primary inputs: The plan and phase details above, and .copilot-tracking/research/2026-10-16/public-browser-access-344-research.md, read in full.
* Caller requirements: Public access through Front Door Premium/WAF/Private Link or an external environment is authorized. SQL publicNetworkAccess must stay Disabled. Changes are ama-only, with no deletion, resource-group deletion, policy bypass or prohibited legacy/private-file reads. The chosen additive edge must preserve main's production guard and support the edge callback host.
* Authentication facts supplied: The existing client value is not a usable application registration; matching isolated tenant discovery found no retained workbench registration or credentials. Real sign-in remains Blocked. Browser default must be RedirectToLoginPage, anonymous protected API requests must receive 401 without redirect-suppression headers, and welcome/health remain public.
* Decisions and dependencies: Accept the additive edge rather than environment migration. Do not reopen that owner-authorized choice. Registration, credentials, callback registration and staff binding remain prerequisites for real-user acceptance, not evidence already obtained.
* Locked change contract: No removals; at most one new Bicep entry point and two focused test files if existing tests cannot hold coverage. Preserve workflow/check names, source-image boundaries, historical evidence and owner-controlled acceptance.
* Background considered: Repository instructions, the original case study, the opening exercise-context sections of its addendum, the reference index and owner memory. These do not establish current Azure or application behavior.
* Assessment boundary: Credibility of requirements, research conclusions, phases, tests, deployment dependencies and acceptance claims in the supplied candidate. Source-code implementation and official links named in the research were not independently inspected or revalidated. Findings below identify missing planned controls or resolving evidence, not confirmed deployed vulnerabilities.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Owner networking choice; research C1/C2/W1-W3; P01-T01 | Covered with qualification | Additive edge avoids global publicAccess and environment replacement. Advertised Private Link support is not deployed end-to-end proof. |
| Shared-environment isolation; research Q1/C5; P01-T01/P02-T01 | Partial | Correct origin host is required, but hostile-host routing and non-target app exclusion are not explicit acceptance gates; PC-001. |
| Browser redirect/API 401; research C3/C4; P01-T02/P02-T02 | Partial | Required response semantics are clear; conditional API exemptions do not establish trusted-principal provenance; PC-002. |
| Edge callback; P01-T02 | Covered | Explicit HTTPS URL, hostname validation and Standard proxy configuration are planned; tenant callbacks and real login remain Blocked. |
| SQL/private origin; P01/P02 | Covered | Disabled public networking and metadata-only validation are explicit; require observed evidence rather than local mocks. |
| ama-only/additive deployment; P02-T01 | Covered | Exact edge resources, scoped connection approval and no full-main deployment are specified. |
| Failed cut-over recovery; P02-T01/P02-T02 | Missing | No reversible non-deleting recovery sequence for route/auth changes; PC-003. |
| Historical feature coverage; research Q3; P02-T03 | Partial | Inventory intent and honest blocked rendering are sound, but static presence needs a permitted evidence source distinct from protected redirects; PC-004. |
| Locked tests/change budget; P01-T03; Locked Test and Change Ownership | Covered with findings | Existing suites and bounded additions are retained; PC-001/PC-002 must fit those owners, not expand the budget implicitly. |
| Evidence redaction/acceptance; P02/P03 | Covered | Sanitized evidence, no criterion auto-ticks and no redirect-to-login-success inference are explicit. |
| Review/publication; P03 | Covered | One postimplementation Review, privacy-safe identity configuration, topic PR and no merge are planned. No publication is performed by this critique. |

## Verdict

* Verdict: Revise
* Severity counts: 0 Critical, 2 High, 2 Medium, 0 Low.
* Rationale: The architecture choice and acceptance blockers are credible, but the candidate must make shared-environment routing isolation and the API trust boundary executable gates before exposure. Recovery and inventory provenance also need bounded clarification. These are direct planner corrections; no new owner decision is needed.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Fixed origin routing needs a shared-environment isolation gate

* Related IDs: Research Q1/C5/W2; P01-T01; P01-T03; P02-T01/P02-T02; Functional Requirements.
* Evidence: The research establishes managedEnvironments Private Link support. The plan requires correct origin host/TLS and an explicit /* route. Phase details identify one API origin but do not specify an allowlist of public domains, prohibition of alternate origin selection or hostile-host validation.
* Concern: The private connection targets a shared environment, not an app-specific isolation boundary. A fixed originHostHeader is an important control, not evidence that another public route/domain, routing rule or client-controlled forwarded header cannot select another app or influence callback routing.
* Impact: Public reachability could extend beyond the authorized API, or authentication could construct a callback using an untrusted host. Neither outcome is established as an existing flaw; the plan currently lacks the test that rules it out.
* Smallest useful change: Pin the sole intended API origin, originHostHeader/TLS name, supported edge hostname and route/domain association. Explicitly exclude wildcard/alternate origins and host-rewriting rules. Add compiled-contract tests and a deployment gate for conflicting Host, X-Forwarded-Host and Forwarded inputs. Confirm no other ingress-enabled app is publicly selectable through this edge without reading its application data.
* Action owner: Planning parent, with the infrastructure implementer executing the gate.
* Exact resolving evidence: Revised P01/P02 tasks naming these invariants; compiled edge assertions; sanitized live results demonstrating canonical requests still reach API welcome/health, hostile headers cannot reach another app or generate an attacker-host redirect, and non-allowlisted public host routing is rejected. Record only safe host classifications and statuses.
* Decision route: Direct planner correction within the selected edge architecture. If isolation cannot be established, stop exposure and report the blocker. The already-authorized external-environment alternative is a fallback, not permission to weaken isolation or bypass policy.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: API exemptions require proof of principal-header provenance, not only denial tests

* Related IDs: Research C3/C4; P01-T02; P02-T02; Locked Test and Change Ownership.
* Evidence: P01-T02 proposes narrow platform exemptions if browser mode does not preserve anonymous API 401, backed by server denial and spoof tests. P02-T02 names forged principals and malformed bearers but does not establish how trusted identity survives an exempt path.
* Concern: An exemption can change whether platform authentication validates or supplies a principal. Server denial alone does not prove that a client cannot inject the platform's trusted identity headers; stripping every principal instead could satisfy denial tests while breaking all authenticated API use. Standard forwarded-host handling does not itself establish identity-header trust.
* Impact: The fallback could introduce unauthorized access or make authenticated functionality unusable while satisfying anonymous 401 checks.
* Smallest useful change: Make the exemption branch conditional on documented and tested platform header handling for that exact configuration. Define the exact API path family, trusted identity ingress, stripping/overwriting behavior and server verification. Cover forged identity-header variants, malformed credentials, anonymous 401, unchanged public exemptions and normal browser redirect. Require a positive trusted-principal contract as well as negative tests. If trusted provenance cannot be established, do not enable the exemption; retain a Blocked API/browser coexistence result rather than claim success.
* Action owner: Planning parent and authentication implementer.
* Exact resolving evidence: Updated P01-T02 decision gate and test matrix; passing existing-suite tests for principal acceptance/rejection at the server trust boundary; authoritative platform behavior or bounded live verification for the exempt path. A real authorized HTTP/browser test remains Blocked until registration, credentials and staff prerequisites are satisfied; synthetic principal tests must not be labeled live authentication proof.
* Decision route: Direct planner correction. No tenant creation, secret fabrication, authentication weakening or new owner choice is authorized or required to describe the gate.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: The cut-over needs a non-deleting recovery path

* Related IDs: P02-T01/P02-T02; Non-Functional Requirements; P03-T01.
* Evidence: P02 creates and approves the edge connection, then changes browser/proxy settings. No task captures the prior non-secret auth configuration or defines what happens if public health, API 401, routing isolation or redirect checks fail.
* Concern: Additive resource creation does not make subsequent authentication and route changes harmless. A failed smoke could leave a public edge active against an incorrectly configured app or leave existing ingress behavior regressed.
* Impact: Recovery would become improvised under the explicit no-deletion constraint, and failed acceptance could leave a changed public/authentication boundary in place.
* Smallest useful change: Before mutation, record a sanitized baseline and define ordered gates for route activation, connection approval and auth update. On failure, disable the new route/endpoint as appropriate and restore only the prior non-secret auth/proxy settings on the existing app, without deleting resources, weakening private networking or touching tenant objects. Identify the operator and record the retained resources.
* Action owner: Planning parent and deployment operator.
* Exact resolving evidence: A bounded P02 recovery sequence with trigger conditions, permitted resource scope and baseline fields; configuration round-trip tests where feasible; a sanitized deployment record showing either successful gates or executed recovery and post-recovery status. No intentional live failure injection is required.
* Decision route: Direct planner correction within ama-only authority and the no-deletion rule.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Separate permitted inventory provenance from authentication intercept evidence

* Related IDs: Research Q3; P02-T03; Acceptance Criteria; Locked Test and Change Ownership.
* Evidence: P02-T03 requires a complete per-file inventory of 16 historical assets, static presence and public/authenticated reachability, while allowing all 16 checks to be protected redirects. The plan forbids legacy/private reads but does not identify how each static-presence observation will be obtained without them.
* Concern: A platform redirect may occur before application routing and therefore cannot prove an asset exists in the deployed image. Reconstructing the historical set by opening prohibited legacy locations would also violate the task boundary.
* Impact: The feature audit could silently overstate deployed presence or require prohibited reads, despite correctly labeling rendered acceptance Blocked.
* Smallest useful change: Name the existing permitted parity/reference inventory as the frozen source of historical filenames and link each of its 16 entries to an allowed src/image inventory observation where available. Keep historical inventory, current static presence, edge authentication interception, rendered functionality and real-user acceptance as separate columns. Mark unknown/blocked presence honestly; do not read legacy source to fill gaps.
* Action owner: Planning parent and evidence/audit implementer.
* Exact resolving evidence: Revised P02-T03 naming the permitted inventory source and observation method; the dated 16-row reconciliation with source provenance, current path or explicit gap, and separate authentication/rendering states. Redirect-only rows must not be marked as proof of deployed static presence or functional parity.
* Decision route: Direct planner correction. Existing gap references or a shared prerequisite issue remain appropriate; no feature implementation or expansion of authorized reads is requested.

## Strengths and Residual Risk

* Additive Front Door Premium/WAF Prevention/Private Link is an owner-authorized choice supported by the supplied networking research. The critique does not demand environment migration.
* The production guard and SQL Disabled posture are preserved explicitly; full-main publicAccess deployment is correctly rejected.
* Exact health/welcome exemptions, uncached authenticated content, HTTPS origin handling and a specific edge callback option are appropriate planned controls.
* Missing tenant registration, credentials and staff binding are explicit acceptance blockers. Reaching an Entra-hosted redirect does not prove a valid client, callback completion, session or authorized feature.
* Research Q1-Q3 remain labeled Open despite the readiness narrative. This critique does not treat that label inconsistency as a separate cosmetic finding: deployed network validation and feature acceptance remain work to do.
* Billable edge cost remains an acknowledged trade-off without an invented quote. Current owner authorization resolves the architecture choice, not operational/legal approval.
* Test-file limits and no-removal constraints remain binding while resolving these findings. Reuse existing tests first; do not silently broaden scope.

## Questions or Blocking Evidence Gaps

* No user question is required for these revisions.
* Actual single-app edge routing and exempt-path identity handling must be established before their relevant exposure/configuration gate. Failure to establish either blocks that branch of deployment, not this critique.
* Real sign-in and authenticated feature acceptance remain Blocked on the already-known tenant prerequisites. Do not attempt fresh tenant discovery or write tenant objects merely to close this critique.

## Limitations

* This is a single bounded plan assessment, not a vulnerability assessment, implementation review or Azure validation.
* Research statements and source pointers were assessed as supplied evidence; no fresh Azure, tenant, official-documentation or repository-code inspection was performed.
* No legacy application, private dataset, credential file or prohibited tracking area was read. Existing dirty planning inputs were left untouched.
* No tests were run because no executable source was changed. The output artifact was checked for finding completeness and workspace-only scope.

## Recommended Next Action

* Highest-impact finding: PC-001, shared-environment routing isolation.
* Action owner: Planning parent.
* Smallest next action: Add the explicit single-origin/domain invariants and hostile-host deployment gate to P01/P02, then incorporate PC-002 through PC-004 into the same finalization revision.
* User response required: No.
* Handoff: Return this complete finding set to the active planning parent. Revise directly and finalize without another critique. Implementation and the one planned postimplementation Review remain separate stages.

## Next Steps

The active planning parent should resolve PC-001 through PC-004 within the locked change/test budget and retain all known real-sign-in blockers. No user action, additional critique pass or implementation by this critic is required.
