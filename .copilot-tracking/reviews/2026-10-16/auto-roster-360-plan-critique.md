---
title: Automatic roster 360 final candidate plan critique
description: Single bounded assessment of the supplied automatic roster implementation candidate
ms.date: 2026-10-16
ms.topic: reference
---

## Metadata

* Task ID: auto-roster-360, Refs #360.
* Critique date: 2026-10-16.
* Plan: .copilot-tracking/plans/2026-10-16/auto-roster-360-plan.md
* Phase details: .copilot-tracking/details/2026-10-16/auto-roster-360-phase-details.md
* Critique execution status: Complete.
* Execution bound: exactly one final candidate critique; no implementation, delegation, live setup or Azure operations.

## Inputs and Criterion Boundary

* Assessed the complete supplied plan, phase details and .copilot-tracking/research/2026-10-16/auto-roster-360-research.md.
* Requirements are the owner's follow-up supplied in the critique request: generate only missing/exact-template private rosters using existing SQL `--list-staff`; case-insensitive `admin@` selection with one plain question or `--admin-upn`; admin on the first ProgrammeManager code; distinct seeded, persisted enabled human members on other existing codes; exclude guests, disabled accounts, rooms, shared mailboxes and service principals; preserve SQL roles and Contractor scope; stop with exact shortage; 0700/0600 privacy and no printed personal identifiers; summary and confirmation with `--yes`; read-only no writes; production refusal; continued Entra reconcile/check and SQL check/confirm/apply/restart. Delivery validation must remain offline.
* Relevant named source read only: infra/scripts/setup-entra.py, infra/scripts/initialize-workbench-staff.py, infra/main.bicep and targeted infra/README.md evidence. Repository entry documents were read for context, not used to invent new acceptance requirements.
* Assessed P01-T01 through P02-T03, stated decisions, preservation of existing rosters, profile/identity evidence, failure ordering, persisted format, test ownership and delivery boundaries.
* This is a planning credibility assessment, not implementation acceptance or an independent attestation of actual tenant people, Exchange recipients, deployed profiles, SQL state or restart success.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Missing/exact-template intake; populated invalid roster refusal | Covered | Plan Functional Requirements; P01-T01/T03 and P02-T01 preserve early validation and exact matching. |
| Authoritative SQL codes/roles and Contractor scope; C4/C5 | Partial | Existing candidate path and supplier retention are selected; immutable existing identity bindings are not included in generation/pre-mutation validation (PC-004). |
| Case-insensitive admin selection; none/many question; first ProgrammeManager | Partial | P01-T02 specifies selection and reservation, but not absent ProgrammeManager and invalid explicit-UPN failure behavior (PC-006). |
| Distinct enabled human members; all prohibited account classes | Partial | Guest/disabled checks and naming filters are credible negative checks, not positive human/shared-mailbox evidence (PC-001). |
| Stable seed, sorted inputs, exact shortage and persisted reuse | Partial | Algorithm and no insufficient-user writes are covered; shortage diagnostic contract and interoperable envelope require precision (PC-003, PC-006). |
| Demo/development context; production overrides naming; C8 | Partial | Required outcome is explicit, but resource-bound evidence resolution and conflicts are underspecified (PC-002). |
| Private 0700/0600, outside Git, atomic replacement, no symlinks | Covered | Plan Functional Requirements and P01-T02; P02-T01 explicitly owns privacy/permissions tests. |
| No printed IDs, UPNs or personal names | Partial | General prohibition conflicts with preserving `--admin-upn` in a printed fallback command (PC-005). |
| Summary, roster confirmation, `--yes`, SQL confirmation | Covered | Executive Summary, User Decisions and P01-T02/T03 preserve both confirmation boundaries; `--yes` accepts them. |
| Read-only no writes, lock refusal, Graph pagination | Covered | Plan Non-Functional Requirements and P01-T03/P02-T01; missing-file previews must not enter SQL with a nonexistent file. |
| Entra reconciliation/check before final SQL check/confirm/apply/restart | Covered | P01-T03 explicitly retains continuation ordering and honest final status. |
| Offline tests, docs, delivery, no live operations | Covered | P02-T01/T02/T03; no live setup or Azure writes permitted during delivery. |

## Verdict

* Verdict: Revise.
* Severity counts: Critical 0; High 4; Medium 2; Low 0.
* Rationale: The core approach is coherent, but the candidate does not yet define a supportable human-eligibility gate, deterministic profile provenance, or a safe response to existing immutable SQL identity bindings. Its fallback command also contradicts the privacy requirement. These are substantive implementation inputs, not cosmetic refinements.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Naming filters cannot establish the required human and mailbox eligibility

* Related IDs: P01-T01, P02-T01; research Risks and Residual Uncertainty.
* Evidence: Research explicitly says Graph has no universal human-person flag and resource/shared-mailbox naming is not Exchange recipient-type attestation. Phase details nevertheless propose a shared validator based on existing exclusions plus room/shared/service naming. infra/scripts/initialize-workbench-staff.py:93-103 checks Member/enabled, display name/UPN and `ConfRm`/desk/workspace patterns only.
* Concern: An enabled Member with an ordinary personal-looking name/UPN can still be a shared mailbox or non-human user account. Querying `/users` excludes service-principal objects but does not prove every returned user is human. A documentation caveat and negative naming fixtures do not satisfy the owner's categorical exclusion.
* Impact: Automatic random assignment can grant workbench roles to a prohibited account while tests report eligibility coverage.
* Smallest useful change: Separate negative filters from positive eligibility evidence. Specify an existing trusted human/recipient classification source and fail closed when it is absent or ambiguous; if none is available inside the supplied scope, explicitly block the automatic selection gate rather than describe naming-only selection as acceptance-ready. Do not add Exchange permissions or use `--yes` as implicit attestation.
* Action owner: Planning parent; owner only if a weaker eligibility policy or expanded evidence source is proposed.
* Exact resolving evidence: Revised P01-T01 names the available evidence source, returned classification fields, trust/availability limits and unknown-state behavior. P02-T01 includes a personal-looking enabled Member representing a shared mailbox/non-human account, a genuine eligible human, and absent evidence; prohibited/unknown cases stop before roster persistence or remote mutation. If no source is available, readiness explicitly records this gate as blocked.
* Decision route: Direct planner correction to preserve the explicit exclusion. Accepting naming-only eligibility or authorizing a materially new source would require an explicit owner decision; current instructions do not accept that divergence.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Profile evidence lacks an exact resource-binding and conflict-resolution contract

* Related IDs: P01-T02, P02-T01; research C8 and Q2.
* Evidence: Plan requests a profile tag and support for existing deployment parameters matched to the app/environment; details say evidence must bind to the selected app or managed environment. infra/main.bicep:82-84 defaults deploymentProfile to production, while :130-137 emits environment and non-production-purpose tags without deploymentProfile. infra/scripts/setup-entra.py:382-417 verifies app identity and direct environment linkage, not deployment profile.
* Concern: The candidate does not define the new tag key/propagation, the exact deployed parameter/output relationship proving ownership of the selected resource, handling of deployments omitting the production-default parameter, or precedence when app tags, environment tags and applicable deployments conflict. An unrelated or historical development deployment must not authorize a production resource merely because it shares a group/environment label.
* Impact: The central production prohibition could be implemented as an optimistic tag/history heuristic or could reject every existing untagged deployment without an actionable evidence explanation.
* Smallest useful change: Define a fail-closed evidence algorithm: authoritative tag name and resources, exact selected app/environment ID linkage for fallback deployment evidence, default/unknown interpretation, and refusal of contradictory applicable evidence. A direct-ingress or demo/test/dev label alone cannot establish development.
* Action owner: Planning parent.
* Exact resolving evidence: P01-T02 specifies the lookup/precedence rules and Bicep tag propagation target. P02-T01 adds fixtures for a bound development deployment, unrelated development deployment, stale/ambiguous evidence, omitted profile/default production, absent evidence, and app/environment production conflicts; every refused case proves no candidate SQL lookup, Graph candidate enumeration, roster write or auth mutation.
* Decision route: Direct planner correction. Production refusal is already an owner decision.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: The persisted envelope is not yet a concrete interoperable contract

* Related IDs: P01-T01/T02, P02-T01.
* Evidence: Plan specifies a “versioned private roster envelope with seed and staff array”; details say both readers support it and reject malformed versions. infra/scripts/setup-entra.py:486-520 and infra/scripts/initialize-workbench-staff.py:72-90 currently accept nonempty arrays with different normalization/validation paths.
* Concern: No exact version discriminator/key/value, seed type/range/default semantics, or concrete envelope shape is selected. Neither the shared decoding boundary nor treatment of missing/malformed seed/staff fields is defined. “Reject malformed versions” does not resolve valid-version malformed payloads, and the two command readers must agree on the same file without dropping role/supplier fields needed by the downstream reader.
* Impact: The generated file can work in setup yet fail in SQL continuation or reruns; different readers can interpret an invalid envelope differently.
* Smallest useful change: Pin one complete JSON envelope example using synthetic identifiers, its validation rules and legacy-array behavior. Assign shared envelope decoding or explicit cross-reader contract tests while retaining each reader's existing row safeguards.
* Action owner: Planning parent.
* Exact resolving evidence: P01-T01 contains exact keys, version value, supported seed representation, nonempty row schema and error behavior; P02-T01 tests the same generated envelope through both readers, Contractor preservation, legacy arrays, unknown versions, malformed seed/staff fields and persisted reuse despite later seed flags.
* Decision route: Direct planner correction; no owner decision needed for an internal compatible format.

<!-- rpi:critique id=PC-004 -->
### PC-004 [High]: Random selection ignores existing immutable SQL identity bindings

* Related IDs: P01-T01/T03, P02-T01; research C4 and immutable-binding trace.
* Evidence: infra/scripts/initialize-workbench-staff.py:154-185 requires full code coverage and rejects replacing a populated `old["oid"]`. Its existing :318-320 listing emits only code and role; the proposed extension adds Contractor scope only. P01-T02 shuffles directory people and P01-T03 retains the first full SQL check after Entra reconciliation.
* Concern: A missing local file does not prove SQL staff are unbound. With an already initialized database, the generated random identities can violate immutable bindings even though code, role and Contractor scope are correct. The candidate has no generation-time feasibility check for this state.
* Impact: Setup may persist an unusable roster and change Entra assignments before the final SQL check rejects it, leaving directory and SQL workbench access inconsistent.
* Smallest useful change: Define the already-bound SQL path explicitly. Extend the same private candidate/preflight contract enough to detect incompatible existing bindings before persistence and remote mutation; safely reuse compatible bindings if that preserves the owner algorithm, otherwise stop with a sanitized explanation. Do not weaken immutable-binding checks or invent another SQL source.
* Action owner: Planning parent.
* Exact resolving evidence: P01-T01/T03 defines bound/unbound candidate handling and the pre-mutation gate. P02-T01 tests a missing file with existing bound SQL rows, a conflicting reserved admin, and mixed bound/unbound rows; incompatible cases leave the roster and Entra untouched and do not expose stored identities.
* Decision route: Direct planner correction using fail-closed behavior. Rebinding SQL or relaxing distinct-person constraints is not authorized and would require an owner decision.

<!-- rpi:critique id=PC-005 -->
### PC-005 [High]: The printed private-host command can disclose the administrator UPN

* Related IDs: P01-T03, P02-T01; plan Non-Functional Requirements.
* Evidence: P01-T03 requires a shell-quoted exact setup command retaining “safe mode/profile/app/seed/admin options.” The owner explicitly prohibits printing UPNs; `--admin-upn` necessarily carries one. Shell quoting protects argument boundaries, not confidentiality.
* Concern: Retaining an explicit administrator UPN in the command output contradicts the privacy guarantee. Sanitized Graph errors alone do not cover this output path.
* Impact: Administrator identity can enter terminal recordings, CI logs or copied diagnostic output during the expected private-SQL connectivity failure.
* Smallest useful change: Define a runnable fallback that does not interpolate the private value: omit `--admin-upn` and use the existing plain-question path, or reference a privately supplied shell variable without expanding it into printed text. Preserve non-identifying selection/mode flags and explain the private input step.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P01-T03 includes a synthetic example of the exact privacy-safe command/input flow. P02-T01 exercises failure with a distinctive explicit UPN and checks stdout/stderr contain neither that UPN, directory IDs nor personal names, while verifying that the fallback retains safe mode and resource selection.
* Decision route: Direct planner correction; the privacy prohibition is already explicit.

<!-- rpi:critique id=PC-006 -->
### PC-006 [Medium]: Admin infeasibility and exact shortage outcomes need explicit acceptance cases

* Related IDs: P01-T02, P02-T01; owner admin and exact-shortage requirements.
* Evidence: Details reserve the first ProgrammeManager code and allow explicit UPN to resolve none/many; tests mention admin ambiguity and shortage counts. They do not state behavior when SQL has no ProgrammeManager position or an explicit answer resolves to an absent/ineligible identity, nor specify the exact shortage calculation.
* Concern: SQL is authoritative, so there is no legal fallback role/code when ProgrammeManager is absent. Admin selection also must not bypass the shared eligibility contract. The requested exact shortage should count distinct eligible remaining people after reserving the admin, not all Graph rows or pre-filter candidates.
* Impact: Implementation may invent a position, silently select another role/admin, prompt repeatedly, or report a misleading shortage.
* Smallest useful change: Specify a sanitized early stop for no ProgrammeManager code and invalid/ineligible explicit selection; clarify that one plain question collects one UPN and invalid input stops. Define required remaining positions, available distinct eligible non-admin people and deficit, with no identifiers in the summary.
* Action owner: Planning parent.
* Exact resolving evidence: P01-T02 states these terminal outcomes and the count formula. P02-T01 covers absent ProgrammeManager, mixed-case `ADMIN@`, absent/guest/disabled/non-human explicit admin, one invalid interactive answer, exactly enough people and exactly one short after admin reservation; failure assertions prove no persistence or remote mutation.
* Decision route: Direct planner correction. No owner question is needed because the supplied constraints already require stopping rather than inventing roles or weakening eligibility.

## Strengths and Residual Risk

* The candidate confines generation to missing/exact-template files, preserves legacy populated rosters and refuses shortage rather than reusing identities.
* It retains SQL roles/supplier scope, explicit confirmation, private atomic persistence, read-only previews, lock refusal, complete Graph pagination and the final Entra-to-SQL continuation.
* The production override and unknown-context refusal are correct policy choices; PC-002 concerns operational evidence precision, not a request to reconsider that policy.
* Seeded reproducibility, persistence over later seed flags and complete-coverage/distinct-user SQL checks are sound intended safeguards.
* Offline-only validation is appropriate for this delivery. Actual sign-in, live identity/recipient eligibility, SQL binding and restart remain Not run. That limitation cannot substitute for defining an enforceable eligibility contract before implementation.

## Questions or Blocking Evidence Gaps

* Positive human/recipient eligibility evidence is not supplied. The planning parent must identify an available trusted source or mark that generation gate blocked. Accepting naming-only classification would be a divergent owner decision, not a routine residual risk acceptance.
* No clarification is necessary to apply the existing production, privacy, immutable-binding or stop-on-shortage constraints.

## Limitations

* No external research, Graph/Exchange/Azure query, live setup, application test or implementation validation was performed or authorized.
* Source inspection was bounded to the named relevant infra trace. Existing functions are evidence of current behavior, not claims that the proposed implementation already exists.
* Plans, details and research remain unchanged. This artifact is the complete actionable finding set for this bounded pass; no additional critique pass is requested.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Resolve the positive-eligibility evidence gate, then revise P01-T01/T02/T03 and P02-T01 once to address PC-001 through PC-006 before implementation.
* User response required: No for direct corrections and fail-closed behavior. Yes only if the parent proposes a weaker eligibility rule or materially expanded authority/source; do not infer that approval.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-16/auto-roster-360-plan.md](.copilot-tracking/plans/2026-10-16/auto-roster-360-plan.md) | Assessed final candidate plan |
| [.copilot-tracking/details/2026-10-16/auto-roster-360-phase-details.md](.copilot-tracking/details/2026-10-16/auto-roster-360-phase-details.md) | Assessed task details |
| [.copilot-tracking/research/2026-10-16/auto-roster-360-research.md](.copilot-tracking/research/2026-10-16/auto-roster-360-research.md) | Supplied bounded research |
| [.copilot-tracking/reviews/2026-10-16/auto-roster-360-plan-critique.md](.copilot-tracking/reviews/2026-10-16/auto-roster-360-plan-critique.md) | Complete critique, verdict Revise |

## Next Steps

Return this verdict to the active planning parent for direct revision and finalization without another critique. Do not implement or perform live setup from this critique. No user action is required unless the parent requests an explicit divergent eligibility/evidence decision.
