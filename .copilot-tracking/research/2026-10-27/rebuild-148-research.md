<!-- markdownlint-disable-file -->

# Task Research: rebuild-148

| Field | Value |
| --- | --- |
| Date | 2026-10-27 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-27/rebuild-148-research.md |

## Research Brief

* Research repeatable from-empty rebuild and ordered teardown for #148.
* Audience: repository maintainers reviewing a source-only draft PR.
* Scope: existing infrastructure helpers, package layout, local synthetic tests.
* Non-goals: deployment, cloud reads/writes, private data, secrets, deleting ama.
* Criteria: all four issue criteria mapped to actual evidence or explicit gaps.
* Requested outputs: research, plan/details, implementation/change record, Review.
* Output mode: convergence.

## Research Parameters

* Posture: focused, selected for the bounded named issue.
* Internal candidates: infra/README.md, ADR 0002/0006, src packages and tests.
* External candidates: named GitHub issues only; no cloud inspection.
* Resolved evidence root: .copilot-tracking/.
* Limits: local tests only; no --all gate; at most one locked --changed gate
  for large work. No uv, secrets, private datasets or Azure deployment.

## Extension Registry and Provenance

* Repository instructions selected for layout, evidence and branch safety.
* RPI skills selected in order; one independent critique and one Review.
* Domain research agents skipped: this is one coupled internal trace.
* Web, legal and AI skills skipped: no relevant changes intended.

## User Participation and Research Decisions

The explicit full-loop request authorizes phase progression for this task.
No interaction is needed for the source-only scope. Actual resource destruction,
live disposable-environment acceptance and tenant approval remain outside scope.

## Scope and Success Criteria

Read #148, dependency #138 and parent #136. Existing branch feat/rebuild-148
has no PR and started clean. Reuse it for one draft PR targeting main.

## Task Research Requests

Determine safe reusable sequencing, dependency deletion ordering, synthetic
seed/staff boundaries and locally provable acceptance.

## Direction Controls

* Authoring/local validation only; never deploy or delete ama.
* Do not infer cloud acceptance from mock or disposable local tests.
* Use Refs #148 unless every criterion is proven.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What current helpers and architecture define the rebuild? | depth | answered |
| Q2 | How can teardown be bounded and verified without deleting ama? | depth | answered |
| Q3 | What synthetic seed/staff tests can run entirely locally? | depth | answered |

## Prior Knowledge Gate

Read original/addendum, knowledge-base index and owner memory. Issue #148
describes the 2026-10-12 manual rebuild; verify against current implementation
before reusing it. #138 remains open, so dependency acceptance is not assumed.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Read named issues and route through current infra README, ADRs and package guides.
Inline investigation avoids splitting one continuous execution trace.

Reflection: pipeline helpers already exist; the old issue description does not
establish that their live deployment gates have been satisfied.

#### Wave 2: Deeper

Current rebuild requires dependency-only deployment, immutable images, a separately
authorized credential boundary, SQL grants/seed, app deployment, auth/staff
reconciliation and identity-bound postchecks (C3). ADR 0006 assigns all new code
to src packages (C4). An orchestrator-owned checked sequencing engine can own
these contracts without adding another deployment/credential implementation.

Reflection: no secret or arbitrary command needs to enter the sequencing API.
The existing deployment/release/auth helpers stay authoritative. A disposable
local backend can test the actual sequencing, persisted SQL seed/staff checks
and teardown inventory contracts without pretending to implement Azure.

#### Wave 3: Contrarian

Challenge: a sorted generic resource list is insufficient. Budgets are a separate
inventory, resource children must precede parents, apps/private endpoints precede
environment/network, Foundry projects precede accounts, and AMPLS precedes linked
components. Unknown resource types, locks, cross-group IDs, disappearing/changing
inventory and unconfirmed deletion must fail rather than be skipped (C3, C5).
Immutable storage/legal holds may prevent removal and must not be bypassed.
Tenant reconciliation cannot be simulated as real Entra acceptance (C6).

Reflection: select a source-only sequencing engine, offline dry-run and explicitly
synthetic disposable SQLite backend. Do not ship an Azure apply path that would
guess destructive scope/retention authority, tenant provisioning or preservation
of the continuing private 60,000-home/980-case lineage.

#### Parent Synthesis and Disposition

* Accepted C3-C5: fail-closed sequencing and explicit ordered resource contracts.
* Accepted C6-C7: local proof is not application or tenant acceptance.
* Rejected a second Azure driver: duplicates #138/#360 helpers and would require
  unresolved exact-resource preservation/retention and tenant approval.
* Deferred actual Azure adapter and disposable Azure exercise to authorized work.

#### Cycle Re-entry Evaluation

No further cycle needed for authoring/local scope: relevant contracts covered.
Fresh cloud evidence could change acceptance, but is expressly excluded.

## Evidence Log

| ID | Claim | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Two-phase bootstrap prevents unauthenticated placeholder workbench | infra/README.md:201 | high |
| C2 | Existing wrapper rejects non-ama groups and preserves images | infra/README.md:218 | high |
| C3 | Manual sequence and separate budget inventory | infra/README.md:3037 | high |
| C4 | New code belongs in isolated src packages with external tests | docs/adrs/0006-src-layout-and-cutover.md:58 | high |
| C5 | Locks, immutable audit storage, and child resources exist | infra/modules/storage.bicep:1 | high |
| C6 | Real tenant/SQL setup is distinct from synthetic staff data | infra/scripts/setup-entra.py:1942 | high |
| C7 | Local/mock checks do not satisfy deployed application acceptance | docs/brds/agentic-retrofit-programme-brd.md:1487; docs/prds/zava-forward-retrofit-programme-demonstrator.md:509 | high |
| W1 | Four criteria; dependency #138 and parent #136 remain open | https://github.com/jmservera/ama/issues/148 | high, retrieved 2026-10-27 |

## Findings Mapped to Questions and Evidence

Q1: reuse existing helper contracts (C1-C4); no workflow rename.
Q2: bounded exact-ID inventory plus ordered deletion and readback (C3, C5).
Q3: generated reserved-domain staff and SQLite seed/reopen checks (C6-C7);
do not read any operator-selected dataset or profile.

## Alternatives and Decision State

Selected: a standard-library orchestration contract and local disposable adapter
in src/orchestrator. Emit the full rebuild stage list in a no-I/O dry-run.
Execute local stages and dependency teardown with SQLite state, two inventories,
fixed synthetic data and explicit verification. Production helpers are named
integration points, not invoked or represented as complete integration.

Rejected: direct cloud script under infra/scripts (violates new-code placement,
duplicates helpers and crosses current authorization). Rejected: unconstrained
shell hooks (cannot establish secret-free command lines or checked steps).

## Open Questions, Risks, and Residual Uncertainty

Cloud disposable-environment evidence cannot be produced under this authorization.
Exact preservation/deletion/retention authority, private lineage restoration,
tenant permissions, credential provisioning and #138 live acceptance remain
required before live automation. No human decision is needed for independent
authoring; no live decision is guessed.

## Current Decisions

* Confirmed, owner scope: authoring/local validation only; Refs #148.
* Proposed, C3-C7: local engine delivery is partial and does not close #148.

## Potential Next Research

Deferred: authorized exact-resource/retention/preservation inventory and #138
integration readiness, when owner selects a later live-automation task.

## Planning Readiness

Ready for independent authoring only (C3-C7). Research disposition: executed.
No authoring blocker. Whole-issue acceptance is not Ready.

## Closeout Record

Research Complete; Wider, Deeper and Contrarian executed inline; self-check
passes for this scope. No delegated research. No source edits in Research.
Continuation owner: explicitly requested full-loop RPI Agent.

## Advisory Next Step

Parent transitions to Plan after persisting intent; no additional owner action
needed for source-only authoring. Evidence path is this primary artifact.

## Sources

W1: https://github.com/jmservera/ama/issues/148 (retrieved 2026-10-27).
Linked dependency #138 and parent #136 were also read via gh issue view.

## Artifact Self-Check

Questions answered; ordered waves and reflections complete; posture, scope,
extension provenance, participation, evidence, alternatives, decisions,
uncertainty and readiness recorded. No secrets or private datasets read.
