<!-- markdownlint-disable-file -->

# Task Research: sensor-privacy-boundary-112

| Field | Value |
| --- | --- |
| Date | 2026-10-17 |
| Researcher | RPI Agent, rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-17/sensor-privacy-boundary-112-research.md |

## Research Brief

Audit actual sensor admission and AI/map/cluster/log exports for #112 before
selecting bounded controls. Audience: implementation and independent Review.
Scope: src sensor analysis, ingestion, read models, prompt assembly and relevant
tests. Non-goals: whole-repository security audit, live data/cloud, new providers,
legal approval, deleting authorized manual detail or unrelated service holds.
Criteria: no raw readings/device identifiers at external boundaries, verifiable
synthetic-only admission, explicit refusal for unknowns, source-authorized minimal
derived indicators. Output mode: convergence for the requested full RPI loop.

## Research Parameters

Focused posture, selected from caller's bounded scope. Evidence root:
`.copilot-tracking/`. Source edits prohibited during Research. External scope:
read-only GitHub issue/branch metadata only. No paid calls, private datasets,
Azure, IAM, deployment or other worktrees. Stable task ID: 112.

## Extension Registry and Provenance

Repository instructions and component guides selected. rpi-research selected;
privacy planning/legal assessment skipped because no new legal approval is
requested. Security exploit audit and web-design skills skipped unless source
evidence changes the backend-only scope. Inline investigation selected because
the admission-to-export trace is continuous, not independent delegated lanes.

## User Participation and Research Decisions

Explicit full ordered loop is authorization for automatic phase progression.
No routine confirmation required; approvals for real sensor use remain absent.
Supplied base and clean branch verified at 74617981b71bc3f10bd21d0b78691bc3cf36c473.
No existing PR on this branch. Parent #109 is hierarchy, not dependency.

## Direction Controls

Preserve current domain controls and parallel #88/#102 work; declare actual
shared-file overlap before editing. Preserve #175 unresolved origins. No
pseudonymization-as-synthetic, filename admission or hidden recursive exports.
No memory changes, no second Review, at most two concrete correction cycles.

## Research Questions

| ID | Question | Status |
| --- | --- | --- |
| Q1 | Where are sensor data admitted and classified? | Answered |
| Q2 | Which actual AI/map/cluster/log boundaries expose sensor data? | Answered |
| Q3 | What existing provenance, access and projection contracts can be reused? | Answered |
| Q4 | Which focused sentinel regressions prove the actual criteria? | Answered |

## Prior Knowledge Gate

Read original/addendum, KB index/memory and current #112 body. Stale Not started
is not delivery evidence; prior PR references are not treated as current proof.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline inventory found only an offline sensor generator/SQL loader, not an
implemented sensor_analysis runtime or IoT consumer. Map points/clusters already
use explicit field lists; legacy AI facts interpolate values; chat recursively
flattens the projected home dictionary. No sensor task is registered.
Reflection: protect the existing seams, not invent a monitoring service.

#### Wave 2: Deeper

Traced loader validation, snapshot hashes/source revision, chat context and
actual prompt assembly, map construction, server log behavior and assistant
capture. Loader registers sensors before checking reading classifications and
permits absent manifest; a label alone is insufficient. Existing hash helpers
provide integrity, not synthetic origin. Deterministic replay can verify exact
generator output before any SQL call, preserving normal and stock exercise data.
Reflection: replay from supplied parameters and explicit stock Selection is
stronger than a caller-controlled synthetic label or manifest hash.

#### Wave 3: Contrarian

Challenged a universal recursive sensor-key filter: rejected because hidden
diagnostics and future aliases bypass it and it alters manual detail. Closed
chat field projection removes unknown nested home payloads without mutating the
stored/manual record. Scalar type refusal prevents dictionaries/lists being
stringified in legacy AI/map fields. Existing assistant pick already refuses
nested values. No numeric health threshold or AI sensor capability is justified.
Third-party tile URLs are static deployment configuration, not sensor payloads;
HTTP request logging is suppressed. Replay must load verified private temporary
bytes, not reopen original mutable inputs. Stock origins remain unverified:
replayed observations prove construction, not genuine consent or stock truth.

### Parent Synthesis and Disposition

Accept replay admission and closed export contracts. Reject filename/label-only
admission, arbitrary sensor deletion, new provider/framework and legal activation.
No additional cycle: actual in-scope seams are traced; remaining real-use
inventory/lawful basis/DPIA/retention/thresholds are deliberately unavailable.

## Evidence Log

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Loader permits absent manifest and writes register before reading checks | src/core/src/zava_forward/core/synthetic/sensor_backfill.py:356 | High |
| C2 | Existing payload hashes and recursive privacy checker are integrity/pattern aids, not origin proof | src/core/src/zava_forward/core/synthetic/privacy.py:214 | High |
| C3 | Reproducible generator has explicit seeds/window/revision and stock Selection | src/core/src/zava_forward/core/synthetic/sensor_backfill.py:195 | High |
| C4 | Chat carries whole home and recursively flattens it | src/core/src/zava_forward/core/chat_isolation.py:75; src/core/src/zava_forward/core/chat_panel.py:203 | High |
| C5 | Legacy AI interpolation permits nested values | src/core/src/zava_forward/core/store.py:695; src/core/src/zava_forward/core/ai_tasks.py:46 | High |
| C6 | Map fields explicit but untyped values can be serialized | src/core/src/zava_forward/core/insights.py:125 | High |
| C7 | Registered assistants already use closed scalar capture and fixed failure logs | src/core/src/zava_forward/core/assistants.py:73 | High |
| C8 | Static tile template, manual alternative retained; HTTP logs suppressed | src/api/src/zava_forward/api/server.py:46; src/api/src/zava_forward/api/server.py:179 | High |
| C9 | Real use blocked on open inventory/lawful basis/DPIA/retention/thresholds | docs/adrs/0003-journey-derived-capabilities-runtime-fit.md:120; docs/brds/agentic-retrofit-programme-brd.md (OD-43) | High |

No external legal/currentness assertions or new external sources used.

## Findings Mapped to Questions and Evidence

Q1 answered C1-C3: exact deterministic origin must precede SQL admission.
Q2 answered C4-C8: chat recursion is a real leak; typed export fields prevent
structured hidden diagnostics entering legacy prompt/map outputs.
Q3 answered C2/C3/C7: reuse generator/hash/pick/access contracts.
Q4 answered: real prompt callable capture, point/forced-cluster serialization,
log captures and no-SQL-on-refusal loader tests with rehashed malicious inputs.

## Alternatives and Decision State

Selected exact generator replay, loading replayed bytes after verification;
closed projected chat fields and explicit malformed export refusal. Source
authorization is current generator provenance, with explicit stock Selection
for stock mode. Unknown/real/malformed inputs refuse before persistence.
No registered sensor AI purpose exists; sensor fields therefore remain outside
AI/map/log contracts rather than granting a new sensor inference permission.

## Risks and Residual Uncertainty

Free prose can contain arbitrary human-entered content; these controls are not
semantic DLP or universal PII detection. Deterministic replay costs generation
time/temp disk. Historical generator revisions require explicit regeneration.
No manual sensor UI exists to remove. Existing authorized case detail remains.
No real-data activation path or retention/threshold approval is invented.

## Artifact Self-Check

Three ordered inline waves complete; alternatives, evidence, caller boundaries,
residual uncertainty and concrete handoff recorded. No source changes made.

## Planning Readiness

Ready. Research disposition: executed, complete. Parent may advance to Plan.
