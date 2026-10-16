---
title: Issue 138 deployment pipeline plan critique
description: One bounded offline assessment of the deployment pipeline candidate
ms.date: 2026-10-16
---

## Metadata

* Task ID: 138 / cicd-deploy-pipeline-138
* Critique date: 2026-10-16
* Plan: .copilot-tracking/plans/2026-10-16/cicd-deploy-pipeline-138-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/cicd-deploy-pipeline-138-phase-details.md
* Research: .copilot-tracking/research/2026-10-16/cicd-deploy-pipeline-138-research.md
* Critique execution status: Complete
* Assessment count: Exactly one bounded assessment; no implementation or second critique.

## Inputs and Criterion Boundary

The caller requires OIDC rather than stored deployment secrets, an attached PR
infrastructure what-if, environment-approved deployment, four versioned source
images, reuse of existing hardening and src/trivy.yaml, exact health 200 and
protected API 401, and no unauthenticated protected success. Only resource group
ama is permitted; deletion and public SQL are prohibited. This task permits no
Azure execution, private-data/environment-file/VS Code inspection, or retired
directory inspection. Tests belong in infra/tests, with at most two new test
files and three new helper files.

The supplied plan, phase details and research are the primary evidence.
Bounded corroboration used .github/workflows/src-ci.yml, infra/main.bicep,
infra/main.bicepparam, infra/main.test.bicepparam,
infra/main.pilot.example.bicepparam, infra/README.md,
infra/scripts/deploy.py, infra/modules/registry.bicep, relevant authentication
sections of infra/modules/containerapps.bicep, relevant HTTP probe sections of
infra/scripts/private-cutover-proof.py, src/trivy.yaml, src/check-container.py,
and the four workload Dockerfiles. Required repository context was read in
docs/reference/README.md, docs/reference/memory.md,
docs/case_study_48_original.md and docs/case_study_48_addendum.md. No additional
research lane, private inputs or live cloud evidence was used.

The active branch is feat/cicd-deploy-pipeline-138; read-only PR inspection
returned no existing PR for that branch. Supplied planning artifacts and a
session-state artifact were already untracked. They were left untouched.

For traceability, this critique assigns requirement labels, not new requirements:

| Label | Caller requirement |
| --- | --- |
| R1 | OIDC, least privilege, trusted-code and environment approval boundaries |
| R2 | PR infrastructure what-if attached safely |
| R3 | Four versioned src images, path-aware reuse, existing hardening/Trivy |
| R4 | Approved immutable release and consistent template/parameters |
| R5 | Exact health/denial probes; no unauthenticated protected success |
| R6 | ama only, never delete, SQL always private |
| R7 | Offline-only work, forbidden inputs excluded, bounded infra test ownership |
| R8 | Honest acceptance audit and external prerequisite handoff |

P01-T01, P02-T01 and P03-T01, research C1-C6, the research trust decision,
the plan's acceptance criteria and its listed follow-ups were assessed once
across their full supplied boundary. Generic intentions are credited as
intentions, not executable contracts or observed proof.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| R1; research trust decision; P01-T01/P02-T01 | Partial | OIDC clients, fork exclusion and environments named; trusted execution, effective role permissions and credential isolation undefined (PC-001, PC-002, PC-006). |
| R2; C2/C5; P01-T01 | Partial | Sanitized attachment promised; structured fail-closed parsing, trusted publication and revision binding missing (PC-007, PC-008). |
| R3; C1/C3; P01-T01 | Partial | Four images and scan reuse stated; dependency closure, provenance, tags, promotion and quarantine handoff unspecified (PC-009, PC-010, PC-011). |
| R4; C5; P01-T01/P02-T01 | Partial | Digests promised, but exact approved release inputs, parameter contract and serialization absent (PC-003, PC-004, PC-014). |
| R5; C4/C6; P01-T01 | Partial | HTTP checks promised; default authentication mode conflicts with the exact anonymous 401 requirement and probe contract is unspecified (PC-005, PC-012). |
| R6; C2; P01-T01 | Partial | Scope/Delete/SQL intentions present; effective scope policy and non-vacuous SQL checks missing (PC-007, PC-013). |
| R7; P03-T01; test ownership | Partial | Ownership and file caps explicit; persistent CI wiring, behavioral matrix and offline compiler boundary missing (PC-015). |
| R8; P02-T01/P03-T01; acceptance criteria | Partial | Live limitations acknowledged; criterion-level closure and inherited hosted-hardening limitation need explicit disposition (PC-016). |

## Verdict

* Verdict: Revise
* Severity summary: 12 High, 4 Medium, 0 Critical, 0 Low.
* Rationale: The sources support offline implementation planning, but the
  current candidate leaves material authorization, trust, parameter and release
  boundaries to implementation-time invention. These are planning corrections,
  not proof of exploitable implementation defects. The supplied evidence is
  sufficient to identify and disposition the gaps without executing Azure.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Same-repository PR membership does not establish trusted execution

* Related IDs: R1, R2; research trust decision; P01-T01/P02-T01.
* Evidence: Research lines 35-45 prohibits untrusted PR execution with OIDC on privileged runners, then selects "trusted same-repository PR what-if." Phase details lines 9-11 names fork exclusion and exact-candidate approval without defining how trust is established.
* Concern: A contributor branch can change helpers, workflow configuration and Bicep. Fork exclusion alone does not authorize executing that branch on a runner with private-network access. A privileged pull_request_target checkout or a workflow_run consuming attacker-controlled artifacts would also cross this boundary. Environment approval must identify the actual PR head, not merely the base workflow ref.
* Impact: OIDC and private-network access can become available to code that has not received the intended review; stale approval can apply to a later head.
* Smallest useful change: Specify the event/job/ref trust graph. Run untrusted validation without OIDC on non-private runners. Use a protected, trusted workflow/helper revision for privileged planning, approve the exact candidate SHA, and treat candidate Bicep as constrained input rather than executing candidate scripts. Revalidate PR head/base and invalidate stale approval before privileged work. Explicitly prohibit privileged checkout/execution of unreviewed PR code and cross-run unverified artifacts.
* Action owner: Planning parent for the workflow contract; repository administrator for runner-group and environment restrictions.
* Exact resolving evidence: Revised P01-T01 event/ref matrix plus tests showing fork, same-repository unapproved, changed-head, privileged base-trigger checkout and forged cross-run artifact cases cannot reach OIDC or private execution. Administrator configuration remains a separately recorded live prerequisite.
* Decision route: Direct planner correction. The caller already forbids untrusted privilege; no new user decision is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: The identity permission model conflicts with role-assignment declarations

* Related IDs: R1, R4, R6; P01-T01/P02-T01; plan scope and follow-ups.
* Evidence: Plan lines 28-29 excludes role assignment changes; phase details lines 11 and 24 only names separate clients and "ama-only roles." infra/main.bicep passes role assignments to storage, registry, Key Vault and other modules; infra/modules/registry.bicep declares Microsoft.Authorization/roleAssignments directly.
* Concern: Separate client IDs are not a least-privilege action/scope design. The main template submits role-assignment resources even on redeploy. A generic Contributor assumption can fail, while granting Owner or unrestricted role-assignment authority violates the stated boundary. What-if authorization requirements also must not be reduced to a claim that ordinary resource read access necessarily suffices.
* Impact: The pipeline either fails with undocumented permissions or expands privilege to work around a foreseeable failure. Declaration submission and an actual new/changed assignment are not interchangeable.
* Smallest useful change: Define action/scope matrices for planning, registry publication/quarantine and application deployment, including required deployment operations and template role-assignment submissions. Keep directory rights and subscription governance absent. State whether the release is existing-stack-only, require manually provisioned approved assignments, reject unapproved assignment deltas, and document any constrained authorization needed for idempotent submissions. If that cannot fit the existing no-change boundary, leave apply blocked instead of granting broader authority.
* Action owner: Planning parent; platform IAM owner supplies and approves actual federated credentials/RBAC later.
* Exact resolving evidence: Revised permission and bootstrap matrix, offline fixtures for missing/excess privileges and forbidden assignment changes, and a named live RBAC verification gate. No offline role matrix is called proof that Azure will authorize the deployment.
* Decision route: Direct planner correction under current constraints. Any later request to expand assignment/delegation authority requires a separate owner decision, not automatic implementation.

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Approval is not bound to the exact deployment release

* Related IDs: R1, R4; P01-T01; plan functional requirements.
* Evidence: Plan lines 33-35 promises the same template/parameter set and digests; phase details lines 9-18 contains no artifact identity or dependency order. infra/README.md, Orchestrator image selection, warns that discovery runs again at apply and recommends pinning the same explicit digest.
* Concern: A PR what-if precedes a merged-main release and possibly image publication. It cannot automatically approve final images, merged code or later environment values. Recompilation, mutable tags, repeated discovery and changed configuration between planning and apply can invalidate review. A main-only dispatch by itself does not prove required CI passed for the selected commit.
* Impact: An approved plan can deploy a different template, image set or configuration.
* Smallest useful change: Define an immutable release manifest containing commit, trusted workflow/tool revision, environment/workload, compiled template hash, canonical effective-parameter hash, four image digests and scan evidence references. Keep identifiers/private values out of published evidence. Require successful relevant CI for that exact commit; perform a release-specific what-if with final digests before deployment approval. Verify manifest/run/artifact identity at apply, prohibit fresh tag discovery/rebuild/reparameterization, and require renewed review when material inputs change. Treat PR what-if as advisory candidate evidence, not release authorization.
* Action owner: Planning parent.
* Exact resolving evidence: Revised job dependency/artifact graph and mutation tests rejecting changed SHA, failed/unrelated CI, parameter/template/digest mismatch, untrusted artifact origin and missing final approval. Same-commit digest promotion is explicit.
* Decision route: Direct planner correction; environment-approved immutable deployment is already requested.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Parameter replacement lacks a typed, validated compilation contract

* Related IDs: R4, R5, R6; C2/C4; P01-T01.
* Evidence: Phase details lines 12-14 says to replace placeholders from environment variables with allowed overrides, without listing names, types or precedence. All three committed examples contain required placeholders; infra/main.bicep has string, boolean, integer, array, object and secure inputs. Its budgetStartDate defaults to utcNow.
* Concern: Text substitution is not equivalent to compiling Bicep parameters. Values may break quoting or become expressions; strings such as "false" may become truthy; omitted placeholders or silent defaults can change deployment identity/authentication. Dynamic defaults can also make separately generated what-if/apply inputs differ.
* Impact: Invalid or unintended parameters reach ARM; unsafe settings or stale placeholder evidence can pass superficial checks.
* Smallest useful change: Specify the exact example mapping, trusted offline Bicep compilation method and relative using-path handling. Enumerate allowed variable-to-parameter mappings, types, precedence and mandatory values. Parse booleans/numbers/objects explicitly; reject unknown/duplicate overrides, unresolved placeholders, zero identifiers, example.invalid mailboxes and inconsistent environment/profile/workload inputs. Validate release authentication and all four digest inputs. Resolve time-dependent values once. Generate JSON by serialization, not executable text interpolation, in protected ephemeral files without publishing values.
* Action owner: Planning parent.
* Exact resolving evidence: A parameter schema/table plus fake-process tests for all three examples, quoting/newline/injection strings, boolean false, arrays/objects, unknown overrides, missing placeholders, path handling and stable canonical what-if/apply inputs. Pilot remains blocked until its recorded decisions exist.
* Decision route: Direct planner correction. No actual identifiers or private completed parameter files are needed for planning/tests.

<!-- rpi:critique id=PC-005 -->
### PC-005 [High]: Default application authentication cannot satisfy the secretless exact-401 path

* Related IDs: R1, R5; C4/C6; P01-T01/P02-T01.
* Evidence: Examples leave entraClientId empty. infra/main.bicep defaults deployApplications=true and entraBearerOnly=false. infra/modules/containerapps.bicep lines 87, 114-115 and 182-214 condition authentication on a nonempty client ID; browser mode uses a vault client secret and RedirectToLoginPage, while bearer-only mode uses Return401. infra/README.md documents the opt-in secretless service-smoke mode.
* Concern: Merely filling ordinary placeholders can leave authentication disabled or select browser redirect behavior instead of the required anonymous 401. OIDC deployment authentication does not determine application ingress authentication. The plan does not distinguish "no stored deployment secrets" from existing browser application credentials.
* Impact: Deployment can expose an unprotected application or fail the requested denial probe despite otherwise successful infrastructure rollout.
* Smallest useful change: Define the supported release target/authentication contract before apply. For the already documented secretless service-smoke target, require a valid audience, entraBearerOnly=true and compatible token-store settings; reject empty auth or placeholder images before activation. Do not silently convert an existing shared browser deployment to bearer-only. Document browser credentials/initialization separately and block any incompatible target pending explicit approval.
* Action owner: Planning parent; application/platform owner handles existing target compatibility and manual initialization.
* Exact resolving evidence: Revised environment/auth-mode matrix and tests rejecting empty audience, browser redirect mode for the exact-401 service target, incompatible token storage and unauthenticated application activation. Existing-stack compatibility remains a live prerequisite, not an assumed fact.
* Decision route: Direct planner correction for the specified service proof. A later change to shared browser behavior requires a separate owner decision; this critique does not authorize it.

<!-- rpi:critique id=PC-006 -->
### PC-006 [High]: Build/runtime validation must not inherit publishing or deployment credentials

* Related IDs: R1, R3; P01-T01.
* Evidence: Phase details lines 11 and 15-17 names separate clients but no job boundary. Workload Dockerfiles execute build steps, and src/check-container.py executes image content. Plan lines 40-42 only limits id-token permission to jobs.
* Concern: A build or runtime-test job with id-token write can request credentials for its entire lifetime. Logging out before or after building is not equivalent to removing token issuance, ambient managed identity, Docker registry credentials or private-network authority from executable source content.
* Impact: Source/image execution can gain release authority beyond what is needed to build and test.
* Smallest useful change: Separate credential-free build/runtime/scan execution from trusted publication and apply. Specify immutable transfer of the tested image bytes/digests into a publisher that does not execute candidate content, with deploy credentials absent from both. Define private runner network/ambient-identity restrictions, fresh runner isolation, timeouts and cleanup of Docker/Azure credential state; ephemeral alone does not remove authority during a job.
* Action owner: Planning parent; runner administrator owns effective network and ambient-identity restrictions.
* Exact resolving evidence: Job permission/runner matrix and structure/behavior tests proving executable build/test steps have no OIDC issuance or publish/deploy credential context, and the publisher verifies the exact scanned digest. Live runner isolation is separately unverified.
* Decision route: Direct planner correction; do not introduce stored secrets as a shortcut.

<!-- rpi:critique id=PC-007 -->
### PC-007 [High]: Rejecting Delete alone does not define an ama-only safe apply policy

* Related IDs: R2, R4, R6; P01-T01.
* Evidence: Plan line 19 requires incremental ama-only deployment; phase details line 14 only specifies "Reject Delete." infra/main.bicep is resource-group scoped, but nested templates and future candidate changes still require inspection. infra/README.md explicitly excludes subscription governance, exemptions and modifications outside ama.
* Concern: Incremental mode is not a no-delete permission boundary. A Modify can weaken SQL/privacy controls or change identities without a Delete classification. Unknown/Ignore/unsupported what-if results, nested scopes and changes not understood by the policy have no specified disposition.
* Impact: An incomplete or superficially safe what-if can authorize a prohibited operation or out-of-scope effect.
* Smallest useful change: Make create explicitly Incremental and use one structured what-if policy for PR and release. Validate every affected resource and nested deployment against the expected subscription and ama scope. Reject Delete, unapproved authorization/policy changes, SQL public/firewall changes and forbidden profile relaxations; fail closed on unknown, malformed, incomplete or unevaluated critical changes. Do not call group delete, subscription deployment, governance, policy exemption or network-bypass commands. Combine static compiled controls, restrictive IAM and reviewed what-if rather than presenting any one as a complete guarantee.
* Action owner: Planning parent.
* Exact resolving evidence: Explicit policy/action list and tests for nested/external scopes, complete-mode mutation, forbidden Modify, Delete, unknown/Ignore critical resources, partial JSON and nonzero Azure results; fixtures assert no apply command is produced.
* Decision route: Direct planner correction under the caller's existing ama/no-delete/private-SQL direction.

<!-- rpi:critique id=PC-008 -->
### PC-008 [High]: Sanitization and the PR attachment lack an explicit safe publication path

* Related IDs: R1, R2; C5; P01-T01/P02-T01.
* Evidence: Plan lines 34 and 40-42 promises attachment and no raw Azure output. infra/scripts/deploy.py prints selected image references, includes Azure stderr in errors and forwards deployment stdout/stderr. It is not already a sanitized pipeline interface.
* Concern: Reusing the wrapper unchanged leaks information before a later sanitizer can act. A plain job summary is not necessarily an attached PR artifact. Granting PR write permission to the OIDC job to post a comment would unnecessarily combine trust domains. Counts-only output may also omit the configuration classes an approver must review.
* Impact: Identifiers, parameter values or exception text can enter logs/artifacts, or the requested PR evidence is absent/unreviewable.
* Smallest useful change: Define a trusted adapter that captures subprocess output, parses structured results and emits only an allowlisted schema: candidate SHA, environment alias, action/type counts, safe symbolic resource references, relevant control-change classifications and outcome. Suppress raw commands/tracebacks and sanitize compiler/login/what-if/apply failures, not just success. Attach a named retained artifact bound to PR/head/run, with an explicit PR link or isolated trusted publisher if comments are needed; avoid PR write on cloud jobs. Never upload raw parameters, CLI caches or raw what-if.
* Action owner: Planning parent.
* Exact resolving evidence: Revised publication/permission contract plus canary tests placing fake identifiers and sensitive strings in stdout, stderr, exceptions, nested JSON and log-control characters, asserting none appears in logs or attachments. Tests also assert the exact PR/run/SHA artifact binding and attachment path.
* Decision route: Direct planner correction; no new comment permission is implied by the request.

<!-- rpi:critique id=PC-009 -->
### PC-009 [High]: Content fingerprints do not yet prove safe image reuse

* Related IDs: R3; C1/C3; P01-T01.
* Evidence: Phase details lines 15-17 says shared dependencies are included but gives no dependency closure or reuse verification. src/api/Dockerfile copies core, agents, API, build-requirements.txt, API requirements and agents/evals/ai_priority_golden.json. Other Dockerfiles also depend on shared core/build inputs.
* Concern: Project-directory-only fingerprints miss shared build inputs, Docker context filtering or golden assets. A mutable fingerprint tag and an old scan result are not proof of source provenance or current vulnerability status. Network-installed OS packages also mean a source hash is a cache key, not proof of reproducible bytes.
* Impact: Changed code/dependencies can retain a stale image, or an overwritten/cache-poisoned mapping can be promoted.
* Smallest useful change: Enumerate the four dependency closures, including Dockerfiles/base digests, build requirements, requirements/project metadata, shared sources, copied eval assets and context rules. Bind each trusted fingerprint record to an immutable image digest and originating source/build evidence; verify registry ownership and mapping before reuse. Pull, runtime-check and rescan the exact reused digest using the current hardening/Trivy policy. Define cache absence versus query failure; ambiguous or mismatched provenance must not silently reuse.
* Action owner: Planning parent.
* Exact resolving evidence: Dependency table and mutation fixtures for shared core, agents-to-API, eval asset, lock/build/base/context changes, unrelated changes, poisoned tag/digest and failed lookup. Gate/full reports identify the actual reused or built digest and current policy revision.
* Decision route: Direct planner correction. Retaining unchanged bytes is allowed; it must not be described as a fresh reproducible build.

<!-- rpi:critique id=PC-010 -->
### PC-010 [Medium]: Version tags, project mapping and cross-environment promotion are unspecified

* Related IDs: R3, R4; C3; P01-T01/P02-T01.
* Evidence: Plan says "versioned images"; research C3 requires project tags. .github/workflows/src-ci.yml builds api, agents, orchestrator and importer with src context, while the importer distribution name is zava-forward-import. infra/README.md requires same-commit digest promotion without environment rebuilds.
* Concern: No exact four-project repository/parameter/version map, collision policy or promotion interface is defined. Re-running a manual release per environment could rebuild or overwrite a version, despite deploying digest references afterward.
* Impact: Inconsistent image naming or mutable release tags make the release hard to audit and promotion unreliable.
* Smallest useful change: Define each Dockerfile, registry repository, Bicep image parameter and project-scoped immutable version tag, including importer naming. Bind version to source/release identity; reject reuse of a version for different bytes. Separate build-once release creation from environment promotion consuming the same four digests and template commit, while allowing reviewed environment-specific parameters.
* Action owner: Planning parent.
* Exact resolving evidence: Four-row mapping, tag/collision contract and tests proving all four images are present, duplicate versions cannot change digest, importer maps correctly and promotion does not rebuild.
* Decision route: Direct planner correction; a conservative commit-derived version needs no new user decision.

<!-- rpi:critique id=PC-011 -->
### PC-011 [High]: Production quarantine is only a documentation prerequisite, not an executable gate

* Related IDs: R1, R3, R4; P01-T01/P02-T01.
* Evidence: Phase details line 25 lists "quarantine release prerequisite." infra/modules/registry.bicep enables quarantine by default; test and pilot examples retain it. Workload pull identities receive AcrPull.
* Concern: Local scan-before-push does not establish that a newly pushed digest is released from registry quarantine. Ordinary push/pull permissions need not include the separate quarantine operations. A successful push can therefore be followed by an unpullable deployment.
* Impact: Test/pilot rollout can fail or invite disabling quarantine to make the release work.
* Smallest useful change: Specify the approved digest-bound quarantine handoff and its identity/permissions. Either implement the already-authorized supported release path or make apply explicitly blocked until a separately authorized operator supplies verified release evidence for the exact digest. Check release/pull readiness before apply; never disable quarantine or widen registry access as fallback.
* Action owner: Planning parent; registry/platform owner approves the actual release mechanism and permissions.
* Exact resolving evidence: Defined digest/status evidence contract and tests where unreleased, missing, mismatched or unavailable quarantine state prevents deployment. Actual registry quarantine support and identity operation remain a live prerequisite.
* Decision route: Direct planner correction to fail closed. New quarantine authority would require separate owner authorization, not a silent privilege expansion.

<!-- rpi:critique id=PC-012 -->
### PC-012 [High]: HTTP acceptance needs endpoint binding and a complete negative-test contract

* Related IDs: R5; C6; P01-T01/P03-T01.
* Evidence: Phase details line 18 promises exact checks without redirects, but does not enumerate them. infra/scripts/private-cutover-proof.py, smoke, names /healthz and /api/me and includes anonymous, malformed-bearer and forged-principal denials; its http_status uses urllib's default redirect behavior.
* Concern: Reusing the existing probe unchanged would not satisfy the no-redirect requirement. An arbitrary configured URL, old serving revision, skipped probe or transport failure can also produce misleading acceptance unless target identity and result handling are specified.
* Impact: Login redirects, a wrong target, or partial probes can be mistaken for protected ingress success.
* Smallest useful change: Require /healthz exactly 200 and /api/me exactly 401 for anonymous, malformed bearer and forged X-MS-CLIENT-PRINCIPAL requests, without cookies or genuine tokens. Reject redirects, other 2xx, other statuses, DNS/TLS/timeout failures and missing results. Verify HTTPS and the expected deployed origin/revision/image identity using scoped management output, with bounded readiness retries and no insecure TLS fallback. Do not log response bodies or identity headers, and do not reuse the existing redirect-following helper unmodified.
* Action owner: Planning parent.
* Exact resolving evidence: Explicit four-probe matrix and local HTTP tests covering all expected statuses, 200/204 anonymous failure, 302 redirect trap, malformed/forged-header behavior, wrong target, missing probe and transport failure. Later private-runner results remain separate live evidence.
* Decision route: Direct planner correction; public health/static exemptions are not prohibited authenticated API success.

<!-- rpi:critique id=PC-013 -->
### PC-013 [High]: SQL verification can pass vacuously and occurs too late to prevent exposure

* Related IDs: R6; P01-T01/P03-T01.
* Evidence: Phase details line 19 says scoped list and failure on any non-Disabled server. Plan line 36 only requires a post-deployment check. infra/main.bicep names a target SQL server from workload/environment and uniqueString scope; the template's private setting is a static guarantee only for its current reviewed content.
* Concern: An empty list, wrong subscription, omitted property or missing intended server can satisfy "no non-Disabled server." A post-check alone detects a forbidden change only after it happened. Resource-group name ama is not unique across subscriptions.
* Impact: A wrong-account or incomplete verification can falsely attest private SQL, or a candidate can temporarily enable public access before failing.
* Smallest useful change: Bind the Azure account to approved tenant/subscription variables before queries; require the expected deployment SQL server in the ama-scoped result, validate result schema and fail on empty/missing/null/unknown values or any non-Disabled server. Apply static/what-if private-SQL gates before apply and verify again afterward. Never open public SQL, change firewalls or bypass policy to run checks; no data-plane SQL read is required.
* Action owner: Planning parent; platform owner supplies the expected account/target configuration outside committed artifacts.
* Exact resolving evidence: Fixtures for wrong account, zero servers, missing target, malformed/unknown state, public server elsewhere in ama and denied list access; each fails. Tests demonstrate SQL-changing mutations block apply before a post-check.
* Decision route: Direct planner correction under the existing always-private requirement.

<!-- rpi:critique id=PC-014 -->
### PC-014 [Medium]: Concurrent releases and failed rollout handling are undefined

* Related IDs: R4, R6; P01-T01/P02-T01.
* Evidence: The plan/details contains no concurrency, cancellation or recovery contract. .github/workflows/src-ci.yml uses cancel-in-progress for CI, which is not a safe apply policy. All environments share ama.
* Concern: Two manual releases can interleave review/apply, use overlapping named ARM deployments or change state after what-if. Canceling an in-flight apply does not roll back Azure. A failure after push or rollout has no stated publication/acceptance disposition.
* Impact: Approval becomes stale, evidence mixes releases, or an operator attempts destructive recovery.
* Smallest useful change: Define shared deployment serialization at the actual ama resource-overlap boundary, unique run/deployment identifiers, and cancel-in-progress=false for apply. Recheck approval/input/state freshness before applying. Distinguish image publication from deployment acceptance; failed smoke or SQL verification fails the release and stops promotion. Recovery requires a new approved digest/parameter rollout, never deletion or public-network repair.
* Action owner: Planning parent.
* Exact resolving evidence: Concurrency/failure-state contract and structure/behavior fixtures for overlapping dispatches, stale what-if, partial push, failed apply/probes and rerun. Documentation does not promise workflow-local concurrency coordinates unrelated external actors.
* Decision route: Direct planner correction; no automatic rollback/delete authority is granted.

<!-- rpi:critique id=PC-015 -->
### PC-015 [Medium]: Tests are named but their persistent CI and behavioral coverage are not

* Related IDs: R7; P01-T01/P03-T01; test ownership.
* Evidence: Plan lines 57-59 caps files and names infra/tests/test_pipeline.py, but only says "structure tests parse YAML." Phase details lines 29-31 names tools without commands or outcomes. Existing src-ci namespace discovers infra/tests but its infra ruff/mypy selectors explicitly list existing files.
* Concern: Merely creating tests does not ensure new YAML is valid, policy mutations fail, new helpers are type/lint checked or workflow-only changes trigger validation. Generic string checks can pass when executable job dependencies or permission placement are wrong. The blanket "no Azure commands" wording also needs to distinguish local Bicep compilation from actual cloud operations required by neither offline tests nor this critique.
* Impact: The planned safety properties regress unnoticed, or tests silently skip the evidence they are meant to provide.
* Smallest useful change: Map each finding/requirement to behavioral fixtures and workflow structure/mutation checks. Specify a canonical helper/test layout within the stated limits, runner commands, tool availability/failure handling and persistent CI/path-filter wiring without renaming existing checks. Add new files to actual lint/type selectors. Allow only explicitly offline local compilation where needed; fake all Azure management/data calls and never dispatch deployment during validation. Missing required tooling must be reported, not counted as a pass.
* Action owner: Planning parent.
* Exact resolving evidence: Revised test/command/CI matrix with at most two new infra/tests files and three new helpers; it covers PC-001 through PC-014, malformed/failed subprocesses and unsafe workflow mutations. Existing infra regression checks and pinned action/workflow syntax validation have explicit recorded outcomes.
* Decision route: Direct planner correction; do not add another test suite location or new tooling without necessity.

<!-- rpi:critique id=PC-016 -->
### PC-016 [Medium]: Acceptance must preserve the inherited hosted-hardening and live-evidence limits

* Related IDs: R3, R7, R8; C1/C4; P02-T01/P03-T01; plan acceptance criteria.
* Evidence: Plan lines 44-47 reduces acceptance to passing offline tests and documented external gaps. infra/README.md, Hardened source image rollout (#118), explicitly says Container Apps does not expose the checked read-only/capability/no-new-privileges settings and hosted enforcement remains unmet. src-ci separates fixable HIGH/CRITICAL failure gating from full unfixed-inclusive reports.
* Concern: "Always run hardening" can be interpreted as satisfying hosted controls that the evidence expressly does not establish. The plan also does not enumerate the original requested outcomes in its acceptance audit, attach owners and resolving evidence to every live gate, or specify retention of both scan reports when the fixable gate fails.
* Impact: A successfully merged offline workflow can be mislabeled as completed OIDC, private runtime, deployment approval or infrastructure hardening acceptance.
* Smallest useful change: Add criterion-level outcomes for federation, least privilege, approval restrictions, attached what-if, four versioned/scanned digests, quarantine, apply, exact denial checks and SQL privacy. Separate planned/offline-passed/live-blocked for each. Preserve the existing fixable-only blocking and full/unfixed reporting policy using src/trivy.yaml, retain both reports on gate failure when produced, and state that local Docker controls plus compatible non-root startup are not hosted enforcement. Assign each live gate an owner, prerequisite and exact resolving evidence; leave hosted enforcement explicitly Partial/Blocked unless separately resolved.
* Action owner: Planning parent for the audit; repository/platform/application owners for the respective live gates.
* Exact resolving evidence: Acceptance matrix and evidence retention/job conditions, plus a limitations section matching infra/README.md. Live success rows remain unclaimed until authorized external evidence exists; no new hosting architecture or live test is required by this critique.
* Decision route: Direct planner correction. The user already requires honesty and forbids Azure execution; no user response is needed to record unmet evidence.

## Strengths and Residual Risk

* The candidate correctly selects src image context, immutable deployment
  digests, separate OIDC client intentions, private ephemeral runners,
  exact-status probes, incremental ama-only scope and no raw cloud artifacts.
* Fork exclusion, existing environment examples, src/trivy.yaml, existing
  hardening checks and preservation of existing CI names are sound starting
  points; the findings complete their execution contracts rather than replace
  them with a different architecture.
* The research explicitly separates workflow existence from federation,
  review, release and deployment proof. Preserve that distinction.
* Pilot region/subscription ownership, region/quota review, private networking,
  federated credentials, effective permissions, quarantine support, application
  initialization and hosted hardening remain live prerequisites. Listing them
  does not establish that the owner has accepted the residual risk or approved
  deployment.

## Questions or Blocking Evidence Gaps

* No immediate user answer is needed for the planner to revise under the
  existing constraints. The full actionable set is PC-001 through PC-016;
  there is no withheld later finding set.
* The planning parent must not infer unavailable permissions, protected
  environment configuration or existing-stack authentication compatibility.
  Choose fail-closed prerequisite gates now. A future proposal to broaden IAM,
  alter a shared browser target, disable quarantine, change hosting or enable
  pilot requires a separate owner decision.
* The full issue/comment text was not independently retrieved. C3 and the
  caller's explicit requirements define this bounded assessment; unsupported
  issue-level completion claims must not be added from inference.

## Limitations

* This is a plan credibility assessment, not a vulnerability audit or validation
  of implementation that has not been written.
* No Azure login, query, deployment, what-if, workflow dispatch, Docker runtime
  check or application data access was performed. No live acceptance is claimed.
* No private data, environment files, VS Code material or retired directories
  were inspected. Identifiers in tests/resolving evidence must be synthetic.
* No plan, phase-details, research, session-state, source or documentation file
  was changed. Only this requested critique artifact was written.

## Recommended Next Action

* Highest-impact finding: PC-001, the privileged PR execution trust boundary.
* Action owner: Planning parent.
* Smallest next action: Revise P01-T01 to define trusted workflow/ref execution,
  exact-SHA approval, identity action/scope matrices and an immutable release
  graph, then disposition the remaining findings in the same plan/details.
* User response required: No for those corrections. Preserve live blockers and
  seek a separate owner decision only if the proposed implementation would
  exceed existing authorization or alter shared behavior.
* Parent handoff: This single critique is complete. The active planning parent
  revises directly, records all dispositions and finalizes without another
  critique pass; this artifact does not authorize implementation or Azure work.

| .copilot-tracking/plans/2026-10-16/cicd-deploy-pipeline-138-plan.md | Assessed plan, unchanged |
| .copilot-tracking/details/2026-10-16/cicd-deploy-pipeline-138-phase-details.md | Assessed phase details, unchanged |
| .copilot-tracking/research/2026-10-16/cicd-deploy-pipeline-138-research.md | Supplied evidence boundary, unchanged |
| .copilot-tracking/plans/2026-10-16/cicd-deploy-pipeline-138-critique.md | Complete bounded finding set |

## Next Steps

The active planning parent should revise the supplied plan and details once
against PC-001 through PC-016, record direct dispositions and live prerequisite
owners, and finalize without rerunning critique. No user action or Azure
execution is required for that revision.
