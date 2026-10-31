---
title: Demo routing redeploy plan critique
ms.date: 2026-10-31
---

## Metadata

* Task ID: 439ddfed-247a-4d5a-85ce-c60e9b939be3/demo-sites-redeploy-routing
* Critique date: 2026-10-31
* Plan: .copilot-tracking/plans/2026-10-31/demo-sites-redeploy-routing-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/demo-sites-redeploy-routing-phase-details.md
* Critique execution status: Complete
* Execution count: Exactly one independent final-candidate critique. No nested or repeated critique.
* Source pin: 9ecb159bd843411c2e17dc2785ab59f5e837040f, including #610/#611.

## Inputs and Criterion Boundary

* Caller requirements: Two demo redeployments authorized through 2026-11-15; bounded VM-IP-only ACR window with exact private restoration; existing az acr build fallback; no new RBAC, endpoints, public SQL or resident AI activation. At most two sign-in submissions per account using only named credentials inside automation. No production test changes.
* Publication decision: Repeated no-push direction and later PR request remain unresolved. Local deployment/evidence authority is not push authority. Publication stays blocked without clarification and the complete exact-head local gate.
* Supplied planning inputs: The plan, phase details, research pointer and current session state; AC1-AC8, P01-P03 and all six task IDs.
* Historical evidence: .copilot-tracking/changes/2026-10-31/demo-sites-redeploy-1031-changes.md; .copilot-tracking/details/2026-10-31/demo-sites-redeploy-1031-phase-details.md; .copilot-tracking/changes/2026-10-31/demo-sites-redeploy-cache-changes.md; .copilot-tracking/details/2026-10-31/demo-sites-redeploy-cache-phase-details.md; .copilot-tracking/reviews/logs/2026-10-31/demo-sites-redeploy-cache-review.md. Relevant retained rollout and initializer adapter bodies were inspected read-only through these evidence pointers.
* Current-source evidence: src/api/README.md employee acceptance identity procedure; src/api/src/zava_forward/api/resident_demo/chat.py natural-intent routing and unknown examples; src/README.md local publication gate. Read-only Git comparison confirmed no changed .sql paths since 4cb5964f but changes in the two supplied SQL transport/SELECT source files.
* Required context: docs/case_study_48_original.md, relevant addendum context, docs/reference/README.md and docs/reference/memory.md. Memory was treated as context, not proof.
* Boundary: Planning credibility and source/retained-procedure compatibility, not fresh operational acceptance. No implementation, cloud, browser, test or credential access was performed. This artifact is the sole write.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Deployment authority and source pin / AC1 | Covered | Explicit authorization and exact 9ecb159b tracked source; no unrelated source repair. |
| P01-T01 / AC1 | Covered | Fresh protected backups, transitive hashes, archive-only context and concrete resource-subdirectory image proof before publication address the #596/cache8 build-proof failures. |
| P01-T02 / AC2 | Covered | Bounded /32/defaultDeny window, old-manifest protection, close-first exact restoration and fallback assessment from restored baseline; no fallback success inferred. |
| Research C3-C4 / P02-T01 / AC3 | Covered | SQL-touch condition correctly includes transport/SELECT changes. Original narrow initializer is selected, not blanket DDL or new staff transport/RBAC. Retained initializer contains owned retry-only restoration and drift refusal. |
| P02-T02 / AC4 / timeout decision | Partial | Owned intent, pair reconciliation, protected comparisons and min0 retained; actual inherited timeout-to-recovery path conflicts with current decision, PC-001. |
| P03-T01 / AC5 anonymous checks | Covered | Real desktop/mobile browser and curl, source-equal public assets, exact year/immutable and no-store assertions, dock poststates and protected 401/302 boundary. |
| P03-T01 / AC6 employee identity admission | Partial | Credentials and attempt budget are bounded, but independent immutable identity admission is absent, PC-002. |
| P03-T01 / AC6 resident rules and refusal | Covered | Summary/record consent, two specified own-case intents, unknown examples, rules/source grounding and no case-data output; source supports these intents with AI OFF. |
| P03-T01 / AC5-AC6 protected employee assets | Partial | Actual widget200 planned, but protected delivered-byte/version/cache evidence is absent, PC-003. |
| P03-T02 / AC7-AC8 | Covered | Sanitized failed/success provenance, one preserved independent Review, exact-path privacy-safe local commit and Refs-only links; no-push and full exact-head publication gates remain separate blockers. |
| Risks, dependencies and failure routing | Partial | Ordered restoration/init/rollout/acceptance dependencies are sound. PC-001 is a concrete mismatch in the procedure being reused, not a cosmetic detail gap. |

## Verdict

* Verdict: Revise
* Severity counts: Critical 0; High 2; Medium 1; Low 0.
* Rationale: The candidate is substantially bounded and honors owner authority, but it reuses a demonstrably incompatible timeout compensation path and lacks two necessary signed-in acceptance safeguards. All three findings are direct planner corrections. No further critique is required or authorized.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Retained rollout still compensates deadline-only uncertainty

* Related IDs: P02-T02, AC4, Dependencies and Failure Routing; research C1 and the explicit caller timeout boundary.
* Evidence: Current phase details select the original guarded pair. The retained #596 rollout adapter loads the earlier rollout functions and pair coordinator. In that transitive implementation, converge() ends with StartupFailure("Target failed to become healthy within 900s") solely on deadline exhaustion. finish() catches StartupFailure and invokes recover(). The pair coordinator additionally catches RuntimeError, TimeoutError and AssertionError, classifies targets as owned and can recover the earlier healthy member. The cache8 phase details explicitly retained original roll()/finish()/converge()/recover(), so inheriting cache8 does not remove these paths.
* Concern: The plan says timeout alone must lead to read-only diagnosis, but the named reusable implementation can mutate an app before that disposition is reached. Ownership and protected-state equality establish whether a write is safe from concurrent drift; they do not establish that a genuine startup failure occurred.
* Impact: A merely slow or temporarily unobservable new revision can cause unintended recovery of both apps, including an already healthy member. This reproduces the class of unnecessary compensation the current caller explicitly excludes.
* Smallest useful change: Explicitly adapt both the inner convergence/finish path and outer pair handler. Classify deadline/request exhaustion as unresolved and persist read-only diagnosis without recovery. Permit pair compensation only with affirmative genuine deployment-failure evidence; retain existing ownership, auth, protected-state and ambiguous-write guards. Do not leave the timeout decision as prose over unchanged retained code.
* Action owner: Planning parent, then the authorized implementation executor for the named adapter change.
* Exact resolving evidence: Plan/details identify the retained converge(), finish() and pair main() branches and the current adapter changes that prevent every timeout-only route to recover(). Before mutation, bind the adapted/transitive hashes and inspect those branches. Later actual receipts must distinguish genuine failure from timeout/unresolved observations and disclose unexercised recovery branches; no forced live failure or timeout test is required.
* Decision route: Direct planner correction. The owner already resolved the policy; no user decision or additional deployment permission is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Employee signed-in acceptance lacks independent identity admission

* Related IDs: P03-T01, AC6, research readiness and the two-submission employee budget.
* Evidence: src/api/README.md:65-123 requires independently verified expected tenant tid and object oid before sign-in, never copied from observed /api/me, and strict boolean admission with identity rechecks before/after employee stages and at navigation/action boundaries. docs/reference/README.md records denied independent directory attestation and blocked employee acceptance. Current phase details proceed from named credentials to employee chat/capacity without this prerequisite or predicate.
* Concern: Correctly bounded password submissions and successful login do not prove that the authorized expected employee identity and effective role are exercising the UI. The plan neither resolves the known attestation gap nor stops before sign-in if it remains missing.
* Impact: The executor can consume the fresh finite budget while the identity prerequisite is still unavailable, or record employee acceptance for a wrong/stale session. Display email, roster membership or the observed account response cannot safely fill this gap.
* Smallest useful change: Add independently supplied expected tid/oid as a pre-sign-in prerequisite and integrate the canonical boolean identity binding into the fresh capture-free runner. Re-admit before and after chat/capacity navigation and before any submission. If attestation is unavailable or admission fails, mark employee checks blocked and do not submit credentials or act further. Do not add map/case journeys merely to use the existing wider adapter.
* Action owner: Planning parent for prerequisite/failure routing; owner or identity administrator supplies existing identity attestation if available; implementation executor enforces the predicate.
* Exact resolving evidence: Plan/details specify the independent attestation provenance, canonical checks.employee_identity_check binding, strict admitted boolean state and blocked-before-sign-in behavior. Later sanitized runner manifest/receipts bind that expectation without publishing IDs or credentials, account for actual sign-in submissions and record fresh admission at each scoped employee stage. Absence of attestation is an honest blocked receipt, not fabricated acceptance.
* Decision route: Direct planner correction. No user response is needed to revise or to proceed with the remaining deployment scope. Only successful employee acceptance depends on obtaining the missing independent attestation; no new directory permission or identity bypass is authorized.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Signed-in protected widget proof stops at HTTP 200

* Related IDs: P03-T01, AC5-AC6, cache8 RV-001 and current immutable-cache requirement.
* Evidence: Current phase details require employee actual chat widget assets200 and capacity page, while version/source/header assertions are attached to the retained anonymous public verifier. .copilot-tracking/reviews/logs/2026-10-31/demo-sites-redeploy-cache-review.md RV-001 identifies the precise outstanding protected-widget gap and its resolving evidence: actual current versioned widget JS/CSS200, delivered-byte/source bindings and cache headers, not merely packaged image bytes.
* Concern: A successful signed-in asset response does not prove the expected current asset was delivered or that protected widget caching has the required policy. Anonymous 401/302 and local packaged hashes cannot substitute for this missing authenticated evidence.
* Impact: The new signed-in phase could claim the prior employee widget/cache gap resolved despite observing stale bytes, a wrong asset version or missing max-age/immutable headers.
* Smallest useful change: In the already authorized signed-in context, assert the current source-derived widget JS/CSS URLs, HTTP200, delivered-byte equality to the pinned archive/image proof and exact max-age=31536000 plus immutable. Include no-store for the authenticated HTML shell where applicable. Export only status/header/hash booleans, not authenticated bodies or network dumps. Preserve anonymous denials and record any missing assertion as unmet.
* Action owner: Planning parent, then the authorized signed-in acceptance executor.
* Exact resolving evidence: Plan/details explicitly assign these protected assertions to the authenticated phase. Actual sanitized evidence later binds each widget resource/version, archive hash, delivered hash, HTTP status and cache-policy result to the same deployed digest/source pin, after PC-002 admission. A blocked signed-in phase leaves the protected-cache criterion unproven.
* Decision route: Direct planner correction within the requested bounded signed-in/cache verification; no source repair, access change or user decision is needed.

## Strengths and Residual Risk

* Owner authorization resolves the two-app deployment and short private-restored ACR window. Neither requires renewed approval merely because a critique is running.
* SQL source touches are correctly distinguished from an empty .sql-file diff. The reused initializer selects only the unique resident view batch, retains six existing idempotent sensor checks and counts-only receipts, and excludes authority/RBAC/new ledger changes. Read-only inspection confirmed its retry-only ownership restoration and unrelated-drift refusal; no broader job overwrite finding is warranted.
* Pre-publish concrete-subdirectory asset proof and local/live failure separation address the original local verifier bug. Signed-in acceptance failures are not rollback triggers.
* Private registry fallback feasibility, live convergence, resident authentication and employee attestation remain execution uncertainties. The plan permits blocked/unmet reporting and does not certify fallback, model, identity, safety, resident works consent or operational approval.
* Historical console counts remain disclosed residual diagnostics, not evidence of a current deployed defect or a reason to expand this task.
* Local evidence can be committed under existing authority. Push/PR remains blocked by the unresolved directions and by any missing complete current exact-head gate; partial local proofs, timeouts or a historical receipt cannot compensate for that gate.

## Questions or Blocking Evidence Gaps

* No user decision is required for these three direct planning revisions.
* Independent employee tid/oid attestation is an execution prerequisite, not established by the supplied planning evidence. Record employee acceptance blocked if it cannot be supplied independently.
* Publication authority remains unresolved. Only the owner can clarify the no-push/PR conflict; the planning parent must keep publication blocked until then and until all exact-head prerequisites pass.

## Limitations

* No cloud/configuration, deployed-image, database, browser, credential, scanner or test validation occurred. Historical successes were not treated as fresh proof.
* Retained executor inspection covered the specific transitive rollout and initializer paths needed to assess compatibility; it did not certify every helper or live failure branch.
* This is the complete actionable finding set for the supplied candidate boundary. Plan, details, research, historical reviews and current state were not modified. No implementation or nested review was launched.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Directly revise the current details to require timeout-safe inner and outer rollout adapters, then add PC-002 identity prerequisites and PC-003 protected-asset assertions. Record each PC disposition without changing this original verdict or requesting another critique.
* User response required: No for revision or bounded deployment continuation. Employee attestation is needed for that acceptance to pass; clear owner publication authority is required before any push/PR.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-31/demo-sites-redeploy-routing-plan.md](.copilot-tracking/plans/2026-10-31/demo-sites-redeploy-routing-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-31/demo-sites-redeploy-routing-phase-details.md](.copilot-tracking/details/2026-10-31/demo-sites-redeploy-routing-phase-details.md) | Assessed phase details |
| [.copilot-tracking/research/2026-10-31/demo-sites-redeploy-routing-research.md](.copilot-tracking/research/2026-10-31/demo-sites-redeploy-routing-research.md) | Supplied evidence pointer |
| [.copilot-tracking/reviews/plans/2026-10-31/demo-sites-redeploy-routing-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-31/demo-sites-redeploy-routing-plan-critique.md) | This single original critique |

## Next Steps

Active planning parent: apply and record direct dispositions for PC-001-PC-003, finalize without another critique, and retain the employee-attestation and publication blockers. No user action is required for planning revisions. No peer stage is invoked by this critic.
