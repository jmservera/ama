<!-- markdownlint-disable-file -->
---
title: Issue 349 correction3 research
description: Bounded Azure AD provider readiness investigation
ms.date: 2026-10-22
---

## Research Brief

Confirm the Container Apps runtime auth response shape and existing checker
semantics before correcting provider-enabled readiness. Audience: PR #437
coordinator. Output mode: convergence preparing planning. Posture: focused,
selected from the owner's bounded finding.

## Research Parameters and Direction Controls

Task: issue349-tenant-readiness-preflight-correction3. Starting HEAD:
3b881a65c808b02f6ca1bd29d227172f5ad453f6. Reviewed base:
b4d467cad84535ed106cffa1ae9aa303db7bfed2. Work only in this worktree.
Writes limited to checker, tests, and this correction's RPI artifacts.
No tenant/Graph/Azure writes, credential access, deployment, acceptance ticks,
issue comments, PR changes, or push. One local commit and exactly one full gate.

## Extension Registry and Participation

Repository instructions and RPI research protocol selected. Domain/UI skills
not applicable to this read-only backend checker. Research specialist skipped:
one tightly coupled, bounded trace is handled inline. Prior findings are claims
to verify, not instructions. No intake question needed: owner supplied scope,
phase progression, commit authority, gate base and stop conditions.

## Questions and Candidate Areas

* Q1: What JSON structure does the runtime query return?
* Q2: Which flags are required, and how does malformed state behave?
* Q3: Which synthetic tests establish fail-closed and positive behavior?
* Internal: checker, its tests, Container Apps Bicep, previous RPI evidence,
  component gate instructions.
* External: official ARM schema only if local runtime-shape evidence is insufficient.

## Research Cycle Log

### Cycle 1: Wider

Inspected checker, tests, Container Apps auth Bicep and correction2 changes.
Reflection: platform and provider configuration are distinct; existing tests
provide projected responses rather than raw ARM responses.

### Cycle 1: Deeper

Traced the public Azure CLI show handler to its decorator: it returns the
`current` auth resource's `properties`, not the ARM envelope (W1/W2).
Consequently the existing root-level `platform.enabled` query is correct, and
the additional root-level path is `identityProviders.azureActiveDirectory.enabled`.
Reflection: add a projected `providerEnabled` boolean without changing commands
or requesting any registration/credential data.

### Cycle 1: Contrarian

Challenged truthiness: Python `1 == True`, but `1 is True` is false. Missing,
null, string, number, object and array provider projections must fail closed.
The existing `auth-disabled` mismatch reason already covers non-true platform
state and can remain stable for either flag. A separate finding would change
the public check schema unnecessarily. Reflection: strict conjunction preserves
the existing schema, diagnostics and independent checks; no early return needed.

## Evidence Log and Findings

| ID | Finding and question | Source |
| --- | --- | --- |
| C1 | Q1/Q2: deployment enables platform and provider separately | infra/modules/containerapps.bicep:190,194,213-215 |
| C2 | Q1: AUTH_QUERY projects properties; exact allowlist guards query equality | infra/scripts/tenant-readiness-preflight.py:51-60,93-104 |
| C3 | Q2: only strict platform true currently makes auth ready | infra/scripts/tenant-readiness-preflight.py:348-374 |
| C4 | Q3: fake positive response is projected; CLI tests expose code, text/JSON and sanitization assertions | infra/tests/test_tenant_readiness_preflight.py:42-58,425-449 |
| C5 | One full committed-head gate and external receipt required | src/README.md:47-114 |
| W1 | show_auth_config delegates to ContainerAppAuthDecorator.show | https://raw.githubusercontent.com/Azure/azure-cli/dev/src/azure-cli/azure/cli/command_modules/containerapp/custom.py (retrieved 2026-10-22) |
| W2 | decorator.show returns client.get(... current)["properties"] | https://raw.githubusercontent.com/Azure/azure-cli/dev/src/azure-cli/azure/cli/command_modules/containerapp/containerapp_auth_decorator.py (retrieved 2026-10-22) |

## Alternatives and Current Decisions

Accepted: project `providerEnabled` and require both fields `is True` (C1-C4).
Rejected: truthiness, platform-only or registration-presence inference; all can
admit disabled/malformed state. Rejected: separate check/reason or early return,
which unnecessarily changes the stable reporting contract and other diagnostics.
No production source edits during research. No live tenant calls.

## Uncertainty, Further Research and Self-Check

Two attempted official REST/schema URLs returned HTTP 404; no schema content
was inferred from them. W1/W2 plus local Bicep resolve the response shape.
Public CLI `dev` is moving evidence, not proof of the deployed extension version.
No live configuration was read and no actual tenant readiness is claimed.
No further research needed for this bounded correction; all three questions
answered, evidence mapped, contrarian wave complete, no material blocker.

## Planning Readiness

Research disposition: executed, complete. Planning Readiness: Ready.
Parent continues to Plan under the owner's explicit ordered-loop request.
