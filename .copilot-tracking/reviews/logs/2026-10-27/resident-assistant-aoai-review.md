---
title: Resident assistant Azure OpenAI original Review
ms.date: 2026-10-27
---

## Scope and Evidence

* Task: #469 resident-assistant-aoai, refs #466.
* Review date: 2026-10-27.
* Review scope: One independent original Review of the complete current
  uncommitted boundary on feat/resident-assistant-aoai.
* Assessed boundary: All 21 tracked changed files and all 14 untracked files,
  including the five canonical inputs, this record, session state and seven
  new implementation/test files. No ignored/private datasets or secrets read.
* Acceptance basis: The supplied owner requirements and current plan, not the
  historical USD5 proposal or an assumption that provisioning activates AI.
* Canonical inputs:

* .copilot-tracking/research/2026-10-27/resident-assistant-aoai-research.md
* .copilot-tracking/plans/2026-10-27/resident-assistant-aoai-plan.md
* .copilot-tracking/details/2026-10-27/resident-assistant-aoai-phase-details.md
* .copilot-tracking/plans/2026-10-27/resident-assistant-aoai-critique.md
* .copilot-tracking/changes/2026-10-27/resident-assistant-aoai-changes.md

## Opening Review State

* Interpreted review goal: One independent original Review of #469, refs #466;
  identify substantive correctness and requirement gaps without fixing them.
* Review scope: Complete current tracked diff and all untracked implementation,
  tests, infrastructure and task artifacts on feat/resident-assistant-aoai.
* Evidence readiness: All five supplied canonical inputs and the existing
  review record are present. Local and Azure results are supplied implementation
  evidence, not checks independently reproduced by this Review.
* Acceptance basis: Owner's managed-identity-only, USD20 permanent cap,
  five-attempt resident limit, own-case advisory sentence selection, fallback,
  default-off infrastructure and unchanged authority/network boundaries.
* First comparison boundary: P01 runtime and actual SQL accounting, followed
  by P02 infrastructure and complete P03 validation/artifact reconciliation.
* Active read-only boundaries: Only this canonical review record may change.
  No fixes, nested agents, heavy checks, Azure commands or second Review.
* Initial blockers: Actual SQL execution/private migration, new-runtime
  authenticated inference and exact-clean-head publication gate remain
  unavailable or pending; these do not prevent source review.

## Execution Status

* Review execution status: Complete. The complete supplied source/artifact
  boundary was compared once, without delegation or a second Review.
* Planned implementation execution status: Partial. P01/P02 implementation
  exists; P03-T01/T02 remain unchecked. Actual SQL execution, migration,
  new-runtime rollout, authenticated inference and publication are incomplete.
* Outcome: Not accepted for whole-task/live acceptance. This is not a finding
  that provisioning failed or that an observed code defect defeats the cap.
  Two High material acceptance-evidence gaps remain.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record evidence | Reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | SQL accounting, stable own-case hash, narrow EXECUTEs and runtime factory | Implementation reconciled; acceptance partial | Actual accounting procedures have not run; RV-001. |
| P01-T02 | Approved sentence IDs, local mandatory facts, labelled fallback and post-inference authorization | Source direction reconciled | Actual Azure response/MI path remains unexercised; RV-002. |
| P02-T01 | Dedicated default-off account, pinned Standard mini, existing identity account role | Source and supplied provisioning record reconciled | ARM provisioning is not runtime inference. |
| P02-T02 | Architecture, API/infra guides, index/log and safe cloud probes | Reconciled to explicitly limited evidence | Private SQL access and old revision prevent activation claims. |
| P03-T01 | Focused/full tests, policy, browser, lint/type evidence | Correctly unchecked | Required actual SQL and exact-head gate remain unavailable/pending. |
| P03-T02 | Original Review, subsequent commit/gate/publication | Correctly unchecked | This Review completes only its assessment; parent retains publication work. |
| Follow-Up Items | Human/real-identity/privacy/production and hosted/merge gates | Reconciled | Distinct follow-ups, not delivered acceptance or new active scope. |

The plan's final "Ready for Implement" handoff and changes record's "Review is
next" are earlier transition prose. The explicit current P03 markers,
implementation amendments and session state identify the real current state:
Review in progress with blocked validation. These stale handoff sentences do
not obscure a reviewable boundary or establish completion.

## Completed Work Assessment

| Related scope | Files | Assessment and evidence |
| --- | --- | --- |
| P01-T01 | infra/sql/resident-assistant.sql; infra/scripts/resident_assistant_sql.py; infra/scripts/resident_showcase_sql.py | Budget increment and attempt insert share one transaction under a global UPDLOCK/HOLDLOCK; COMMIT precedes accepted SELECT. Cap is 2000 integer cents; five attempts use DB UTC rolling hour. No refund/reset path. Helper reuses verified Entra principal and exact object grants; tables remain denied. Actual SQL behavior is unverified, RV-001. |
| P01-T02 | src/api/src/zava_forward/api/resident_demo/aoai.py; src/api/src/zava_forward/api/resident_demo/app.py; src/api/src/zava_forward/api/resident_demo/__main__.py; src/core/src/zava_forward/core/resident_assistant.py | Startup defaults off and explicitly selects ManagedIdentityCredential. Host derives SHA256 from server-resolved case ID, not request/session-signing-key content. Reserve precedes token/transport; uncertainty returns labelled local rules. Known IDs only; mandatory answer/source/help semantics stay local. Host rechecks session/case authorization after success or fallback. No arbitrary prose, case mutation, specialist decision or other-task interface introduced. |
| P02-T01 | infra/resident-assistant.bicep; infra/role-assignments.json; infra/tests/test_identity_rbac.py; infra/tests/test_resident_assistant.py | Exactly account/deployment/account-scoped inference role are deployable, each under enabled AND ama. Existing identity is referenced, not created. Model/version/Standard capacity1, NoAutoUpgrade, local-auth-off and no dynamic quota align with current amendment. No app, ingress, group or unrelated-role mutation in this template. Supplied actual resource readback is not independently repeated. |
| P02-T02 | docs/architecture/resident-assistant-prototype.md; infra/README.md; src/api/README.md; docs/reference/README.md; docs/reference/log.md | Current USD20 boundary, regional mini tariff, migration/rollback and separate activation gates are documented. Historical owner-decision text is labelled historical; index and append-only log updated. Existing case study/memory remain unchanged. |
| P03-T01 | src/api/tests/test_resident_aoai.py; src/api/tests/test_resident_aoai_sql.py; src/api/tests/test_resident_assistant_api.py; src/core/tests/test_resident_showcase_sql.py | Reviewed mocked provider/factory/usage/prompt/fallback/expiry contracts, cross-case HTTP and revocation tests, narrow permission verifier tests and six opt-in actual-SQL tests. The SQL module targets task-owned loopback database, not Azure/private data. Executable SQL evidence remains absent. |
| P03-T01 | .github/workflows/src-ci.yml; .github/workflows/mvp-ci.yml; tools/rpi-checks.py | Actual accounting selector appended to the existing SQL lists; existing order/check names retained and workflow hashes updated. This does not constitute execution or a passing receipt. |
| P01/P03 | src/api/pyproject.toml; src/api/requirements.in; src/api/requirements.txt | Direct azure-identity dependency declared and existing hashed version retained; no SDK credential-chain substitution. |
| P01/P03 web | src/api/src/zava_forward/api/resident_demo/web/assistant.js; src/api/checks/resident_assistant_browser_check.py | Only explanatory notice and matching assertion changed. Fresh guidelines retrieved and full changed JS file read. No substantive changed-line guideline finding; existing native controls/live regions retained. Browser acceptance is supplied implementation evidence, not rerun here. |
| RPI evidence | Five canonical inputs; .copilot-tracking/rpi-sessions/2026-10-27/resident-assistant-aoai-state.json | Read current and historical decisions, critique dispositions, markers and blockers. State's private-migration/local-lock blockers agree with plan/changes. This Review changes only its own record. |

## Implementation-Time Plan and Detail Update Assessment

| Affected scope | Change and trigger | Reconciliation and assessment |
| --- | --- | --- |
| P01-T01/T02; PC-001 through PC-006 | Critique required useful bounded guidance, mandatory semantic facts, priced wire envelope, real SQL, precise permissions, actual composition and stable resident key | Current plan dispositions and code implement these directions. Mocked cases cover open/closed/unknown/documents/forms; host enforces contextual status IDs while locally appending mandatory facts. This is explicitly constrained selection, not free-text chat or proof of real-model task quality. SQL/live acceptance is still open. |
| P02-T01; PC-002/007 | ARM rejected nano ordinary Standard; 4o-mini ordinary Standard retired; gpt-4.1-mini selected | Current plan/detail amendments, code constants, Bicep, tests, runbooks and changes agree on gpt-4.1-mini 2025-04-14, resident-mini, regional Standard capacity1, swedencentral. Research and earlier detail/critique text retain the historical nano proposal, not current activation instructions. |
| P01/P02; PC-008 | Funding and access authority have different end dates | Inference/tariff and SQL reserve end exclusively at 2026-11-01 UTC. Existing session/SQL admission may end earlier; December funding does not extend it. Post-token, post-response and host authorization checks preserve these boundaries. |
| P02/P03; PC-003/009 | Heavy lock unavailable; private SQL public access disabled; old runtime only | Unchecked P03 markers, changes, plan and state distinguish local capability/resource creation from migration/new-image/MI smoke. No network/role workaround or fabricated success is recorded. |

The revised cost calculation is internally consistent:
8192 * USD0.000484 / 1000 + 256 * USD0.001936 / 1000 =
USD0.004460544, below each permanent USD0.01 reservation. The complete serialized
payload is checked against 4096 bytes; output is bounded at 256 tokens and one
choice. The supplied dated public-rate verification is not independently
repriced in this Review. The cap is application admission, not a universal
subscription spending cap. No unmetered diagnostic request is authorized.

## Critique and Material Revision Assessment

* Original critique remains Complete / Revise, 6 High and 3 Medium; it is not
  rewritten into a pass.
* PC-001/002/004/005/006/007/008 have direct source/planning dispositions
  consistent with the accepted bounded task and current resource selection.
* PC-003's executable actual-SQL requirement remains unproven, RV-001.
* PC-009's migration/new-image/managed-identity/resident acceptance remains
  unproven, RV-002. Resource health/probes do not dispose of that requirement.
* The mini substitution is a justified compatible implementation amendment
  under the supplied cheapest-available regional-model direction: no higher
  cap, GlobalStandard, free text, authority extension or extra role. No
  additional owner decision or second critique is inferred or requested.
* Direct critique corrections are described as preceding implementation;
  no available artifact demonstrates dependent work resumed against an
  unresolved divergent owner decision.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate acceptance | Owner or next action | Assessment |
| --- | --- | --- | --- |
| Human approval, real resident identity, privacy and production acceptance | Synthetic engineering and account provisioning cannot establish these | Owner and named identity/privacy/service approvers | Remain distinct approval work; do not activate or close #469 from local tests. |
| Hosted CI and owner merge | Depend on eligible exact-head publication and human review | Publishing parent, then owner | Remain external gates; local checks and this Review are not substitutes. |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: The durable hard-cap and rate-limit acceptance oracle has not executed

* Class: Material evidence gap, not an observed SQL correctness defect.
* Related scope: P01-T01, P03-T01, PC-003/004; hard USD20 and per-resident limit.
* Evidence: src/api/tests/test_resident_aoai_sql.py defines real procedure tests
  for concurrent last-cent/fifth-attempt admission, rolling-hour release,
  persistence/reapply, duplicate reservation/completion and restricted access.
  The changes record states both timeout-zero lock attempts stopped before
  Docker startup. The supplied SQL boundary suite also has 19 opt-in skips.
* Impact: Mocked reserve callbacks and SQL source inspection cannot establish
  real transaction/driver/ownership-chain behavior. Since durable accounting
  is the admission control for every paid call, whole-task acceptance cannot
  infer that the hard monetary/rate boundary is proven.
* Destination: rpi-research, bounded execution-evidence acquisition for the
  already accepted actual-SQL contract. Not a request for architectural redesign.
* Smallest useful next action: Parent obtains the existing shared heavy lock
  legitimately, runs the task-owned loopback SQL selector through the applicable
  gate, retains results and routes any actual failure to later rpi-implement.
  Do not steal a lock, weaken isolation or substitute cloud SQL for local proof.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: No authenticated managed-identity inference through the new resident runtime is evidenced

* Class: Material requirement/acceptance-evidence gap, not an observed model,
  identity, networking or response-schema failure.
* Related scope: P01-T02, P02-T02, P03, PC-009; real Azure OpenAI requirement.
* Evidence: Changes and supplied owner context report the dedicated account,
  resident-mini deployment and one account role provisioned. Old
  ca-resident-demo--0000002 health200 and anonymous new-AOAI401 do not execute
  new code. No accounting migration, new image/configuration rollout or
  authenticated resident/MI model request occurred. SQL public access is
  Disabled; this host's DNS resolves publicly.
* Impact: Real model/API compatibility, MI token authorization, durable debit,
  validated response and authorized resident delivery have never been observed
  together. Local mocks and ARM listings cannot satisfy real-runtime acceptance.
* Destination: rpi-research, bounded authorized integration-evidence acquisition.
* Smallest useful next action: After local gates and only through the existing
  authorized private SQL/rollout path, verify narrow migration/principal rights
  and exact new image/config, then perform one ledger-metered MI/resident smoke
  using an already authorized available session. Retain safe debit/count/output
  evidence without reading stored credentials or making diagnostic bypass calls.
  If that path needs new authority, parent must route the specific decision to
  rpi-plan; this finding authorizes no ingress, role, group or access change.

## Defects

No high-confidence substantive implementation defect was established in this
boundary. RV-001/RV-002 are missing required evidence, not disguised assertions
that the reviewed implementation is broken. No source fix is prescribed.

## Routed Findings

| Finding | Destination | Owner / next action | Reason |
| --- | --- | --- | --- |
| RV-001 High | rpi-research | Parent obtains actual isolated SQL results under existing lock/gate rules | Hard-cap and rate-limit proof absent. |
| RV-002 High | rpi-research | Parent obtains authorized private-path, new-runtime MI/resident evidence after prerequisites | Real integration acceptance absent. |

Later implementation of an actual failure does not require another Review.

## Residual Work

* Distinct publication follow-up: Publishing parent commits implementation and
  original dated RPI evidence, runs the owner-selected applicable scoped
  exact-clean-head gate, verifies the external receipt against fetched main
  immediately before push and obtains independent exact-head/hosted assessment.
  Full mandatory publication policy still applies; this Review grants no skip
  or downgrade. A passing focused suite is not a gate receipt.
* Hosted checks, owner merge and human/privacy/real-resident/production
  approvals remain distinct follow-ups as above, not newly invented code defects.

## Blockers and Remaining Work

* Actual local SQL: unavailable shared heavy lock; no container/lock touched
  during this Review. RV-001 remains open.
* Live path: no private migration/new runtime/authorized session smoke; no
  weakening SQL publicNetworkAccess, new ingress or developer-token substitute.
  RV-002 remains open.
* Publication: Uncommitted candidate has no clean-head gate/receipt. P03-T01/T02
  remain incomplete even though this one Review is complete.
* Reviewer unit rerun: System python3 lacks installed zava_forward distributions.
  Three selected modules failed during import, before assertions ran. No
  dependency install, PYTHONPATH-to-source workaround or repository change was
  made to disguise this environment limitation.

## Validation Evidence

| Check | Status | Evidence and limit |
| --- | --- | --- |
| Review: focused API unit/HTTP command below | Unavailable; command failed | Three ModuleNotFoundError: zava_forward import errors. No assertion executed; not an observed implementation regression. |
| Review: git diff --check | Passed | Current tracked diff whitespace; no source mutations. |
| Review: node --check src/api/src/zava_forward/api/resident_demo/web/assistant.js | Passed | JS syntax only, not browser acceptance. |
| Review: fresh web guidelines retrieval and changed JS review | Passed within changed-line scope | Current source retrieved successfully; full assistant.js read against rules. No substantive changed-line finding. No fresh browser/WCAG-conformance claim. |
| Supplied focused API/model/legacy/showcase | Passed, not rerun successfully here | 72 tests reported. |
| Supplied full API | Passed with skips, not rerun here | 1108 tests, OK, 314 opt-in skips; not 1108 executed assertions. |
| Supplied core assistant / SQL boundary | Passed with skips, not rerun here | 6 assistant tests; SQL suite 29 tests with 19 skips. |
| Supplied compiled account / RBAC / deploy / Bicep policy | Passed, not rerun here | 3 / 11 / 15 / 50 tests respectively. |
| Supplied local gate tooling | Passed, not a publication receipt | 30 tests; selector wiring reviewed. |
| Supplied changed strict typing / component Ruff | Passed, not rerun here | Scoped engineering evidence only. |
| Supplied resident Chromium | Passed, not rerun here | Keyboard/focus, logout response isolation, retry/error, 320px reflow and reduced motion. |
| Actual new accounting SQL | Not run | Lock acquisition failed before Docker; RV-001. |
| New-runtime authenticated MI/resident inference | Not run | Migration/rollout/private-path prerequisites absent; RV-002. |
| Scoped clean-head publication gate | Pending | Must follow original Review commit; no receipt or publication approval claimed. |

Review attempted from src/api, without bytecode writes:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=tests:../core/tests:../agents/tests \
  python3 -m unittest -q test_resident_aoai test_resident_assistant_api \
  test_resident_assistant_provider
```

Web guideline report for the changed line:

```text
## src/api/src/zava_forward/api/resident_demo/web/assistant.js
pass - no substantive changed-line finding
```

## Outcome

* Review execution: Complete.
* Planned execution: Partial.
* Outcome: Not accepted for full #469/live acceptance, because RV-001 and
  RV-002 leave material hard-cap and real-runtime criteria unproven.
* Severity summary: 0 Critical; 2 High evidence gaps; no observed code defect.
* Completed source direction is consistent with the bounded owner-selected
  sentence-selection design and justified mini substitution. This is neither
  rejection of that design nor closure/activation approval.
* The original critique and this original Review outcome remain preserved.
  Parent owns later evidence, corrections if actual failures emerge, and gates;
  no second Review is requested.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | None established | No speculative fix. |
| Decision gap / invalid assumption | None currently established | rpi-plan only if authorized activation needs a new explicit decision. |
| Material evidence gap | rpi-research | Parent: RV-001 actual local SQL; RV-002 authorized new-runtime MI/resident evidence. |
| Non-blocking residual work | Distinct publication and approval follow-ups | Publishing parent, hosted checks and owner/appropriate approvers. |

Only this canonical review file was edited. No source/artifact fixes, cloud
operations, heavy commands, nested agents or new review artifacts were made.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-27/resident-assistant-aoai-research.md](.copilot-tracking/research/2026-10-27/resident-assistant-aoai-research.md) | Research and historical selection. |
| [.copilot-tracking/plans/2026-10-27/resident-assistant-aoai-plan.md](.copilot-tracking/plans/2026-10-27/resident-assistant-aoai-plan.md) | Current acceptance, dispositions and incomplete P03. |
| [.copilot-tracking/details/2026-10-27/resident-assistant-aoai-phase-details.md](.copilot-tracking/details/2026-10-27/resident-assistant-aoai-phase-details.md) | Current implementation details and mini amendment. |
| [.copilot-tracking/plans/2026-10-27/resident-assistant-aoai-critique.md](.copilot-tracking/plans/2026-10-27/resident-assistant-aoai-critique.md) | Preserved original Revise verdict. |
| [.copilot-tracking/changes/2026-10-27/resident-assistant-aoai-changes.md](.copilot-tracking/changes/2026-10-27/resident-assistant-aoai-changes.md) | Supplied implementation and validation evidence. |
| [.copilot-tracking/rpi-sessions/2026-10-27/resident-assistant-aoai-state.json](.copilot-tracking/rpi-sessions/2026-10-27/resident-assistant-aoai-state.json) | Parent phase/blocker state. |
| [.copilot-tracking/reviews/logs/2026-10-27/resident-assistant-aoai-review.md](.copilot-tracking/reviews/logs/2026-10-27/resident-assistant-aoai-review.md) | This single original Review and routing. |

## Next Steps

Active parent: preserve and commit this original outcome with the candidate,
retain incomplete P03/acceptance, and acquire RV-001/RV-002 evidence through
later bounded rpi-research under the existing authority and gate rules.
Publication and human approvals remain separate. If blocked, retain the
blockers rather than bypass them. No second Review or user response is required
for this assessment.
