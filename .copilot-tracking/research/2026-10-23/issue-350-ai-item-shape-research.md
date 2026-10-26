<!-- markdownlint-disable-file -->
---
title: Offline feedback AI item shape correction research
description: Bounded runtime-contract investigation for issue 350 and draft PR 436
ms.date: 2026-10-23
---

## Research Brief

* Topic: reject malformed captured priority items without expanding offline acceptance.
* Purpose/audience: prepare a bounded correction and evidence for the coordinator.
* Scope: `tools/check-demo-feedback.py`, its focused tests, runtime `priority_items`
  and API response path, and directly related documentation.
* Non-goals: semantic citation resolution, network/AI activation, credentials,
  deployed/SQL acceptance, issue closure or unrelated cleanup.
* Criteria: established runtime field types and nonempty values; red-first
  regression tests; preserve prior RPI history and all blocked acceptance.
* Requested outputs: genuine research, plan/details/critique, changes and one Review,
  committed candidate, one complete local gate, verified receipt and draft PR update.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | What shape does runtime/API produce; what can offline validation establish? |
| Initial internal areas | Checker/tests, ai_tasks.py, API server, prior correction4 artifacts |
| External scope | None; GitHub metadata only for delivery |
| Posture/provenance | Focused, bounded caller request with named sources and reproduction |
| Explicit limits | Only specified worktree/branch/PR; one full gate; no Azure/paid acceptance |
| Completion basis | In-scope contract and material counterexamples covered |
| Research edits | Evidence/tracking only; no source edits |
| Resolved evidence root | This worktree's `.copilot-tracking/research/2026-10-23/` |

## Extension Registry and Provenance

| Kind | Candidate | Provenance and authority | Disposition |
| --- | --- | --- | --- |
| Instructions | Repository guidance supplied at intake | Package layout, privacy identity, full gate, branch preservation | Selected |
| Skill | rpi-research | Active phase contract | Selected |
| Skill | rpi-plan / implement / review | User-requested subsequent phases | Deferred until phase transitions |
| Specialist | RPI Researcher | Available independent lanes | Skipped: one tightly coupled small contract trace |
| UI/security skills | No matching implementation or explicit security review | Offline Python shape guard only | Skipped |

## User Participation and Research Decisions

Intake is explicit and sufficient; no questions needed. The user authorizes the
complete ordered loop and normal push/update, not live acceptance. Worktree was
clean, on `test/deployed-feedback-harness-350`, at
`5f14378c383f35bffe91abdda7730045baaecb1d`; origin/main is
`140d8f494482c78e84d15f3d46b9223d3c487af0`. Draft PR #436 is open
and targets main. Prior artifacts will remain unchanged.

## Direction Controls

All caller scope/exclusions above are active. Validate captured structure, not
semantic citation truth or arbitrary limits. Keep #350 open and unticked.

## Research Questions

| ID | Question | Class | Status |
| --- | --- | --- | --- |
| Q1 | Which item types/nonempty constraints does runtime enforce? | Depth | Answered C2/C7 |
| Q2 | Does API preserve this shape and what can checker prove offline? | Depth | Answered C1/C3/C7 |
| Q3 | Which tests/commands and residual blockers must be preserved? | Straightforward | Answered C4/C5/C6 |

## Prior Knowledge Gate

Caller reproductions are hypotheses pending source confirmation. Repository
case study, addendum, knowledge index, memory, sector primer and source-layout
guide read. Memory is context, not evidence. Prior correction history discovered;
its exact relevant outcomes will be read, not overwritten.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline investigation located checker field validation, runtime `priority_items`,
the POST API path and existing test fixture. The checker currently tests only
dict/list/nonempty cites shape (C1). The runtime has a materially stronger
output contract (C2). The POST path returns the store record directly (C3).
Reflection: follow the store producer before choosing output-field guards;
model-input coercion may differ from captured API output.

#### Wave 2: Deeper

Prioritized runtime validation/output construction and package-based tests.
`priority_items` rejects duplicate/unknown IDs, requires string reasons with
non-whitespace content and emits stripped string citations only after source
resolution (C2). Checker has no corresponding source-label snapshot. Baseline
focused test invocation with system Python failed for missing installed
`zava_forward`; installed core, agents and API dev distributions into a new
external venv, following C5, without PYTHONPATH workarounds.
Reflection: check captured output types/content only; preserve absence of
semantic verification and independent deployed acceptance.

#### Wave 3: Contrarian

Producer inspection confirms `ai_priority` passes validated items into
`_rec_view`, which enriches them with display fields without changing
case_id/reason/citation element types (C7). Direct probes confirm both supplied
malformed examples currently PASS, while runtime rejects dict/bool/null/empty/
whitespace citation examples against the synthetic `Stage: S` source. A genuine
`priority_items` positive output remains accepted by the checker (C8).
Reflection: input coercion is not a reason to allow non-string captured output.
Do not require enriched display fields, field-length caps, new ID formats or
arbitrary citation syntax; these are unnecessary for this shape correction.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Nonempty string case_id/reason and each citation | C1/C2/C7/C8 | Accepted | Necessary captured output shape |
| Import runtime validator to resolve captured citations | C2/C7 | Rejected | Requires unavailable source evidence; would invent semantic assurance |
| Enforce display fields, lengths or citation syntax | C4/C7 | Rejected | Not part of this bounded malformed-shape correction |
| Full runtime ID membership/revalidation | C2/C7 | Deferred | No source snapshot; checker does not recreate priority execution |
| Review then commit then one full gate | C5/C6 | Accepted | Explicit current user sequence removes prior sequencing contradiction |

#### Cycle Re-entry Evaluation

No further cycle: contract/API trace, positive and negative probes and validation
layout are established; remaining live acceptance is explicitly out of scope.

## Evidence Log

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| C1 | AI checker accepts dicts with any nonempty cites list; no case/reason/citation element validation | `tools/check-demo-feedback.py:461` | High |
| C2 | Runtime validates IDs/reasons, resolves citations and emits strings | `src/core/src/zava_forward/core/ai_tasks.py:134` | High |
| C3 | POST returns `s.ai_priority(...)` record directly | `src/api/src/zava_forward/api/server.py:887` | High |
| C4 | Valid synthetic fixture already includes case_id/reason/string cites; structural safety and acceptance guards exist | `tools/test_check_demo_feedback.py:118`, `:580`, `:727` | High |
| C5 | Installed distributions and external exact-HEAD gate required; Review then commit before full gate | `src/README.md:45`, `:55` | High |
| C6 | Prior correction4 adverse Review and sequencing blocker must be preserved, not rewritten | `.copilot-tracking/reviews/logs/2026-10-22/issue-350-demo-feedback-correction4-review.md:120` | High |
| C7 | Runtime validates before publishing and enriches item views without changing required shape | `src/core/src/zava_forward/core/store.py:760`, `:805`, `:813` | High |
| C8 | 64 baseline tests pass in installed venv; supplied repros PASS; runtime positive/rejection probes confirm output distinction | `tools/test_check_demo_feedback.py:118`, `src/core/src/zava_forward/core/ai_tasks.py:149` (2026-10-23 executed probes) | High |

## Findings Mapped to Questions and Evidence

Q1: captured case_id/reason/citation elements must be nonempty strings (C2/C7).
Q2: API preserves these; offline checks can establish shape, not source truth (C1/C3/C7).
Q3: use installed packages, targeted unittest/Ruff; preserve blocked durability,
not-run spend/admin and not-accepted verdict (C4/C5). Prior Review remains intact (C6).

## Alternatives and Current Decisions

Selected: extend existing `nonempty_str`-based item guard; no new imports,
abstractions or semantic validator. Confidence high (C1/C2/C7/C8).
Caller owns live acceptance and coordinator review. No unresolved implementation
decision. No further research selected unless tests expose a contract conflict.

## Risks and Residual Uncertainty

Captured data is self-reported; shape PASS is not a real AI task, source
verification, SQL durability or deployment acceptance. No external service or
private dataset was accessed. Full gate and independent assessment are pending.

## Sources

No external sources used.

## Planning Readiness

Ready. Research disposition: executed, complete. All three waves completed
inline because one small continuous trace did not justify delegation.
Evidence C1-C8 supports the bounded guard and red-first test matrix.
No research blockers. Automatic parent proceeds to Plan under the explicit
full-loop request; the research skill itself does not advance phases.

## Artifact Self-Check and Closeout

All questions answered; posture, limits, extension registry and parent
dispositions recorded. Stable evidence IDs include source locations.
Alternatives and residual uncertainties are explicit. No source edits occurred.
Next action: parent activates rpi-plan and writes checklist/details before source.
