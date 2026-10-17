---
title: Demo setup readiness implementation review
description: Single full-task Review, execution, outcome and routed live prerequisites
ms.date: 2026-10-17
---

## Scope and Evidence

Current status: the historical internal Review below missed the independently
reproduced credential-reuse defect. Its PC-001/no-defect conclusion is not the
current acceptance verdict. See the appended P05 disposition; independent
**Revise** remains authoritative pending independent correction verification.

* Task ID: issue-360 / demo-setup-readiness-360.
* Review date: 2026-10-17.
* Scope: full bounded task, candidate 6f43559 against abaca78; P01/P02
  implementation, P03 publication gate, actual issue criteria a-f.
* Plan: .copilot-tracking/plans/2026-10-17/demo-setup-readiness-360-plan.md
* Details: .copilot-tracking/details/2026-10-17/demo-setup-readiness-360-phase-details.md
* Critique: .copilot-tracking/reviews/2026-10-17/demo-setup-readiness-360-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-17/demo-setup-readiness-360-changes.md
* Research: .copilot-tracking/research/2026-10-17/demo-setup-readiness-360-research.md
* Resource receipt: .copilot-tracking/changes/2026-10-17/demo-setup-readiness-360-resource-receipt.json
* Live criterion audit: docs/architecture/cutover-evidence-pack.md,
  Laptop Setup and Restricted Migration Readiness (2026-10-17).

## Opening Review State

* Goal: assess whether the delivered laptop transports, authorized restricted
  migration, privacy/approval boundaries and acceptance claims match the
  confirmed plan and caller direction; do not conflate source and live readiness.
* Scope: one full-task review, not a penetration test or deployment approval.
* Evidence readiness: all canonical artifacts available; implementation committed,
  local gates passed and actual staging receipt supplied. Existing research/plan
  wording is historical at those completed phases; current changes/state own
  implementation completion and P03 owns remaining Review/publication.
* Acceptance basis: caller's full-loop/private/no-fallback/no-Graph/no-role-write/
  no-new-paid-service constraints; plan requirements and acceptance criteria;
  PC-001/002/003 direct dispositions; actual a-f criterion boundaries.
* First comparison: protocol/credential/guard implementation and regression
  evidence, then preservation/readback, descriptive plan updates and routing.
* Read-only boundary: no source, plan, details, critique, research or changes
  edits; only this canonical Review record. Parent owns lifecycle state.
* Initial blockers: private proof-image publication, exact scoped IAM activation
  and human tenant/live acceptance. They block release, not evidence comparison.

## Execution Status

* Execution status: Complete.
* Review execution evidence: one inline Review of 6f43559, completed 2026-10-17.
  No workers, additional critique, live writes or second Review. Source and
  plan-family artifacts remained read-only during this phase.

## Plan-to-Change Reconciliation

| Current scope | Changes/evidence | Reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Bounded ARM relay, same-VNet discovery and job/tag cleanup | Reconciled | Explicit terminal/authentication/cleanup gates retained; no console requirement |
| P01-T02 | secureString deployment, exact what-if and metadata guard | Reconciled | Supported control plane, not vault networking bypass; live secret write Not run |
| P01-T03 | Offline tag role/matrix/tests and surgical setup wiring | Reconciled | Grants not applied; #358 expiry/reuse and secret preservation untouched |
| P02-T01 | 319 infra, 33 focused subset, 32 API auth; lint/type/Bicep | Reconciled | Installed source distributions with pip after missing import; no Docker success claim |
| P02-T02 | Two-resource restricted additive deployment and readbacks | Reconciled | Stable FQDN but four 403s; no auth-before-exposure gap or retirement |
| P02-T03 | Runbook, ADR/evidence, index and append-only log | Reconciled | Historical sections retained; a/b source delivery is not live d acceptance |
| P03 | One Review and prepared publication | Reconciled at Review boundary | Publication intentionally pending parent; no ready/live claim while gates open |
| Follow-Up Items 1-4 | Publisher, IAM, tenant/runtime and retirement | Reconciled | Distinct externally gated work; not omitted active implementation |

Plan's final Ready-for-Implement prose is its original Plan handoff, not a
claim that the current state is still Plan. Checked P01/P02 markers, final
changes evidence, dated persistent completion and parent state identify the
current candidate unambiguously. No stale statement prevents a credible verdict.

## Completed Work Assessment

| Marker | Files | Change and reason | Evidence/validation | Assessment |
| --- | --- | --- | --- | --- |
| P01-T01 | infra/scripts/staff_azure.py; infra/scripts/staff-azure-worker.py | Existing encrypted envelope relayed through source job tags, not private logs | 200-char frames/max40; request binding, tamper/timeout/terminal/cleanup tests; no console invocation | Meets bounded source contract; live worker gate RV-001/RV-002 |
| P01-T02 | infra/scripts/credential_arm.py; infra/scripts/setup-entra.py | One-secret secure ARM template and Azure-mode storage guard | Private body files; no outputs; only intended Create; failure/expiry/URI checks; valid KV reuse and failed-write preservation | Meets source contract without changing #358 selection/rebuild portions |
| P01-T03 | infra/staff-initializer-rbac.bicep; infra/role-assignments.json; infra/tests/test_identity_rbac.py; .github/workflows/src-ci.yml | Exact offline API restart and source-job tags scope; quality gates wired | No wildcard/jobs-write/Graph grant; real four-Create preview, no apply | No role authorization inferred |
| P02-T02 | Resource receipt and changes record | Approved immutable-image replacement in existing external environment | Reviewed exact two Creates; pre-apply source fingerprint/readback; Healthy/Running; four 403s; six Disabled public flags | Restricted staging supported, not criterion d |
| P02-T03 | infra/README.md; docs/architecture/cutover-evidence-pack.md; docs/adrs/0001-azure-architecture.md; docs/reference/README.md; docs/reference/log.md | Current laptop command, actual actions, historical separation and owner gates | Append-only log and current a-f audit inspected | Documentation aligned; no 302/mock acceptance |

Protocol assessment: AES-GCM key remains in operator memory/owned job secret;
run/operation/payload digest bind results. Only bounded ciphertext leaves worker
through tags. Missing, oversized, failed or unauthenticated results cannot
return success. Source configuration is not modified; owned temporary job
absence is confirmed before deleting only the exact run's tags. Hard-kill and
cross-host serialization limits are disclosed, not hidden by a fallback.

Credential assessment: metadata preflight uses the existing private RBAC vault;
minimal template has one secureString input and one selected child secret,
no output. Asynchronous what-if completion is obtained through the existing
CLI adapter, permitting only same-root Ignore rows and the exact Create.
Deployment status and enabled/expiry/versionless URI metadata are required.
Captured CLI output and temporary 0600 files stay outside Git; failures never
activate app storage. Existing future-valid Key Vault reuse remains unchanged.

## Implementation-Time Plan and Detail Update Assessment

| Area | Update and trigger | Reconciliation and decision | Assessment |
| --- | --- | --- | --- |
| P02-T02 / PC-002 | Replaced external=false staging with supported Deny 0.0.0.0/0 rule because internal FQDN would defeat direct laptop discovery | Plan/details/changes describe stable FQDN, auth-before-removal and failure restriction; owner-approved migration retained; official IP restriction evidence and actual 403 readback | Immediately relevant implementation refinement, not new authority or divergent public exposure |
| P01-T02 | Real ARM what-if includes unrelated resource Ignore rows | Exact selected-secret Create still mandatory, all rows same root; real preview proved behavior | Strict contract preserved; no expanded write scope |
| P01-T01 | Exact parent initializer automatically selected only after expected demo job is absent | Both actual environments/subnets independently verified in same ama VNet; API environment remains execution target | Existing planned same-VNet alternative made one-command usable |
| P02-T01 | Missing imports/tools required pip installation | Existing source distributions/runtime requirements and CI tool pins only; no uv, daemon permission or framework change | Within plan and caller intent |
| P02-T02 | Provider returned maxInactiveRevisions=100 where source omitted it | Explicit one-default normalization; other template/config/identity/auth comparisons remain exact | Supported provider materialization, not silent data/config loss |

## Critique and Material Revision Assessment

* PC-001: satisfied in source by early Azure-mode app-state guard plus credential
  boundary guard. Tests cover explicit, recorded and referenced app storage
  before Graph writes, preserved valid vault reuse, preflight and write failure.
  The no-fallback rule is not limited to a replaced vault call.
* PC-002: satisfied for performed action by initial deny-all payload, exact
  reviewed what-if, readback and four 403s. No exposure method or auth-failure
  rollback was invoked. Real UUID/browser/runtime checks remain prerequisites.
* PC-003: publication gate preserved. No material source defect identified in
  this Review; known publisher/IAM/operator dependencies still block live
  readiness. Any future material finding needs blocked/draft handling, not
  an unqualified readiness claim.
* No significant divergent decision or unapproved dependent-work resumption
  identified. Exactly one final-candidate critique, no new critique requested.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner/next action | Route |
| --- | --- | --- | --- |
| 1 private image publication | No approved available private publisher; local Docker denied and private ACR no task/pool | Authorized existing private publisher supplies/pins proof digest, no new paid service/network bypass | Distinct follow-up, RV-001 |
| 2 narrow role activation | Caller explicitly excludes inferred role creation/assignment authority | IAM owner explicitly authorizes exact reviewed demo-API/source-job-only deployment | Distinct follow-up, RV-002 |
| 3 human setup and actual acceptance | SP has no directory authority; private roster/mailbox decisions and genuine user required; #349/#350 runtime/model gaps remain | Human tenant operator and runtime owners after dependencies, then reviewed exposure/browser/SQL/AI evidence | Distinct follow-up, RV-003 |
| 4 retirement | d is unmet; destructive scope must be exact and authorized | Coordinator/owner only after replacement acceptance | Distinct follow-up, RV-004 |

These are release-blocking residual dependencies, not source defects or newly
added active P01/P02 work. No follow-up begins in this bounded task.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Retained proof image does not publish the new worker

* Related scope: P01-T01, P02-T01; plan Follow-Up 1.
* Evidence: research C7, changes Resource Actions/Final Implementation Evidence;
  source initializer retains the earlier proof digest, private ACR has no task/
  pool and local Docker is permission-denied.
* Impact: source tests cannot establish the laptop worker executes live.
* Destination: distinct private-image publication follow-up, authorized publisher.
* Smallest next action: use an explicitly approved existing private publisher,
  build from retained source API plus infra worker assets, push/pin immutable
  proof digest without registry exposure or new billable build services.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: Required resource-scoped worker grants remain unapplied

* Related scope: P01-T03; plan Follow-Up 2.
* Evidence: final demo-target what-if has exactly two role definitions and
  assignments on ca-cutover-test-demo-api/job-cutover-test-init; no apply.
* Impact: worker cannot relay/restart with its current rights; ambient RG Owner
  does not authorize this executor to create or assign roles.
* Destination: distinct IAM authorization/activation follow-up.
* Smallest next action: explicit IAM-owner authorization and fresh reviewed
  deployment at those two resource scopes only; no broad or Graph grant.

<!-- rpi:review id=RV-003 -->
### RV-003 [High]: Criterion d is unproven and intentionally restricted

* Related scope: issue criterion d; plan Follow-Up 3.
* Evidence: resource receipt's four 403s; managed-identity client sentinel/no
  browser credential; no live Graph/SQL/credential/AI/browser execution.
* Impact: welcome/health 200, real human session, role boundaries, SQL persistence/
  restart and AI behavior cannot be claimed. Restriction removal now is unsafe.
* Destination: distinct human tenant/setup and #349/#350 runtime acceptance.
* Smallest next action: after RV-001/RV-002, isolated authorized human command
  with private persisted roster and mailbox decisions; verify registration/
  credential/runtime, review exact exposure scope, then run genuine criteria.

<!-- rpi:review id=RV-004 -->
### RV-004 [Medium]: Retirement correctly remains blocked behind acceptance

* Related scope: criterion e; plan Follow-Up 4.
* Evidence: source pre-apply fingerprint preserved, no retired resource, d unmet.
* Impact: old stack/Front Door cannot yet be retired; this is preserved safety
  gating, not incomplete authorized source work.
* Destination: distinct owner/coordinator retirement follow-up after d.
* Smallest next action: accept verified replacement and review exact retirement
  scope under retained approval; never delete ama or preserved backing assets.

## Defects

No material implementation defect identified in the supplied boundary. This is
not independent certification or proof of behavior through the undeployed image.
All RV entries are known externally gated residual work, not deferred source fixes.

### Independent Review Correction Disposition - 2026-10-17 (P05)

This is the caller-requested correction record, not another internal Review.
Independent review of published662c11b showed that a future-valid generated
app-backed credential, absent store/name tags and current auth reference, was
reused despite requested keyvault; record_credential_store then wrote app.
The finding is accepted. Original PC-001 and no-material-defect assessments
missed this concrete bypass and cannot support acceptance of that candidate.

Selected-candidate storage checks now run before either generated/legacy reuse
return. The early Azure pre-reconciliation guard looks up the registration
read-only and executes the same secret_reference expiry/selection path in
read-only reuse-only mode before locking or directory writes. No alternate
candidate, migration or rotation silently resolves incompatible reuse.

Two failing-before-fix regression methods yielded11 failing subcases, including
real fixture callback reconciliation before rejection. Four final additions
cover direct readonly/apply, configured/sentinel/explicit registration lookup,
check/dry-run, valid KV priority versus app candidates, unrelated/expired/
missing-expiry preservation, and read-only pending handoff/no-storage.
Final focused41, unchanged setup101 and full infra333 passed with zero skips.
Existing11-file Ruff/format, setup F checks/compile, strict check-container/
pipeline and scoped three-module mypy, pip and whitespace checks passed.
Exact upstream preservation helpers, setup/mutation tests, legacy delegate
and sensor source retained. No live resource, role, credential or directory
write occurred. The final publication SHA is recorded at the PR boundary.

Disposition: implementation correction delivered for independent verification;
**not independently accepted**. Do not merge until the independent reviewer
verifies the correction. Historical RV-001 through RV-004 remain unresolved.
IAM management readback actions ["*"] without exclusions shows no demonstrated
IAM inability; no activation attempted, narrow-grant authorization outstanding.
Actual Docker socket denied; no observed ACR Tasks/import IAM denial. Existing
deny-all403 responses are neither ready welcome/health nor live login. #360 d/e
remain UNMET and open.

Correction source/evidence head
23db069a32618678a04bd8a0fa58d3d9ed723e99 was normally pushed and verified.
The subsequent completion-only artifact head is reported exactly in PR #375;
it does not change tested source. Both this finding disposition and that
final head require independent verification before merge, not a repeated
internal Review or self-issued acceptance.

### Same-session integration after #376 - 2026-10-17

Owner authorized rebase onto0bdcb2f0, not another Review. Correction1 evidence
and historical hashes above retained exactly. Credential scripts/tests/runbook
remain byte-identical to190391a; both knowledge histories/index and queue
source retained. Fresh focused41/setup101/full infra333/no skips and existing
quality gates passed on integrationc18790917ea558bcfda8d09aa3fb1d3af51a00d1.
Rebased correction source85c2713. Exact final evidence-only head is reported
in PR375. Reviewer4536f9cc checking190391a has NOT been treated as Pass on
this final head. Original finding remains open until independent final-head
Pass; draft/no-merge/live-prerequisite gates remain.

## Routed Findings

| Finding | Destination | Owner/next action | Reason |
| --- | --- | --- | --- |
| RV-001 | Distinct publication follow-up | Authorized existing private publisher | Missing permitted execution path, no new framework/service |
| RV-002 | Distinct IAM follow-up | Explicitly authorized IAM operator | Required authorization boundary, not an implementation workaround |
| RV-003 | Distinct tenant/runtime acceptance | Human tenant operator and #349/#350 owners | Real login/data/model evidence cannot be simulated |
| RV-004 | Distinct gated retirement | Owner/coordinator after d | Destructive action withheld until replacement verified |

No current finding is routed to rpi-implement, rpi-plan or rpi-research.
No second Review or current-task correction/closure pass is requested.

## Residual Work

RV-001 through RV-004 cover all four current plan follow-ups. Each remains
outside immediate source/staging scope, with explicit next owner and dependency.
IAM activation is the smallest bounded next authorization; image publication is
the other prerequisite to any live worker run. Human setup follows both;
retirement follows actual d acceptance. No work is invented to fill a queue.

## Blockers and Remaining Work

* Release blockers: RV-001/RV-002/RV-003. RV-004 follows d; old resources retained.
* Active implementation remaining: none in P01/P02. Parent records Review
  completion and publishes Refs #360, with exact head and actual criterion audit.
* Human sign-off remains incomplete; no approval checkbox is checked by Review.
* Ordinary source PR publication may proceed with prominent live-blocked status;
  this outcome is not a declaration the demo or issue is ready/closed.

## Validation Evidence

| Command/evidence | Scope | Status | Result or limit |
| --- | --- | --- | --- |
| REQUIRE_AZ_BICEP=1 /tmp/ama-360-readiness-venv/bin/python -m unittest discover -s infra/tests -q | Full infra | Passed | 319 tests, zero skips, 62.799s |
| Same interpreter, unittest discover -s infra/tests -p test_staff_azure.py -q | Focused subset | Passed | 33 tests; baseline 21, 12 additions, none removed |
| PYTHONPATH=src/core/tests:src/agents/tests, unittest discover -s src/api/tests -p test_auth.py -q | Existing API auth loopback | Passed | 32 tests, 11.202s; test-helper path only |
| az bicep build/lint for infra/*.bicep and infra/modules/*.bicep | All 22 templates | Passed | Offline build/lint, not deployment |
| Existing isolated E,F,I,B,UP Ruff and format selectors | Eleven relevant CI files, including new adapter | Passed | No exemption/framework change |
| mypy --strict src/check-container.py; mypy --strict infra/scripts/pipeline.py | Existing strict CI gates | Passed | One source each |
| mypy --follow-imports=silent --ignore-missing-imports, staff client/worker/credential adapter | Existing scoped gate plus new module | Passed | Three sources |
| pip check; git diff --check | Installed requirements/whitespace | Passed | No broken requirements or whitespace |
| Real credential what-if | Selected vault, noncredential secure parameter | Passed within limit | PUT intercepted, no secret creation or exchange |
| Demo-target role what-if | Two definitions/two exact-scope assignments | Passed within limit | No roles deployed |
| Migration what-if/apply/readback, direct no-redirect probes | Two new resources, preservation and restriction | Passed within limit | Succeeded/Healthy/Running; four 403s; six backing public flags Disabled |
| Docker/private image publication | Runtime image | Unavailable | Daemon permission/private publisher gate, no privilege escalation |
| Real operator Graph/credential/worker/SQL/browser/AI acceptance | Issue criterion d | Not run | RV-001/RV-002/RV-003, no simulated success |
| Restriction removal and resource retirement | Criteria d/e | Not run | Auth/runtime and d gates retained |

The commands/results above are implementation evidence, inspected here; Review
did not rerun them as a second verification cycle or perform any Azure write.

## Outcome

* Outcome: Residual work.
* Rationale: bounded source delivery and approved deny-all staging have evidence;
  all three critique corrections are reflected. Release prerequisites and
  actual d/e remain open. A conformant live-readiness outcome would be false.
* Review completion persisted here on 2026-10-17, one execution only.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None identified | No current-task reimplementation |
| Decision gap or invalid assumption | None identified | No new plan or critique |
| Material evidence gap needing discovery | None beyond named live gates | No new research merely to wait for authority |
| Residual dependencies | RV-001 through RV-004 distinct follow-ups | Authorized publisher, IAM, tenant/runtime owners, then retirement coordinator |

* Execution status: Complete.
* Outcome: Residual work.
* Validation coverage: local relevant suites/quality gates and bounded live
  staging evidence only, not real tenant acceptance or certification.
* Parent next action: record separate Review execution/outcome, commit this
  record and persistent completion, publish Refs #360, then stop as requested.
