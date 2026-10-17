<!-- markdownlint-disable-file -->
---
title: Issue 358 credential preservation research
description: Focused RPI evidence for credential expiry and Container App secret references
ms.date: 2026-10-17
---

## Research Brief

Research stored-but-expired credentials, Key Vault-reference preservation during
secret rebuilds, and the legacy delegating CLI for issue #358. Audience: owner,
reviewer and #360 coordinator. Output mode: convergence, preparing planning.
Scope: existing infra setup code/tests, linked merged PRs and runbook/evidence.
Non-goals: broader setup/job readiness, runtime redesign, cloud or directory
writes, secret/private dataset reads, image builds, spend and network changes.
Success requires real failing-before regressions, killed guard/KV mutations,
existing infra validation, and an explicit unmet-criterion audit, not invented
non-production acceptance.

## Research Parameters

| Field | Value |
| --- | --- |
| Posture | Focused, selected from the owner's surgical scope |
| Resolved evidence root | .copilot-tracking/ |
| Initial internal candidates | infra/scripts/setup-entra.py; infra/tests/test_setup_entra.py; infra/scripts/initialize-api-auth.py; infra/README.md; docs/architecture/cutover-evidence-pack.md |
| Initial external candidates | Issue #358; merged PRs #356, #352, #370; issue #360; official management schema only if needed |
| Questions | Q1 stored expiry behavior; Q2 complete secret reference reconstruction across shapes/errors; Q3 legacy delegation; Q4 lawful safe live evidence |
| Limits | No Azure/Graph writes, secret values or private data reads, role changes, image builds/new spending, exposure of private services |
| Completion basis | In-scope contracts evidenced and unresolved live gate named |

## Extension Registry and Provenance

| Kind | Candidate | Disposition and authority |
| --- | --- | --- |
| Instruction | Repository guidance, all files | Selected: topic branch, pip venv, evidence honesty, append-only KB log, privacy-safe commit |
| Skill | rpi-research | Selected: three ordered waves, stable C/W evidence IDs |
| Specialist | RPI Researcher | Skipped: this is one tightly coupled trace; inline research avoids duplicate context |
| Skills | RPI plan/implement/review | Deferred until parent-owned phase transition |

## User Participation and Research Decisions

The explicit full-loop request authorizes automatic progression and push/PR,
not cloud actions. Noninteractive operation requires no routine questions.
Live evidence remains conditional on an already authorized safe scope.

## Direction Controls

* Preserve main abaca788, merged PR #370 staff job and CI corrections.
* Keep legacy delegating main(); do not duplicate setup logic.
* Do not weaken crypto, identity or network guards.
* #360 owns broader setup/job readiness; report overlap for sequencing.

## Prior Knowledge Gate

Read the original/addendum, KB index and owner memory (context, not evidence).
Read issue #358 and merged #356/#352/#370 metadata. Worktree was clean on the
requested branch with no existing branch PR. PR #352 already reports retaining
the delegating main(); verify current behavior rather than resolve stale conflicts.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Initial issue/PR/history and scoped code inventory executed inline. #358
originated from #356's expiry/KV coverage gaps. Current code already contains
additional expired-rotation tests, so their exact guard coverage needs deeper
inspection. #352 is merged and retains delegated compatibility. #370 is merged
and must not be disturbed.

Reflection: prioritize the stored-and-selected expired pair, secret rebuild
response shapes, and error ordering. Historical mocked expiry coverage is not
evidence that the stored-expiry guard bites.

#### Wave 2: Deeper

Traced expiry selection, both generated-name and legacy-name reuse branches,
the raw listSecrets rebuild, and final verification. C3's existing test expires
a generated-name credential; it does not cover the selected legacy-name branch.
C4 rebuilds directly from listSecrets without reconciling known configuration
references or validating items. C5 polls only for the new name. Public schema W6
allows name/value/identity/keyVaultUrl but requires none of the individual fields.
The production code therefore needs fail-closed reconstruction, not a claim that
every service response will contain every field.

Reflection: add coverage for generated and legacy expiry, fixed time boundaries,
full and sparse KV responses, omitted references, missing app values and malformed
inventory. Retain current guards and reconstruct only from actually read-visible
metadata/value entries; do not attempt to recover an omitted secret value.

#### Wave 3: Contrarian

Challenged the assumption that the current rotation test closes the issue:
it covers only the generated-name branch (C3). Challenged raw listSecrets
preservation: W6 documents KV fields, but does not require them; a name/value
shape can lose known metadata under C4. Challenge safe success: C5 can accept
a response missing an old reference once the new name exists. Challenge live
proof: a schema read or offline PATCH mock cannot establish actual preservation.
No live setup/check command is safe within this task's constraints: setup
creates credentials/secrets and --check can create a temporary Azure job (C6).
No cloud scope or permission discovery is needed to conclude those actions
are prohibited; no Azure API was called.

Reflection: add readback reference verification alongside reconstruction.
No broader runtime or job change is justified. Keep the existing CLI regression.

#### Parent Synthesis and Disposition

| Material | Disposition | Evidence and rationale |
| --- | --- | --- |
| Generated expiry test exists | Accepted | C3; augment rather than duplicate only that scenario |
| Legacy expiry is covered by that test | Rejected | C2/C3 use distinct reuse paths |
| Raw listSecrets always preserves references | Rejected | C4/W6; known configuration metadata must survive sparse responses |
| A new name alone proves complete rebuild | Rejected | C5; verify old reference metadata too |
| Live acceptance can be declared offline | Rejected | W1/C6 and owner limits |
| Broader #360 readiness changes | Deferred | W5; different workstream |

#### Cycle Re-entry Evaluation

No further cycle needed for focused delivery. In-scope paths and public schema
settle the implementation decision. Live testing is constraint-blocked, not a
reason to perform prohibited discovery or invent acceptance.

## Evidence Log

| ID | Source | Finding |
| --- | --- | --- |
| W1 | https://github.com/jmservera/ama/issues/358 (retrieved 2026-10-17) | Stored expiry mutation survives prior tests; non-production KV preservation requested; retain delegate |
| W2 | https://github.com/jmservera/ama/pull/356 (retrieved 2026-10-17) | Original setup and offline-only acceptance boundaries |
| W3 | https://github.com/jmservera/ama/pull/352 (retrieved 2026-10-17) | Merged conflict resolution keeps delegate; read-visible preservation limits documented |
| W4 | https://github.com/jmservera/ama/pull/370 (retrieved 2026-10-17) | Merged staff job implementation; preserve unchanged |
| W5 | https://github.com/jmservera/ama/issues/360 (retrieved 2026-10-17) | Separate direct-demo and broader setup acceptance |
| C1 | infra/scripts/initialize-api-auth.py:179 | Legacy main delegates via runpy to setup-entra.py |
| C2 | infra/scripts/setup-entra.py:1229 | Credential selection and secret rebuild investigation target |
| C3 | infra/tests/test_setup_entra.py:988 | Existing expired test covers generated credential only |
| C4 | infra/scripts/setup-entra.py:1292 | Rebuild trusts raw value list and validates only outer list type |
| C5 | infra/scripts/setup-entra.py:1333 | Poll checks only new name, not retained references |
| C6 | infra/README.md:1414 | Azure --check may create/remove temporary job and secret |
| C7 | infra/tests/test_setup_entra.py:1324 | Existing legacy CLI test checks option forwarding and delegated return code |
| W6 | https://github.com/Azure/azure-rest-api-specs/blob/main/specification/app/resource-manager/Microsoft.App/ContainerApps/stable/2025-07-01/ContainerApps.json (retrieved 2026-10-17) | SecretsCollection requires value array; ContainerAppSecret fields name/value/identity/keyVaultUrl are individually optional |

## Findings Mapped to Questions and Evidence

| Question | Finding | Confidence |
| --- | --- | --- |
| Q1 | Both reuse paths require expiry regression and mutation evidence | High, C2/C3 |
| Q2 | Reconcile KV metadata with captured app values, fail before password creation on unsafe inventories, verify reference readback | High, C4/C5/W6 |
| Q3 | Merged conflict resolved; retain existing delegate and regression unchanged | High, C1/C7/W3 |
| Q4 | Actual non-production preservation Not run; no permitted live round-trip here | High, owner limits/C6 |

## Alternatives and Current Decisions

Selected: surgical helper in setup-entra.py plus exact reference readback and
behavioral tests in the existing setup suite (C2-C5/W6). Reject tests-only raw
copy because sparse data can lose known KV metadata. Reject exporting secrets,
replacing KV refs with resolved values, or cloud experimentation because those
violate owner controls. Confidence high for offline contracts, not live behavior.
No frontend, policy, crypto, Graph authority or network change is needed.

## Open Questions and Residual Uncertainty

Actual service acceptance and preservation on existing authorized non-production
resources remain UNMET. Owner/coordinator must separately authorize a safe
round-trip with sanitized before/after reference-only evidence; no real secrets
may be altered/deleted and no private service exposed. Schema is not live proof.
Initial Microsoft Learn and old raw-schema paths returned 404; the corrected
official repository schema above was successfully retrieved.

## Planning Readiness

Research disposition: executed, complete. Planning Readiness: Ready for partial,
offline delivery (C1-C7/W1-W6); live acceptance remains blocked by the explicit
no-write/no-secret-read scope. RPI parent may proceed automatically to Plan.

## Artifact Self-Check

All questions answered or explicitly blocked; all three waves completed in order
inline; evidence IDs, source dates, directions, alternatives, provenance, owner
decisions and honest live limits recorded. No delegated worker claimed.

## Explicit Phase Log

* 2026-10-17 Research opened after status/branch/open-PR safeguards and linked-PR inspection.
* 2026-10-17 Research completed; handoff to Plan with live criterion explicitly unmet.
