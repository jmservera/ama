---
title: Demo setup readiness implementation evidence
description: Actual changes, validation and resource actions for issue 360
ms.date: 2026-10-17
---

Task: issue-360 / demo-setup-readiness-360. Scope: full approved plan P01-P03.
Implementation started after one critique; PC-001/002/003 directly applied.
Research, Plan, Implement and the single Review complete, independently
committed. Refs #360 PR #375 published; session stopped per caller.

## P01 - Laptop-safe transports

Implement the plan's bounded ARM ciphertext relay and secureString Key Vault
deployment, preserving #358 expiry/secret-rebuild ownership. No delegation.

P01-T01/T02/T03 complete: existing worker/client now use 200-character encrypted
frames, maximum 40, source initializer tag-only Merge/Delete; terminal execution
success and confirmed job/tag cleanup are mandatory. Same-VNet parent initializer
reuse verifies both environments/subnets and runs in the API environment.
The credential adapter uses a single secureString ARM resource with expiry,
exact Create-only what-if, bounded deployment polling and metadata verification.
Azure-mode compatibility guard rejects app-backed state before reconciliation;
late fallback also rechecks at the credential boundary. Expiry selection and
configuration.secrets preservation are untouched. Twelve added focused test
methods, no removed tests; focused total 33 passed. Ruff/format and
scoped mypy pass. Workflow selectors include the new credential module.

Implementation judgment: ARM what-if includes unrelated ama resources as Ignore.
Accept only same-root Ignore entries plus exactly the selected secret Create,
not an impossible single-row total. CLI what-if follows async ARM polling;
az rest initial 202 body alone is not scope proof. No second critique needed.

## Validation Baseline

System Python failed with missing zava_forward. Created isolated pip-only venv
`/tmp/ama-360-readiness-venv`, installed all five source distributions with
--no-deps, hashed API runtime requirements and pinned PyYAML. Existing focused
test_staff_azure baseline: 21 tests passed. No uv or PYTHONPATH source workaround.

## Resource Actions

Initial research discovery and constant ARM Log Analytics query only, before
the additive staging below. Query correctly denied by private workspace policy. No private datasets,
secret values, Graph mutation, image build or role activation.

2026-10-17 permission what-if Succeeded: four actionable Creates only: two
custom role definitions, one API-only assignment and one existing-initializer-
only tag assignment. All other resource rows Ignore. **Not applied**: explicit
role creation/assignment activation is not authorized by the caller. Existing
API auth readback still uses the managed-identity sentinel instead of a real
registration and has no browser credential. No sign-in inference.

## P02 - Fail-closed migration staging

Immediately relevant plan update, no new owner decision: stage external ingress
with Deny 0.0.0.0/0 rather than external=false. The latter changes the FQDN to an
internal hostname and fails existing direct-setup discovery. Official
https://learn.microsoft.com/en-us/azure/container-apps/ip-restrictions
(retrieved 2026-10-17) defines deny IPv4 CIDR restrictions; no private backing
service network changes are involved. Preserve stable public FQDN and management
reachability, but block *all* public application requests before auth creation.
No rule removal until real registration/auth/runtime verification and another
exact reviewed what-if. PC-002 fail-closed intent is preserved.

Full infra suite: 316 tests passed, zero skips with REQUIRE_AZ_BICEP=1.
pip check passed. Real selected-vault one-secret what-if through the new adapter
succeeded; intercepted the subsequent deployment PUT before sending it. This
was a schema/scope probe with a noncredential secure parameter, **not** a
credential deployment, secret creation or simulated successful sign-in.

## Blockers and Remaining Work

Private image publication path absent; source-job tag and API-scoped restart
roles require explicit authorized activation. Tenant operator login/Graph,
staff and actual browser/SQL/AI acceptance remain blocked. Migration staging is complete; public exposure and genuine acceptance remain blocked.

## Final Implementation Evidence

Implement complete on 2026-10-17, bounded source and authorized staging scope.
P01/P02 complete; all remaining work is explicitly gated live/operator work,
not silently accepted criteria. Exactly twelve added focused methods (21 to 33),
no removed methods. Coverage includes automatic verified parent discovery,
existing Key Vault-backed reuse without rotation, failed vault write preserving
auth/secrets without fallback, and rejected app-backed state before writes.

* Full infra: 319 tests passed, zero skips, REQUIRE_AZ_BICEP=1 (62.799s).
* Existing API auth loopback: 32 tests passed (11.202s).
* All 22 infra/module Bicep templates built/linted offline.
* All eleven existing relevant CI Ruff/format files passed, including the new
  credential adapter; strict mypy for check-container/pipeline and scoped mypy
  for staff client/worker/credential adapter passed; pip check passed.
* Git diff whitespace review passed. setup-entra diff confirms no changes to
  expiry/reuse selection or configuration.secrets preservation owned by #358.
* Real Docker/build/runtime-image/Graph/SQL/credential exchange and browser
  acceptance Not run. No simulated success or 302 acceptance.

Deployment `demo-stage-360-20261017` Succeeded. Exact what-if, repeated against
unchanged reviewed input, contained only Creates for the demo API and auth child.
The receipt is
`.copilot-tracking/changes/2026-10-17/demo-setup-readiness-360-resource-receipt.json`.
Readback compared the retained source against the pre-apply fingerprint, not
merely a later snapshot. New template/runtime configuration/identity/auth match
the reviewed preservation payload; provider default maxInactiveRevisions=100
is explicitly normalized. New revision is Healthy/Running; four direct HTTP
routes return 403 under deny-all, not live criterion d. Old resources remain.
All six backing-service publicNetworkAccess properties remain Disabled.

Final demo-target RBAC what-if Succeeded: two custom role definitions,
assignment at ca-cutover-test-demo-api and tags assignment at job-cutover-test-init.
No actionable change outside those four Creates. **Not applied**.
No image publication, role/Graph/secret write, SQL/private-data access,
restriction removal, old-stack/Front Door retirement or ama deletion.

Current a-f audit is in docs/architecture/cutover-evidence-pack.md,
section Laptop Setup and Restricted Migration Readiness (2026-10-17).
a/b source delivery and f documentation delivered; c approved additive step
done; d/e **UNMET**. Readiness remains blocked, issue closure stays coordinator-owned.

## Persistent Phase Completion

* Research complete: 3e24e7c, executed, Ready for bounded implementation.
* Plan complete: 96871b3, one critique executed, Revise findings directly applied.
* Implement complete: this artifact, P01/P02 evidence above; operator gates open.
* Review complete: exactly one canonical Review, execution Complete and outcome
  Residual work. No material source defect identified; RV-001/002/003/004
  route existing publisher/IAM/human/retirement gates, not another current-task
  implementation or Review. No further live actions.

## Review Handoff

Canonical Review:
`.copilot-tracking/reviews/logs/2026-10-17/demo-setup-readiness-360-review.md`.
Reviewed implementation commit 6f43559. Source changes accepted as bounded delivery, not live readiness.
Published Refs #360 PR #375, no Closes, merge or issue tick. Initial remote
head 4b50561cff0a0f1b6598bad3451e962f66e4f890 was read back from the open PR.
The final receipt-only commit records publication and stopped state, with no
source or live change; its exact final head is resolved/read back at closeout.
Publication receipt:
`.copilot-tracking/changes/2026-10-17/demo-setup-readiness-360-publication-receipt.json`.
All four phases have persistent completion; no child work is started.

## P04 - Same-session owner-authorized continuation

2026-10-17 caller resumes the same #360 session/PR #375, explicitly authorizing
rebase and force-with-lease of this topic only. Starting clean head
662c11bdb60e19879c0bf2d905e39dfab82727e6; origin/main is 51db4fa8
(#374 credential preservation), after #373 sensor faults. Independent reviewer
4536f9cc is assessing the prior candidate; its findings remain actionable and
new SHA must be reported, not represented as already reviewed.

Scope P04-T01/T02/T03/T04: preserve upstream expiry/inventory/handoff/legacy
contracts and tests exactly, integrate Azure ARM transport/no-app-store guard,
retain all knowledge histories, test combined paths and full relevant suites,
research concrete existing-resource private publisher alternatives, then push.
No new credentials/roles/network services, no private data or live sign-in,
no nested loop/merge/issue closure. Existing one-pass Review remains historical.

### P04-T01 - Upstream preservation and rebase

Rebased onto 51db4fa80a29528f5a3d19420b1c7e1597d27213 using caller's
explicit history-rewrite authorization. Rebase conflicts resolved additively:
retained #358 credential evidence section and index row, #373 sensor index
changes, entire upstream append-only log prefix and this branch's later entries.
setup-entra retains exact upstream source for secret_inventory,
preserve_app_secrets, secret_reference_digest and verify_secret_handoff.
The secret selection/expiry logic and new expected-digest PATCH/readback/
pending-handoff recovery are unchanged. Existing infra/tests/test_setup_entra.py
and infra/scripts/initialize-api-auth.py are byte-identical to upstream.
No #373 source/test changes relative to main.

Local AST/source equality, git diff and prefix/index assertions passed.
Rebased original source commit is 439cc57 (previously 6f43559); completed
original Review still applies only to its recorded historical candidate and
does not assert independent review of this newly integrated head.
Reviewer 4536f9cc could not be messaged: tool returned "No agent found".
No public PR review/comment findings were available at inspection. Final PR
comment will provide exact new SHA and request retention of any prior findings;
absence of visible findings is not an approval.

### P04-T02 - Combined secret paths

Added four test methods in infra/tests/test_staff_azure.py, none removed;
original focused 21 + prior 12 + new 4 = 37, within max25 branch additions.
Uses upstream synthetic inventory fixtures without modifying upstream tests.
Five provider response shapes exercise ARM-created credentials plus complete
KV URL/identity and app/empty-value preservation, digest readback/marker removal,
unchanged token-store references and valid KV reuse without rotation.
Corrupted/missing references block auth and rerun; interrupted readback reuses
the same credential only after pending digest verifies. Invalid inventories
fail before addPassword/ARM deployment. Generated/legacy Key Vault references
retain missing/expired/equal/future expiry semantics in Azure apply/check/dry-run.
Azure dry-run intentionally returns incomplete where no private SQL job is
created; no test rewrites that existing evidence boundary.

Initial new-test assertions incorrectly rejected management-only "az keyvault
list" discovery and assumed Azure dry-run could claim private SQL success;
corrected assertions to forbid only secret data-plane calls and retain expected
dry-run incompleteness. Initial Ruff caught loop-closure binding and UTC alias
in added tests; corrected the tests only. No production fix hidden by weakening
upstream tests or changing expiry/handoff source.

Passed: focused 37, upstream setup/legacy/mutation suite 101; full infra 329,
zero skips with REQUIRE_AZ_BICEP=1 (64.873s). All eleven CI Ruff/format files,
strict check-container/pipeline and scoped three-module mypy passed; all22
Bicep build/lint and pip check passed. Broader retained workflow suites follow.

### P04-T03 - Concrete publication and IAM blocker investigation

Actual read-only operations and their limits (2026-10-17):

* docker version fails with permission denied connecting to
  unix:///var/run/docker.sock. No sudo/group/daemon change attempted.
  buildah/podman/buildctl/skopeo/crane are not installed; not permission failures
  and not installed as a new speculative publication framework.
* Existing registry read succeeds: Premium, publicNetworkAccess Disabled,
  networkRuleBypassOptions None; agentpool list and task list both return [].
  Five most recent historical quick runs Succeeded, newest dbb on 2026-10-16,
  all agentPool null. This proves past default quick-run use, not a currently
  private-connected agent or authorization for new spend.
* Anonymous HTTPS /v2/ on the target returns HTTP403 from this host.
  It is not an authenticated push attempt or evidence of missing AcrPush.
  No registry login token/secret is requested. Current networking is preserved.
* Official ACR private-endpoints documentation explicitly says default
  az acr build fails when public access is disabled; supported alternatives
  are dedicated agent pool or public task IP firewall access. No existing pool;
  new paid pool/network opening is prohibited. Therefore no quick build or
  source upload attempted, and no fabricated scheduleRun authorization error.
* Official import documentation requires trusted-service network bypass for
  restricted source/target registries. Bypass here is None; import is not a
  supported no-network-change substitute. No import attempted, even by digest.
* GitHub's latest inspected successful src CI run 39028596880 retained only
  regulatory UX and four Trivy JSON report artifacts; workflow builds local
  zava-forward-*:ci images but neither saves/exports nor pushes images.
  Paginated artifact metadata showed no OCI/docker/proof image archive (names
  containing image were Trivy reports). SBOMs/reports are not reusable images.
  Source API CI also does not construct the infra proof layer.
* GitHub user container-package inventory GET actually returned HTTP403:
  "You need at least read:packages scope to list packages." Therefore external
  package inventory is unknown, not claimed empty. No token scope expansion.
  The initial incorrect repository-package endpoint returned404 and was replaced
  with the correct user endpoint; not treated as image-absence evidence.
* Repository self-hosted runner inventory succeeds and is empty. Resource list
  in ama has existing application jobs, no VM/ACI private builder. All retained
  proof jobs use the old digest; none is a ready new-worker publisher. No
  outside-group host search or new build job/image/framework created.
* Initializer exact-scope assignment reads: AcrPull on registry; [] at source
  initializer job and demo API, including inherited assignments. SQL admin is
  separate existing authority. Pull cannot be repurposed into registry push.
  IAM activation not attempted: caller reserves explicit approval for role
  creation/assignment; this is an authorization boundary, NOT an observed
  Azure AuthorizationFailed. Prior four-Create what-if remains the scope basis.

Official sources retrieved 2026-10-17:
https://learn.microsoft.com/en-us/azure/container-registry/container-registry-private-endpoints
(Use az acr build with private endpoint and private registry);
https://learn.microsoft.com/en-us/azure/container-registry/container-registry-import-images
(Important restricted-network/trusted-services prerequisite);
https://learn.microsoft.com/en-us/azure/container-registry/tasks-agent-pools
(VNet support and billing based on pool allocation). The guessed
container-registry-tasks-virtual-network URL returned404; replaced by these
retrieved official sources, no claim it supplied evidence.

Conclusion: no discovered already-authorized existing-resource/no-new-spend
private build/import route is executable here. No build/push/import or IAM
activation was attempted or represented as a failed service operation.
Minimum publisher action: owner identifies an already existing private-connected
builder/operator with existing target-registry push authority; that operator
builds infra/cutover-proof.Dockerfile with the retained immutable API base,
pushes a new proof tag and returns the digest. Do not grant daemon access here,
provision a pool, open ACR or mint credentials as a workaround. If no such
builder exists, proceeding needs a separate explicit infrastructure/spend
decision outside this task.

Minimum separate IAM approval: explicitly authorize only the reviewed
staff-initializer-rbac deployment for apiName=ca-cutover-test-demo-api and
initializerIdentityName=id-cutover-test-init (two definitions/two assignments).
Until approval, no role PUT; after approval, fresh exact what-if then apply.
These two actions unblock worker publication/relay/restart, not tenant consent
or criterion d. Human login remains subsequent, and d/e stay UNMET.

### Broader retained workflow validation completion

Full source API from workflow-defined src/api cwd: 563 tests, OK with110 skips,
180.974s. Skip inspection:109 require disposable SQL Server (ZF_TEST_MSSQL=1);
one rendered check requires opt-in local Playwright browser. Neither disposable
server nor browser acceptance is inferred. Initial root-directory invocation
failed six test/checks namespace imports (498 tests/errors6/skips61); reran
the exact existing component working directory, not a source PYTHONPATH hack,
and it passed. No source changed to hide that invocation failure.

Full core (including upstream #373 sensor faults):546 tests, OK with1 skip,
293.397s; skip is explicitly isolated synthetic Azure SQL resident test.
Orchestrator:22 tests, OK. Legacy branding migration:25 tests, OK after
observed missing PIL/pptx; installed the existing pinned
tools/rename-zava-requirements.txt with pip only. Expected broken-PPTX fixture
diagnostic is not a failure. Browser app/assistants JS syntax passed; pip check
still clean. No private data, live SQL or Docker-based SQL acceptance.

P04-T01/T02/T03 complete. P04-T04 next: commit/push the rebased/integrated
candidate using exact lease on remote662c11bdb60e19879c0bf2d905e39dfab82727e6.
No visible independent-review findings removed; none were exposed through PR
comments/reviews at inspection. Reviewer-agent messaging unavailable, so PR
comment is the durable exact-SHA notification channel. Existing Review is not
rerun or relabelled as review of this head.

### P04-T04 - Authorized topic publication and stop

Completed exact-lease topic force push from
662c11bdb60e19879c0bf2d905e39dfab82727e6 to
63aea6445bb89fe5a12064aa932a9df84fea85e9. git ls-remote confirms the new
topic SHA; base is51db4fa80a29528f5a3d19420b1c7e1597d27213. Only the
owner-authorized topic history was rewritten. PR remains375; #360 is open.
This final completion-record commit changes only tracking/log, not source,
tests or acceptance evidence, and is followed by an ordinary topic push.
Final exact head is reported durably in the PR comment, avoiding a self-hash
inside the commit. No force push of main, merge, credentials or live resource
write; no new critique/Review/child task. Automatic session stopped under the
caller's bounded continuation direction. Original Review is historical, not
an approval of the integrated head or resolution of unseen reviewer findings.

## P05 - Independent-review correction, same session

2026-10-17 owner provides independent reviewer4536f9cc's concrete Revise on
published662c11b: untagged/unreferenced generated future-valid app-backed
candidate bypasses both Azure guards, gets reused and tags storage app despite
requested keyvault. Accept as blocking source defect, not residual IAM/image
work. Historical internal no-defect/PC-001-complete assertions were incomplete.
Starting clean integrated headb847509fc9fe47284de30b3575e8e2e604cf07f6,
main51db4fa8 unchanged. Scope P05-T01/T02/T03 only: failing regression, actual
selected-candidate guard plus equivalent early pre-reconciliation check,
existing relevant gates, disposition and normal topic push. No rerun full
Research/Plan/Review, no merge or live writes. Independent verification remains
mandatory; implementation cannot self-clear Revise.

Reviewer clarification adopted: management permission readback actions ["*"]
with no exclusions is not demonstrated IAM inability. Activation was never
attempted; only explicit narrow-grant authorization is outstanding. Docker
socket denial is observed; ACR private/bypassNone/zero tasks/pools and route403
remain networking/execution evidence, not IAM denial or welcome/login readiness.

### P05-T01 - Failing independent reproduction

Before production edits, two new regression methods failed in11 subcases.
Direct secret_reference readonly/apply did not raise for the actual unreferenced
app-backed candidate. Full setup apply reconciled registration callbacks before
rejecting/finishing, and check/dry-run returned incomplete2 rather than blocked1.
Cases cover configured-client, managed-identity sentinel/name discovery and
explicit client selection, with no recorded storage/name or auth reference.
The fixture deliberately adds supported callback drift to expose early writes;
an initial invalid signInAudience fixture instead triggered unrelated rejection
and was replaced, not accepted as sufficient reproduction.

### P05-T02 - Selected-candidate rule and equivalent early preflight

azure_credential_guard accepts the actual selected candidate and rejects it
when Azure/browser mode requires Key Vault but that candidate is app-backed.
Both generated and legacy reuse returns call it before record_credential_store.
No fallback to another candidate, migration or credential rotation is allowed.

Pre-reconciliation discovers the existing registration read-only and runs
secret_reference with readonly=True/reuse_only=True before authentication lock
and directory reconciliation. This reuses the SAME existing expiry/matching/
current-reference priority as actual reuse, not a separate name-prefix guess.
No eligible candidate means preflight returns without storage discovery or
creation. Guard forbids write-mode reuse_only; pending-handoff verification
remains read-only at preflight. Actual write path still independently guards
its selected candidate; automatic late Azure-mode switching remains covered.

No #374 expiry comparator, legacy predicate, secret inventory/digest/readback
helper or pending-handoff algorithm changed. New tests preserve unrelated
app/KV values, expired/missing-expiry and nonmatching app secrets, preferred
valid KV versus last eligible app candidate. Four additive methods overall
(41 focused vs original21, within max25 additions); upstream tests untouched.
Focused40 and unchanged setup101 passed immediately after the source fix;
final41 and full infra/quality gates follow.

### P05-T03 - Final validation and independent verification gate

Final focused41 passed; full REQUIRE_AZ_BICEP=1 infra333 passed, zero skips,
including unchanged setup/legacy/mutation101 and existing Bicep gates. Existing
11-file Ruff E/F/I/B/UP and format passed; changed legacy setup F-only check
and py_compile passed without reformatting it. Strict check-container/pipeline,
scoped three-module mypy, pip check and diff whitespace passed. Exact upstream
secret_inventory/preserve_app_secrets/secret_reference_digest/verify_secret_handoff
source, test_setup_entra.py, legacy initialize-api-auth.py and sensor core retained.
Upstream persistent-log prefix preserved.

External finding implemented, not independently accepted. Existing Review now
records its original missed PC-001 assessment and current independent Revise
gate. No second Review, no source-test alteration to evade mutation protections,
no Azure/Graph/role/credential/network/data writes. IAM explicitly
authorization-outstanding, not permission-blocked; image actual Docker socket
denied, Tasks/import unattempted, no demonstrated IAM denial. Existing four403s
are deny-all evidence only; #360 stays open with d/e UNMET. Publication next:
privacy-safe conventional commit, ordinary topic push, exact final SHA in PR.

### P05 completion and verified publication

P05-T01/T02/T03 complete. Privacy-safe source/evidence commit
23db069a32618678a04bd8a0fa58d3d9ed723e99 normally pushed; git ls-remote
confirmed exact topic head. Base remains51db4fa8, no rebase/force push.
Following commit changes only completion artifacts; exact final head is
reported in PR #375 and verified against its headRefOid/remote ref.
Review gate remains independent Revise, not overridden by local success.
Stop after final evidence push; no merge, issue closure, live resource action,
new Research/Plan/Review, child task or waiting indefinitely for human login.
