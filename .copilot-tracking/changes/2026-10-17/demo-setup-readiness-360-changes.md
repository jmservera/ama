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
