---
title: Setup API selection implementation Review
description: One independent bounded implementation Review for issue 360
ms.date: 2026-10-17
---

## Scope and Evidence

* Task ID: 360/setup-api-selection-360
* Review date: 2026-10-17
* Review scope: New source commit f48cc9b4661f3375110a96b66829eb5678d32057 only, relative to its parent, on main d400eb8d1d0d6567445b0fc11803260eab897a65.
* Assessed boundary: API discovery, read-only staff transport safety, canonical setup/staff tests, directly related runbook and KB routing/log. No broad finance review.
* Plan: .copilot-tracking/plans/2026-10-17/setup-api-selection-360-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/setup-api-selection-360-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-17/setup-api-selection-360-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-17/setup-api-selection-360-changes.md
* Research: .copilot-tracking/research/2026-10-17/setup-api-selection-360-research.md

## Opening Review State

* Interpreted review goal: Independently assess the new selection and no-write implementation once, preserve historical ACR evidence and separate offline conformance from issue acceptance.
* Review scope: P01-T01 through P01-T03 and P02 readiness; publication remains parent-owned.
* Evidence readiness: Research, revised plan/details, one critique and implementation receipts are available; initial inspection confirms only setup integration tracking metadata was dirty.
* Acceptance basis: Unique eligible explicitly direct API selection, exact overrides, true ambiguity refusal, legacy preservation, no writes in check/dry-run/list-staff, PC-001 through PC-003 dispositions, and bounded regression coverage.
* First comparison boundary: Compare f48cc9b source/tests to accepted selection and central transport contracts, then inspect surrounding call paths and documentation.
* Active read-only boundaries: Only this canonical Review record may be written. No source edits, second reviewer, Azure calls, private data, SQL/Graph calls, image operations, dependency installation or remote publication.
* Initial blockers: None. Earlier stale progress prose is explicitly superseded by the final integration receipt and plan handoff.

## Execution Status

* Execution status: Complete.
* Review execution evidence: One local independent comparison of the full supplied new-task boundary. No nested reviewer, source correction, remote call or publication was performed.
* Implementation assessment: P01-T01 through P01-T03 complete on the reviewed source. P02-T01 concludes through this record and parent reconciliation; P02-T02 remains parent-owned publication.
* Integrated source: f48cc9b4661f3375110a96b66829eb5678d32057. Main d400eb8d1d0d6567445b0fc11803260eab897a65 is an ancestor, independently checked.

## Current Source Fingerprints

Independently calculated from current files; all match the supplied final candidate.

| Path | SHA256 |
| --- | --- |
| infra/scripts/setup-entra.py | 8cf36e2d01d19c8b94cca0dcda9f6105bcaf14471eead977dc3ed4e961f060bb |
| infra/tests/test_setup_entra.py | 9bf651ef1eab149b0e90a58a8e5823c6cd0a27570abf7a8bd98ea8558b16f9fb |
| infra/tests/test_staff_azure.py | 626a78dc1144cc3bed8cf23ac317daa937ee2f79ba6a85f4d74d4a8f78504c1f |

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Assessment |
| --- | --- | --- | --- |
| P01-T01; acceptance 1-3 | Red-first deployed pair, mixed ambiguity and transport failures recorded before implementation | Reconciled with canonical tests and final inventory | Five new methods, none removed; supplied red-first chronology is not independently re-executed |
| P01-T02; acceptance 1-2 | Existing explicit direct tag plus modern API role or absent-role legacy API workload | Reconciled with discover and canonical selection tests | Unique direct pool wins; mixed direct cardinality refuses before choose can prefer modern tags |
| P01-T02; acceptance 3 | Central azure_staff check/dry-run/list-staff guard | Reconciled with candidate_staff, sql_staff_step and setup | Guard precedes payload/Graph preparation and execute, including fallback; internal operation check remains available in mutating invocations |
| P01-T03; acceptance 4 | Combined 164 tests and scoped lint/types/format/compile before and after integration | Reconciled with supplied receipt and source identity | Reported passing validation is distinct from independently performed static checks |
| P01-T03; documentation | Runbook changes, KB route and additive log | Reconciled with actual behavior and retained history | Active Azure read-only transport advice removed; no live acceptance invented |
| P02-T01 | Final integrated handoff says review-ready, not already reviewed | Reconciled as input snapshot | Current record supplies the one new Review; parent updates its own markers afterward |
| P02-T02 | Publication pending | Pending parent lifecycle | No remote publication or final PR head claimed by this Review |
| Follow-Up Items | Runtime/operator acceptance, exact image smoke/pin and retirement | Reconciled and still outside active work | Routed separately below; #360 d/e remain unmet |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01/T02 | infra/scripts/setup-entra.py; infra/tests/test_setup_entra.py | Recognize the actual legacy-workload/direct pair without name/order inference | New pair test checks exact name, ID and FQDN in both orders; existing modern-direct tests retained | Parent setup suite 104 passed; independent static inspection | Conformant |
| P01-T01/T02 | Same source and setup tests | Refuse mixed direct ambiguity; retain exact override and legacy edge | Both mixed orders refuse; either exact target succeeds; explicit old and single legacy retain edge discovery; wrong exact name refuses | Existing environment/origin guards unchanged; no edge calls asserted for direct tests | Conformant |
| P01-T01/T02 | infra/scripts/setup-entra.py; infra/tests/test_staff_azure.py | Stop read-only cloud job/secret transport before request payload | Real wrapper exercised for three modes and three operations; listing and fallback assertions observe requests/writes, not only final cleanup | Independent isolated actual-function guard check: nine combinations passed | Conformant |
| P01-T03 | infra/tests/test_staff_azure.py | Adapt superseded Azure listing/check-success expectations without deleting expiry or mutation coverage | Explicit Azure and local failure/timeout check cases; baseline credential bytes, counts, write/tag/request snapshots retained | Parent staff suite 43 passed; existing mutation check/apply/restart sequence retained | Conformant |
| P01-T03 | infra/README.md; docs/reference/README.md; docs/reference/log.md | Explain compatible selector and private-host read-only handoff | Scoped diff is consistent with implementation and does not upgrade historical acceptance | Diff whitespace and main-log prefix independently passed | Conformant |

Per-resource role authority excludes a conflicting modern role from the new direct pool. Generic legacy/name selection outside that pool remains unchanged, as required; this Review does not assert a new global role-filter contract. Exact overrides bypass preference, not the subsequent subscription/resource-group, ingress/environment and origin safety checks.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01/T02/T03 | Include list-staff in no-write transport predicate and adapt listing tests | PC-001; already-confirmed no-cloud-writes requirement | Current requirements, acceptance 3, phase details, tests and runbook agree | Accepted direct correction, no divergent decision | Reconciled |
| P01-T01/T02 | Direct-pool cardinality precedes generic chooser | PC-002; true ambiguity refusal already required | Plan distinguishes per-resource role authority from global candidate priority; implementation and mixed-order tests agree | Accepted direct correction | Reconciled |
| P01-T01/T03 | Existing reusable-credential Azure check now incomplete, not successful SQL verification | PC-003; cloud transport prohibited even for valid reusable credentials | Existing generated/legacy expiry cases retain original credential bytes and later mutation reuse/rotation expectations | Accepted direct correction | Reconciled |
| P01-T03 | Dependency/tool recovery after recorded missing-import/tool failures | Changes record; pip-only worktree-local constraint | Final checks identify local tools and no new production dependency | Compatible execution detail, not scope expansion | Supplied evidence accepted; no installation by reviewer |
| P02 handoff | Integrate advanced main d400eb8; preserve upstream log and owned history | Supplied authorized integration; no selected-source conflict | Current plan handoff, final changes receipt and state identify f48cc9b and repeated checks | No renewed functional design or second critique needed | Reconciled |

Earlier changes headings retain historical phrases such as "P01-T01 active" and "Green validation pending"; the later dated integration/completion receipt and current state explicitly supersede them. Phase details retain the initial bbbc924 intake observation and conditional integration instructions, not a contradictory claim that d400eb8 integration is absent. These are understandable execution history, not a material evidence gap. The parent should now reconcile P02 status to this persisted Review without rewriting earlier receipts.

## Critique and Material Revision Assessment

* Exactly one new-task critique is present. PC-001 High, PC-002 High and PC-003 Medium are accepted and substantively resolved in current plan/details and implementation.
* PC-001: list-staff now fails before payload/execute; both existing Azure-listing/fallback tests assert no attempted requests/writes/tag writes. Existing local listing success coverage remains.
* PC-002: direct candidate cardinality includes both modern and compatible legacy resources; both orders and exact overrides are covered.
* PC-003: the existing generated/legacy expiry test changes only overall read-only completion expectations and strengthens preservation assertions; mutation-mode reuse/rotation remains.
* No significant divergent decision, invalid planning assumption or evidence of dependent work proceeding through an unresolved critique gate was found. Chronology is assessed from supplied records, not reconstructed from live systems.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Real operator setup and runtime acceptance | Explicitly excluded from offline selection/safety task; no authority for live setup | Owner/operator arranges separately authorized real tenant/browser/role/SQL/AI verification | Open residual RV-001 |
| Exact image smoke/pin | Historical ACR result remains separate and unaccepted; this source change is not publication | Existing image-delivery owner preserves exact source/run/digest gate before any pin | Open residual RV-002 |
| Old-edge retirement | Requires separate explicit owner authorization and relevant acceptance | Owner decides only after acceptance; retain current old API/edge/services | Open residual RV-003 |

Unresolved follow-ups are not implementation defects or additions to active P01/P02 acceptance scope.

## Findings

Complete finding set: no implementation defect, unresolved significant decision or material evidence gap was identified in the supplied new-source boundary. Severity summary: 0 Critical, 0 High, 2 Medium residuals, 1 Low residual. No correction cycle is requested.

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Real operator and deployed acceptance remain unproved

* Related scope: Plan Follow-Up Items; acceptance 3-4 evidence boundary.
* Evidence: .copilot-tracking/changes/2026-10-17/setup-api-selection-360-changes.md records only offline setup/staff/legacy regressions and expressly excludes live setup, SQL/Graph writes, browser/AI acceptance and restart. infra/README.md preserves incomplete/private-host handoff language.
* Impact: Correct offline discovery and refusal behavior do not establish laptop end-to-end success, tenant/browser/role behavior, actual private SQL binding/restart or AI acceptance. Issue #360 d/e cannot be closed.
* Destination: Distinct follow-up, owner/operator; not rpi-implement.
* Smallest useful next action: Preserve unmet acceptance and obtain a separately authorized operator/environment acceptance window; do not execute setup or infer acceptance from this Review.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Image/publication/runtime identity gates remain outside this source Review

* Related scope: Plan Follow-Up Items and historical initializer-acr-cli-360 evidence.
* Evidence: Original .copilot-tracking/reviews/logs/2026-10-17/initializer-acr-cli-360-review.md and command receipt remain byte-identical to pre-task d11c273. The new task supplies no exact hosted-image smoke, digest/pin or initializer execution proof.
* Impact: This selection Review must not replace or upgrade the original ACR Review, its residual result, or image/publication/runtime acceptance.
* Destination: Distinct existing image-delivery follow-up, owner/operator.
* Smallest useful next action: Keep original receipt/Review unchanged; apply the existing separately authorized exact-image acceptance gate before any later pin or runtime claim.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Retained old API and edge still require a later retirement decision

* Related scope: Plan Follow-Up Items; exact old-API override preservation.
* Evidence: infra/tests/test_setup_entra.py retains deliberate old-target/Front Door selection; plan and runbook explicitly preserve existing services and prohibit retirement in this task.
* Impact: Coexistence support is intentional, not evidence that old infrastructure can be removed.
* Destination: Distinct follow-up, owner.
* Smallest useful next action: Retain old resources until relevant acceptance and explicit retirement authorization; do not add teardown to this implementation.

## Defects

* None identified. No rpi-implement correction, source edit or second Review is requested.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | Distinct live acceptance follow-up | Owner/operator obtains explicit authority and acceptance context | Excluded live/human acceptance, not a source defect |
| RV-002 | Existing image-delivery follow-up | Owner/operator preserves exact-image gate and original evidence | No image/publication/runtime proof in this task |
| RV-003 | Distinct retirement follow-up | Owner decides after acceptance and separate approval | Deliberately retained infrastructure |

Later implementation of any actual routed defect would not require another Review; no such defect is found here.

## Residual Work

* RV-001 through RV-003 remain open outside active implementation. Ordinary source publication remains the parent's existing P02-T02 lifecycle task, not an implementation finding.

## Blockers and Remaining Work

* Review blockers: None.
* Remaining active implementation: None identified for P01.
* Parent lifecycle: Reconcile this one Review into setup task metadata, then complete authorized privacy-safe commit/push/PR #385 head reporting. This Review does not attest publication.
* Acceptance blockers/residuals: Image identity/publication/runtime, real tenant/browser/SQL/AI behavior and retirement remain separate; #360 d/e remain unmet.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| Parent receipt: ../../.venv/bin/python -m unittest test_setup_entra test_staff_azure test_initialize_api_auth -q, from infra/tests | Full relevant offline suites | Passed, supplied evidence | 164 tests: 104 setup, 43 staff, 17 legacy; reported twice including after integration |
| Parent scoped Ruff F setup/source/test, full staff E/F/I/B/UP lint and format, mypy --follow-imports=silent --ignore-missing-imports infra/scripts/setup-entra.py, compile | Changed executable scope | Passed, supplied evidence | No claim these were independently rerun |
| .venv/bin/python -B, AST inventory comparing current files with f48cc9b parent | Canonical test ownership | Passed independently | Exactly 3 setup plus 2 staff new methods, 0 removals; legacy unchanged; 164 total test methods |
| .venv/bin/python -B, compile(text, path, "exec") | Three changed Python files | Passed independently | In-memory syntax compilation; no bytecode or scratch files |
| .venv/bin/python -B, extracted actual azure_staff function with only guard globals | Check/dry-run/list-staff x candidates/check/apply | Passed independently | Nine combinations raise StaffJobError before unavailable payload/Graph/execute globals; isolated function validation, not full setup integration |
| sha256sum on three reviewed Python files | Final reviewed source | Passed independently | Matches all three caller fingerprints |
| .venv/bin/python -B, byte comparison of eight initializer-acr-cli-360 artifacts against d11c273 | Original ACR evidence preservation | Passed independently | Research, plan, details, critique, changes, command receipt, state and original Review all byte-identical |
| In-memory main-log prefix comparison against d400eb8 | KB additive history | Passed independently | Full main log is exact prefix; new owned history retained |
| git diff --check f48cc9b^ f48cc9b; git diff --check; git merge-base --is-ancestor d400eb8 HEAD | Diff hygiene and integration ancestry | Passed independently | No whitespace failures; current source includes required main |
| Independent full suite/lint/mypy rerun | Dynamic integration regression | Skipped | Parent supplied two matching final-source runs; Review's canonical-file-only write boundary excludes test scratch/bytecode writes. No package installation or dependency change |
| Azure, SQL, Graph, image/runtime/browser/AI or private-data checks | Live acceptance | Skipped, prohibited | Not authorized; no corresponding acceptance claim |

The supplied red-first receipt is retained as recorded evidence, not presented as a new red execution by this reviewer. No source mutation, Azure command, SQL/Graph request, private input read, job execution, payload logging or package installation occurred.

## Outcome

* Outcome: Residual work.
* Outcome rationale: Reviewed selection and central read-only transport implementation are conformant within the accepted offline boundary, with no identified source defects. The plan's separate live acceptance, image and retirement follow-ups remain open. Complete Review execution is not issue completion or image/runtime acceptance.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No correction requested |
| Decision gap or invalid assumption | None | No replanning requested |
| Material evidence gap | None within reviewed source boundary | No research handoff needed |
| Non-blocking residual work | Distinct RV-001/RV-002/RV-003 follow-ups | Owner/operator retains unmet acceptance and separate authority |

* Execution status: Complete.
* Outcome: Residual work; source implementation conformant.
* Validation coverage: Parent's 164 offline regression passes and scoped tools assessed; independent syntax, nine isolated guard combinations, test inventory, fingerprints, ancestry, whitespace and historical-byte preservation passed.
* Blockers: None to this Review; broader acceptance remains unmet.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-17/setup-api-selection-360-research.md](.copilot-tracking/research/2026-10-17/setup-api-selection-360-research.md) | Bounded metadata and safety research |
| [.copilot-tracking/plans/2026-10-17/setup-api-selection-360-plan.md](.copilot-tracking/plans/2026-10-17/setup-api-selection-360-plan.md) | Revised accepted plan |
| [.copilot-tracking/details/2026-10-17/setup-api-selection-360-phase-details.md](.copilot-tracking/details/2026-10-17/setup-api-selection-360-phase-details.md) | Phase contracts and review/publication boundaries |
| [.copilot-tracking/reviews/plans/2026-10-17/setup-api-selection-360-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-17/setup-api-selection-360-plan-critique.md) | One critique, PC-001 through PC-003 resolved |
| [.copilot-tracking/changes/2026-10-17/setup-api-selection-360-changes.md](.copilot-tracking/changes/2026-10-17/setup-api-selection-360-changes.md) | Red-first, regression and integration receipts |
| [.copilot-tracking/reviews/logs/2026-10-17/setup-api-selection-360-review.md](.copilot-tracking/reviews/logs/2026-10-17/setup-api-selection-360-review.md) | This one independent implementation Review |

## Next Steps

Parent reconciles this persisted Review and completes the existing authorized P02-T02 publication lifecycle. No correction or second reviewer is requested. Keep RV-001 through RV-003 as distinct owner/operator follow-ups; preserve original ACR evidence and leave #360 d/e unmet. No user action is required for the bounded source Review.
