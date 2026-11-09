---
title: IoT and Resident Architecture Review
description: Source-grounded diagram update and main-route deployment-slide review
ms.date: 2026-11-08
ms.topic: reference
---
<!-- markdownlint-disable-file -->

## Review Identity and Confirmed Scope

* Review slug: iot-resident
* Review date: 2026-11-08
* System under review: Zava Forward, existing shared-API demonstrator and separately gated integrations.
* Confirmed focus: reliable sensor admission, operational evidence/storage, and audience-readable deployment boundaries.
* Owner direction: update both tagged Excalidraw drawings and the current capstone diagrams; add a new full Azure deployment slide to the main route, including supporting services and gated options.
* Renderer: existing Excalidraw models and local Excalidraw CLI. The installed architecture-diagrams/C4 skills do not support this renderer; the owner-selected .agents/skills/excalidraw/SKILL.md supplies the delegated workflow.
* Participants: repository owner, System Architecture Reviewer, delegated Excalidraw implementation agent, AMA Presentation Communications Strategist.
* Decision owners: existing ADR owners and named human/resident approval boundaries remain unchanged.

## Evidence Sources and Research Artifacts

| Evidence ID | Source or artifact | Evidence state | Review use |
| --- | --- | --- | --- |
| E1 | docs/case_study_48_original.md and docs/case_study_48_addendum.md | Read; original preserved | Requested quality/sensor purpose, optional resident access, original L2-L4 boundaries |
| E2 | docs/capstone/source/diagrams/architecture/text-equivalent.md | Read; source topology, not live inventory | Existing IoT Hub/Event Hubs/SQL contracts, managed-service and gated-option boundaries |
| E3 | src/core/README.md, Versioned sensor analysis slice (111) | Read; source-coded analysis | Retained-readings derivation is read-only; no task, ranking or diagnosis authority |
| E4 | src/api/README.md, Live simulator container (184) | Read; synthetic engineering | Simulator daily-average inputs are not stored real observations; sunlight schema integration remains unresolved |
| E5 | docs/reference/method/ama-capstone-assessment-guide.md | Read in full | All twenty criteria, section floors and individual-criterion floor; no inferred live score |
| E6 | .agents/skills/excalidraw/SKILL.md and excalidraw render --help | Read; local CLI 0.3.0 available | Delegated native source edits and local no-upload rendering |
| E7 | Owner clarification in current session | Confirmed | Update everything; add a new full deployment slide to the main route |
| E8 | .copilot-tracking/architecture-diagrams/2026-11-08/zava-forward/validation.json | Delegated implementation evidence read | Four native models, six previews, fourteen source/browser/geometry tests and original preservation |
| E9 | docs/capstone/source/diagrams/architecture/text-equivalent.md, current continuation | Read after implementation | Exact current-versus-target service, averages, resident and Quality Verification distinctions |
| E10 | docs/capstone/source/validation.json and review-2026-11-08-cxo.md | Strategist implementation evidence read | Build/Verify, 55 slides/notes, 108 destinations, cost guards, insertion refusals, PDF and narrative checks |

Local evidence is adequate for this documentation/model update. No current
price, service adoption, licensing choice or benchmark is being recommended;
external RPI Research is not required.

## Context, Constraints, and Assumptions

| ID | Type | Statement | Evidence IDs | Status or owner |
| --- | --- | --- | --- | --- |
| CTX-1 | Verified context | The 54-slide native baseline remains immutable. The delivered source has 55 slides, inserting S11A at physical 13 using package part 55. | E2, E7, E10 | Insertion-aware mapping/navigation verified |
| CTX-2 | Constraint | Sensor transport, calibration, consent and live acceptance must not be inferred from an authored diagram. | E1-E4 | Separate owner/professional release gates |
| CTX-3 | Constraint | Resident showcase and proposed shared-case service are different states; login does not grant case access or works consent. | E1-E2 | Preserve explicit labels and assisted service |
| CTX-4 | Constraint | Do not adopt a new analytics database, standalone worker or cloud topology to illustrate a service responsibility already supported by the shared API and SQL. | E2-E4 | Verify exact storage/average semantics |
| CTX-5 | Verified context | Exercise baseline/early/late means are computed on read. Persisted per-home averages and post-retrofit sensor linkage to Quality Verification are target/gated, not current runtime integration. | E3-E4, E8-E9 | Explicit source/target labels preserved |
| CTX-6 | Owner decision | Owner explicitly authorized inclusion of the installed Excalidraw skill and skill lock in this PR. | E6-E7 | Preserve imported bytes; MIT notice included |

## Pillar Findings and Non-Findings

| Focus area or pillar | Disposition | Evidence IDs | Finding, non-finding, or unassessed limit | Priority |
| --- | --- | --- | --- | --- |
| Reliability | Finding addressed in diagrams; operational acceptance remains unassessed | E2-E4, E8-E9 | Complete device -> Hub -> Event Hubs -> validated intake -> SQL path is now visible. Invalid data has owned DQ/manual handling, not empty success or safety release. API-initiated receive is not an Event Hubs push. | High |
| Operational Excellence | Finding addressed with explicit target/source split | E2-E4, E8-E9 | Shared-API household telemetry/history/averages service is shown, backed by SQL. Accepted observations are retained; exercise means are computed on read. Materialized averages and Quality Verification sensor integration are visibly gated targets. Platform monitoring is separate. | High |
| Performance Efficiency / deployment communication | Source/render/deck finding addressed; live performance and rehearsal unassessed | E2, E5, E7-E10 | Connected 2400 x 1170 deployment frame includes core, support services, sensor chain, resident site and alternatives. Minimum projected text is approximately 12.1 pt. Added 45-second narration makes a 24:30 plan with 5:30 reserve, not measured rehearsal; no capacity, allocation or SLA claim is inferred. | High |

## Options, Drivers, Trade-Offs, and Research Recommendation

### Decision Drivers

* Make the home-to-quality evidence path visible, not merely list sensors.
* Keep existing application ownership and human/resident authority.
* Explain a full Azure deployment view without replacing the CxO summary or hiding operational services.
* Preserve all native navigation, financial evidence and original source baselines.

### Candidate Options

| Option | Benefits | Trade-offs | Evidence IDs | Current disposition |
| --- | --- | --- | --- | --- |
| Existing shared API intake/analysis plus SQL telemetry/history | Reuses existing contracts, persistence and permissions | Must label derived and not-yet-materialized averages accurately; live acceptance remains separate | E2-E4 | Selected for source verification |
| New standalone analytics datastore/stream worker | Could provide an independently scalable future pipeline | No current adoption requirement/evidence; would create an unrequested architecture decision | E1-E4 | Rejected for this update |
| Replace main summary with the full map | No new slide or timing change | Owner explicitly requested a new main-route deployment slide | E7 | Rejected |
| Add main deployment projection; retain summary and full-resolution source | Distinct executive and technical depth with common model | Requires insertion-aware native navigation/build verification and rehearsal | E5, E7 | Owner selected |

### Research Recommendation

* Recommendation: source-faithful documentation update, not new infrastructure adoption.
* Evidence IDs: E1-E7.
* Confidence: high for source/target distinctions and confirmed scope; no live acceptance inferred.
* Unresolved trade-offs: diagram density, added narration time and live integration gates.

## Reviewer Disposition

| Recommendation or field | Disposition | Rationale | Decision owner |
| --- | --- | --- | --- |
| Update all four diagrams in Excalidraw | Accepted | Explicit owner clarification; preserve native editable sources | Repository owner |
| Add new full main-route deployment slide | Accepted | Explicit owner selection instead of replacement-only summary | Repository owner |
| Use existing SQL and shared API responsibilities | Accepted | Named service responsibility reuses current ownership; persisted averages and sensor-to-Quality linkage remain explicit targets | Existing architecture owners |
| Claim live device, managed resident identity or production acceptance | Rejected | Source diagrams and local renders do not supply that evidence | Named release/compliance owners |

## Recommendations and Priorities

| Priority | Recommendation | Evidence IDs | Owner | Next action |
| --- | --- | --- | --- | --- |
| High | Complete editable model/derivative consistency and source checks | E2-E4, E6 | Delegated diagram implementer | Native generation, source tests and local render |
| High | Preserve added main slide, all note blocks and original native destinations | E5, E7, E10 | Presentation strategist | Completed Build/Verify and Linux preview; native viewer and human acceptance remain separate |
| High | Retain exact-head local/publication gates and disclose missing evidence | E1-E7 | Parent reviewer | Validate final candidate before publication |

## Escalations and Human Decision Owners

| Escalation | Why human judgment is required | Decision owner | Required evidence or action |
| --- | --- | --- | --- |
| Real-home telemetry activation | Device identity, calibration, consent, access and safety interpretation cannot be granted by a diagram | Existing named device/privacy/professional owners | Bounded live acceptance and approved controls |
| Resident shared-case identity/integration | Separate login, household/representative grants and recovery remain consequential controls | Existing Programme/Engagement/Digital/privacy owners | Approved integration and release evidence |
| Added main-route timing | Authored notes are not actual live delivery | Presenter | Rehearse within confirmed slot |

## ADR Links

| Significant decision | ADR path | Status | Authority note |
| --- | --- | --- | --- |
| Pilot/application boundaries | docs/adrs/0002-pilot-readiness-architecture.md | Existing record | No decision changed by this diagram update |
| Basic IoT Hub exercise and same-API intake | docs/adrs/0003-journey-derived-capabilities-runtime-fit.md | Owner-accepted with amendment, 2026-10-15 | Existing ADR/human authority retained; not live provisioning acceptance |

No new significant technology, storage, API or deployment decision is adopted
by this documentation update; no new ADR is needed unless source verification
reveals an actual requested decision.

## Limits and Unassessed Areas

* Diagram source/browser/geometry checks: fourteen passed, zero failed/skipped. Six native PNG views inspected by the delegated implementer; generators verified and 152 local links checked. This is not independent exact-head review.
* The implementer staged previews in dated repository tracking, not external scratch as requested. Original October generators and adverse evidence remain unchanged. Only the compact receipt is intended for publication; scratch cleanup has no automatic authorization.
* Final deck Build/Verify passes with 55 slides/notes and all 108 fixed destinations; the baseline remains unchanged. Thirty-two native-shape checks, six insertion refusal mutations, protected-cost guards and ten PDF navigation regressions pass. Thirty required service terms were extracted from actual deployment notes/alternative text.
* Linux preview inspected ten affected/adjacent pages and 427 native frames, with all words retained. It reports 128 inherited word-box hints, not new source overflow or native PowerPoint bound validation. No claim of accessibility acceptance follows.
* Exact-head independent assessment and local publication gate remain pending. Their final outcomes belong in the PR/external receipt without changing the tested candidate or overwriting original evidence.
* No Azure inventory, cloud deployment, private dataset, credentials or paid model call inspected or performed.
* No full security assessment or compliance/legal acceptance is claimed.
* Native Windows PowerPoint rendering, live Q&A, rehearsal and a fresh panel score remain separate.
