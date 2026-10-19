<!-- markdownlint-disable-file -->
# Review: issue360-rg-loop

## Scope and Evidence

* Task ID: #360, issue360-rg-loop.
* Review date: 2026-10-19.
* Review scope: One original postimplementation Review, including supplied source, tracked diff, untracked implementation and dated RPI artifacts.
* Assessed boundary: Undeployed private publisher candidate, infra tests, documentation and sanitized live evidence; full live objective assessed separately from candidate execution.
* Base: 634a024d97d2da7168b8a7d5f343ab26e6108cf3.
* Branch: fix/demo-private-publisher-360.
* Plan: .copilot-tracking/plans/2026-10-19/issue360-rg-loop-plan.md
* Phase details: .copilot-tracking/details/2026-10-19/issue360-rg-loop-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-10-19/issue360-rg-loop-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-19/issue360-rg-loop-changes.md
* Other evidence: Research, session state, sanitized live receipt and known operator-produced evidence only.

## Opening Review State

* Interpreted review goal: Assess substantive implementation bugs, evidence consistency, critique dispositions and unfulfilled acceptance without fixing or rerunning this Review.
* Review scope: Complete supplied #360 boundary; distinguish bounded implementation completion from blocked live outcome.
* Evidence readiness: Branch and tracked/untracked boundary identified; dated research, plan, details, original critique, changes, receipt and state located. Detailed comparison pending.
* Acceptance basis: Current plan requirements and markers, preserved original critique and dispositions, owner authorization and explicit non-acceptance of blocked live objectives.
* First comparison boundary: Read the complete dated artifact set, then compare actual Bicep, tests and documentation diff with stated scope and validation evidence.
* Active read-only boundaries: Only this canonical Review record may change. No source changes, cloud writes, subagents or private-data discovery. No external raw IDs/payloads copied.
* Initial blockers: Both authorized provider preflights reportedly failed capacity; no allocation, role grant, build/upload/digest/pin, SQL/AI/browser acceptance or complete local gate. These block acceptance, not necessarily this evidence review.

## Execution Status

* Execution status: Complete.
* Review execution evidence: This is the one original Review. Compared all seven dated artifacts, the complete tracked documentation diff against the supplied base, both untracked source files, and relevant existing guard/IAM/gate contracts. No subagents, source changes, cloud operations or test reruns.
* Implementation execution status: Partial for P01-P03. P01-T01, P02-T03, P03-T01 and P03-T02 have bounded completion evidence; P01-T02, P02-T01 and P02-T02 remain blocked. P03-T03's Review is now complete, but its final commit/full gate/handoff remain pending. Complete Review execution does not mean complete implementation or accepted live outcome.
* Inspected HEAD: 634a024d97d2da7168b8a7d5f343ab26e6108cf3, with the supplied implementation still modified/untracked. This is not a frozen candidate approval.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Canonical template and compiled tests; passing focused runs | Partial | Actual source matches bounded VM direction, but connection/guard regression coverage is incomplete: RV-001. |
| P01-T02 | Two exact provider-capacity refusals; no successful what-if/allocation | Reconciled | Unchecked marker is correct. Unrestricted SKU/quota is not successful allocation: RV-002. |
| P02-T01/T02 | No build/upload/publication/digest verification/pin | Reconciled | Dependent work is blocked, not silently completed. Existing digests are retained historical/current observations, not fresh proof. |
| P02-T03 | Four direct403 results and failed Graph application-read | Reconciled | Bounded probes executed; no browser/role/SQL/AI acceptance: RV-003. |
| P03-T01 | Zero owned resources and unchanged baselines | Reconciled within supplied receipt boundary | No-allocation verification, not execution of a resource-deletion or watchdog test. |
| P03-T02 | Existing runbook, ADR, evidence, KB index and append-only log | Reconciled | Documentation accurately retains adverse results, undeployed status and #360d/e unmet. |
| P03-T03 | One original Review before final commit/full gate | Pending by design | No full-gate receipt exists yet. This is later publication work, not evidence of a failed gate. |
| Follow-Up Items | Capacity, #349, #358, #350/model/human boundaries | Reconciled | Capacity and tenant prerequisites also block the unfinished active live path; follow-up prose cannot remove them from acceptance. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | infra/private-proof-publisher.bicep | Standalone exact-group guarded VM, fixed researched D2as_v5/Jammy, dedicated child subnet/NSG, explicit public-IP outbound, no IAM/backing mutation | Complete untracked source read | Native Bicep/focused pass reported in changes | No concrete deployment-resource bug identified by inspection; not allocatable/live proof. |
| P01-T01 | infra/tests/test_private_proof_publisher.py | Four compiled-template tests | Complete untracked source read | Included in reported focused/full infra runs | RV-001 identifies a material blind spot despite passing tests. |
| P02-T03/P03-T01 | .copilot-tracking/changes/2026-10-19/issue360-rg-loop-live-receipt.json | Sanitized actual failed-capacity, restriction and preservation observations | Local receipt read and compared with changes/docs/state | Underlying private primary files not independently inspected here | Statements are mutually consistent; direct observation is not independently re-established. |
| P03-T02 | infra/README.md; docs/adrs/0002-pilot-readiness-architecture.md; docs/architecture/cutover-evidence-pack.md | Dated candidate, provider failures, limits and acceptance delta | Full base diff read | git diff --check passed | No success substitution; no claim of SQL/private-data reads or backing relaxation. |
| P03-T02 | docs/reference/README.md; docs/reference/log.md | Existing KB routing plus appended dated entry | Full base diff read | Index links inspected against existing paths/headings | Earlier log entries remain unchanged in the diff; no memory/original case change. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T02 | B2als_v2 changed to already researched D2as_v5, then stopped | First exact preflight failed capacity; second failed similarly. Owner permits bounded resources but not speculative escalation | Current Bicep/test size, details, plan status, changes, receipt and docs agree | Existing direction covers researched fallback; no new architecture or larger-size authorization inferred | Justified bounded fallback, not a newly proven viable route. Original research retains its historical B2als_v2 selection. |
| P01-T01/T02; PC-002/004 | IAM removed from Bicep; registry-only assignment staged after actual MI readback | Original all-Bicep IAM parser incompatibility | No IAM resource in actual template; existing parser/matrix untouched | Direct compatible disposition, not a repeated critique | Simplification is supported. It does not test a future external CLI assignment or expanded preview allowlist. |
| P02-T02; PC-001 | Fresh baseline, host-local serialization, error readback and conditional image-only rollback | Original failed-pin/concurrency concern | Current plan/details define stop on unrelated drift | Original Revise retained | Adequate described contract; unexecuted because no image was published. Host lock is not distributed exclusion. |
| P01-T02/P03-T01; PC-003 | Prewrite inventory, absolute deadline, timeout/finally and hard-interruption recovery | Original interrupted-allocation concern | Plan/details agree on operator responsibility and poweroff limitations | Direct disposition retained | No allocation means no watchdog/cleanup lifetime demonstration. Do not infer one. |
| P03-T03; PC-005 | Fresh-main equality, frozen candidate and exact receipt verification | Original stale-base/toolchain concern | Plan/details defer full gate until after Review and commit | Original finding and direct disposition retained | Gate contract is described, not executed. Temporary-path commands in historical artifacts do not override this review environment's file-operation restrictions. |
| All phase markers | Blocked live work and completed bounded evidence recorded | Actual capacity refusals and limited probes | Final status, markers, changes, docs and state agree | No re-critique performed | Changes' opening historical “Active P01-T02” is superseded by its later explicit final blocker/handoff, not treated as current completion. |

## Critique and Material Revision Assessment

* Original critique verdict remains Revise: four High and one Medium PC finding. It is not converted to approval by this Review.
* PC-001: Contract disposition supported; activation/recovery behavior unexecuted.
* PC-002: Exact-target guard and operator preview/inventory contract supported. Claimed negative authorization/security test coverage is not fully present; RV-001 records the concrete source-test gap. No successful expanded what-if exists.
* PC-003: Contract disposition supported; no-allocation inventory is not proof of interruption recovery or billing termination.
* PC-004: Separating runtime CLI assignment from no-IAM Bicep avoids the inspected parser incompatibility without excluding a template or altering the runtime role matrix. Future assignment validation remains an operator gate, not static-parser coverage.
* PC-005: Main/HEAD/receipt freshness contract is present; actual final gate is pending. Do not inherit a prior receipt or claim approved tools/paths solely from disposition prose.
* Material revisions: The researched same-region two-core fallback and no-IAM staging preserve confirmed owner intent. No unaccepted subscription/tenant authority, public-backing bypass, speculative larger allocation or production architecture replacement is introduced by the actual diff.
* Dependent-work pause: Publication/pin stopped at capacity failure. No evidence that affected dependent cloud work resumed early.
* Justification: Supported for bounded source/documentation decisions; not evidence of full source-release conformance or live acceptance.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate completed scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Actual publisher capacity or verified existing private publisher | Neither preflight succeeded; no viable execution route proven | Authorized infrastructure operator obtains successful exact preflight or verifies an existing private-connected publisher | RV-002; distinct capacity-resolution follow-up. P01-T02/P02 remain active blocked scope, not completed by deferral. |
| #349 tenant/staff/interactive acceptance | RG authority supplies neither tenant permissions nor an authorized browser session | Authorized tenant operator establishes registration/consent/private credential/staff, then human-backed acceptance | RV-003; existing #349 dependency, not a new source implementation task. |
| #358 real Key Vault preservation round-trip | Separate sequenced shared-path work; no pin/round-trip here | #358 owner continues after this branch at an authorized boundary | Remains distinct follow-up; not a defect or active completion claim. |
| #350 parity and model/human approvals | Outside this bounded publisher loop | Existing issue and named approval owners | Retain separately; no new task scope or approval inferred. |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Compiled safety tests do not verify the connections that enforce the boundary

* Related scope: P01-T01; acceptance 1; PC-002 disposition.
* Evidence: infra/tests/test_private_proof_publisher.py:38-46 checks expression substrings and only nonempty dependsOn, not the exact guard dependency or refusal branch. Lines48-63 inspect the NSG and subnet separately but never assert subnet.properties.networkSecurityGroup.id, NIC subnet reference, VM NIC reference, or the exact existing-VNet child target. The module contains only four positive shape checks despite the plan's negative-input-guard commitment. The actual Bicep currently wires these resources correctly.
* Impact: Removing the subnet's NSG attachment, pointing the NIC at a different subnet, or replacing a guard dependency with an unrelated dependency can leave these safety tests passing while the promised isolation/exact-target contract no longer holds. Presence of a deny rule in an unattached NSG is not enforcement. This is a regression-test implementation defect, not a claim that the current undeployed VM has exposed anything.
* Destination: rpi-implement.
* Smallest useful next action: Strengthen the existing single test module to assert exact compiled relationships and guard/refusal semantics, with bounded negative/mutated fixtures proving detached/wrong-target/unguarded variants fail. Keep external preview/assignment checks explicitly operator-owned unless an actual validator is delivered; do not claim they were exercised. No source correction is made by this Review.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: Private publication and initializer activation remain unexecuted

* Related scope: P01-T02, P02-T01/T02; acceptance 1-5; #360 technical publication objective.
* Evidence: .copilot-tracking/changes/2026-10-19/issue360-rg-loop-live-receipt.json records both B2als_v2 and D2as_v5 capacity refusals, successful_what_if false, deployment_create_invoked false, image_published false and digest_pull_run_verified false. Plan markers remain unchecked. Changes and all five documentation deltas preserve these facts.
* Impact: No publisher allocation, private endpoint reachability, source upload/build, manifest/runtime smoke, pushed digest pull/run, image-only pin or actual cleanup/recovery is established. Available quota and unrestricted SKU metadata cannot close this gap. The undeployed candidate is not a working source-bound publication route.
* Destination: Distinct capacity-resolution follow-up owned by the authorized infrastructure operator/coordinator; resume the existing blocked implementation only after its prerequisite is established.
* Smallest useful next action: Obtain actual capacity for the bounded researched route or verify an existing connected publisher. Then execute the already required exact preview/runtime/preservation checks with fresh evidence. No speculative larger sizes, public bypass, invented receipt or automatic new approval.

<!-- rpi:review id=RV-003 -->
### RV-003 [High]: Direct live acceptance and verification-before-retirement remain unmet

* Related scope: P02-T03; acceptance 6; #360d/e; #349 dependency.
* Evidence: .copilot-tracking/changes/2026-10-19/issue360-rg-loop-live-receipt.json records four direct403 responses, no Graph roles/delegated scopes, failed application-read, real_browser_role_sql_ai_acceptance “Not run”, frontdoor_retired false and resource_group_preserved true. docs/architecture/cutover-evidence-pack.md explicitly marks #360d/e UNMET.
* Impact: Restriction evidence is not health200, a real authorized role session, SQL persistence or task-bound real AI acceptance. #360 cannot be closed or Front Door retired on this record. Preserving the old stack is correct while these prerequisites are missing.
* Destination: Distinct existing #349 tenant/human acceptance follow-up, then the authorized #360 acceptance owner; not a new code defect or inferred tenant grant.
* Smallest useful next action: Authorized tenant operator supplies approved registration/permissions/consent/private credential/staff, followed by genuine permitted browser/role/SQL/AI checks after technical prerequisites. Keep RG, Front Door and private backing intact meanwhile.

## Defects

* RV-001: Test-contract defect routed to a later rpi-implement invocation.
* No additional concrete current-template functional bug established by this bounded source inspection.
* RV-002/RV-003 are known incomplete outcome/dependency work, not manufactured code defects.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | rpi-implement | Implementation owner strengthens compiled relationship and negative guard tests | Existing accepted safety direction; no new architecture decision required. |
| RV-002 | Distinct capacity-resolution follow-up | Infrastructure operator/coordinator establishes an actually viable bounded private publisher | Known technical blocker, not lack of resource authority or grounds for size escalation. |
| RV-003 | Existing #349 acceptance follow-up | Tenant operator and authorized human acceptance owner | Tenant/credential/session/live evidence cannot be supplied by static tests or RG authority. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Coordinator must freeze the final implementation plus original dated RPI evidence in a clean commit, then actually run all17 local gate groups, fetch main, verify the fresh external receipt and independently assess exact HEAD/base/receipt before any push/PR.
* That required sequencing was explicitly deferred until after this Review; its absence now is not a fabricated test failure or a new implementation defect.
* Retain #358 and #350/model/human work as distinct follow-ups; do not silently add them to this source change or mark them accepted.

## Blockers and Remaining Work

* Both actual provider preflights failed capacity. P01-T02 and P02-T01/T02 remain blocked.
* Tenant prerequisites and genuine direct acceptance remain outstanding. Do not read unknown SQL/application/private data to work around them.
* P03-T03 remains unfinished after its Review substep until the final clean commit and full verified gate exist.
* Primary-evidence limitation: Known operator evidence was supplied at external temporary paths. This review environment forbids temporary-directory file operations; none of those files were opened, copied or mutated. The assessment uses the committed-candidate sanitized receipt, detailed changes and caller-supplied actual results. The coordinator must independently compare the known primary files in an authorized context; this Review does not certify their bytes, raw failure details, test logs or private inventory.
* No Azure profile, environment file, private dataset, raw identifier/payload or unknown operator file was accessed. No cloud operation was performed.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| git diff --check 634a024d97d2da7168b8a7d5f343ab26e6108cf3 | Tracked patch | Passed in Review | No whitespace errors. Does not validate untracked content or runtime behavior. |
| Full tracked diff plus direct reads of both untracked source files and dated artifacts | Supplied implementation boundary | Completed in Review | Reviewed current source, not only tracked diff. No independent live state or compile execution implied. |
| Native Bicep build and focused publisher/proof/IAM/setup/staff/auth selectors | Candidate before cloud operations | Passed as supplied; not rerun | 233 tests, zero skips, per changes/caller. Original failed compile/dependency attempts retained externally. |
| Complete infra unittest discovery | All infra tests | Passed as supplied; not rerun | 363 tests, zero skips, after restoring existing pinned PyYAML6.0.3. Primary logs not read here. |
| B2als_v2 and D2as_v5 exact provider preflights | Actual allocation gate | Failed as supplied | SkuNotAvailable/capacity despite unrestricted SKU/quota; no successful what-if or allocation. |
| Four-route HTTPS and bounded Graph probe | Available live restriction/credential checks | Executed as supplied; acceptance failed/unavailable | Each403; application-read failed; no roles/scopes. No real session acceptance. |
| Final management preservation readback | Existing resources/private backing | Passed as supplied | Zero owned resources, unchanged subnet/registry baselines and Disabled backing access. No deletion/cleanup runtime proved. |
| Publication, digest pull/run, image pin, watchdog and deletion recovery | Dependent cloud runtime | Not run | Capacity blocker; no success inferred from static source. |
| Real browser/role/SQL/AI acceptance | #360d/e | Not run | Technical/tenant/credential/human prerequisites missing; no unknown-data workaround. |
| tools/rpi-checks.py --all and --verify-receipt | Frozen final candidate/full17 groups | Not run yet | Owner-prescribed later step after Review and final clean commit. No historical receipt substituted. |

## Outcome

* Outcome: Not accepted for the full #360/live objective and full source release.
* Bounded candidate assessment: Useful source/documentation execution with a Medium test defect and residual blocked live work. Not labeled Conformant.
* Severity summary: 0 Critical, 2 High known acceptance/dependency gaps, 1 Medium test-contract defect, 0 Low.
* Outcome rationale: Honest bounded documentation and reported passing local infra tests do not supply a viable publisher, fresh source-bound image, preserved initializer activation, live role/SQL/AI acceptance or final release gate. No evidence contradiction justifies replacing the recorded preflight failures with SKU/quota success.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | rpi-implement, RV-001 | Strengthen the single compiled safety test module. |
| Decision gap or invalid assumption | None newly established | Current fallback/staging remain within confirmed intent; any future alternative requires its own scoped decision. |
| Material evidence gap | No new rpi-research route | Known failed execution is not relabeled missing research. Underlying external evidence verification belongs to coordinator handoff. |
| Residual/dependency work | RV-002 capacity; RV-003 #349; separate #358/#350; final publication gate | Preserve distinct owners and blockers without expanding accepted active scope. |

* Review execution status: Complete.
* Implementation execution status: Partial.
* Outcome: Not accepted.
* Validation coverage: Source/artifact comparison and diff whitespace checked here; reported233/363 zero-skip infra passes, failed actual capacity/restriction evidence; no live acceptance or full17 gate.
* Approval boundary: Parent/coordinator alone owns continuation, final clean freeze/full receipt and independent exact-head/base assessment. This Review authorizes no source fixes, cloud writes, push, PR, merge or approval.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-19/issue360-rg-loop-research.md](.copilot-tracking/research/2026-10-19/issue360-rg-loop-research.md) | Original research and dated selection limits |
| [.copilot-tracking/plans/2026-10-19/issue360-rg-loop-plan.md](.copilot-tracking/plans/2026-10-19/issue360-rg-loop-plan.md) | Current plan, markers, direct dispositions and follow-ups |
| [.copilot-tracking/details/2026-10-19/issue360-rg-loop-phase-details.md](.copilot-tracking/details/2026-10-19/issue360-rg-loop-phase-details.md) | Current task contracts and blocked execution |
| [.copilot-tracking/reviews/2026-10-19/issue360-rg-loop-plan-critique.md](.copilot-tracking/reviews/2026-10-19/issue360-rg-loop-plan-critique.md) | Preserved original Revise verdict |
| [.copilot-tracking/changes/2026-10-19/issue360-rg-loop-changes.md](.copilot-tracking/changes/2026-10-19/issue360-rg-loop-changes.md) | Ordered implementation and supplied validation evidence |
| [.copilot-tracking/changes/2026-10-19/issue360-rg-loop-live-receipt.json](.copilot-tracking/changes/2026-10-19/issue360-rg-loop-live-receipt.json) | Sanitized live observations |
| [.copilot-tracking/rpi-sessions/2026-10-19/issue360-rg-loop-state.json](.copilot-tracking/rpi-sessions/2026-10-19/issue360-rg-loop-state.json) | Parent-owned state at Review entry; intentionally not mutated |
| [infra/private-proof-publisher.bicep](infra/private-proof-publisher.bicep) | Undeployed candidate source |
| [infra/tests/test_private_proof_publisher.py](infra/tests/test_private_proof_publisher.py) | Compiled tests and RV-001 evidence |
| [infra/README.md](infra/README.md) | Dated operator runbook and limitations |
| [docs/adrs/0002-pilot-readiness-architecture.md](docs/adrs/0002-pilot-readiness-architecture.md) | Dated architecture delta |
| [docs/architecture/cutover-evidence-pack.md](docs/architecture/cutover-evidence-pack.md) | Explicit unmet acceptance matrix |
| [docs/reference/README.md](docs/reference/README.md) | Existing KB routing update |
| [docs/reference/log.md](docs/reference/log.md) | Append-only dated evidence entry |
| [.copilot-tracking/reviews/logs/2026-10-19/issue360-rg-loop-review.md](.copilot-tracking/reviews/logs/2026-10-19/issue360-rg-loop-review.md) | This one original Review |

## Next Steps

Return this record to the active parent. Parent routes RV-001 to later rpi-implement, retains RV-002/RV-003 dependency follow-ups and preserves the original critique and this verdict without repeating Review. Coordinator then owns the final clean commit, actual complete local gate, fresh-main receipt verification and independent exact-HEAD/base/primary-evidence assessment before any publication decision. No user response is required by this Review; no push/PR or cloud action is authorized here.
