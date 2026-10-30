<!-- markdownlint-disable-file -->

# Task Research: demo-sites-redeploy

| Field | Value |
| --- | --- |
| Date | 2026-10-30 |
| Researcher | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-30/demo-sites-redeploy-research.md |

## Research Brief

Research the exact #542/#545 deployment procedure, current main compatibility,
RG ama prerequisites and requested live feature checks. Audience: owner and
publication coordinator. Output mode: convergence supporting planning.
Success requires both sites on pinned current main, preserved guardrails,
approved SQL initialization, counts-only proof and honest feature results.
Non-goals: source feature changes, private dataset reads, .env reads, broad
RBAC, new private endpoints, RG deletion, pushing or merging.

## Research Parameters

Focused posture, selected for a bounded task with named sources.
Evidence root: .copilot-tracking/. Azure authority supplied directly by owner
2026-10-30 through 2026-11-15, limited to RG ama. Heavy work requires
nonblocking /tmp/ama-rpi-heavy.lock. No secret output.
Initial internal areas: prior deployment evidence, infra operations notes,
SQL initializer and src Dockerfiles. External areas: named GitHub PRs/issues
and scoped Azure management reads.

## Extension Registry and Provenance

Repository instructions and RPI phase skills selected. Research specialist
delegation skipped because this is one coupled operational trace.
Web design skills are not applicable to deployment-only work; no web edits
or standalone design/conformance review is requested.

## User Participation and Research Decisions

User explicitly requests all four phases and authorizes scoped deployment,
minimum IoT data-plane role and existing in-VNet SQL initialization.
Non-interactive execution: no routine questions. This is a full-loop request,
not an inferred automatic-mode switch.

## Direction Controls

* Preserve min replicas 0, eight Manual jobs, ACR policies and live digests.
* Record blocked steps and stop their dependent actions without guessing.
* Commit locally with Refs and required trailer; never push.

## Research Questions

| ID | Question | Status |
| --- | --- | --- |
| Q1 | What exact prior procedure and rollback invariants apply? | In progress |
| Q2 | Are Azure, build, SQL and least-privilege prerequisites available? | Open |
| Q3 | What live acceptance is possible without reading secrets? | Open |

## Prior Knowledge Gate

Read original specification, addendum opening, knowledge-base index opening,
owner memory, #542/#545 PR descriptions and prior phase details.
Clean topic branch chore/ops-redeploy-both-sites-1030 has no known PR.
`git pull --ff-only origin main` succeeded, already up to date at
ffd8f35e63b24905b9aeb937dbf2a7fe9968747f, equal origin/main.
#550 is not a PR; resolve supplied feature references as issues next.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline inspection identifies local Docker plus narrowly temporary VM-only
ACR access, raw-template app PATCH, and existing Manual initializer as the
prior successful route. Reflection: #542's resident rollback is not success;
#545's SQL compatibility correction and exact request handling are essential.

#### Wave 2: Deeper

Read infra operations notes and exact previously successful external executors.
`infra/README.md:3217` identifies hub Registry Contributor as the narrow missing
device-registry role; no broader Data Contributor is needed. Caller is the
current VM managed identity, verified from in-memory token oid, not guessed
from Graph `/me` (which fails for service principals). Existing hub has no such
role for this principal. SensorConsumer._schema supplies canonical SQL DDL;
sensor_register DDL comes from STOCK_SQL_DDL. No policy/control rows or sensor
data need creation. Reapply only the optional-view batch after table creation.
Reflection: copy the prior reviewed executor into private current-session
scratch and correct known IP normalization/log overwrite deficiencies before use.

#### Wave 3: Contrarian

Public health cannot establish new revision health or authenticated acceptance.
The resident password is owner-held and cannot be retrieved; employee requires
interactive Entra sign-in. Therefore inspect anonymous paths/assets in the live
browser, report authenticated feature steps blocked unless an existing authorized
session is available, and never bypass auth or fabricate live acceptance.
No live sensor feed is enabled by schema or a registry grant.
Shared nonblocking lock probe returned 0; actual build still must acquire it.
Current-main SHA differs from yesterday's source, so no old build is reused.
Reflection: no new endpoints, service SAS keys, device identity creation, private
dataset access, model invocation or scope expansion is needed.

#### Parent Synthesis and Disposition

Accept exact prior route with documented bounded corrections (C1,C3,C4).
Reject public-health-only acceptance, broad roles and SQL row seeding.
Defer unavailable authenticated acceptance, not independent deployment steps.
Another research cycle is unnecessary: procedure and conditional stop contracts
are evidence-backed; remaining unknowns are execution preconditions, not guesses.

## Evidence Log

| ID | Finding | Source |
| --- | --- | --- |
| C1 | Raw PATCH, finite ACR windows, job retry restoration and immutable source contracts | .copilot-tracking/details/2026-10-29/demo-sites-live-correction-phase-details.md:21 |
| C2 | Full gate is required for publication, not evidence of live acceptance | src/README.md:69 |
| C3 | Hub role and counts-only/schema/view limitation | infra/README.md:3259 |
| C4 | Canonical sensor schema without configuring policy or inserting data | src/core/src/zava_forward/core/sensor_consumer.py:267; src/core/src/zava_forward/core/synthetic/sensor_backfill.py:53 |
| C5 | Optional sensor view binds only at view apply, no extra grants | infra/sql/resident-showcase.sql:25 |
| W1 | Prior resident image failed and was rolled back | https://github.com/jmservera/ama/pull/542 retrieved 2026-10-30 |
| W2 | Both corrected sites deployed with SQL view update | https://github.com/jmservera/ama/pull/545 retrieved 2026-10-30 |
| W3 | Shared widget delivery; live acceptance remains outstanding | https://github.com/jmservera/ama/pull/556 retrieved 2026-10-30 |
| W4 | Expanded-map filters delivery; owner acceptance outstanding | https://github.com/jmservera/ama/pull/553 retrieved 2026-10-30 |
| W5 | Case UX delivery; residual layout review gap | https://github.com/jmservera/ama/pull/554 retrieved 2026-10-30 |

## Findings Mapped to Questions and Evidence

Q1 answered by C1/W1/W2: resident-first exact raw-template rollout after SQL
compatibility proof and private registry restoration. Q2 answered by scoped
inventory, Enabled subscription, Docker29.9.0, available lock probe and C3-C5;
full preflight still required. Q3 answered conditionally by W3-W5 and operations
notes: no credential disclosure, no auth bypass, live anonymous browser possible.

## Risks and Residual Uncertainty

No actual all-in spend/headroom query was performed; supplied renewed redeploy
authority is not a measured cost statement. No current live-to-SQL activation,
authenticated browser or human accessibility acceptance is established.
Historical /me failure and mixed issue/PR reference lookup failure are retained,
resolved via token claims and gh issue view respectively.

## Alternatives and Decision State

Prefer the previously approved exact route; reject broad network/RBAC changes,
CLI-normalized secretRef mutation and treating public health as feature proof.

## Planning Readiness

Ready for scoped implementation planning with explicit execution stop conditions.
Research disposition: executed, complete. Self-check: three waves, evidence IDs,
owner controls, alternatives, gaps and readiness recorded.
