---
title: Rebuild teardown dependency research
description: Focused evidence for the PR 511 Front Door teardown ordering correction
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

# Task Research: rebuild-148-teardown-order

| Field | Value |
| --- | --- |
| Date | 2026-10-30 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-30/rebuild-148-teardown-order-research.md |

## Research Brief

* What to research: why lexical teardown ordering removes a managed environment before its Front Door consumer, and how to cover the dependency locally.
* Why it matters: resolve the supplied Copilot finding on PR #511, Refs #148.
* Audience or intended use: implementation planning and independent review.
* Scope: orchestrator rebuild module/tests, edge Bicep dependency, component validation commands.
* Non-goals: Azure access, deployment, push, issue closure, unrelated rebuild findings.
* Criteria: prove the source dependency, preserve existing teardown safety, use established test patterns.
* Requested outputs: dated full RPI artifacts, regression, requested local checks and local Conventional Commit.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Q1: What order is required? Q2: What regression and validation prove it locally? |
| Codebase scope | src/orchestrator; infra/modules/edge.bicep |
| External scope | Read-only PR lifecycle and authenticated identity only |
| Initial internal candidate areas | rebuild.py, test_rebuild.py, edge.bicep, orchestrator README and pyproject |
| Initial external candidate areas | None; source-defined dependency |
| Research posture | focused |
| Posture provenance | Default for named source and supplied failure evidence |
| Explicit limits / deadline | No Azure access; no push; /tmp/mv validation |
| Posture-specific completion basis | Focused scope and materiality |
| Edits allowed during research? | No source edits |
| Resolved evidence root | .copilot-tracking/ |
| Known constraints / excluded sources | No private data, cloud fallback or modification of historical RPI outcomes |

## Extension Registry and Provenance

* Precedence: host safety, caller scope, repository instructions, phase skill, supporting extensions.

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
| --- | --- | --- | --- | --- |
| Instruction | .github/copilot-instructions.md and supplied repository guidance | All repository files | Branch reuse, component checks, local-only publication boundary, dated evidence preservation | Selected |
| Skill | rpi-research | Bounded source research | Three ordered evidence waves and readiness | Selected |
| Research specialist | hve-core-all:rpi-researcher | Host-visible independent research agent | Separate bounded lane evidence | Skipped: a single tightly coupled trace, handled inline |
| Skill | Web/design/accessibility skills | Frontend-only descriptions | UI work | Skipped: backend ordering correction only |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision |
| --- | --- | --- | --- |
| Intake | Explicit full-loop request and exact dependency provide sufficient scope; non-interactive execution | User supplied full loop, checks, environment and local-only commit boundary | Execute the requested loop without routine phase prompts |

## Scope and Success Criteria

* Correct profile-before-environment ordering independently of input sequence and lexical names.
* Preserve fail-closed unknown/locked/retained resource handling and all existing relative dependencies.
* Record actual requested check results, independent critique and independent Review.
* Treat synthetic results as local evidence, not Azure acceptance.

## Task Research Requests

* Fix the supplied finding; add a regression in src/orchestrator/tests.
* Run ruff check, ruff format --check, mypy and orchestrator tests using /tmp/mv.
* Commit locally with Conventional Commit and required Copilot trailer; do not push.

## Direction Controls

| Control type | Direction or boundary | Source / checkpoint | Effect |
| --- | --- | --- | --- |
| narrow | Profile dependency ordering and direct regression only | User intake | No unrelated implementation |
| exclude | Azure, push, private datasets | User and repository guidance | Offline checks only |

## Research Questions

| # | Sub-question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | What dependency and current sorting behavior establish the defect? | straightforward | H | answered |
| Q2 | Which existing tests and commands provide a sufficient local regression? | straightforward | H | answered |

## Prior Knowledge Gate

* Reviewed project specification, addendum, reference index, memory, housing primer, component guides and tracking retention policy.
* Existing state: .copilot-tracking/rpi-sessions/2026-10-30/rebuild-148-refresh-state.json records completed refresh, original open findings and publication blockers. Preserve it unchanged.
* Git confirms clean matching feat/rebuild-148 and open PR #511. No branch switch or rewrite needed.
* Cross-session lookup found no recent sessions for this branch; repository evidence remains authoritative.

## Research Cycle Log

### Cycle 1

* Active direction controls: bounded fix, no Azure, no push.
* Active research posture and completion basis: focused; source dependency, tests and validation contracts.
#### Wave 1: Wider

* Inline lane: inspect rebuild module, test inventory helpers, edge template and component README/pyproject.
* Evidence: C1 (shared priority), C2 (Private Link environment target), C3 (existing MemoryBackend and dependency tests), C4 (component checks).
* Reflection: the reported defect is source-backed. The current dependency regression omits Front Door; no Azure investigation is needed. Prioritize sort behavior and the dry-run surface.

#### Wave 2: Deeper

* Inline lane: inspect canonical validation, sort keys, teardown readbacks, dry-run output and full existing rebuild tests.
* Evidence: C1 establishes type priority before depth/name; C3 already exercises fail-closed teardown; C5 shows dry-run derives its type list from ORDER.
* Reflection: a priority correction is sufficient for both actual modeled teardown and advertised dry-run order. /tmp/mv import failed with ModuleNotFoundError for the orchestrator distribution; implementation must install the local packages before running tests. No dependency manifest change is indicated.

#### Wave 3: Contrarian

* Challenge targets: could input reversal or resource depth already resolve the tie; could raising environment priority unnecessarily change other dependencies; does a graph add value for this fixed contract?
* Evidence: runpy reproduction of the existing module printed environment then profile for both input permutations, even with profile name aaa-profile and environment name zzz-environment. Both IDs have equal depth, so namespace lexical order determines the tie (C1). Changing profile priority to 1 preserves app/job priority 0, environment 2 and WAF 3.
* Reflection: no counter-evidence invalidates the report. An explicit dependency graph adds machinery without improving this fixed modeled contract; moving the environment later alters more unrelated ordering. The local backend does not currently seed Front Door, so the existing roundtrip test alone cannot regress this bug (C5).

#### Parent Synthesis and Disposition

| Material / claim | Evidence | Disposition | Rationale | Treatment |
| --- | --- | --- | --- | --- |
| Shared priority reverses teardown dependency | C1, C2 | accepted | Actual offline reproduction and Bicep target agree | Fix profile priority |
| Existing roundtrip alone suffices | C3, C5 | rejected | No profile exists in that fixture | Add dedicated edge-chain test |
| Graph or later environment tier | C1 | rejected | More change than needed for a fixed modeled contract | Keep existing sort structure |
| Actual Azure deletion verification | C2, user constraint | deferred | No Azure access authorized | Explicit residual only |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no.
* Stop basis: exact defect reproduced; source target, safety contracts and check configuration verified.
* Revised brief: none.
* Readiness: Ready; missing local package is a known setup action, not an unresolved design question.

## Evidence Log

* Delegation: inline; one tightly coupled, low-volume source trace does not justify a separate research lane.

### Codebase Evidence

| ID | Claim / finding | Location | Tool | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| C1 | Profile and environment share tier 2; sort uses tier, depth, then lowercased ID | src/orchestrator/src/zava_forward/orchestrator/rebuild.py:79,82,164-175 | view, rg, offline runpy | high | Reproduced environment-first in both input permutations |
| C2 | Front Door origin managed Private Link targets environmentId | infra/modules/edge.bicep:76-89 | view | high | Profile must be removed before its environment |
| C3 | Resource helper and MemoryBackend exercise actual teardown and readbacks | src/orchestrator/tests/test_rebuild.py:34-74,117-165 | view | high | Reuse rather than add new framework |
| C4 | Component pins Ruff 0.17.1 and mypy 2.4.0; strict source/test checks | src/orchestrator/pyproject.toml:13-35 | view, pip show | high | /tmp/mv tools match pins; orchestrator not installed; core points to a different worktree |
| C5 | Local fixture lacks profile; dry-run derives teardown order from ORDER | src/orchestrator/src/zava_forward/orchestrator/rebuild.py:273-290,319-329 | view | high | Add direct regression and check dry-run order |
| C6 | Component tests need installed local distributions and core test fixtures | src/orchestrator/README.md:15-17; src/README.md:50-59 | view | high | Install current core/orchestrator after observed missing-package failure |

### External Evidence

No external technical evidence required.

### Contradictions / Conflicts

* None for the bounded fix. Historical publication blockers remain historical and are not resolved by local tests.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Implication |
| --- | --- | --- | --- | --- |
| Q1 | Fixed tier must place profile before managed environment | C1, C2 | high | Set profile tier 1 |
| Q2 | Dedicated dependency-chain regression and CLI contract assertion cover both surfaces | C3, C5 | high | Include reversed input and real MemoryBackend deletion trace |
| Q2 | Requested venv needs local editable packages before checks | C4, C6 | high | Setup from this worktree, preserving pinned dev versions |

## Key Discoveries

* The defect reproduces regardless of inventory order (C1).
* Dry-run consumes the same priority map, so both modeled and advertised orders are affected (C5).
* Synthetic SQLite roundtrip lacks the resource pair and cannot substitute for the regression (C5).

## Alternatives and Decision State

### Selected Recommendation

* Set Microsoft.Cdn/profiles priority to 1. Add one dedicated test covering apps/jobs, profile, environment and WAF under forward and reversed inventory orders, plus a dry-run assertion in the existing CLI test.
* Evidence: C1-C3, C5. High confidence for the local fixed contract; not live Azure deletion acceptance.
* Files: rebuild.py, test_rebuild.py and directly related orchestrator README.

### Alternative: Raise managed environment priority

* Rejected: changes its relation to other resources unnecessarily; adjusting the consumer is smaller (C1).

### Alternative: Explicit dependency graph

* Rejected: no dynamic adapter or dependency data exists; unnecessary abstraction for one fixed-map defect (C1, C5).

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none for local implementation.
* Residual: no Azure adapter, real Private Link teardown or issue #148 acceptance is established.
* Existing publication and original review findings are outside this task; preserve them unchanged.

## Current Decisions

| Decision | Status | Owner / source | Rationale | Evidence | Implication |
| --- | --- | --- | --- | --- | --- |
| Use profile tier 1, keep environment tier 2 | confirmed | Evidence and caller-authorized priority fix | Minimal fixed dependency correction | C1, C2 | Plan narrowly |
| No Azure or push | confirmed | User | Local-only task | C6 and intake | No publication claim |

## Unresolved Decisions

None for this local correction.

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Evidence |
| --- | --- | --- | --- | --- | --- |
| deferred | Actual adapter teardown acceptance | Real resource verification | Separate explicit Azure authority | no | C2, C5 |

## Planning Readiness

* Status: Ready.
* Decision state: convergence selects profile priority 1 and dependency regression.
* Evidence basis: C1-C6.
* Preconditions: source dependency and regression pattern verified; package setup action known.
* Blockers: none for local work.
* Smallest action to change readiness: none.

## Closeout Record

| Field | Record |
| --- | --- |
| Research execution status | Complete |
| Completed waves | Wider, Deeper, Contrarian, in order |
| Lane evidence | Inline; source trace fits direct execution |
| Research disposition | executed |
| Planning Readiness | Ready, C1-C6 |
| Blockers | None for local work |
| Continuation owner | Automatic RPI parent, as explicitly requested full loop |

## Advisory Next Step

* Parent advances to Plan with C1-C6 and the existing local-only boundaries.
* Research performed no production edits; planning owns the independent critique gate.
* Further focused research would not change the source-backed decision.

## Sources

No external sources used.

## Artifact Self-Check

* [x] Questions answered and all three waves recorded in order.
* [x] Posture, extension provenance, participation and direction controls recorded.
* [x] Findings, alternatives, decisions and readiness cite stable code evidence.
* [x] Parent dispositions and cycle stop basis recorded; no invented external citations.
* [x] No secrets, private data, source edits or Azure access; historical evidence preserved.
