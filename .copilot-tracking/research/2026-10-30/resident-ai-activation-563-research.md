<!-- markdownlint-disable-file -->
# Task Research: resident-ai-activation-563

| Field | Value |
| --- | --- |
| Date | 2026-10-30 |
| Researcher | RPI Agent / rpi-research |
| Status | Complete; activation blocked |
| Artifact path | .copilot-tracking/research/2026-10-30/resident-ai-activation-563-research.md |

## Research Brief

Research exact optional resident model settings, identity, live deployment,
cost/expiry enforcement and safe verification/rollback for #563.
Audience: owner and activation reviewer. Output mode: convergence.
Scope: resident code, API guide, existing ca-resident-demo and
aoai-resident-469 in RG ama. No employee activation or source redesign.
Criteria: explicit consent, own-record grounding, labelled model/fallback,
exact private backup before mutation, narrow identity role and reversible change.

## Research Parameters

Focused posture, selected for the owner's bounded operations request.
Evidence root: .copilot-tracking/. Read-only research; only evidence/state writes.
USD20 ceiling; pilot approval expires 2026-11-01; redeploy authority ends
2026-11-15. Keep minimum replicas zero and every job Manual. No new resource
groups, private endpoints or broad roles. Never delete ama. At most two
resident sign-in attempts; credentials may be read only inside automation.
No push. Local commit only, Refs #563.

## Extension Registry and Provenance

Repository guidance applies to all paths. Selected rpi-research and subsequent
explicitly requested RPI phases. Web design skills are not applicable to this
configuration-only operation; no UI edits or conformance claim planned.
Independent critique and Review will use bounded registered agents.
No research delegation: one tightly coupled low-volume investigation.

## User Participation and Research Decisions

The explicit full-loop request authorizes sequential phases without routine
questions. Owner activation approval supplied at 2026-10-30T16:31Z.
Non-interactive execution; concrete unsafe prerequisites will block mutation.

## Direction Controls

Only the named resident app and model account; prefer managed identity.
Back up exact app configuration privately, never expose secret values.
Roll back if verification fails. Record commands/results in changes evidence.

## Research Questions

| ID | Question | Status |
| --- | --- | --- |
| Q1 | What exact settings and model authentication does resident code accept? | Open |
| Q2 | Can existing Azure resources enforce cap/expiry without scope expansion? | Open |
| Q3 | How to prove live consent, grounded AI, fallback and denied/unset paths safely? | Open |

## Prior Knowledge Gate

Read original specification, addendum, reference index, owner memory and sector
primer. Clean worktree on owner-selected ops/resident-ai-activation-563;
no open PR on this head. Issue #563 remains open with live criteria unproved.
Do not treat prior source delivery or owner approval as live proof.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Starting areas: src/api/README.md, resident modules/tests, infra guides,
read-only Azure app/account/deployment/job metadata.
Initial guide search distinguishes employee AI_ENDPOINT from resident settings;
resident configuration must be traced separately.

Reflection: existing account, model, identity and scale are suitable. Source
deployment history says the last SQL initializer did not migrate AI accounting;
presence of the model account cannot establish the ledger.

#### Wave 2: Deeper

Traced startup wiring and SQL reservation code (C1-C4). Only two new environment
variables are accepted; existing MSI SQL settings provide the model identity.
No configurable cap/expiry variables exist: both boundaries are pinned in code
and SQL, not the later portal-access expiry. Existing resource-scoped model
role already exists, so no role creation is necessary.

Reflection: verifying SQL procedures, permissions and remaining headroom is a
mandatory prerequisite. Do not enable first and infer cap safety from fallback.

#### Wave 3: Contrarian

Considered keys, developer inference, changing networking, running/mutating a
private job and trying activation before inspecting the ledger. Rejected:
keys are disabled/unsupported, developer inference bypasses resident admission,
and network/job changes exceed resident-app-only scope. Direct read-only SQL
preflight obtained a token only in memory and received Azure SQL 47073
(public network interface disabled). TCP reachability does not mean SQL access.
No VM exists in ama. Private ACR manifest lookup also returned firewall denial;
prior committed rollout evidence supplies deployed digest provenance instead.

Reflection: no safe currently authorized route establishes accounting headroom
or migration state. Stop activation rather than weakening a prerequisite.

## Evidence Log

| ID | Source | Finding |
| --- | --- | --- |
| C1 | src/api/README.md:1021-1048 | Exact settings, SQL prerequisites, USD20 and November1 boundary |
| C2 | src/api/src/zava_forward/api/resident_demo/aoai.py:342-361 | Only ENABLED/ENDPOINT accepted, existing SQL MSI client selects identity |
| C3 | src/api/src/zava_forward/api/resident_demo/assistant.py:12 | Exclusive 2026-11-01T00:00:00Z tariff expiry |
| C4 | infra/sql/resident-assistant.sql:1-74 | Locked lifetime 2000-cent cap; one-cent admission; five attempts/hour; no refunds; narrow EXECUTEs |
| C5 | infra/README.md:3567-3593 | Existing authorized private SQL administrator must verify/apply before activation |
| C6 | .copilot-tracking/changes/2026-10-30/demo-sites-redeploy-1030c-changes.md:69-80 | Latest initializer explicitly did not migrate AI accounting |
| C7 | Azure read-only queries, 2026-10-30 | Existing account-only OpenAI User role; model gpt-4.1-mini 2025-04-14; app min0/max1; eight Manual jobs |
| C8 | External resident_sql_preflight.py execution, 2026-10-30 | Read-only connection blocked by SQL 47073; no query/migration ran |

## Findings, Alternatives and Decision State

Q1 answered by C1-C4. Q2 blocked for actual SQL state by C5/C8. Q3 has a
source-backed Playwright pattern in
src/api/checks/resident_generated_answer_browser_check.py:78-179, but actual
live proof must wait for safe activation. It must include no-consent refusal,
real grounded repair answer, thin AI label, collapsed sources and out-of-scope
rules/manual route; outage/disabled proof must be distinguished from mocking.

Selected recommendation: perform private exact configuration backup and
document a safety-blocked activation without any Azure mutation. Reject
keys, broad RBAC, network opening or accounting resets. Defer authenticated
browser verification and paid inference rather than misrepresent them.

## Open Questions, Risks and Residual Uncertainty

Actual ledger/procedure presence, permissions, reserved cents and remaining
per-resident attempts are unknown. Need an already authorized private SQL
execution route and reviewed read-only receipt (or separately approved
accounting migration). No spend or headroom is inferred from old source.
The portal's December31 serving expiry is not AI authority.

## Planning Readiness

Research disposition: executed. Ready for a blocked-safe operations plan;
not ready for live activation. One complete focused cycle covers the scoped
questions; further public queries cannot resolve private SQL state.
Self-check: source IDs and ordered waves recorded, alternatives explicit,
no secrets, no source/Azure writes, no legal or live acceptance claim.
