---
title: Demo setup readiness implementation plan
description: Bounded issue 360 full-loop delivery plan
ms.date: 2026-10-17
---

Task: issue-360 / demo-setup-readiness-360. Mode: automatic.
Status: Same-session continuation authorized for PR #375: rebase onto latest
origin/main, preserve merged #358 contracts, validate integrations and establish
concrete private publication/IAM blockers. Historical Review remains unchanged;
d/e remain unmet. No new delivery loop or merge.

## Executive Summary

Remove private console dependence by relaying only bounded authenticated
ciphertext through tags on the existing initializer job. Keep the encryption
key only in the owned temporary job secret/operator memory. Deploy the browser
credential through a minimal ARM secureString template into the existing
private vault; verify write-only metadata, never read a secret back. Neither
path needs public backing access, another service or a Graph token in Azure.
Scoped tag/restart permission activation and private image publication remain
explicit human blockers. Evaluate additive migration of the existing immutable
API image to the already-ready external environment; never retire the old path
until real sign-in, roles, SQL and AI pass.

## Sources

Research: `.copilot-tracking/research/2026-10-17/demo-setup-readiness-360-research.md`
(C1-C8/W1-W5). Issues #360/#349/#350/#358; merged #370.

## User Decisions and Requirements

* Complete Research -> Plan -> Implement -> Review, dated committed artifacts
  and persistent phase completion; publish a Refs #360 PR, no merge or closure.
* Use the existing assets; one laptop command, no private-host primary workflow.
* Preserve SQL/data/images/identity/configuration, ama and backing isolation.
* Retain owner migration/image and Key Vault selection approvals; do not infer
  app-secret fallback, role-assignment authority or a new billable build path.
* Graph/login stay with a human operator; this VM is a service principal.
* Do not edit the expiry or secret-preservation portions owned by #358.
* Stop after publication, or an exhausted concrete human blocker; no child loop.

## Goals

Laptop transport works without console access; safe credential storage is
available via ARM; live readiness and remaining operator actions are factual.

## Scope and Non-Goals

Transport/worker, credential transport adapter and surgical wiring, narrowly
scoped offline RBAC definition, existing tests, runbook/evidence/index/log.
No new framework, public backing route, Graph mutation, data reseed or teardown.
No permission deployment, paid agent pool or unsupported image build.

## Functional Requirements

* Preserve AES-GCM run/operation/digest binding; require both authenticated result
  and terminal Succeeded. Missing/tampered/oversized/failed results fail closed.
* Relay on the verified existing initializer only; bounded tag frames, Merge
  only per-run keys; Delete only owned run keys. Never change source job config.
* Stop/delete owned temporary job before cleaning result tags and before return.
  Unknown cleanup blocks success; recoverable name only, no private payload.
* A parent initializer can serve the demo only if both environments are verified
  in the same ama VNet; execute the temporary job in the API's actual subnet.
* ARM credential template has one selected vault child secret, secureString
  value, epoch expiry and no secret outputs. Strict what-if scope before apply,
  bounded completion and enabled/name/expiry metadata verification.
* `--run-in-azure` uses Key Vault via ARM; no automatic app fallback on failure.
  Reject explicit/recorded app mode and app-backed current credentials before
  reconciliation/Graph writes; do not migrate or rotate them. Existing
  private-host/explicit app mode behavior outside this mode remains.
* Migration stages with an ingress deny-all IPv4 rule; verify auth/runtime
  before a separately reviewed rule-removal transition. The public FQDN stays
  stable for laptop management-plane setup; missing real registration means
  leave the rule in place, not expose an unauthenticated replacement.

## Non-Functional Requirements

No private input in command arguments, logs, artifacts or plaintext tags.
No operator token uploaded. Sanitized errors and existing timeout conventions.
Tag read/write permission limited to existing initializer resource; API restart
role stays API-only. Live role changes are blocked, regardless of ambient Owner.

## Acceptance Criteria

* Focused regression proves ARM-only result path, no console invocation,
  tamper/timeout/failure/cleanup, tag preservation/limits and same-VNet guards.
* Credential regressions prove secure body files, exact what-if scope,
  read-only mode, expiry/metadata verification and no fallback.
* Existing setup/private worker/full infra suites and exact relevant lint/type
  checks pass, source packages installed with pip. Docker remains Not run.
* Reviewed narrow migration what-if either permits a preservation-checked
  additive apply, or records the exact safety/prerequisite blocker.
* Criterion audit a-f separates implemented/offline, live Pass, Not run and
  blocked; no 302, redirect or source existence is accepted as sign-in.

## Phase Checklist

<!-- phase: P01 -->
### P01 - Implement laptop-safe transports

* [x] P01-T01 Replace console capture with bounded encrypted ARM tag relay.
* [x] P01-T02 Add minimal secure ARM credential deployment and surgical wiring.
* [x] P01-T03 Extend offline scoped RBAC and tests; coordinate #358 boundary.

<!-- phase: P02 -->
### P02 - Validate and execute authorized readiness actions

* [x] P02-T01 Install source packages after observed import failure; focused then
  full infra tests, relevant lint/type/Bicep checks.
* [x] P02-T02 Review exact additive API migration what-if/preservation; perform
  only supported authorized changes, record resource actions and HTTP results.
* [x] P02-T03 Update runbook, evidence, index and append-only knowledge log.

<!-- phase: P03 -->
### P03 - Review and publish

* [x] P03-T01 One post-implementation Review; route later findings, no review loop.
* [x] P03-T02 Reconcile state, persistent completions, criterion audit; commit,
  push and create Refs #360 PR; record exact remote head in publication receipt.

## Test Ownership and Locked Validation

<!-- phase: P04 -->
### P04 - Owner-authorized upstream integration and blocker evidence

* [ ] P04-T01 Rebase run-owned topic onto latest origin/main, preserving upstream
  #373/#374 source/tests and both index/log histories; integrate ARM transport
  without changing #358 expiry/inventory/pending-handoff/legacy CLI contracts.
* [ ] P04-T02 Add focused combined secret-path regressions, run full relevant
  infra/legacy and existing lint/format/type gates; report any material finding.
* [ ] P04-T03 Research existing private build/import/CI reuse options, distinguish
  actual failed tools/permissions from unattempted authority-limited actions.
  Execute only already authorized existing-resource/no-new-spend paths.
* [ ] P04-T04 Commit and authorized force-with-lease topic push to PR #375,
  report exact new SHA to independent reviewer 4536f9cc; keep #360 open and stop.

## Continuation Test Boundary

Preserve all upstream #358 tests exactly, with additive integration tests owned
by test_staff_azure.py within the original 25-addition budget. Full infra and
legacy suites plus existing CI lint/type/Bicep gates remain required.

## Test Ownership and Locked Validation (Original Scope)

Canonical tests: infra/tests/test_staff_azure.py (relay/worker/integration),
infra/tests/test_setup_entra.py (only credential transport additions, not expiry/
preservation), new focused credential ARM tests if needed, test_identity_rbac.py.
Exact removals: none. Maximum additions: 25 targeted tests, no generated tests.
Semantic assertions cover security boundaries; existing SQL/Graph tests retain
regression ownership. Existing workflow lint/mypy selectors include new modules.
No new test framework or dependency. Docker/live Graph/human acceptance not run.

## Critique Disposition

Executed exactly once:
`.copilot-tracking/reviews/2026-10-17/demo-setup-readiness-360-plan-critique.md`.
Verdict Revise, three findings, all directly resolved by current owner intent:

* PC-001 accepted: pre-reconciliation Azure-mode compatibility guard blocks
  app-backed credentials/recorded/explicit store. No #358 selection edits.
* PC-002 accepted: additive API starts with deny-all ingress; separate exact
  what-if and verified real auth/runtime required before removing the rule.
  Without tenant prerequisites, staging stays restricted and exposure blocked.
* PC-003 accepted: material Review findings block readiness; publish only a
  clearly blocked draft if any remain, no more live actions and no second
  Review. Known deployment prerequisites alone are not source defects.

Plan complete on 2026-10-17; persistent completion recorded here. No second
critique, source edits or Azure writes during Plan.

## Follow-Up Items

1. Authorized image publisher: approved private push/build path with no registry
   public-access or bypass change. Existing ACR has no private task pool.
2. Authorized IAM operator: explicitly approve/activate source-job tag and
   API-only restart roles after reviewed what-if. No live role writes here.
3. Tenant operator: isolated human login, authorized registration/mailbox/roster
   and browser role/session checks; AI/config/parity from #349/#350.
4. Retirement only after #360 d and clear destructive authorization.

## Handoff

Changes path:
`.copilot-tracking/changes/2026-10-17/demo-setup-readiness-360-changes.md`.
Original Plan handoff authorized Implement with the above gates; no source or
Azure writes occurred in Plan. Current delivery completed Research/Plan/
Implement/Review and published PR #375. The publication receipt records the
observed remote head; its final receipt-only commit is resolved by Git/PR head.
No remaining source implementation or current-task Review, merge or closure.
