---
title: Issue 211 rule-card research
ms.date: 2026-10-16
---

## Research Brief

Implement issue #211 in the existing src core and API projects. Audience: maintainers
and exercise reviewers. Output mode: convergence; posture: focused, selected from
the explicit bounded task. No private data, new legal interpretation, live approval,
workload imports into core, or Azure changes. Research disposition: executed.

## Research Parameters and Direction Controls

Use the issue acceptance criteria, owner comments and ADR 0006. Preserve exercise
labels and existing append-only evidence. The user explicitly requests automatic
Research, Plan, Implement, Review, local validation, commit, push and PR to main.
Do not read properwarm.json, .env or .vscode. No interaction is needed: direction
and permitted publishing actions are explicit.

## Extension Registry and Participation

Repository instructions and ADR 0006 govern placement and evidence. RPI research
is selected for evidence; planning, implementation and review follow under the
explicit parent. Legal/privacy skills are not selected: no legal assessment is
being made. No research delegation: this is one tightly coupled store/API trace.

## Research Questions and Prior Knowledge Gate

1. Which behavior is already merged, and what remains caller-controlled?
2. How can existing authenticated identities enforce independent rule roles?
3. How can law source ingestion retain approved cards across both SQL adapters?

The initial issue statement alone is insufficient: merged #250 supplied a core
store, but the owner explicitly left identity binding open.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Read the issue with comments, original case study, relevant addendum sections,
knowledge-base index/memory, ADR 0006, parity matrix and all five project README
entry points. Existing core rulecards and lawstore are migrated; API exposes
read-only law routes, not rule-card writes. Reflection: extend, do not duplicate.

#### Wave 2: Deeper

Trace core lifecycle, source ingestion, database adapters, API authentication,
CSRF and endpoint inventory. Rulecards currently requires raw SQLite, commits
each event, accepts caller roles, and is not connected to law source ingestion.
TrustedProxyProvider validates tenant and maps one staff app role to provisioned
staff. Reflection: carry separate rule capability claims alongside the existing
staff role, using authenticated staff email for durable author/owner identity.

#### Wave 3: Contrarian

Challenge UI-only gating, shared-password approvals, dual-role self-approval,
placeholder owners, malformed dates, partial supersession and source changes.
Reject caller-supplied role/actor/date fields and password-provider authority.
Keep unassigned fixture owners and exercise-only approval labels. Serialize
entire mutations in one transaction, not individual events; use the existing
law SQL adapters rather than a second storage implementation.

#### Parent Synthesis and Disposition

Accept reuse plus server-derived dedicated rule claims. Keep every card exercise
only; owner nomination is not approval. Retain old snapshots, versions and events.
No second cycle needed: the remaining questions concern bounded implementation
and validation, not unavailable policy decisions.

## Evidence Log

* C1: `src/core/src/zava_forward/core/rulecards.py:1` existing lifecycle,
  append-only tables, two draft exercise seeds and review records.
* C2: `src/core/src/zava_forward/core/lawstore.py:135` existing SQLite and
  SQL Server adapters; `:273` ingestion appends versions without notifying cards.
* C3: `src/api/src/zava_forward/api/auth.py:100` trusted principal validation
  binds a staff record and app role; existing separate rule capabilities absent.
* C4: `src/api/src/zava_forward/api/server.py:478` authenticated POST and CSRF
  boundary; `:230` read-only law routing.
* C5: `src/api/tests/test_role_endpoint_inventory.py:58` route inventory gate.
* C6: `docs/adrs/0006-src-layout-and-cutover.md:64` src-only dependency contract.
* C7: `docs/architecture/mvp-to-src-parity-matrix.md:1` migrated implementation
  remains distinct from outstanding owner, rule-engine and UI acceptance.
* W1: https://github.com/jmservera/ama/issues/211 retrieved 2026-10-16:
  acceptance criteria and owner comment explicitly leave caller-role binding open.
* W2: https://github.com/jmservera/ama/issues/211#issuecomment-6196718708
  retrieved 2026-10-16: ADR 0006 location update; criteria unchanged.

## Findings, Alternatives and Current Decisions

C1-C4 answer questions 1-3. Selected: extend RuleCardStore with the law adapters,
transactional writes and input validation, attach to LawStore, and expose a
staff-readable API with trusted-proxy-only rule write capabilities. Dedicated
`ZavaForward.RuleAuthor` and `ZavaForward.RuleOwner` claims do not grant a staff
workbench role by themselves. Reject mapping ordinary programme roles to legal
approval authority. Agents receive no approval interface.

## Open Questions, Risks and Potential Next Research

Real tenant assignments, human approval of specific cards, current-source legal
review, rule-engine integration and operational UI acceptance remain unevidenced.
These do not block the labelled local engineering slice. SQL Server/Azure behavior
must not be claimed observed without a corresponding run.

## Planning Readiness and Closeout

Planning Readiness: Ready. Research disposition: executed. Evidence covers the
bounded change. Parent may advance to Plan under the user's full-loop request.
Artifact self-check: evidence pointers, alternatives, three ordered waves,
authority limits and remaining acceptance gaps are recorded.
