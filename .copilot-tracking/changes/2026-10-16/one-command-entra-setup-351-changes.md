---
title: One-command Entra setup changes
description: Implementation evidence and acceptance boundary for issue 351
ms.date: 2026-10-16
---

## Scope and State

Full plan P01/P02 authorized by expanded owner request. Implementation delivered
for review; the one independent Review is Complete / Not accepted. Three
Medium findings block ready delivery. Publication will be draft, not accepted.
Plan/details/critique use the stable one-command-entra-setup-351 slug.
No Azure mutation or private roster read is authorized for this development run.

## P01 Implementation

Implemented the standard-library setup CLI, its isolated safe Azure runner,
typed private user/group roster, tag/name and origin-linked discovery,
additive application/SP/role/callback convergence, bounded human consent
polling, optional app/Key Vault credential handoff and auth/runtime wiring.
The old CLI routes to the new flow while the old imported Python API remains.
API/edge tags are additive; no networking or policy changes.

## P02 Validation and Delivery

101 targeted tests passed, combining:

`PYTHONPATH=/home/azureuser/source/ama-wt/issue-351/src/core/tests:/home/azureuser/source/ama-wt/issue-351/src/agents/tests <session-venv>/bin/python -m unittest infra.tests.test_setup_entra infra.tests.test_initialize_api_auth infra.tests.test_edge_module infra.tests.test_identity_rbac infra.tests.test_bicep_policy -q`

The new setup suite has 39 tests. Initial combined run found source packages
missing; installed core/agents/api editable with pip --no-deps in the isolated
session venv, then reran successfully. Initial ruff was unavailable; installed
ruff/mypy with pip in the same session venv after that observed failure.
New-code ruff (--target-version py310) and mypy passed. Both CLI --help local
launches passed; git diff --check passed. Bicep tests compile locally, not
Azure deployment. No application serving code changed; full API server/SQL/AI
launch is not applicable to this standard-library infrastructure CLI slice.

Updated infra guide, manifest metadata, knowledge index and append-only log.
No private roster, dataset, live identity, secret or environment file was read.
Final preservation-patch validation passed: all 39 new setup tests, ruff,
mypy and git diff --check. Review executed independently once and reproduced
two gaps with memory-only fake data; see its canonical record. PR pending.

## Acceptance Audit

| Criterion | Evidence/status |
| --- | --- |
| Single command, no required arguments, legacy CLI | Implemented; local CLI launch and full fake-az no-argument runs |
| API tag discovery, fallback names, ambiguity and overrides | Offline proven, including wrong-app candidate guidance |
| API/edge discovery across main and pending 344 | Offline proven for linked origin/routes/default/custom domains; local branch/pending diff read only; live topology not exercised |
| App registration, SP, roles, callbacks and safe reruns | Offline proven, including non-UUID sentinel, preservation, unknown-create outcome and no duplicate writes |
| Optional secret handling | Offline proven for app and Key Vault, no secret in output/argv, private-file cleanup and interrupted handoff blocker; live vault identity/secret validity unproven |
| Auth and runtime wiring | Offline proven, including null/disabled auth, HTTPS/proxy, exclusions/token-store preservation and failed rollout verification |
| Private fictional roster, user/group app roles | Partial: generated synthetic identifiers only; actual private file not read; RV-001 shows a fresh planned conflict is rejected only after registration/SP writes; zero-write invalid-role rejection UNMET |
| Consent and human instructions/polling | Offline proven matching Graph User.Read grant and timeout; actual human consent not performed; no automatic broad management grant |
| Isolated device login/profile and SP authority guidance | Offline proven for prompts, missing login, tenant binding, 0700 profile and Option A/B; actual interactive sign-in not performed |
| Python/az/extension/network/Graph preflight and friendly failures | Partial: mocked tools/ARM/Graph checks pass, but RV-002 selected-vault endpoint probe before credential creation is UNMET; actual network/tenant authority unexecuted |
| Check/dry-run and final summaries | Partial: no remote mutation/login/profile creation and drift/pending summaries proven; RV-003 a converged config with an already-Failed rollout can pass check, so failed-no-op detection is UNMET |
| Tests under infra/tests, stdlib implementation | Implemented; 101 combined targeted tests pass |
| SQL staff binding/restart and human browser acceptance | UNMET / not executed; explicit separate private-network/human gates, not claimed by configuration setup |
| Legal/consent/safety boundaries and private data | Preserved; no operational approval or source-currentness claim |
| Push/PR/checks/owner merge | Draft publication pending; ready merge blocked by RV-001 through RV-003; issue body checkboxes intentionally untouched |

## Amendments and Divergences

Critique corrections are incorporated in the final plan. No new user decision.
The old callback-only Python API remains available for existing importers/tests;
the CLI will route to the supported setup flow.
Current-state amendment: add `entraClientSecretName` with the unchanged
historical default and pass it through Bicep. A setup-generated app-bound vault
secret otherwise would be overwritten by the fixed historical reference on a
later declarative deployment. Compiled regression covers forwarding and use.
This is narrowly coupled deployment persistence, not a new feature direction.
Explicit --bearer-only gates intentional service-mode selection; no-argument
runs preserve the existing action and report browser acceptance incomplete.
No automatic-session mode or child task was started.

## Independent Review and Routing

Review: .copilot-tracking/reviews/logs/2026-10-16/one-command-entra-setup-351-review.md.
Execution Complete, outcome Not accepted; three Medium findings, no Critical
or High finding. No second critique/Review or source correction was performed
after this task's one Review. Findings route to later rpi-implement:

* RV-001: preflight fresh planned effective roster conflicts before directory writes.
* RV-002: probe the selected vault endpoint before addPassword, without secret reads.
* RV-003: reject failed/in-progress provisioning even when runtime settings match.

This explicit draft boundary follows the accepted PC-008 delivery gate.
No claim that the script fully satisfies all expanded acceptance criteria.

## Remaining Human Gates

Live tenant execution, admin consent, private SQL bindings/restart and browser
sign-in are unexecuted. Juan Manuel Servera remains the exercise Legal,
Compliance and DPO owner; setup does not activate legal rules or grant approval.
