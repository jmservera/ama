<!-- markdownlint-disable-file -->

# Task Research: iot-nominal-pacing-508

| Field | Value |
| --- | --- |
| Date | 2026-10-29 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-29/iot-nominal-pacing-508-research.md |

## Research Brief

* What to research: carry nominal slot time through synthetic frames to publisher scheduling without changing faulted payload timestamps.
* Why it matters: out-of-order suffix slots 3..4 currently produce an artificial 24-hour wait, not the nominal 8-hour cadence.
* Audience or intended use: PR #508 implementation and independent review.
* Scope: core synthetic sensor_stream, API iot_stream, existing external test modules, directly related documentation.
* Non-goals: mvp, Azure, deployment, full API suite, unrelated review findings, push.
* Criteria: unchanged reordered payloads, nominal 28.8-second delay at speed 1000, bounded successful 60-second run, existing rate/deadline protections preserved.
* Requested outputs: dated research, plan/details/critique, implementation/validation and independent Review.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Q1: where is nominal time lost? Q2: how can a publisher regression prove payload and scheduling independently? |
| Codebase scope | src/core and src/api synthetic replay/publisher and their tests |
| External scope | None |
| Initial internal candidate areas | Frame, replay, HubPublisher.run, Pacer, test_sensor_stream, test_iot_stream |
| Initial external candidate areas | None |
| Research posture | focused |
| Posture provenance | Default for named code finding and caller-bounded regression |
| Explicit limits / deadline | No Azure, mvp, full API suite or push; use /tmp/mv |
| Posture-specific completion basis | Focused scope and materiality |
| Edits allowed during research? | No source edits |
| Resolved evidence root | .copilot-tracking/ |
| Known constraints / excluded sources | No private data; existing local fixtures only |

## Extension Registry and Provenance

* Precedence: host safety, caller scope, repository instructions, RPI contracts, domain skills.

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
| --- | --- | --- | --- | --- |
| Instruction | .github/copilot-instructions.md | Repository-wide guidance supplied at intake | src layout, topic branch, dated evidence, local gates | Selected |
| Skill | rpi-research | Full-loop request | Three-wave evidence synthesis | Selected |
| Skill | rpi-plan / rpi-implement / rpi-review | Full-loop request | Later-phase protocols | Selected for later phases |
| Specialist | hve-core-all:rpi-researcher | Registered internal research agent | Independent research lane | Skipped: one tightly coupled code trace |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision |
| --- | --- | --- | --- |
| Intake | Exact finding, branch, expected outcome and checks supplied | Full loop explicitly requested | Proceed autonomously within scope |

## Scope and Success Criteria

* Preserve fault payload identity and timestamps; schedule from nominal metadata.
* Test in existing test files outside packages.
* Run requested Ruff, formatting, mypy and relevant unittests, never full API discovery.
* Preserve human/hosted/publication gates; coordinator owns push.

## Task Research Requests

* Fix only the suffix replay pacing finding on PR #508.
* Pull/rebase first; rubric conflicts or replacement use origin/main.
* Commit with Conventional Commit and required Copilot trailer; no push.

## Direction Controls

| Control type | Direction or boundary | Source / checkpoint | Effect |
| --- | --- | --- | --- |
| narrow | Nominal pacing and suffix publisher regression only | User intake | No unrelated fixes |
| exclude | Azure, mvp, full API suite, push | User intake | Local targeted work only |

## Research Questions

| # | Sub-question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | How do nominal slots, faulted timestamps and publisher pacing interact? | depth | H | answered |
| Q2 | Which existing fake client/pacer tests can verify suffix timing and payloads? | straightforward | H | answered |

## Prior Knowledge Gate

* Supplied finding is a hypothesis to verify against current pulled source.
* Project original, addendum, reference index and owner memory read; none supplies a different pacing requirement.
* Existing historical IoT RPI artifacts are retained unchanged; this is a distinct correction.

## Research Cycle Log

### Cycle 1

* Active controls: bounded src-only nominal pacing correction; no network services.
* Posture: focused; stop when source trace, counter-evidence and regression design cover Q1/Q2.

#### Wave 1: Wider

* Inline trace identified Frame and replay in core, HubPublisher copying and scheduling in API, and two existing test modules.
* Reflection: nominal slot index survives, but nominal timestamp is not in Frame; inspect test helpers and every construction before selecting the change.

#### Wave 2: Deeper

* Inspected every Frame constructor (three sites), core fault/suffix tests and API PublisherTests.
* Local reproduction with /tmp/mv returned slots [3, 4], payload times 2024-10-01T16:00:00Z and 2024-10-02T16:00:00Z, 24 model hours / 86.4 seconds at speed 1000.
* Reflection: a required datetime nominal_at field can derive from origin plus slot cadence, survive duplicates and publisher snapshotting, and leave wire bytes/reference untouched.
* Regression can use the actual Pacer with a virtual clock and patched sleep, existing inert X509/client mocks, a 60-second budget, and capture send instants.

#### Wave 3: Contrarian

* Challenged deriving cadence from payloads or slot differences: payloads are intentionally reordered, and slot indices alone do not retain arbitrary configured cadence.
* Challenged simply sorting payload timestamps: this would change fault order, suffix identity and exercise semantics.
* Existing duplicate/multiple-device behavior requires zero nominal delay for equal slots; burst must still skip model spacing and retain rate admission.
* Reflection: explicit nominal UTC timestamp covers custom origins/cadences, duplicate/same-slot frames and suffixes without changing Pacer or the payload schema.

#### Parent Synthesis and Disposition

| Material / claim | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Carry required nominal_at datetime on Frame | C1-C4 | accepted | All constructors are internal and can be updated together; no optional fallback to faulted time |
| Schedule from nominal_at, preserve row bytes | C1-C3 | accepted | Separates intended scheduling from injected measurement anomalies |
| Regression uses real Pacer and virtual time | C3-C5 | accepted | Exercises scaling and deadline, not just a mocked interval assertion |
| Sort rows or infer cadence from observations | C1-C2 | rejected | Removes intended fault or retains its timing defect |

#### Cycle Re-entry Evaluation

* Another complete cycle needed: no.
* Stop basis: all constructors, pacing, fault semantics and existing fixtures inspected; direct reproduction confirms exact failure.
* Planning Readiness: Ready.

## Evidence Log

* Delegation: inline; tightly coupled trace needs no isolated research lane.

### Codebase Evidence

| ID | Claim / finding | Location | Tool | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| C1 | Replay selects nominal slots but swaps the observation row for out_of_order | src/core/src/zava_forward/core/synthetic/sensor_stream.py:174 | view | high | Slots 3/4 select source indices 2/5 |
| C2 | Publisher snapshots Frame then computes waits from row observed_at | src/api/src/zava_forward/api/iot_stream.py:343 | view | high | Faulted interval leaks into scheduling |
| C3 | Pacer divides requested interval by speed and retains deadline/rate controls | src/core/src/zava_forward/core/synthetic/sensor_stream.py:260 | view | high | Need nominal 28800 seconds, not 86400 |
| C4 | Only three Frame construction sites exist | src/core/src/zava_forward/core/synthetic/sensor_stream.py:185; src/core/src/zava_forward/core/synthetic/sensor_stream.py:192; src/api/src/zava_forward/api/iot_stream.py:346 | rg | high | Update original, duplicate and publisher snapshot |
| C5 | Existing publisher mocks are inert; core tests demonstrate virtual-clock sleep | src/api/tests/test_iot_stream.py:404; src/core/tests/test_sensor_stream.py:232 | view | high | Reuse patterns without Azure or real sleeps |

### External Evidence

No external sources used.

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Readiness implication |
| --- | --- | --- | --- | --- |
| Q1 | Faulted rows produce 24-hour positive delta across nominally adjacent slots 3/4 | C1-C3 | high | Required nominal time must accompany each frame |
| Q2 | Actual Pacer plus virtual time/client mocks proves both sends occur 28.8 seconds apart and payloads remain reordered | C3-C5 | high | Existing test file supports exact regression |

## Alternatives and Decision State

* Selected recommendation: append required nominal_at datetime to Frame, derive from Replay origin/cadence before fault application, retain through duplicates/copy, schedule from it.
* Preserve row schema, reference hash, seed/window identity, rate admission, burst and deadline controls.
* Add a publisher suffix regression plus core assertions covering fault modes, custom cadence/origin, duplicates and suffix equivalence.
* Alternative payload sorting rejected because injected faults are intentional (C1-C2).
* Alternative optional metadata with observed_at fallback rejected because it retains the unsafe scheduling source (C2-C4).

## Open Questions, Risks, and Residual Uncertainty

* No unresolved implementation questions.
* Full publication gate conflicts with the caller's no-full-API validation scope; do not run it or claim publication readiness. Coordinator owns publication and its gates.

## Current Decisions

* Required metadata, no fallback; exact two-frame suffix regression, local-only checks and commit.

## Potential Next Research

* None needed for this bounded correction.

## Sources

* C1-C5 only; no external sources used.

## Self-check

* Three waves completed in order, alternatives challenged, all material claims have internal evidence, scope unchanged, no source changes during research.

## Planning Readiness

* Research disposition: executed.
* Planning Readiness: Ready (C1-C5).
